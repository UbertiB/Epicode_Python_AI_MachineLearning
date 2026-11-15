"""
FASE 4 - NATURAL LANGUAGE ANALYST

L'utente fa una domanda in italiano, l'LLM scrive codice Python (Pandas + Matplotlib),
il backend lo controlla, lo esegue in un processo separato e restituisce testo e grafico.

Il client OpenAI funziona sia con LM Studio (default, tutto in locale) sia con le API OpenAI:
basta cambiare le variabili nel file .env.
"""

import ast
import base64
import builtins
import io
import json
import multiprocessing as mp
import os
import queue
import re
import time

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------------------------------------------------------
# 1. CONFIGURAZIONE LLM (da file .env, con valori di default per LM Studio)
# -----------------------------------------------------------------------------
load_dotenv()
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "lm-studio")
LLM_MODEL = os.getenv("LLM_MODEL", "openai/gpt-oss-20b")

TIMEOUT_ESECUZIONE = 20  # secondi massimi per eseguire il codice generato

client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY, timeout=300)


def llm_raggiungibile() -> bool:
    """
    Controllo per l'health check: chiede l'elenco dei modelli,
    se risponde true altrimenti false.

    """
    try:
        client.with_options(timeout=2, max_retries=0).models.list()
        return True
    except Exception:
        return False


# -----------------------------------------------------------------------------
# 2. PROMPT ENGINEERING
# -----------------------------------------------------------------------------
def crea_system_prompt(df: pd.DataFrame) -> str:
    """Descrive all'LLM la struttura del dataset: colonne, tipi e intervallo dei valori."""
    descrizione = "\n".join(
        f"- {col} ({df[col].dtype}): min {df[col].min()}, max {df[col].max()}"
        for col in df.columns
    )
    return f"""Sei un data analyst esperto di Python.
Lavori su un DataFrame pandas chiamato `df` con {len(df)} righe e queste colonne:
{descrizione}

Rispondi SOLO con un blocco di codice Python, senza spiegazioni fuori dal codice.
Regole:
- `df`, `pd` (pandas), `np` (numpy) e `plt` (matplotlib.pyplot) sono già disponibili.
- Non leggere né scrivere file, non usare la rete, non usare os, sys o subprocess.
- Se serve un grafico, creane uno solo con plt, con titolo ed etichette in italiano.
- Salva la risposta testuale breve (in italiano, con i numeri chiave) nella variabile `risultato`.
"""


def estrai_codice(testo: str) -> str:
    """Prende il contenuto del blocco ```python ... ```; se manca, usa tutto il testo."""
    blocco = re.search(r"```(?:python)?\s*\n(.*?)```", testo, re.DOTALL)
    return (blocco.group(1) if blocco else testo).strip()


def chiedi_codice(domanda: str, df: pd.DataFrame) -> str:
    """Invia domanda e struttura del dataset all'LLM e restituisce il codice generato."""
    risposta = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": crea_system_prompt(df)},
            {"role": "user", "content": domanda},
        ],
        temperature=0,
    )
    return estrai_codice(risposta.choices[0].message.content)


# -----------------------------------------------------------------------------
# 3. CONTROLLO DI SICUREZZA DEL CODICE (analisi statica con AST)
# -----------------------------------------------------------------------------
# AST = Abstract Syntax Tree: il codice viene letto come struttura, senza eseguirlo.
MODULI_CONSENTITI = {"pandas", "numpy", "matplotlib", "matplotlib.pyplot", "math", "statistics"}
FUNZIONI_VIETATE = {"open", "exec", "eval", "compile", "__import__", "input", "globals",
                    "locals", "vars", "getattr", "setattr", "delattr", "breakpoint",
                    "exit", "quit", "help"}
# Metodi pandas/matplotlib che leggono o scrivono file
PREFISSI_VIETATI = ("read_", "to_csv", "to_excel", "to_pickle", "to_parquet", "to_sql",
                    "to_json", "to_hdf", "to_feather", "to_html", "savefig")


def verifica_codice(codice: str) -> None:
    """Solleva ValueError se il codice contiene istruzioni non consentite."""
    albero = ast.parse(codice)
    for nodo in ast.walk(albero):
        if isinstance(nodo, (ast.Import, ast.ImportFrom)):
            moduli = [a.name for a in nodo.names] if isinstance(nodo, ast.Import) else [nodo.module]
            for m in moduli:
                if m not in MODULI_CONSENTITI:
                    raise ValueError(f"Import non consentito: {m}")
        elif isinstance(nodo, ast.Name) and nodo.id in FUNZIONI_VIETATE:
            raise ValueError(f"Funzione non consentita: {nodo.id}")
        elif isinstance(nodo, ast.Attribute):
            if nodo.attr.startswith("_"):
                raise ValueError(f"Accesso ad attributi interni non consentito: {nodo.attr}")
            if nodo.attr.startswith(PREFISSI_VIETATI):
                raise ValueError(f"Operazione su file non consentita: {nodo.attr}")


# -----------------------------------------------------------------------------
# 4. ESECUZIONE IN UN PROCESSO SEPARATO CON TIMEOUT
# -----------------------------------------------------------------------------
def _import_sicuro(nome, *args, **kwargs):
    """Sostituisce __import__: permette solo i moduli della lista."""
    if nome not in MODULI_CONSENTITI:
        raise ImportError(f"Import non consentito: {nome}")
    return builtins.__import__(nome, *args, **kwargs)


def _esegui(codice: str, df: pd.DataFrame, coda) -> None:
    """Gira nel processo figlio: se si blocca o va in crash, il server non ne risente."""
    import matplotlib
    matplotlib.use("Agg")  # backend senza finestre: il grafico resta in memoria
    import matplotlib.pyplot as plt
    import numpy as np

    builtin_sicuri = {k: v for k, v in vars(builtins).items() if k not in FUNZIONI_VIETATE}
    builtin_sicuri["__import__"] = _import_sicuro
    ambiente = {"__builtins__": builtin_sicuri, "df": df.copy(), "pd": pd, "np": np, "plt": plt}

    try:
        exec(codice, ambiente)
        immagine = None
        if plt.get_fignums():  # è stato creato almeno un grafico
            buffer = io.BytesIO()
            plt.gcf().savefig(buffer, format="png", dpi=110, bbox_inches="tight")
            immagine = base64.b64encode(buffer.getvalue()).decode()
        coda.put({"risultato": str(ambiente.get("risultato", "")), "immagine": immagine,
                  "errore": None})
    except Exception as e:
        coda.put({"risultato": "", "immagine": None, "errore": f"{type(e).__name__}: {e}"})


def esegui_in_sicurezza(codice: str, df: pd.DataFrame) -> dict:
    """
    Controllo statico + esecuzione in un processo separato con tempo massimo.
    Nota: è una protezione ragionevole per un progetto didattico, non una sandbox completa.
    In produzione il codice andrebbe eseguito in un container isolato.
    """
    try:
        verifica_codice(codice)
    except (ValueError, SyntaxError) as e:
        return {"risultato": "", "immagine": None, "errore": f"Codice rifiutato: {e}"}

    contesto = mp.get_context("spawn")  # stesso comportamento su Windows e Linux
    coda = contesto.Queue()
    processo = contesto.Process(target=_esegui, args=(codice, df, coda))
    processo.start()

    # Aspettiamo il risultato controllando ogni mezzo secondo se il processo è ancora vivo:
    # così un crash viene segnalato subito, senza attendere tutto il timeout.
    scadenza = time.monotonic() + TIMEOUT_ESECUZIONE
    while True:
        try:
            esito = coda.get(timeout=0.5)
            break
        except queue.Empty:
            errore = None
            if not processo.is_alive():
                errore = "Il processo di analisi si è interrotto senza risultato"
            elif time.monotonic() > scadenza:
                processo.terminate()
                errore = f"Tempo massimo di {TIMEOUT_ESECUZIONE} s superato"
            if errore:
                esito = {"risultato": "", "immagine": None, "errore": errore}
                break
    processo.join()
    return esito


def analizza(domanda: str, df: pd.DataFrame) -> dict:
    """Pipeline completa: domanda -> codice LLM -> esecuzione -> risultato."""
    codice = chiedi_codice(domanda, df)
    return {"codice": codice, "modello": LLM_MODEL, **esegui_in_sicurezza(codice, df)}


# -----------------------------------------------------------------------------
# 5. COMMENTO DEI RISULTATI (training e validazione)
# -----------------------------------------------------------------------------
# Regola: i numeri li calcola Python, l'LLM li commenta soltanto.
# Così il commento non può contenere valori inventati o calcolati male.

# Soglie usate per trasformare i numeri in giudizi (sono scelte di progetto, non leggi):
SOGLIA_COLLAPSE_KL = 0.1        # KL sotto questo valore: il modello ignora lo spazio latente
SOGLIA_STABILE_PERC = 1.0       # loss migliorata meno dell'1% nell'ultimo 10% delle epoche
SOGLIA_SCARTO_MEDIA_PERC = 20   # media sintetica lontana più del 20% della deviazione standard
RAPPORTO_STD_MIN, RAPPORTO_STD_MAX = 0.7, 1.3   # variabilità sintetica accettabile

ISTRUZIONI_COMMENTO = """Sei un data scientist che spiega i risultati di un VAE (Variational
Autoencoder) per dati tabellari sintetici a un pubblico misto: un docente di machine learning
e persone senza competenze tecniche.
Scrivi in italiano, 5-8 frasi. Usa i termini tecnici corretti (loss, KL, posterior collapse,
correlazione...) ma spiega ognuno con parole semplici, in modo che chiunque possa capire.
Niente elenchi puntati, niente titoli.
Usa SOLO i numeri presenti nei FATTI: non calcolarne di nuovi e non inventarne.
Se un fatto segnala un problema, dillo chiaramente. Concludi con un consiglio pratico."""


def riassumi_training(storico: list, parametri: dict) -> dict:
    """Trasforma le loss per epoca in pochi fatti già calcolati."""
    prima, ultima = storico[0], storico[-1]
    finestra = max(1, len(storico) // 10)            # ultimo 10% delle epoche
    riferimento = storico[-finestra - 1] if len(storico) > finestra else prima
    miglioramento_finale = (riferimento["loss"] - ultima["loss"]) / riferimento["loss"] * 100
    return {
        "parametri": parametri,
        "epoche_eseguite": len(storico),
        "loss_iniziale": round(prima["loss"], 4),
        "loss_finale": round(ultima["loss"], 4),
        "riduzione_loss_percentuale": round((prima["loss"] - ultima["loss"]) / prima["loss"] * 100, 1),
        "ricostruzione_finale": round(ultima["ricostruzione"], 4),
        "kl_finale": round(ultima["kl"], 4),
        "miglioramento_ultimo_10_percento_epoche": round(miglioramento_finale, 2),
        "training_stabilizzato": abs(miglioramento_finale) < SOGLIA_STABILE_PERC,
        "posterior_collapse": ultima["kl"] < SOGLIA_COLLAPSE_KL,
    }


def riassumi_report(report: dict) -> dict:
    """Estrae dal report di validazione i fatti essenziali per il commento."""
    statistiche = pd.DataFrame(report["statistiche"])
    rapporto_std = statistiche["std_sintetica"] / statistiche["std_reale"]
    lontane = statistiche[statistiche["scarto_media_su_std_%"] > SOGLIA_SCARTO_MEDIA_PERC]
    varianza_anomala = statistiche[(rapporto_std < RAPPORTO_STD_MIN) | (rapporto_std > RAPPORTO_STD_MAX)]
    return {
        "differenza_media_correlazioni": report["differenza_media_correlazioni"],
        "nota_correlazioni": "0 = identiche; sotto 0.1 di solito buono",
        "colonne_confrontate": len(statistiche),
        "colonne_con_media_lontana": lontane["colonna"].tolist(),
        "colonne_con_variabilita_anomala": varianza_anomala["colonna"].tolist(),
        "privacy": report["privacy"],
        "nota_privacy": "quota_sintetici_troppo_vicini attesa intorno al 5% o meno",
    }


def commenta(argomento: str, fatti: dict) -> str:
    """Chiede all'LLM un commento in linguaggio naturale sui fatti già calcolati."""
    risposta = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": ISTRUZIONI_COMMENTO},
            {"role": "user", "content": f"Commenta i risultati del {argomento}.\n"
                                        f"FATTI:\n{json.dumps(fatti, ensure_ascii=False, indent=2)}"},
        ],
        temperature=0.2,
    )
    return risposta.choices[0].message.content.strip()

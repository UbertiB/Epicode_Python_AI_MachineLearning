"""
FASE 5 - BACKEND FASTAPI

Endpoint:
- GET  /health           servizio attivo e raggiungibilità dell'LLM
- POST /upload           carica il CSV reale e lo preprocessa
- POST /train            avvia l'addestramento del VAE in background (risponde subito)
- GET  /train/status     avanzamento e risultato dell'addestramento
- GET  /train/commento   commento dell'LLM sui risultati del training
- POST /generate         genera il dataset sintetico e lo salva nel backend
- GET  /synthetic-data   scarica l'ultimo dataset sintetico generato (CSV)
- GET  /real-data        dataset reale pulito (riferimento per i grafici della UI)
- GET  /report           statistiche, correlazioni e privacy check
- GET  /report/commento  commento dell'LLM sul report di validazione
- POST /analyze          domanda in linguaggio naturale sui dati sintetici

Regola HTTP seguita:
- GET  solo per leggere: non modifica nulla e ripeterlo dà sempre lo stesso risultato
       (metodo "sicuro" e "idempotente")
- POST per le azioni che modificano lo stato del backend

Avvio:  python api.py   (porta letta da API_PORT nel file .env, default 8001)
"""

import io
import logging
import math
import os
import threading
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from dotenv import load_dotenv
from fastapi.responses import Response
from pydantic import BaseModel, Field

import analista_llm
import vae
import validazione
from data_engine import DataEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
# La porta 8000 è spesso già occupata o riservata da Windows (Hyper-V, WSL, Docker)
API_PORT = int(os.getenv("API_PORT", 8001))
MAX_RIGHE_GENERATE = 500_000  # copre anche Credit Card Fraud (284.807 righe)

# -----------------------------------------------------------------------------
# 1. STATO DELL'APPLICAZIONE
# -----------------------------------------------------------------------------
# Lo stato resta in memoria nel processo del server: semplice e sufficiente per un utente.
# Con più utenti servirebbe salvare dataset e modelli su disco o su un database.
stato = {"engine": None, "reale": None, "X_reale": None, "modello": None,
         "storico": None, "sintetico": None}

# Avanzamento dell'addestramento, che gira in un thread separato (training asincrono).
# Valori di "stato": nessuno -> in_corso -> completato oppure errore
training = {"stato": "nessuno", "epoca": 0, "epoche_totali": 0, "storico": [], "errore": None,
            "parametri": None}
# Il lock impedisce che due richieste /train contemporanee avviino due addestramenti
lock_training = threading.Lock()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Prima di yield: avvio. Dopo yield: chiusura."""
    logger.info(f"Backend avviato. Dispositivo VAE: {vae.device}. LLM: {analista_llm.LLM_MODEL}")
    yield
    logger.info("Backend chiuso.")


app = FastAPI(title="Synthetic Data Sandbox - VAE Edition", lifespan=lifespan)


# -----------------------------------------------------------------------------
# 2. SCHEMI DELLE RICHIESTE (Pydantic valida i parametri in ingresso)
# -----------------------------------------------------------------------------
class ParametriTraining(BaseModel):
    latent_dim: int = Field(8, ge=2, le=64)
    epochs: int = Field(300, ge=1, le=2000)
    batch_size: int = Field(64, ge=8, le=4096)
    lr: float = Field(1e-3, gt=0, le=0.1)
    beta: float = Field(0.05, ge=0, le=10)


class ParametriGenerazione(BaseModel):
    n_righe: int = Field(768, ge=1, le=MAX_RIGHE_GENERATE)
    seed: int | None = None  # con lo stesso seed si ottengono gli stessi dati


class Domanda(BaseModel):
    testo: str = Field(..., min_length=3, max_length=500)


def richiedi(chiave: str, messaggio: str):
    """Restituisce un elemento dello stato o un errore 400 se il passaggio precedente manca."""
    if stato[chiave] is None:
        raise HTTPException(status_code=400, detail=messaggio)
    return stato[chiave]


def a_csv(df: pd.DataFrame) -> Response:
    return Response(df.to_csv(index=False), media_type="text/csv")


def senza_nan(df: pd.DataFrame) -> pd.DataFrame:
    """Il JSON non accetta NaN (es. correlazione di una colonna costante): diventa null."""
    return df.astype(object).where(pd.notna(df), None)


# -----------------------------------------------------------------------------
# 3. ENDPOINT
# -----------------------------------------------------------------------------
@app.get("/health")
def health():
    """
    Health check. Se la risposta arriva, il backend è vivo.
    In più verifica la dipendenza esterna (LM Studio / OpenAI):
    - "ok"         tutto funziona
    - "degradato"  backend funzionante, ma l'analista LLM non è disponibile
    I flag dataset_caricato e modello_addestrato sono DERIVATI dallo stato,
    non memorizzati: si ricalcolano a ogni chiamata e non possono contraddirlo.
    """
    llm_raggiungibile = analista_llm.llm_raggiungibile()
    return {
        "servizio": "ok" if llm_raggiungibile else "degradato",
        "llm": analista_llm.LLM_MODEL,
        "llm_raggiungibile": llm_raggiungibile,
        "dataset_caricato": stato["reale"] is not None,
        "modello_addestrato": stato["modello"] is not None,
        "training": training["stato"],
    }


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    """Legge il CSV, lo pulisce e prepara la matrice per il VAE. Azzera i passaggi successivi."""
    try:
        df = pd.read_csv(io.BytesIO(file.file.read()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV non leggibile: {e}")
    if df.empty:
        raise HTTPException(status_code=400, detail="Il file è vuoto.")
    # Un nuovo dataset durante l'addestramento renderebbe incoerente il modello in arrivo
    if training["stato"] == "in_corso":
        raise HTTPException(status_code=409, detail="Addestramento in corso: attendi la fine.")

    engine = DataEngine()
    reale = engine.fit(df)
    stato.update(engine=engine, reale=reale, X_reale=engine.transform(reale),
                 modello=None, storico=None, sintetico=None)
    training.update(stato="nessuno", epoca=0, epoche_totali=0, storico=[], errore=None)
    logger.info(f"Dataset caricato: {file.filename}, {len(reale)} righe")
    return {"file": file.filename, "riepilogo": engine.riepilogo}


def _esegui_training(X, parametri: dict):
    """
    Gira in un thread separato. Aggiorna 'training' a ogni epoca e, alla fine,
    salva il modello in 'stato'. Gli errori vengono registrati, non persi:
    in un thread un'eccezione non arriverebbe mai al client.
    """
    def a_fine_epoca(perdite: dict):
        # Loss NaN o infinita (es. learning rate troppo alto): il modello è divergente.
        # Si interrompe subito; in più il JSON non accetta NaN e /train/status andrebbe in errore.
        if not math.isfinite(perdite["loss"]):
            raise ValueError(f"loss non valida all'epoca {perdite['epoca']}: "
                             "prova a ridurre il learning rate")
        training["epoca"] = perdite["epoca"]
        training["storico"].append(perdite)

    try:
        modello, storico = vae.addestra(X, callback=a_fine_epoca, **parametri)
        stato.update(modello=modello, storico=storico)
        training["stato"] = "completato"
        logger.info(f"Training completato, loss finale {storico[-1]['loss']:.4f}")
    except Exception as e:
        training.update(stato="errore", errore=f"{type(e).__name__}: {e}")
        logger.exception("Training fallito")


@app.post("/train", status_code=202)
def train(parametri: ParametriTraining):
    """
    Addestramento asincrono: l'endpoint avvia il training in un thread separato e risponde
    subito con 202 (Accepted = "richiesta accettata, il lavoro è in corso").
    Streamlit non resta bloccato in attesa: interroga GET /train/status per l'avanzamento.
    Così anche un training lungo non va in timeout lato client.
    """
    X = richiedi("X_reale", "Carica prima un dataset con /upload.")
    with lock_training:  # controllo e avvio devono avvenire insieme, senza interruzioni
        if training["stato"] == "in_corso":
            raise HTTPException(status_code=409, detail="Un addestramento è già in corso.")
        # Il modello precedente e i suoi dati sintetici non valgono più
        stato.update(modello=None, storico=None, sintetico=None)
        training.update(stato="in_corso", epoca=0, epoche_totali=parametri.epochs,
                        storico=[], errore=None, parametri=parametri.model_dump())
        threading.Thread(target=_esegui_training, args=(X, parametri.model_dump()),
                         daemon=True).start()
    logger.info(f"Training avviato: {parametri.epochs} epoche")
    return {"stato": "in_corso", "epoche_totali": parametri.epochs}


@app.get("/train/status")
def train_status():
    """Solo lettura: stato, epoca corrente e storico delle loss calcolate finora."""
    return {**training, "storico": list(training["storico"])}


@app.post("/generate")
def generate(parametri: ParametriGenerazione):
    """
    Decoder + vettori casuali N(0,1) -> nuovi record, riportati ai valori originali.
    È un POST perché crea un nuovo dataset e sostituisce il precedente:
    """
    modello = richiedi("modello", "Addestra prima il modello con /train.")
    X_sintetico = vae.genera(modello, parametri.n_righe, parametri.seed)
    stato["sintetico"] = stato["engine"].inverse_transform(X_sintetico)
    logger.info(f"Generati {parametri.n_righe} record sintetici")
    return {"righe": len(stato["sintetico"]), "colonne": list(stato["sintetico"].columns),
            "seed": parametri.seed}


@app.get("/synthetic-data")
def synthetic_data():
    """Solo lettura: restituisce sempre lo stesso file finché non si genera di nuovo."""
    return a_csv(richiedi("sintetico", "Genera prima i dati con /generate."))


@app.get("/real-data")
def real_data():
    return a_csv(richiedi("reale", "Carica prima un dataset con /upload."))


@app.get("/report")
def report():
    reale = richiedi("reale", "Carica prima un dataset con /upload.")
    sintetico = richiedi("sintetico", "Genera prima i dati con /generate.")
    correlazioni = validazione.confronta_correlazioni(reale, sintetico)
    return {
        "statistiche": senza_nan(validazione.confronta_statistiche(reale, sintetico)).to_dict("records"),
        "correlazione_reale": senza_nan(correlazioni["reale"]).to_dict(),
        "correlazione_sintetica": senza_nan(correlazioni["sintetica"]).to_dict(),
        "differenza_media_correlazioni": correlazioni["differenza_media"],
        "privacy": validazione.privacy_check(
            reale, sintetico, stato["X_reale"], stato["engine"].transform(sintetico)),
    }


@app.post("/analyze")
def analyze(domanda: Domanda):
    """L'analisi lavora sui dati SINTETICI: i dati reali non vengono mai mostrati all'LLM."""
    sintetico = richiedi("sintetico", "Genera prima i dati con /generate.")
    try:
        return analista_llm.analizza(domanda.testo, sintetico)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Errore LLM: {e}")


# -----------------------------------------------------------------------------
# 4. COMMENTI DELL'LLM SUI RISULTATI
# -----------------------------------------------------------------------------
# Endpoint separati dal training e dalla generazione: se l'LLM non risponde,
# il resto dell'applicazione continua a funzionare (il commento restituisce 502).
# Sono GET perché non modificano lo stato; il testo però cambia a ogni chiamata,
# per questo Streamlit lo salva e non lo richiede a ogni rerun.
def _commento_llm(argomento: str, fatti: dict) -> dict:
    try:
        commento = analista_llm.commenta(argomento, fatti)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM non disponibile: {e}")
    return {"commento": commento, "fatti": fatti, "modello": analista_llm.LLM_MODEL}


@app.get("/train/commento")
def commento_training():
    if training["stato"] != "completato":
        raise HTTPException(status_code=400, detail="Nessun addestramento completato da commentare.")
    fatti = analista_llm.riassumi_training(training["storico"], training["parametri"])
    return _commento_llm("training", fatti)


@app.get("/report/commento")
def commento_report():
    # Riusa l'endpoint /report: stessi controlli (dataset e sintetici presenti) e stessi numeri
    return _commento_llm("report di validazione", analista_llm.riassumi_report(report()))


# -----------------------------------------------------------------------------
# 5. AVVIO DIRETTO:  python api.py
# -----------------------------------------------------------------------------
# Alternativa al comando "uvicorn api:app": il server viene avviato da Python stesso.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=API_PORT)

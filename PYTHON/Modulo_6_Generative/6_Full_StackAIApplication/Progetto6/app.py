"""
FASE 5 - DASHBOARD STREAMLIT

L'interfaccia non contiene logica di machine learning: chiama solo gli endpoint FastAPI.
Avvio (con il backend già acceso):  streamlit run app.py
"""

import base64
import io
import os
import time

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. CONFIGURAZIONE
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Synthetic Data Sandbox", layout="wide")
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8001")
RIGHE_DATASET_GRANDE = 50_000


# -----------------------------------------------------------------------------
# 2. FUNZIONI DI SUPPORTO
# -----------------------------------------------------------------------------
def chiama_api(metodo: str, endpoint: str, ferma_su_errore: bool = True, **kwargs):
    """
    Chiamata HTTP al backend. In caso di errore mostra il messaggio e ferma la pagina.
    Con ferma_su_errore=False restituisce None e lascia proseguire la pagina:
    serve per le funzioni facoltative (es. il commento dell'LLM).
    """
    try:
        risposta = requests.request(metodo, f"{API_URL}{endpoint}", timeout=600, **kwargs)
    except requests.exceptions.ConnectionError:
        st.error(f"Backend non raggiungibile su {API_URL}. Avvialo con: python api.py")
        st.stop()
    if not risposta.ok:
        dettaglio = risposta.json().get('detail', risposta.text)
        if not ferma_su_errore:
            st.warning(f"Errore {risposta.status_code}: {dettaglio}")
            return None
        st.error(f"Errore {risposta.status_code}: {dettaglio}")
        st.stop()
    return risposta


def mostra_commento(etichetta: str, endpoint: str, chiave: str):
    """
    Commento dell'LLM su richiesta (bottone). Il risultato viene salvato in session_state:
    senza, a ogni rerun si richiamerebbe l'LLM (lento) e il testo cambierebbe ogni volta.
    """
    if st.button(etichetta):
        with st.spinner("L'LLM sta scrivendo il commento..."):
            risposta = chiama_api("GET", endpoint, ferma_su_errore=False)
        if risposta is not None:
            st.session_state[chiave] = risposta.json()
    if chiave in st.session_state:
        esito = st.session_state[chiave]
        with st.container(border=True):
            st.markdown(esito["commento"])
            st.caption(f"Commento generato da {esito['modello']}")
        with st.expander("Numeri passati all'LLM (calcolati in Python, non dall'LLM)"):
            st.json(esito["fatti"])


def leggi_csv(risposta) -> pd.DataFrame:
    return pd.read_csv(io.StringIO(risposta.text))


def heatmap(ax, matrice: pd.DataFrame, titolo: str):
    """Disegna una matrice di correlazione con scala fissa da -1 a +1."""
    immagine = ax.imshow(matrice.values.astype(float), cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(matrice)), matrice.columns, rotation=90, fontsize=8)
    ax.set_yticks(range(len(matrice)), matrice.index, fontsize=8)
    ax.set_title(titolo)
    return immagine


# -----------------------------------------------------------------------------
# 3. SEZIONI DELLA PAGINA
# -----------------------------------------------------------------------------
def sezione_dati():
    st.subheader("1. Caricamento file e preprocessing")
    file = st.file_uploader("Carica qui il CSV", type="csv")
    if file and st.button("Carica e preprocessa", type="primary"):
        esito = chiama_api("POST", "/upload", files={"file": (file.name, file.getvalue())}).json()
        st.session_state.clear()  # nuovo dataset: si riparte da zero
        st.session_state.riepilogo = esito["riepilogo"]
        st.session_state.reale = leggi_csv(chiama_api("GET", "/real-data"))

    if "riepilogo" in st.session_state:
        r = st.session_state.riepilogo
        c1, c2, c3 = st.columns(3)
        c1.metric("Righe iniziali", r["righe_iniziali"])
        c2.metric("Righe dopo pulizia", r["righe_dopo_pulizia"])
        c3.metric("Dimensione vettore VAE", r["dimensione_vettore_vae"])
        st.write("**Numeriche (MinMaxScaler):**", ", ".join(r["colonne_numeriche"]))
        st.write("**Categoriche (One-Hot):**", ", ".join(r["colonne_categoriche"]) or "nessuna")
        st.write("**Valori nulli imputati:**", r["nulli_imputati"] or "nessuno")
        st.dataframe(st.session_state.reale.head(10))


def segui_training(esito: dict) -> dict:
    """
    Interroga GET /train/status ogni secondo e aggiorna barra e grafico finché il
    training è in corso (tecnica del "polling"). Restituisce lo stato finale.
    """
    barra = st.progress(0.0)
    grafico = st.empty()  # segnaposto: il grafico viene ridisegnato a ogni aggiornamento
    while esito["stato"] == "in_corso":
        totali = max(esito["epoche_totali"], 1)
        barra.progress(esito["epoca"] / totali, text=f"Epoca {esito['epoca']} di {totali}")
        if esito["storico"]:
            grafico.line_chart(pd.DataFrame(esito["storico"]).set_index("epoca")[["ricostruzione", "kl"]])
        time.sleep(1)
        esito = chiama_api("GET", "/train/status").json()
    barra.empty()
    grafico.empty()
    return esito


def sezione_training():
    st.subheader("2. Addestramento del VAE")
    # Per dataset grandi (RIGHE_DATASET_GRANDE) propongo un numero di epoche inferiore
    # ed un batch size maggiore
    # questo per evitare tempo troppo lunghi sul mio pc poco performante.
    grande = len(st.session_state.reale) > RIGHE_DATASET_GRANDE
    if grande:
        st.info("Dataset grande: proposti batch 512 e 20 epoche per tempi di training ragionevoli.")
    c1, c2, c3, c4, c5 = st.columns(5)
    parametri = {
        "latent_dim": c1.number_input("Dimensione latente", 2, 64, 8),
        "epochs": c2.number_input("Epoche", 1, 2000, 20 if grande else 300),
        "batch_size": c3.number_input("Batch size", 8, 4096, 512 if grande else 64),
        "lr": c4.number_input("Learning rate", 0.0001, 0.1, 0.001, format="%.4f"),
        "beta": c5.number_input("Beta (peso KL)", 0.0, 10.0, 0.05, step=0.01,
                                help="Con 1.0 i dati sintetici escono quasi tutti uguali"),
    }
    if st.button("Avvia addestramento", type="primary"):
        # Training asincrono: il backend risponde subito e addestra in background
        chiama_api("POST", "/train", json=parametri)
        # Nuovo training: risultati e commenti precedenti non valgono più
        for chiave in ("storico", "sintetico", "commento_training", "commento_report"):
            st.session_state.pop(chiave, None)

    # Lo stato del training si legge SEMPRE dal backend, anche dopo un ricaricamento della
    # pagina: il training continua sul server anche se Streamlit viene chiuso o aggiornato.
    esito = chiama_api("GET", "/train/status").json()
    if esito["stato"] == "in_corso":
        esito = segui_training(esito)
    if esito["stato"] == "completato" and "storico" not in st.session_state:
        st.session_state.storico = pd.DataFrame(esito["storico"]).set_index("epoca")
        st.rerun()  # ridisegna la pagina: si sblocca la scheda di generazione
    elif esito["stato"] == "errore":
        st.error(f"Addestramento fallito: {esito['errore']}")

    if "storico" in st.session_state:
        storico = st.session_state.storico
        st.caption(f"Loss finale: {storico['loss'].iloc[-1]:.4f}")
        st.line_chart(storico[["ricostruzione", "kl"]])
        mostra_commento("Spiega i risultati del training", "/train/commento", "commento_training")


def sezione_generazione():
    st.subheader("3. Generazione e validazione")
    n_righe = st.number_input("Numero di righe da generare", 10, 500_000,
                              len(st.session_state.reale))
    if st.button("Genera dati sintetici", type="primary"):
        chiama_api("POST", "/generate", json={"n_righe": n_righe})        # azione: crea i dati
        st.session_state.sintetico = leggi_csv(chiama_api("GET", "/synthetic-data"))  # lettura
        st.session_state.report = chiama_api("GET", "/report").json()
        st.session_state.pop("commento_report", None)   # nuovi dati: il vecchio commento non vale

    if "sintetico" not in st.session_state:
        return
    reale, sintetico, report = (st.session_state.reale, st.session_state.sintetico,
                                st.session_state.report)

    st.download_button("Scarica il CSV sintetico", sintetico.to_csv(index=False),
                       file_name="dataset_sintetico.csv", mime="text/csv")

    # Tabella comparativa
    c1, c2 = st.columns(2)
    c1.write("**Dati reali**")
    c1.dataframe(reale.head(10))
    c2.write("**Dati sintetici**")
    c2.dataframe(sintetico.head(10))
    st.write("**Statistiche a confronto**")
    st.dataframe(pd.DataFrame(report["statistiche"]).set_index("colonna"))

    # Correlazioni
    st.write(f"**Correlazioni** (differenza media assoluta: "
             f"{report['differenza_media_correlazioni']})")
    fig, assi = plt.subplots(1, 2, figsize=(12, 5))
    heatmap(assi[0], pd.DataFrame(report["correlazione_reale"]), "Reale")
    immagine = heatmap(assi[1], pd.DataFrame(report["correlazione_sintetica"]), "Sintetico")
    fig.colorbar(immagine, ax=assi, shrink=0.8)
    st.pyplot(fig)

    # Distribuzioni
    colonna = st.selectbox("Distribuzione della colonna", reale.columns)
    fig, ax = plt.subplots(figsize=(8, 3.5))
    if reale[colonna].nunique() <= 10:  # categorica: frequenze relative affiancate
        pd.DataFrame({"Reale": reale[colonna].value_counts(normalize=True),
                      "Sintetico": sintetico[colonna].value_counts(normalize=True)}
                     ).plot.bar(ax=ax)
    else:  # numerica: istogrammi sovrapposti normalizzati
        ax.hist(reale[colonna], bins=30, alpha=0.5, density=True, label="Reale")
        ax.hist(sintetico[colonna], bins=30, alpha=0.5, density=True, label="Sintetico")
        ax.legend()
    ax.set_title(f"Distribuzione di {colonna}")
    st.pyplot(fig)

    # Privacy
    p = report["privacy"]
    st.write("**Privacy check**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Record identici ai reali", p["copie_esatte"])
    c2.metric("Distanza mediana sintetico-reale", p["dcr_mediana_sintetici"],
              help=f"Riferimento reale-reale: {p['dcr_mediana_reali']}")
    c3.metric("Sintetici troppo vicini a un reale", f"{p['quota_sintetici_troppo_vicini_%']}%",
              help="Quota sotto il 5° percentile delle distanze reale-reale. Atteso circa 5% o meno.")
    if p["copie_esatte"] > 0:
        st.warning("Ci sono record copiati dai dati reali: possibile overfitting.")

    # commento da LLM
    mostra_commento("Spiega il report di validazione", "/report/commento", "commento_report")


def sezione_analista():
    st.subheader("4. Natural Language Analyst (sui dati sintetici)")
    st.session_state.setdefault("chat", [])

    for messaggio in st.session_state.chat:
        with st.chat_message(messaggio["ruolo"]):
            st.markdown(messaggio["testo"])
            if messaggio.get("codice"):
                with st.expander(f"Codice generato da {messaggio['modello']}"):
                    st.code(messaggio["codice"], language="python")
            if messaggio.get("immagine"):
                st.image(base64.b64decode(messaggio["immagine"]))
            if messaggio.get("errore"):
                st.error(messaggio["errore"])

    domanda = st.chat_input("Es. Fai una domanda (puoi includere anche grafici).")
    if domanda:
        st.session_state.chat.append({"ruolo": "user", "testo": domanda})
        with st.spinner("L'LLM scrive il codice e il backend lo esegue..."):
            esito = chiama_api("POST", "/analyze", json={"testo": domanda}).json()
        st.session_state.chat.append({"ruolo": "assistant", "testo": esito["risultato"] or "",
                                      **esito})
        st.rerun()


# -----------------------------------------------------------------------------
# 4. MAIN
# -----------------------------------------------------------------------------
def main():
    st.title("Synthetic Data - VAE - (Progetto M6)")
    st.caption("Impara le distribuzioni di un dataset sensibile e lo rigenera senza dati reali.")

    with st.sidebar:
        # Risposta di GET /health: se il backend è spento, chiama_api mostra l'errore e si ferma
        info_backend = chiama_api("GET", "/health").json()
        st.header("Stato sistema")
        st.write(f"Backend: {API_URL}")
        st.write(f"Dataset caricato: {'si' if info_backend['dataset_caricato'] else 'no'}")
        st.write(f"Modello addestrato: {'si' if info_backend['modello_addestrato'] else 'no'}")
        st.write(f"LLM: {info_backend['llm']}")
        if info_backend["llm_raggiungibile"]:
            st.success("LLM raggiungibile")
        else:
            st.warning("LLM non raggiungibile: l'analista non funzionerà. "
                       "Avvia il server di LM Studio o controlla il file .env.")

    # Ogni scheda si attiva solo quando il passaggio precedente è completato:
    # schede è una lista di tuple
    # la lista contiene i 4 folder:
    #       1) dati
    #       2) addestramento
    #       3) generazione e validazione
    #       4) analista llm
    # ogni fold contiene 4 dati: 
    #       1) etichetta: mostrato come titolo della scheda
    #       2) funzione da lanciare: ogni funzione deve essere già definita (sezione_dati, sezione_training, sezione_generazione, sezione_analista)
    #       3) requisito
    #       4) testo di default da mostrare in assenza dei requisisti
    #
    schede = [
        ("Dati", sezione_dati, None, ""),
        ("Addestramento", sezione_training, "reale", "Carica prima un dataset."),
        ("Generazione e validazione", sezione_generazione, "storico", "Addestra prima il modello."),
        ("Analista LLM", sezione_analista, "sintetico", "Genera prima i dati."),
    ]
    for scheda, (_, funzione, requisito, messaggio) in zip(st.tabs([s[0] for s in schede]), schede):
        with scheda:
            if requisito is None or requisito in st.session_state:
                funzione()  #esegue la funzione associato al fold
            else:
                st.info(messaggio)  # messaggio standard se non ho i requisiti per eseguire la funzione


if __name__ == "__main__":
    main()

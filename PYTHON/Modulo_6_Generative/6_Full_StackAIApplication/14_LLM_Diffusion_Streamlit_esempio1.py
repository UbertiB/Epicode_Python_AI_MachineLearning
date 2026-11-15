
"""

LMM + Diffusion

una chat tutta in locale

Chat locale: LLM (LM Studio) + modello di diffusione (Stable Diffusion via diffusers)

Logica:
  1. L'utente scrive un messaggio.
  2. L'LLM risponde in JSON e decide se serve un'immagine (fa da "router").
  3. Solo se serve, il modello di diffusione genera l'immagine dal prompt preparato dall'LLM.

Installazione (venv attivo):
  pip install streamlit openai diffusers transformers accelerate torch
  (con scheda NVIDIA installa torch con CUDA dal comando indicato su pytorch.org)

Avvio:
  streamlit run chat_immagini.py
"""

import json
import time

import streamlit as st
from openai import OpenAI



LMSTUDIO_URL = "http://localhost:1234/v1"
# Modello di diffusione scaricato da Hugging Face al primo avvio (circa 4-5 GB)
MODELLO_DIFFUSIONE = "stable-diffusion-v1-5/stable-diffusion-v1-5"

ISTRUZIONI = """Sei un assistente. Rispondi SEMPRE e SOLO con un JSON valido, così:
{"risposta": "testo per l'utente in italiano",
 "genera_immagine": true oppure false,
 "prompt_immagine": "descrizione dell'immagine in INGLESE, max 60 parole, oppure null"}
Metti genera_immagine a true SOLO se l'utente chiede esplicitamente di creare,
disegnare o generare un'immagine. In tutti gli altri casi false e prompt_immagine null."""


# ---------------------------------------------------------------- LLM
client = OpenAI(base_url=LMSTUDIO_URL, api_key="lm-studio", timeout=300)

st.set_page_config(page_title="Chat + immagini", layout="wide")

@st.cache_data(ttl=60)
def modelli_llm():
    return [m.id for m in client.models.list().data
            if "embed" not in m.id and "diffusion" not in m.id]


def interpreta(testo):
    """Estrae il JSON dalla risposta. Se il modello non lo rispetta, niente immagine."""
    try:
        dati = json.loads(testo[testo.find("{"): testo.rfind("}") + 1])
        return {"risposta": dati.get("risposta") or "",
                "genera_immagine": bool(dati.get("genera_immagine")),
                "prompt_immagine": dati.get("prompt_immagine")}
    except (ValueError, TypeError):
        return {"risposta": testo, "genera_immagine": False, "prompt_immagine": None}


def chiedi_llm(modello, storico):
    messaggi = [{"role": "system", "content": ISTRUZIONI}] + [
        {"role": m["role"], "content": m["content"]} for m in storico]
    r = client.chat.completions.create(model=modello, messages=messaggi, temperature=0.3)
    return interpreta(r.choices[0].message.content), r.model


# ---------------------------------------------------------------- DIFFUSIONE
@st.cache_resource(show_spinner="Carico il modello di diffusione (la prima volta lo scarica)...")
def carica_diffusione():
    import torch
    from diffusers import StableDiffusionPipeline

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    pipe = StableDiffusionPipeline.from_pretrained(MODELLO_DIFFUSIONE, torch_dtype=dtype)
    return pipe.to(device), device


def genera_immagine(prompt, passi):
    pipe, device = carica_diffusione()
    t0 = time.time()
    img = pipe(prompt, num_inference_steps=passi, height=512, width=512).images[0]
    return img, device, time.time() - t0


# ---------------------------------------------------------------- INTERFACCIA
st.sidebar.header("Modelli")
try:
    elenco = modelli_llm()
except Exception as e:
    st.sidebar.error(f"LM Studio non raggiungibile: {e}")
    st.stop()

predefinito = "google/gemma-4-e4b"
modello_llm = st.sidebar.selectbox(
    "LLM (LM Studio)", elenco,
    index=elenco.index(predefinito) if predefinito in elenco else 0)
st.sidebar.text_input("Modello di diffusione", MODELLO_DIFFUSIONE, disabled=True)
passi = st.sidebar.slider("Passi di diffusione", 10, 50, 20,
                          help="Più passi = più qualità ma più lento")
if st.sidebar.button("Nuova conversazione"):
    st.session_state.chat = []

st.title("Chat con generazione immagini")
st.caption(f"LLM: **{modello_llm}**  |  Diffusione: **{MODELLO_DIFFUSIONE}**")

if "chat" not in st.session_state:
    st.session_state.chat = []

# ridisegno la conversazione (a ogni rerun lo script riparte da capo)
for m in st.session_state.chat:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("immagine") is not None:
            st.image(m["immagine"], caption=m["didascalia"])
        if m.get("info"):
            st.caption(m["info"])

domanda = st.chat_input("Scrivi qui (es. 'genera un'immagine di un magazzino automatizzato')")
if domanda:
    st.session_state.chat.append({"role": "user", "content": domanda})
    with st.chat_message("user"):
        st.markdown(domanda)

    with st.chat_message("assistant"):
        try:
            with st.spinner(f"{modello_llm} sta rispondendo..."):
                esito, llm_usato = chiedi_llm(modello_llm, st.session_state.chat)
            st.markdown(esito["risposta"])

            nuovo = {"role": "assistant", "content": esito["risposta"],
                     "immagine": None, "didascalia": None,
                     "info": f"LLM: {llm_usato} | immagine richiesta: "
                             f"{'sì' if esito['genera_immagine'] else 'no'}"}

            if esito["genera_immagine"] and esito["prompt_immagine"]:
                with st.spinner("Genero l'immagine..."):
                    img, device, secondi = genera_immagine(esito["prompt_immagine"], passi)
                nuovo["immagine"] = img
                nuovo["didascalia"] = f"Prompt: {esito['prompt_immagine']}"
                nuovo["info"] += (f" | Diffusione: {MODELLO_DIFFUSIONE} su {device.upper()}"
                                  f" in {secondi:.0f} s")
                st.image(img, caption=nuovo["didascalia"])

            st.caption(nuovo["info"])
            st.session_state.chat.append(nuovo)
        except Exception as e:
            st.error(f"Errore: {e}")
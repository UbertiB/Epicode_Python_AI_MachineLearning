
"""

LM Studio interfaccia in Streamlit
una chat tutta in locale
"""
import streamlit as st
from openai import OpenAI

# 1) connessione a LM Studio (timeout: dopo 5 minuti va in errore invece di aspettare all'infinito)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio", timeout=300)

# 2) QUI SCEGLI IL MODELLO: nome copiato esattamente dalla lista
MODELLO = "google/gemma-4-e4b"

st.title("Assistente locale")
st.caption(f"Modello: {MODELLO}")

# 3) memoria della conversazione
if "msg" not in st.session_state:
    st.session_state.msg = []

# 4) ridisegna i messaggi precedenti (a ogni rerun lo script riparte da capo)
for m in st.session_state.msg:
    st.chat_message(m["role"]).markdown(m["content"])

# 5) nuova domanda
domanda = st.chat_input("Scrivi qui")
if domanda:
    st.session_state.msg.append({"role": "user", "content": domanda})
    st.chat_message("user").markdown(domanda)

    try:
        with st.spinner("Sto pensando..."):
            r = client.chat.completions.create(
                model=MODELLO,                    # <-- il modello va qui
                messages=st.session_state.msg,
                temperature=0.2,
            )
        testo = r.choices[0].message.content
        st.session_state.msg.append({"role": "assistant", "content": testo})
        st.chat_message("assistant").markdown(testo)
        st.caption(f"Risposto da: {r.model}")
    except Exception as e:
        st.error(f"Errore: {e}")
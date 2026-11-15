
"""

LM Studio interfaccia in Streamlit
"""

import streamlit as st
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# escludo embedding e stable diffusion, che non servono per la chat
modelli = [m.id for m in client.models.list().data
           if "embed" not in m.id and "diffusion" not in m.id]

MODELLO = st.selectbox("Modello", modelli)
domanda = st.text_input("Domanda", "Cos'è la scorta di sicurezza?")

if st.button("Chiedi"):
    with st.spinner(f"{MODELLO} sta pensando..."):
        r = client.chat.completions.create(
            model=MODELLO,
            messages=[{"role": "user", "content": domanda}],
            temperature=0.2,
        )
    st.caption(f"Risposto da: {r.model}")
    st.markdown(r.choices[0].message.content)
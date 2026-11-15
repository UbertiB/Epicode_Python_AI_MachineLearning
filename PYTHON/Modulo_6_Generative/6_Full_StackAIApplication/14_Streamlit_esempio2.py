
"""
PER ESEGUIRE:
in powershell con il venv attivo:  streamlit run 14_streamlit_esempio2.py

"""

"""
rerun in azione
parte ad ogni modifica di dato, 
lo script parte dall'alto al basso ad ogni modifica di dato
"""

import streamlit as st

st.title("Calcolo valore riga ordine")

qta = st.number_input("Quantità", min_value=0, value=10)
prezzo = st.number_input("Prezzo unitario €", min_value=0.0, value=12.5)
sconto = st.slider("Sconto %", 0, 50, 0)

totale = qta * prezzo * (1 - sconto / 100)
st.metric("Totale riga", f"{totale:,.2f} €")

if st.button("Conferma"):
    st.success("Riga confermata")
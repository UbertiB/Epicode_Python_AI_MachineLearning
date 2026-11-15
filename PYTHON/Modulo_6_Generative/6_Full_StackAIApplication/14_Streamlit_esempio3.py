
"""
PER ESEGUIRE:
in powershell con il venv attivo:  streamlit run 14_streamlit_esempio3.py

"""

"""
input file, elaborazione con pandas, output con tabella, grafico e download.
"""

import streamlit as st
import pandas as pd

st.title("Analisi ordini da CSV")

file = st.file_uploader("Carica un CSV ordini", type="csv")

if file is not None:
    df = pd.read_csv(file, sep=";")
    st.subheader("Dati")
    st.dataframe(df)

    st.subheader("Fatturato per cliente")
    per_cliente = df.groupby("cliente")["importo"].sum().sort_values(ascending=False)
    st.bar_chart(per_cliente)

    st.download_button("Scarica riepilogo", per_cliente.to_csv(sep=";"),
                       file_name="riepilogo.csv")
else:
    st.info("Carica un file con colonne: cliente;articolo;quantita;importo")
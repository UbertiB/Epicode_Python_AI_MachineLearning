
"""
PER ESEGUIRE:
in powershell con il venv attivo:  streamlit run 14_streamlit_esempio4.py

"""

"""
Sidebar, filtri, cache e session_state
"""
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(page_title="Magazzino", layout="wide")

@st.cache_data          # eseguita una volta sola, poi il risultato resta in memoria
def carica_dati():
    time.sleep(2)       # simula una query lenta
    rng = np.random.default_rng(1)
    return pd.DataFrame({
        "articolo": [f"ART{i:03}" for i in range(50)],
        "famiglia": rng.choice(["Viteria", "Lamiere", "Motori"], 50),
        "giacenza": rng.integers(0, 500, 50),
        "scorta_min": rng.integers(20, 150, 50),
    })

df = carica_dati()

# Filtri nella barra laterale
st.sidebar.header("Filtri")
famiglie = st.sidebar.multiselect("Famiglia", df["famiglia"].unique(),
                                  default=df["famiglia"].unique())
solo_sotto = st.sidebar.checkbox("Solo sotto scorta minima")

f = df[df["famiglia"].isin(famiglie)]
if solo_sotto:
    f = f[f["giacenza"] < f["scorta_min"]]

# KPI su colonne
c1, c2, c3 = st.columns(3)
c1.metric("Articoli", len(f))
c2.metric("Giacenza totale", int(f["giacenza"].sum()))
c3.metric("Sotto scorta", int((f["giacenza"] < f["scorta_min"]).sum()))

st.dataframe(f, use_container_width=True)

# session_state: lista di articoli segnalati che resta tra i rerun
if "segnalati" not in st.session_state:
    st.session_state.segnalati = []

scelta = st.selectbox("Segnala articolo al buyer", f["articolo"])
if st.button("Aggiungi"):
    st.session_state.segnalati.append(scelta)

st.write("Segnalati:", st.session_state.segnalati)
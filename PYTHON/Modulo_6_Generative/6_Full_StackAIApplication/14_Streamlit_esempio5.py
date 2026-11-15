
"""
PER ESEGUIRE:
in powershell con il venv attivo:  streamlit run 14_streamlit_esempio4.py

"""

"""
Collegamento a un database con SQL, cache e form
"""
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Proposte MRP", layout="wide")

@st.cache_resource      # risorsa condivisa (connessione), non un dato
def get_conn():
    conn = sqlite3.connect("demo.db", check_same_thread=False)
    conn.execute("""CREATE TABLE IF NOT EXISTS proposte(
        id INTEGER PRIMARY KEY, articolo TEXT, fornitore TEXT,
        qta INTEGER, stato TEXT DEFAULT 'DA_RIVEDERE')""")
    if conn.execute("SELECT COUNT(*) FROM proposte").fetchone()[0] == 0:
        conn.executemany("INSERT INTO proposte(articolo,fornitore,qta) VALUES(?,?,?)",
            [("ART001","Rossi Spa",100),("ART002","Bianchi Srl",40),
             ("ART003","Rossi Spa",250)])
        conn.commit()
    return conn

@st.cache_data(ttl=60)  # dati in cache per 60 secondi
def leggi_proposte():
    return pd.read_sql("SELECT * FROM proposte", get_conn())

conn = get_conn()
st.title("Revisione proposte d'ordine")

df = leggi_proposte()
stato = st.radio("Stato", ["DA_RIVEDERE", "CONFERMATA", "SCARTATA"], horizontal=True)
st.dataframe(df[df["stato"] == stato], use_container_width=True)

# form: i widget dentro non scatenano rerun finché non premi Invia
with st.form("revisione"):
    id_sel = st.selectbox("ID proposta", df.loc[df["stato"] == "DA_RIVEDERE", "id"])
    nuova_qta = st.number_input("Nuova quantità", min_value=0, step=10)
    azione = st.selectbox("Azione", ["CONFERMATA", "SCARTATA"])
    inviato = st.form_submit_button("Salva")

if inviato and id_sel is not None:
    conn.execute("UPDATE proposte SET qta=?, stato=? WHERE id=?",
                 (nuova_qta, azione, int(id_sel)))
    conn.commit()
    leggi_proposte.clear()          # svuota la cache dopo la scrittura
    st.success(f"Proposta {id_sel} aggiornata")
    st.rerun()
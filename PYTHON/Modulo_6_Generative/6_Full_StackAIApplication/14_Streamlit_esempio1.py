"""
STREAMLIT
Streamlit è una libreria Python open source (licenza Apache 2.0 gratuita) per creare applicazioni web orientate ai dati. Trasforma scritp python in web app interattive. Ci si costruiscono dashboard, report o app di chat.
Scrivi solo python, senza html, css, o javascript, e ottieni una pagina web con bottoni, filtri, tabelle e grafici.
Streamlit genera il front-end al tuo posto, partendo dal codice python

Il server è il processo Python che esegue il programma. Il browser mostra la pagina e gli invia le azioni all'utente.

Un widget è un controllo della pagina, esempio un campo numerico, un menu, u pulsante. Quando confermi una modifrica di un widget, normalmente Streamlit fa un rerun. Riesegue il codice dall'alto verso il basso. Il widget restituisce il valore aggiornato. Python rifà i calcoli e la pagina mostr ail nuovo risultato.
Ogni volta che l'utente 'tocca' un widget, Streamlit riesegue tutto lo script dall'inizio alla fine.
1) Le variabili normali si azzerano a ogni interazione. Se vuoi che qualcosa resti in memoria (un contatore, un carrello, uno storico) devi usare st.sessione_state
2) Le operazioni lente (query al gestionale, lettura di excel grandi, modelli LLM) vanno messe in cache con @st.cache_data o @st.cach_resource, altrimenti ripartono ad ogni clic
3) Il codice si legge dall'alto in basso.
"""

"""
PER ESEGUIRE:
in powershell con il venv attivo:  streamlit run 14_streamlit_esempio1.py

"""

"""
st.write è il comando “universale”: 
mostra testo, numeri, tabelle e grafici, e capisce da solo cosa gli passi.
"""

import streamlit as st

st.title("La mia prima app")
st.write("Ciao Barbara, Streamlit funziona.")
st.write(2 + 3)
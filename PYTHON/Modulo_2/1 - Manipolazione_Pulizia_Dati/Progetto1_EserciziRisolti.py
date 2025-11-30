import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# # Introduzione

# # L’obiettivo è lavorare su un dataset di vendite storiche per capire la struttura dei dati, 
# # pulirli, analizzarli e realizzare previsioni semplici dei prossimi giorni usando Pandas e Python puro.
# # Gli step principali:
# # Caricamento e esplorazione dati
# # Pulizia
# # Analisi esplorativa
# # Raggruppamenti e aggregazioni
# # Implementazione di due previsioni semplici
# # Confronto tra previsioni
# # Output richiesti
# # Parte 1 – Caricamento e esplorazione dati
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# # Simulazione dataset vendite storiche
data = {
     "Data": pd.date_range(start="2025-01-01", periods=30),
     "Prodotto": ["A","B","C","A","B","C","A","B","C","A","B","C","A","B","C","A","B","C","A","B","C","A","B","C","A","B","C","A","B","C"],
     "Vendite": [10, 5, 2, 12, 6, 3, np.nan, 7, 4, 11, 5, 2, 13, 6, 3, 14, 7, 4, 12, 5, 2, 13, 6, 3, 10, 5, 2, 12, 6, 3],
     "Prezzo": [100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200, 100, 150, 200]
 }

df = pd.DataFrame(data)

# #
# # Parte 1 – Esplorazione dati

# # Visualizzare prime righe
print(f"\n df.head(), mostra le prime righe: \n{df.head()}") #head() mostra le prime righe per avere un’idea dei dati.

# # Informazioni sul dataset

print(f"\n df.info(), verifica i tipi ed i valori mancanti: \n{df.info()}") # info() verifica tipi e valori mancanti.
# # Statistiche descrittive
print(f"\n df.describe(), calcola media, minimi, massimo e std: \n{df.describe()}")  #calcola medie, minimi, massimi, std delle colonne numeriche.

# #
# # Parte 2 – Pulizia dati

# # Gestione valori mancanti
df["Vendite"] = df["Vendite"].fillna(df["Vendite"].mean())  # Valori mancanti in “Vendite” sostituiti con media.

# # Rimuovere duplicati
df = df.drop_duplicates()  # Duplicati rimossi per evitare distorsioni.

# # Controllo tipi dati
df["Data"] = pd.to_datetime(df["Data"])  # Assicurato che le date siano datetime.
df["Vendite"] = df["Vendite"].astype(float) # Assicurato che le quantità siano numeriche.
df["Prezzo"] = df["Prezzo"].astype(float)

print(df.info())

#
# # Parte 3 – Analisi esplorativa

# # Vendite totali per prodotto
totali_per_prodotto = df.groupby("Prodotto")["Vendite"].sum() # groupby aggrega le vendite per prodotto.
print(f"\nTotali per prodotto: \n{totali_per_prodotto}")

# # Prodotto più e meno venduto
print("Prodotto più venduto:", totali_per_prodotto.idxmax())  # idxmax() e idxmin() identificano i prodotti con vendite estreme.
print("Prodotto meno venduto:", totali_per_prodotto.idxmin())

# # Vendite medie giornaliere
medie_giornaliere = df.groupby("Data")["Vendite"].mean()# groupby("Data") calcola la media giornaliera delle vendite totali.
print(f"Medie giornarliere: {medie_giornaliere}")

# # Parte 4 – Raggruppamenti e aggregazioni
# # Vendite mensili

df["Mese"] = df["Data"].dt.to_period("M")  # Aggiunta colonna “Mese” per aggregare per mese.
vendite_mensili = df.groupby("Mese")["Vendite"].sum()
print(f"\nVendite mensili: \n{vendite_mensili}")

# # Visualizzare trend
plt.plot(df["Data"], df["Vendite"], marker='o')  # Grafico lineare mostra trend giornaliero.
plt.title("Trend Vendite Giornaliero")
plt.xlabel("Data")
plt.xticks(rotation=45)
plt.ylabel("Vendite")
plt.grid(True)
plt.show()

#ho un solo mese, quindi il grafico a barre non è molto significativo, ma lo includo comunque
vendite_mensili.plot(kind="bar", title="Vendite mensili totali")  # Grafico a barre semplice mostra trend mensile.
plt.ylabel("Vendite")
plt.show()

#
# # Parte 5 – Previsioni di base
# # Metodo 1: media storica
media_storica = df["Vendite"].mean()  

# # Metodo 2: ultimo valore osservato
ultimo_valore = df["Vendite"].iloc[-1] 

print("Previsioni per i prossimi giorni:")
print("- media storica:", media_storica)
print("- ultimo valore osservato:", ultimo_valore)

#
#PREVISIONI  (semplice, solo con dati statistici, non modelli avanzati)
#

# # Applicazione su 7 giorni futuri
future_days = pd.date_range(start=df["Data"].max() + pd.Timedelta(days=1), periods=7)

previsione_media = pd.DataFrame({"Data": future_days,
                                "Vendite_Prev_Media": [media_storica]*7})  # La previsione media storica assume che le vendite future siano simili alla media passata.

previsione_ultimo = pd.DataFrame({"Data": future_days,"Vendite_Prev_Ultimo": [ultimo_valore]*7}) # La previsione ultimo valore osservato assume che le vendite rimangano costanti come nell’ultimo giorno.

print(f"Previsione da media: \n{previsione_media}")
print(f"previsione da ultimo valore: \n{previsione_ultimo}")

#
# # Parte 6 – Confronto previsioni
# Visualizza vendite storiche e previsioni su 7 giorni futuri.
# Permette di confrontare i due metodi e capire quale è più coerente col trend osservato.
plt.figure(figsize=(10,6))
plt.plot(df["Data"], df["Vendite"], color="skyblue", label="Storico")
plt.plot(previsione_media["Data"], previsione_media["Vendite_Prev_Media"], label="Previsione Media", color="red", linestyle="--")
plt.plot(previsione_ultimo["Data"], previsione_ultimo["Vendite_Prev_Ultimo"], label="Previsione Ultimo Valore", color="green", linestyle="--")
plt.title("Confronto previsioni vendite")
plt.xlabel("Data")
plt.xticks(rotation=45)
plt.ylabel("Vendite")
plt.legend()
plt.grid(True)
plt.show()

#
# # Parte 7 – Output richiesti

# # Notebook commentato: ogni cella con spiegazione.

# # Tabelle: aggregazioni per prodotto, vendite giornaliere e mensili, previsioni.

# # Grafici: trend storici e confronto previsioni.

# # Breve relazione (max 1 pagina) con:

# # Descrizione dataset e pulizia

# # Logica delle previsioni

# # Riflessi sul confronto delle due metodologie

"""
il dataset simulato contiene vendite di 3 prodotti su 30 giorni.
----- PARTE 1: ESPLORAZIONE DATI -----
Come prima cosa si VISUALIZZANO LE PRIME RIGHE (df.head) per cominciare a prendere familiarietà.
Si verificano i tipi ed i valori mancanti (df.info())
Calcola media, massimi, minimi e std (df.describe())
----- PARTE 2: PULIZIA DATI -----
Successivamente si puliscono i dati gestendo i VALORI MANCANTI (sostituiti con la media delle vendite) e RIMUOVENDO DUPLICATI.
Si VERIFICA CHE I TIPI DI DATI siano corretti (date come datetime, vendite e prezzi come float).
Valori mancanti (df["Vendite"].fillna)
Rimozione duplicati (df.drop_duplicates())
Controllo dei tipi (to_datetime e astype)
----- PARTE 3: ANALISI ESPLORATIVA -----
Si calcolano le VENDITE TOTALI PER PRODOTTO, identificando il PRODOTTO PIÙ E MENO VENDUTO (df.groupby("Prodotto")["Vendite"].sum(), idxmax() e idxmin()).
Si calcolano anche le VENDITE MEDIE GIORNALIERE.
----- PARTE 4: RAGGRUPPAMENTI E AGGREGAZIONI -----
Si RAGGRUPPANO I DATI per mese per visualizzare le vendite mensili totali 
e si crea un GRAIFCO per mostrare il trend delle vendite giornaliere.
----- PARTE 5: PREVISIONI DI BASE -----
Si implementano DUE METODI DI PREVISIONE semplici:
1) MEDIA STORICA delle vendite
2) ULTIMO VALORE OSSERVATO
Si applicano queste previsioni sui PROSSIMI 7 GIORNI.
----- PARTE 6: CONFRONTO PREVISIONI -----
Si confrontano le due previsioni graficamente insieme ai dati storici per valutare quale metodo sia più coerente col trend osservato.
----- PARTE 7: OUTPUT RICHIESTI -----

I grafici mostrano il trend delle vendite e il confronto tra le due previsioni.
In questo caso, le previsioni sono molto semplici e non tengono conto di stagionalità o trend complessi. (previsione media, previsione ultimo valore)
In un contesto reale, modelli più sofisticati sarebbero necessari per previsioni accurate.
La previsione dell'ultimo valore osservato può essere più reattiva a cambiamenti recenti, mentre la media storica è più stabile ma meno sensibile a variazioni recenti.
Leggendo il grafico, si può notare che la previsione basata sull'ultimo valore osservato tende ad essere inferiore alla media storica.
Non ci sono dati sufficienti per determinare il motivo di questa diminuzione delle ultime vendite, ma potrebbe essere dovuto a fattori stagionali, non considerati in questo modello.

"""
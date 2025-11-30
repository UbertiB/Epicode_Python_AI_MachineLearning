import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
PROGETTO 1 - PREVISIONE VENDITE
Traccia:
Lavorare su un dataset di vendite storiche per comprendere i dati, pulirli, trasformarli 
e produrre delle previsioni di base usando metodi semplici e direttamente implementabili con Pandas e Python “puro”.
Dataset (esempio di struttura)
    Data — data della vendita
    Prodotto — nome o codice prodotto
    Vendite — quantità venduta quel giorno
    Prezzo — prezzo unitario (opzionale)
I dati possono contenere valori mancanti, duplicati o inconsistenze.
"""

"""
CONSEGNA
Parte 1 - Caricamento e esplorazione dati
    1. Leggere il dataset con Pandas.
    2. Visualizzare le prime righe, la struttura (.info()), e statistiche descrittive (.describe()).
Parte 2 - Pulizia
    3. Gestire valori mancanti (es. sostituire con 0 o media).
    4. Rimuovere duplicati.
    5. Verificare che i tipi di dato siano corretti (date come datetime, quantità come numeri, ecc.).
Parte 3 - Analisi esplorativa
    6. Calcolare vendite totali per prodotto.
    7. Individuare il prodotto più venduto e quello meno venduto.
    8. Calcolare vendite medie giornaliere.
"""
#
#CARICAMENTO DEI DATI
#

store_valori = np.array([" Negozio1 ", "   NEGOZIO2", "negozio3        ", np.nan], dtype=object)   # necessario per mantenere il valore mancante
prodotto_valori = np.array(["A", "B", "C", "D", np.nan],dtype=object)

data = {
    "Store": np.random.choice(store_valori,size=60),
    "Data": np.random.choice(pd.date_range(start="2025-01-01", periods=60),size=60),
    "Prodotto": np.random.choice(prodotto_valori,size=60),
    "Quantita": np.random.randint(1,100,size=60),
    "Prezzo": np.random.randint(100,300,size=60)
 }
df = pd.DataFrame(data)
#aggiunto valori duplicati (ho caricato due volte i primi elementi)
df=pd.concat([df, df[:10]], ignore_index=True)
#aggiungo valori mancanti su prezzo e quantita

#aggiunto duplicati
df_temp = df.loc[:9].copy()   # prime 10 righe
df = pd.concat([df, df_temp], ignore_index=True)
#aggiungo outlier
df_temp=df.tail(9).copy()
df_temp["Prezzo"].iloc[-1]=df_temp["Prezzo"].iloc[-1]*10
df_temp["Prezzo"].iloc[-2]=df_temp["Prezzo"].iloc[-2]*20
df_temp["Quantita"].iloc[-2]=df_temp["Quantita"].iloc[-2]*20
df = pd.concat([df, df_temp], ignore_index=True)
#aggiungo mancanti sulla quantita
df_temp=df.tail(9).copy()
df_temp["Quantita"]=np.nan
df = pd.concat([df, df_temp], ignore_index=True)
#
#ESPLORO I DATI
#

#visualizzo i dati
#print(f"Visualizzo le prime righe delle vendite \n{df.head()}") #visualizzo le prime righe
#Informazioni sul dataset
print(f"dimensione dataframe: {df.shape}")  #dimensione dataframe
print(f"\n{df.info()}")
print("\nValori mancanti per colonna:")
print(df.isna().sum())
print(f"\n df.describe(), calcola media, minimi, massimo e std: \n{df.describe()}")  #Statistiche descrittive: calcola medie, minimi, massimi, std delle colonne numeriche.


#
#PULIZIA
#

#Rimuovere duplicati
df = df.drop_duplicates()  # Duplicati rimossi 
print(f"* Rimozione duplicati - Duplicati rimossi: {df.shape}") 
#Gestione valori mancanti
print(f"* Gestione valori mancanti: \n  {print(df.isna().sum())}")
df["Store"] = df["Store"].fillna("NON VALORIZZATO")  # Valori mancanti sostituzione con valore fisso
df["Prodotto"] = df["Prodotto"].fillna("NON VALORIZZATO")
df["Quantita"]=df["Quantita"].fillna( df.groupby("Prodotto")["Quantita"].median()).fillna(0)
print(f"    ora valori mancanti: {print(df.isna().sum())}")
#Controllo tipi di dati
df["Store"]=df["Store"].astype("category")
df["Data"]=pd.to_datetime(df["Data"])
df["Prodotto"]=df["Prodotto"].astype("category")
df["Quantita"]=df["Quantita"].astype("Int16")
df["Prezzo"]=df["Prezzo"].astype("Float32")
print(df.info())

#
#ANALISI ESPLORATIVA
#
#Quantita totali per prodotto
totali_per_prodotto = df.groupby("Prodotto")["Quantita"].sum() # groupby aggrega le vendite per prodotto.
print(f"\nTotali quantita per prodotto: \n{totali_per_prodotto}")

#Prodotto più e meno venduto
print("Prodotto più venduto:", totali_per_prodotto.idxmax())  # idxmax() e idxmin() identificano i prodotti con vendite estreme.
print("Prodotto meno venduto:", totali_per_prodotto.idxmin())

#Quantita medie giornaliere
medie_giornaliere = df.groupby("Data")["Quantita"].mean()# groupby("Data") calcola la media giornaliera delle vendite totali.
print(f"Medie giornarliere: {medie_giornaliere}")

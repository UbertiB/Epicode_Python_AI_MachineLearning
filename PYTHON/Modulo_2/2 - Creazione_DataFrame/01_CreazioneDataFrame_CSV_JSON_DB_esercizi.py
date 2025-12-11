"""
ESERCIZIO 1
- Input: un file transaction.csv con colonne date, production_id, qty, price
- Compito: leggere il file CSV (parse_dates=["date"]), assicurati che product_id sia category,
           calcolare revenue=qty*price e stampare le 5 righe con revenue piu alte
ESERCIZIO 2
- Input: sales_*.csv (più files mensili), 
         stores.jsoni(store meta), 
         tabella promotions in SQLlite.
- Compito: leggere tutti i CSV in straming (chuncksize), unirli ai metadata
JSON e alle tabella SQL, ottimizzare tipi e calcolare vendite mensili per region.

ESERCIZIO 3
- Input: dataset reale con : CSV grandi, JSON annidati cliente, DB SQL con prezzi e promozioni
- Compito: costruire una pipeline che: legge le sorgenti, normalizza JSON annidati,
  unisce tutto, applica best-pratice (usecols, dtype, parse_dates, downcast, category), 
  indica e gestisce valori mancanti, salva risultato pulito clean_data.csv e salva mapping categorie in file (pickle).
  Documenta ogni passaggio
"""

import pandas as pd
import numpy as np
import sqlite3
import json
from pathlib import Path
import glob

print("-------------------------------------------")
print("------------ ESERCIZIO 1 ------------------")
print("-------------------------------------------")

file=Path(r".\2 - CreazioneGestione_DataFrame\transaction.csv")
if not file.exists():   
    raise FileNotFoundError (f"File: {file} non trovato.")
#leggo il file
df_csv=pd.read_csv(file,parse_dates=["date"],dtype={"production_id":"category", "qty":"int32"})

#calcolo revenue
df_csv["revenue"]=df_csv["price"]*df_csv["qty"]
print(df_csv.nlargest(5,"revenue"))

print("-------------------------------------------")
print("------------ ESERCIZIO 2 ------------------")
print("-------------------------------------------")

# # Consegna: Input: sales_*.csv (più file mensili), stores.jsonl (store meta), tabella promotions in SQLite.
# # Compito: leggere tutti i CSV in streaming (chunksize), unirli ai metadata JSON e alla tabella SQL, ottimizzare tipi, e calcolare vendite mensili per region.
# # Output richiesto: CSV aggregato monthly_region_sales.csv + breve nota su scelte dtype e imputazioni.

#Lettura file stores
file=Path(r".\2 - CreazioneGestione_DataFrame\stores.json")
if not file.exists(): 
    raise FileNotFoundError(f"File: {file} non trovato.")
stores=pd.read_json(file,lines=True)
#print(stores)
file=Path(r".\2 - CreazioneGestione_DataFrame\production.json")
if not file.exists(): 
    raise FileNotFoundError(f"File: {file} non trovato.")
productions=pd.read_json(file,lines=True)
#print(productions)

#Lettura di tutti i files csv nella cartella
base = Path(r".\2 - CreazioneGestione_DataFrame")  # cartella corrente
files = list(base.glob("sales_*.csv"))
chunks=[]
for f in files:
    #print(f)
    for chunk in pd.read_csv(f, parse_dates=["date"],dayfirst=True, chunksize=3):
        if "price" in chunk.columns:
            chunk["price"]=chunk["price"].astype("float32")
        if "prodotto" in chunk.columns:
            chunk["prodotto"]=chunk["prodotto"].astype("category")
        if "production_id" in chunk.columns:
            chunk["production_id"]=chunk["production_id"].astype("category")
        if "qty" in chunk.columns:
            chunk["qty"]=chunk["qty"].astype("int16")            
        chunk=chunk.merge(stores, on=["prodotto"],how="left")
        if "qty" in chunk.columns:
            chunk["promo"]=chunk["promo"].astype("boolean")
        chunk=chunk.merge(productions, on=["production_id"],how="left")         
        if "price" in chunk.columns:
            chunk["price"]=chunk["price"].astype("float32")
        chunk["sconto"] = 0
        chunk.loc[chunk["promo"] == True, "sconto"] = 20
        chunk = chunk.drop(columns=["promo"])
        chunk["revenue"]=chunk["qty"]*chunk["price"]
        mask = chunk["sconto"] != 0
        chunk.loc[mask, "revenue"] = (chunk.loc[mask, "revenue"] * (1 - chunk.loc[mask, "sconto"] / 100))
        chunk = chunk.drop(columns=["sconto"])
        chunks.append(chunk)
df_sales=pd.concat(chunks,ignore_index=True)
df_sales["mese"]=df_sales["date"].dt.to_period("M").astype(str)
df_sales=df_sales.drop(columns=["date"])
df_sales=df_sales.groupby(["mese","prodotto", "production_id"],observed=True, sort=False)["revenue"].sum().reset_index()
print(df_sales)

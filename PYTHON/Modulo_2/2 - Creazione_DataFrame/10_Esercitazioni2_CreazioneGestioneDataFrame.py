"""
fonti:
- clienti
- prodotti
- ordini

costruire un df completo applicando filtri ed aggregazioni complesse, gestire subset di interesse
come clienti Premium, calcolare metriche chiave per prodotto, cliente e categoria
e serilizzare i dati in formati efficienti come Parquet. 
Durante il progetto si applicano tecniche di merge, join multipli, multiindex, concatenazioni,
ottimizzazione tipi, chunk e pulizia dei dati, permettendo di simulare un contesto lavorativo
reale, pronto per dashboard, reportistica e analisi predittive.
"""

import pandas as pd
import numpy as np
import time
import json
from pathlib import Path

n_clienti=30
file_Clienti_CSV="Pfinale_clienti.csv"
clienti=pd.DataFrame({
    "ClienteID": np.arange(1,n_clienti),
    "Ragionesociale":["Cliente_"+str(i) for i in range(1,n_clienti)],
    "Tipologia":np.random.choice(["Premium","Basic", "Star"],size=n_clienti-1)
})
#print(clienti)
clienti.to_csv(file_Clienti_CSV,sep=";",index=False)

n_prodotti=30
file_Prodotti_CSV="Pfinale_prodotti.csv"
prodotti=pd.DataFrame({
    "ProdottoID": np.arange(1,n_prodotti),
    "Descrizione":["Prodotto_"+str(i) for i in range(1,n_prodotti)],
    "Prezzo": np.random.rand(n_prodotti-1)*100
})
#print(prodotti)
prodotti.to_csv(file_Prodotti_CSV,sep=";",index=False)

date_possibili = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
n_ordini=1_000_000
n_ordini=30
#n_ordini=2
file_Ordini_JSON="PFinale_Ordini.json"
ordini=pd.DataFrame({
    "OrdineID":np.arange(1,n_ordini+1),
    "Data": np.random.choice(date_possibili, size=n_ordini),
    "ClienteID":np.random.randint(1,n_clienti,n_ordini),
    "ProdottoID":np.random.randint(1,n_prodotti,n_ordini),
    "Quantita": np.random.randint(1,20,n_ordini)
})
#print(ordini)
ordini.to_json(file_Ordini_JSON,date_format="iso")

sconto_tipologia=pd.DataFrame({
    "Tipologia":(["Premium","Star"]),
    "Sconto":np.random.randint(0,10, size=2)
})

#leggo i files da diverse fonti
df_clienti=pd.read_csv(file_Clienti_CSV,sep=";")
df_prodotti=pd.read_csv(file_Prodotti_CSV,sep=";")
start=time.time()
file=Path(file_Ordini_JSON)
if not file.exists(): 
    raise FileNotFoundError(f"File: {file_Ordini_JSON} non trovato.")
with open(file, "r", encoding="utf-8") as f:
    data = json.load(f)
df_ordini = pd.DataFrame.from_dict(data)

print(f"Tempo lettura json ordini: {time.time()-start}")
print(f"Ordini :numero ordini={len(df_ordini)} \nmemory={df_ordini.memory_usage(deep=True).sum() / (1024**2):.2f} MB")

#print(df_ordini.head())
#pulizia e downcasting colonne
df_ordini["OrdineID"]=df_ordini["OrdineID"].astype("int32")
df_ordini["ClienteID"]=df_ordini["ClienteID"].astype("category")
df_clienti["ClienteID"]=df_clienti["ClienteID"].astype("category")
df_ordini["ProdottoID"]=df_ordini["ProdottoID"].astype("category")
df_ordini["ProdottoID"]=df_ordini["ProdottoID"].astype("category")
df_ordini["Quantita"]=df_ordini["Quantita"].astype("int16")
df_ordini["Data"]=pd.to_datetime(df_ordini["Data"])

#merge
df_ordini=df_ordini.merge(df_clienti,on="ClienteID", how="left").merge(df_prodotti,on="ProdottoID",how="left").merge(sconto_tipologia, on="Tipologia",how="left")
#valori mancanti
df_ordini["Sconto"]=df_ordini["Sconto"].fillna(0)
df_ordini["Importo_scontato"]=(df_ordini["Prezzo"]*(100-df_ordini["Sconto"])).round(2)
#cancello colonne non più necessarie
df_ordini = df_ordini.drop(columns=["Sconto"])
df_ordini = df_ordini.drop(columns=["Prezzo"])

print(f"memory={df_ordini.memory_usage(deep=True).sum() / (1024**2):.2f} MB")
print(df_ordini.head(10))

#report tipologia
report_tipologia = df_ordini.groupby(["Tipologia"]).agg(
    totale_vendite=("Importo_scontato", "sum"),
    media_quantita=("Quantita", "mean"),
    numero_ordini=("OrdineID", "count"),
)
report_tipologia=report_tipologia.reset_index
print(report_tipologia)

#report anno/mese
df_ordini["Mese"] = df_ordini["Data"].dt.to_period("M")
df_ordini["Anno"] = df_ordini["Data"].dt.year
report_mese = df_ordini.groupby(["Anno","Mese"]).agg(
    totale_vendite=("Importo_scontato", "sum"),
    media_quantita=("Quantita", "mean"),
    numero_ordini=("OrdineID", "count"),
)
report_mese=report_mese.reset_index
print(report_mese)

#report prodotto
report_prodotto = df_ordini.groupby(["Descrizione"]).agg(
    totale_vendite=("Importo_scontato", "sum"),
    media_quantita=("Quantita", "mean"),
    numero_ordini=("OrdineID", "count"),
)
report_prodotto=report_prodotto.reset_index
print(report_prodotto)

subset_OrdiniPremium=df_ordini.query("Tipologia=='Premium'").copy()
#print(subset_OrdiniPremium)





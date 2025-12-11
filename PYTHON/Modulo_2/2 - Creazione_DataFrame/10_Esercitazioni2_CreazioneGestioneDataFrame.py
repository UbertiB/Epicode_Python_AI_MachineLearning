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
file_Ordini_CSV="PFinale_Ordini.csv"
ordini=pd.DataFrame({
    "OrdineID":np.arange(1,n_ordini+1),
    "Data": np.random.choice(date_possibili, size=n_ordini),
    "ClienteID":np.random.randint(1,n_clienti,n_ordini),
    "ProdottoID":np.random.randint(1,n_prodotti,n_ordini),
    "Quantita": np.random.randint(1,20,n_ordini)
})
#print(ordini)
ordini.to_csv(file_Ordini_CSV,sep=";",index=False)


sconto_tipologia=pd.DataFrame({
    "Tipologia":(["Premium","Star"]),
    "Sconto":np.random.randint(0,10, size=2)
})

#leggo i files da diverse fonti
df_clienti=pd.read_csv(file_Clienti_CSV,sep=";")
df_clienti["ClienteID"]=df_clienti["ClienteID"].astype("category")
df_prodotti=pd.read_csv(file_Prodotti_CSV,sep=";")
df_prodotti["ProdottoID"]=df_prodotti["ProdottoID"].astype("category")

#lettura ordini senza chunck
start=time.time()
df_ordini=pd.read_csv(file_Ordini_CSV,sep=";")

print(f"Tempo lettura csv ordini: {time.time()-start}")
print(f"Ordini :numero ordini={len(df_ordini)} \nmemory={df_ordini.memory_usage(deep=True).sum() / (1024**2):.2f} MB")

#lettura ordini con chunk
start=time.time()
chunk_size=1000
chunk_list=[]
totale_valore=0

for chunk in pd.read_csv(file_Ordini_CSV, sep=";", chunksize=chunk_size):
    #pulizia e downcasting colonne
    chunk["OrdineID"]=chunk["OrdineID"].astype("int32")
    chunk["ClienteID"]=chunk["ClienteID"].astype("category")
    chunk["ProdottoID"]=chunk["ProdottoID"].astype("category")
    chunk["Quantita"]=chunk["Quantita"].astype("int16")
    chunk["Data"]=pd.to_datetime(chunk["Data"])   
    #merge+merge+merge
    chunk=chunk.merge(df_prodotti,on="ProdottoID",how=("left")).merge(df_clienti,on="ClienteID",how="left").merge(sconto_tipologia, on="Tipologia",how="left")
    #valori mancanti
    chunk["Sconto"]=chunk["Sconto"].fillna(0)
    #aggiunta di colonne
    chunk["Prezzo_scontato"]=(chunk["Prezzo"]/((100-chunk["Sconto"])/100)).round(2)
    chunk["Importo_scontato"]=chunk["Quantita"] * chunk["Prezzo_scontato"]
    #cancello colonne non più necessarie
    chunk = chunk.drop(columns=["Sconto"])
    chunk = chunk.drop(columns=["Prezzo"])  
    #aggiorno lista chunk  
    chunk_list.append(chunk)

    totale_valore+=chunk["Importo_scontato"].sum()
print(totale_valore)
df_ordini=pd.concat(chunk_list,ignore_index=True)
print(df_ordini.head())

print(f"memory={df_ordini.memory_usage(deep=True).sum() / (1024**2):.2f} MB")

#esporto in formato efficiente come parquet per successive elaborazioni
file_Ordini_PARQUET="Pfinale_prodotti.parquet"
df_ordini.to_parquet(file_Ordini_PARQUET, index=False)

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





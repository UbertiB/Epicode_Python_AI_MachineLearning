"""

Progetto2 — Analisi vendite realistica
Traccia:
Sei un data analyst in un'azienda di e-commerce. Ti vengono forniti:
- Un CSV con ordini clienti (ordini.csv) .
- Un JSON con informazioni prodotto (prodotti.json).
- Un CSV con dati clienti (clienti.csv).

Questo progetto simula una situazione reale in cui occorre integrare fonti dati multiple,
ottimizzare memoria, applicare filtri complessi, aggregazioni avanzate e serializzazione
e'iciente, come capita quotidianamente in un contesto lavorativo di Data Analyst o Business Intelligence.

Consegna
---------------------------------
Parte 1 Crea i seguenti DataSet
1. Ordini.csv: 100.000 righe con ClienteID, ProdottoID, Quantità e DataOrdine.
2. prodotti.json: 20 prodotti con Categoria e Fornitore.
3. clienti.csv: 5.000 clienti con Regione e Segmento.
----------------------------------
Parte 2 Creare un DataFrame unificato
4. Unisci ordini.
5. Unisci prodotti.
6. Unisci clienti
--------------------------------
Parte 3 Ottimizzazione
7. Ottimizzare i tipi di dato.
8. Ottimizzare l'uso della memoria.
--------------------------------
Parte 4 Creare colonne e filtra i dati
9. Crea una colonna calcolata (ValoreTotale = Prezzo * Quantità).
10. Filtrare ordini con ValoreTotale > 100 e clienti
"""

import pandas as pd
import numpy as np
import time

print("------------------------------------")
print("-----PARTE 1 Creai i dataset--------")
print("------------------------------------")

#
#CLIENTI
#
n_clienti=5_000
file_clienti_csv="P2_Clienti.csv"
clienti=pd.DataFrame({
    "ClienteID":np.arange(1,n_clienti),
    "RagioneSociale": ["Cliente_"+str(i) for i in range(1,n_clienti)],
    "Segmento": np.random.choice(["Persona giuridica","Persona fisica","Pubblica amministrazione"],size=n_clienti-1)
})
clienti.to_csv(file_clienti_csv,sep=";",index=False)
df_clienti=pd.read_csv(file_clienti_csv,sep=";")

print(df_clienti.head())
print(df_clienti.info())

#
#PRODOTTI
#
n_prodotti=20
file_prodotti_json="P2_Prodotti.json"
prodotti=pd.DataFrame({
    "ProdottoID":np.arange(1,n_prodotti),
    "Descrizione": ["Prodotto_"+str(i) for i in range(1,n_prodotti)],
    "Categoria": np.random.choice(["Casalinghi","Elettrodomestici","Frutta", "Verdura"],size=n_prodotti-1),
    "Fornitore": np.random.choice([1,2,3,4,5],size=n_prodotti-1),
    "Prezzo": np.random.rand(n_prodotti-1)*100
})
prodotti.to_json(file_prodotti_json,orient="records")

df_prodotti=pd.read_json(file_prodotti_json,orient="records")

print(df_prodotti.head())
print(df_prodotti.info())

#
#ORDINI
# 
n_ordini=100_000
file_ordini_csv="P2_Ordini.csv"
date_possibili = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
ordini=pd.DataFrame({
        "OrdineID": np.arange(1,n_ordini+1),
        "ClienteID":np.random.randint(1, df_clienti["ClienteID"].max() + 1, size=n_ordini),
        "ProdottoID":np.random.randint(1, df_prodotti["ProdottoID"].max() + 1, size=n_ordini),
        "Quantita":np.random.randint(1,20,n_ordini),
        "Data":np.random.choice(date_possibili, size=n_ordini),
})
ordini.to_csv(file_ordini_csv,sep=";",index=False)

df_ordini=pd.read_csv(file_ordini_csv,sep=";")
  
print(df_ordini.head())
print(df_ordini.info())

print("-----------------------------------------")
print("--PARTE 2 Creare un DataFrame unificato--")
print("-----------------------------------------")

df_ALL=df_ordini.merge(df_prodotti,on="ProdottoID",how=("left")).merge(df_clienti,on="ClienteID",how="left").copy()
print(df_ALL.info())

print("-----------------------------------------")
print("----PARTE 3 Ottimizza i tipi di dato----")
print("-----------------------------------------")

df_ALL["ClienteID"]=df_ALL["ClienteID"].astype("int16")
df_ALL["RagioneSociale"]=df_ALL["RagioneSociale"].astype("string")
df_ALL["Segmento"]=df_ALL["Segmento"].astype("category")
df_ALL["ProdottoID"]=df_ALL["ProdottoID"].astype("int16")
df_ALL["Descrizione"]=df_ALL["Descrizione"].astype("string")
df_ALL["Categoria"]=df_ALL["Categoria"].astype("category")
df_ALL["Fornitore"]=df_ALL["Fornitore"].astype("category")
df_ALL["OrdineID"]=df_ALL["OrdineID"].astype("int32")
df_ALL["ClienteID"]=df_ALL["ClienteID"].astype("category")
df_ALL["ProdottoID"]=df_ALL["ProdottoID"].astype("category")
df_ALL["Quantita"]=df_ALL["Quantita"].astype("int8")
df_ALL["Prezzo"]=df_ALL["Prezzo"].astype("float64")
df_ALL["Data"]=pd.to_datetime(df_ALL["Data"]) 


print(df_ALL.info())
print(df_ALL.head())

print("-----------------------------------------")
print("---PARTE 4 Crea colonne e filtra i dati--")
print("-----------------------------------------")

df_ALL["ValoreTotale"]=df_ALL["Quantita"]*df_ALL["Prezzo"]
subset=df_ALL.query("ValoreTotale>100 and Segmento not in ('Persona fisica')").copy()
print(subset)




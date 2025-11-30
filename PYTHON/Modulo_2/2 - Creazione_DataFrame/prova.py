
import pandas as pd
import json
import sqlite3

"""
CSV semplici file di testo, ogni riga un record, valori colonne separati da delimitatore (ese ,)
Facili da leggere e modificabili, ma con limitazioni
non strutture annidate e non contengono metadati sul tipo di colonna
inoltre si possono creare dei problemi quando nel testo è presente il separatore
"""

"""
JSON pensato per la flessibilita. possono contenere strutture annidate e coppie di chiavi e valore
le informazioni non devono essere appiattite, perchè hanno una struttura
Se la struttura è semplice il caricamente è diretto, quando i dati sono annidati è spesso
necessario normalizzarli con json.normalized
Possono avere campi mancanti o incoerente tra record diversi
"""

"""
SQL standard dati strutturati in azienda
Prestasre attenzione alla gestione delle connessioni, chiuderle dopo l'uso
"""

"""
STRUTTURE MISTE, provengono da diverse fonti. csv, json, sql, excel, xml ecc
Attenzione a pulizia e normalizzazione dei dati, risolvere incoerenze (ed tipi di dato non 
allineati). Consiglio di validare ogni fonte separatamente e trasformarlo in un df pulito
e solo dopo unirli
"""

"""
dopo ogni importazione validare con dt.info e df.head
specificare i tipi di dati in fase di import (riduce memoria e evita incongruenze)
Documentare le trasformazioni fatte, per ripeterle in futuro
"""
#lista di dizionari
data=[
    {"store_id":"S1","product":"P1","date":"2023-01-01","qty":10},
    {"store_id":"S2","product":"P2","date":"2023-01-02","qty":5},    
    {"store_id":"S1","product":"P1","date":"2023-01-08","qty":7},
]
df=pd.DataFrame(data)
#
#CSV
#
df.to_csv("sales_CSV.csv",index=False)
df_csv=pd.read_csv("sales_CSV.csv",parse_dates=["date"],dtype={"store_id":"category","product":"category","qy":"int"})
#
#JSON
#
df.to_json("sales_JSON",orient="records", lines=True)
df_json=pd.read_json("sales_JSON",orient="records",lines=True)
#
#SQL
#
conn=sqlite3.connect("sales_SQL.db")
df.to_sql("sales",conn, if_exists="replace",index=False)
df_sql=pd.read_sql_query("select store_id, product, date, qty from sales",conn,parse_dates=["date"])
conn.close

#
#CHUNK (per leggere molti dati senza appesantire la macchina)
#
#metto il valore di chunksize molto baso per fare le prove, normalmente messo molto alto, tipo 10000
chunks=pd.read_csv("sales_CSV.csv",parse_dates=["date"],chunksize=1,usecols=["store_id","product","date","qty"])
chunk_list=[]
for chunk in chunks:
    chunk["store_id"]=chunk["store_id"].astype("category")
    chunk["qta"]=pd.to_numeric(chunk["qty"],downcast="integer")
    #print(f"valori per chunk: \n{chunk}")
    chunk_list.append(chunk)

print(chunk_list)

df=pd.concat(chunk_list,ignore_index=True)
print(f"vendite totali: \n{df}")
df_group=df.groupby(["store_id","product"])["qty"].sum()
print(f"vendite per store e prodotto: \n{df_group}")

#
#JSON NORMALIZZATO
#
records=[json.loads(line) for line in open("sales_JSON")]
print(f"JSON records: \n{records}")
df_stores=pd.json_normalize(records)
print(f"JSON normalizzato: \n{df_stores}")

#
#
#
df1_sales=pd.DataFrame({
    "data":["2023-01-01","2023-01-02","2023-01-05","2013-02-01","2023-02-05"],
    "store_id":["S1","S2","S1","S3","S2"],
    "product":["P1","P2","P1","P3","P2"],
    "qta":[10,5,7,3,8],
    "price":[100,200,100,150,220]
})
df1_store=pd.DataFrame({
    "store_id":["S1","S2","S3"],
    "region":["Nord","Centro","Sud"],
    "city":["Milano","Roma","Napoli"]
})
df1_promotions=pd.DataFrame({
    "store_id":["S1","S2","S3"],
    "promo_flag":[1,0,1]
})
df1_sales.to_csv("transaction.csv",index=False)
df1_store.to_json("stores.json1",orient="records",lines=True,force_ascii=False)
conn=sqlite3.connect("example.db")
df1_promotions.to_sql("promotions",conn, if_exists="replace",index=False)

df1_sales=pd.read_csv("transaction.csv",parse_dates=["data"],dtype={"stored_id":"category","product":"category"})
df1_store=pd.read_json("stores.json1",orient="records",lines=True)
conn=sqlite3.connect("example.db")

conn.close()
df1=df1_sales.merge(df_stores, on="store_id",how="left")
df1=df1.merge(df1_promotions,on="store_id",how="left")

df1["promo_flag"]=df1["promo_flag"].fillna(0).astype("int8")
df1_group=df1.groupby(["region"]).agg(total_qty=("qty","sum"),promo_sales=("qty",lambda x:x [df1["promo_flag"]==1].sum()))


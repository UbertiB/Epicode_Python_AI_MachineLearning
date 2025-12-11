"""
Costruire un data1frame da fontidiverse, csv, json e data1bserelazionali

CSV: metodo più usato per scambio di dati.
Il delimitatore di solito è la, ma è possibile cambiarla per esempio con ;
Ogni riga rappresenta un record, ed il valori di colonne sono separati dal delimitatore.
Non hanno strutture annidate o gerarchie, non contengono metadati sui tipi di colonne,
possono diventare ambigui quando i dati hanno il separatore all'interno dei dati.
Per questi motivi ci sono molti parametri per utilizzare i Csv (in pd.read_csv)

JSON formato più moderno e flessibile. Possono contenere struttura
annidate, array, e coppie chiavi valori. Rendendolo ideal per rappresentare dati complessi.
Le informazioni non sono appiattite ma strutturate.
pd.read_json
Quando una struttura è relativamente semplice (esempio una lista di dizionari), 
il caricamento è diretto
Quando i dati sono molto strutturati è spesso necessario normalizzarli json_normalize
I JSON possono utilizzare diversi dati di data, è necessari convertirli con todate
Essendo flessibili possono avere campi mancanti o non dello stesso tipo., per questo 
vanno sempre controllati
E' sempre necessario controllare e ripulire i dati dopo import

SQL standard a livello aziendale
dati strutturati con chiavi interne ed esterne. Per accedere ad un db è necessario utilizzare
un connettore specifico.
E' possibile eseguire query sql direttamente da python, è possibile selezionare solo i dati
necessari.
Bisogna prestare attenzione alla gestione delle connessioni e chiuderle quando non più utilizzate
Per accedere ad un database è necessario un connettore, come può essere sqlserver 
Il risultato della query può essere caricato in un dataframe.

STRUTTURE MISTE rappresentano la realtà di moltissimi progetti di data science.

Excel, Xml, txt, o altri formati, sono ugualmente possibili e possibile integrare con tutte le altri fonti.

Incongruenze ed tipi di dati non allineati
Valori mancanti
Valori duplicati
Validasre prima ogni fonte separatamente, trasforamli in un df pulito e solo dopo unire tutti i df1 insieme
Dopo ogni importazione validare i dati con df.info e df.head(), per avere un anteprima delle
colonne, dei tipi, e dalla presenza di valori nulli o duplicati.
Specificare i tipi di dato già in fase di import
Controllare encoding (perchè i caratteri speciali possono generare errori)
Normalizzare i campi annidati nei json
Nelle query SQL isolare le query in variabili leggibili e documentate
Documentare le trasformazioni fatti per ripeterle in futuro
Quando i dati devono essere importati regolarmente conviene costruire delle pipeline
automatizzata che leggono, puliscono e trasformano i dati sempre allo stesso modo,
garantendo riproducibilità

"""

import pandas as pd
import numpy as np
import sqlite3
import json

#lista di dizionari
data=[
    {"store_id":"S1","product":"P1","date":"2023-01-01","qty":10},
    {"store_id":"S2","product":"P2","date":"2023-01-02","qty":5},
    {"store_id":"S1","product":"P1","date":"2023-01-08","qty":7}
    ]
#trasformo la lista in dataframe
df1=pd.DataFrame(data)

#SALVATAGGIO FILE csv,json,sql
df1.to_csv("sales.csv",sep=",",index=False)
df1.to_json("sales.json",orient="records",lines=True)
conn=sqlite3.connect("example.db")
df1.to_sql("sales",conn,if_exists="replace", index=False)

#LEGGIAMO I FILES PER CARICARE I DATI, con le best practice
#READ_CSV: parse_date, dtype, usecols
df1_csv=pd.read_csv("sales.csv",parse_dates=["date"],dtype={"store_id":"category","product":"category"})
#READ_JSON: leggo semplicemente json se non devo normalizzarlo
df1_json=pd.read_json("sales.json",orient="records",lines=True)
#READ_SQL: parse_date
df1_sql=pd.read_sql_query("select store_id, product, date, qty from sales",conn,parse_dates=["date"])

conn.close()

df2=pd.DataFrame(data)

df2.to_csv("sales.csv",index=False)

#CHUNKS utilizzato per leggere file di grandi dimensioni senza esaurire la memoria.
#la lettura è fatta per blocchi (chunks)
chunks=pd.read_csv("sales.csv",parse_dates=["date"],chunksize=1,usecols=["store_id","product","date","qty"])

agg_list=[] #lista di chunk
for chunk in chunks:
    chunk["store_id"]=chunk["store_id"].astype("category")
    chunk["qty"]=pd.to_numeric(chunk["qty"],downcast="integer")
    #agg_list.append(chunk.groupby(["store_id","product"])["qty"].sum().reset_index())
    agg_list.append(chunk) #aggiorno lista

#UNIONE dei chunck con concat e aggregazione (groupby)                                                 
agg=pd.concat(agg_list).groupby(["store_id","product"])["qty"].sum().reset_index()

#FILE JSON ANNIDATI

with open("stores_nested.json","w") as f:
    f.write(json.dumps({"store_id":"S1","meta":{"city":"Roma","cap":"00100"}})+"\n")

records=[json.loads(line) for line in open("stores_nested.json","r")]    
df_stores=pd.json_normalize(records)  #per appiattire i dati annidati

            



    







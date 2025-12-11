
print("-------------------------------------------")
print("------------ ESERCIZIO 3 ------------------")
print("-------------------------------------------")

"""
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
from pandas import json_normalize

if False:
    #
    #CREAZIONE FILES
    #
    quanti=1_000
    #
    # CSV
    #
    valori = ["Store A","Store B","Store C","Store D"]
    valori2=["Prodotto1", "Prodotto2", "Prodotto3", "Prodotto4", "Prodotto5", "Prodotto6", "Prodotto7", "Prodotto8", "Prodotto9", "Prodotto10"]
    valori3=["Cliente 1","Cliente 2","Cliente 3","Cliente 4","Cliente 5","Cliente 6","Cliente 7","Cliente 8","Cliente 9","Cliente 10"]
    data_vendite={
                    "negozio":np.random.choice(valori,quanti,replace=True),
                    "data":np.random.choice(pd.date_range("2025-01-01", "2025-02-28", freq="D"),quanti,replace=True),
                    "prodotto": np.random.choice(valori2,quanti,replace=True),
                    "qta":np.random.choice(np.arange(150),quanti),
                    "cliente":np.random.choice(valori3,quanti,replace=True),
                }
    df_negozi=pd.DataFrame(data_vendite)
    #print(df_negozi)
    df_negozi.to_csv("es3_vendite.csv",sep=",",index=False)
    #
    #JSON
    #
    #clienti
    df_clienti = pd.DataFrame([
        {"codice": "Cliente 1", "ragione_sociale": "Cliente Uno S.p.A."},
        {"codice": "Cliente 2", "ragione_sociale": "Cliente Due S.r.l."},
        {"codice": "Cliente 3", "ragione_sociale": "Cliente Tre S.a.s."},
        {"codice": "Cliente 4", "ragione_sociale": "Cliente Quattro S.a.s."},
        {"codice": "Cliente 5", "ragione_sociale": "Cliente Cinque SPA"},
        {"codice": "Cliente 6", "ragione_sociale": "Cliente Sei srl"},
        {"codice": "Cliente 7", "ragione_sociale": "Cliente Sette "},
        {"codice": "Cliente 8", "ragione_sociale": "Cliente Otto snc"},
        {"codice": "Cliente 9", "ragione_sociale": "Cliente Nove sas"},
        {"codice": "Cliente 10", "ragione_sociale": "Cliente Dieci "},
    ])
    #indirizzi
    df_indirizzi = pd.DataFrame([
        {"codice": "Cliente 1", "via": "Via Industria 10", "cap": "20861", "citta": "Brugherio", "provincia": "MB", "stato": "IT"},
        {"codice": "Cliente 2", "via": "Corso Italia 5", "cap": "10100", "citta": "Torino", "provincia": "TO", "stato": "IT"},
        {"codice": "Cliente 3", "via": "Mazzini 1", "cap": "26013", "citta": "Crema", "provincia": "CR", "stato": "IT"},
        {"codice": "Cliente 4", "via": "Marini 15", "cap": "15678", "citta": "Cremona", "provincia": "CR", "stato": "IT"},
        {"codice": "Cliente 5", "via": "Calcutta 5", "cap": "26013", "citta": "Matova", "provincia": "MA", "stato": "IT"},
        {"codice": "Cliente 6", "via": "Ettore 11", "cap": "47851", "citta": "Piacenza", "provincia": "PC", "stato": "IT"},
        {"codice": "Cliente 7", "via": "Cavour 6", "cap": "26013", "citta": "Verona", "provincia": "VR", "stato": "IT"},
        {"codice": "Cliente 8", "via": "Mazzini 31", "cap": "2156", "citta": "Crema", "provincia": "CR", "stato": "IT"},
        {"codice": "Cliente 9", "via": "Roma 1", "cap": "877489", "citta": "Brescia", "provincia": "BS", "stato": "IT"},
        {"codice": "Cliente 10", "via": "Madrid 1", "cap": "45646", "citta": "Lodi", "provincia": "LO", "stato": "IT"},
    ])
    records = []

    for _, row in df_clienti.iterrows():
        cid = row["codice"]
        indirizzi = df_indirizzi[df_indirizzi["codice"] == cid].drop(columns=["codice"]).to_dict(orient="records")
        rec = {
            "codice": cid,
            "ragione_sociale": row["ragione_sociale"],
            "indirizzi": indirizzi,
        }
        records.append(rec)
    json_finale = {"customers": records}
    #creo il file
    with open("es3_clienti.json", "w", encoding="utf-8") as f:
        json.dump(json_finale, f, ensure_ascii=False, indent=2)

    #
    #SQL
    #
    es3_prodotti=[
        {"prodotto":"Prodotto1","Descrizione":"Prodotto numero 1","Prezzo":150,"promozione":False},
        {"prodotto":"Prodotto2","Descrizione":"Prodotto numero 3","Prezzo":200,"promozione":True},
        {"prodotto":"Prodotto3","Descrizione":"Prodotto numero 3","Prezzo":105,"promozione":False},
        {"prodotto":"Prodotto4","Descrizione":"Prodotto numero 4","Prezzo":88,"promozione":False},
        {"prodotto":"Prodotto5","Descrizione":"Prodotto numero 5","Prezzo":190,"promozione":True},
        {"prodotto":"Prodotto6","Descrizione":"Prodotto numero 6","Prezzo":80,"promozione":False},
        {"prodotto":"Prodotto7","Descrizione":"Prodotto numero 7","Prezzo":44,"promozione":False},
        {"prodotto":"Prodotto8","Descrizione":"Prodotto numero 8","Prezzo":145,"promozione":False},
        {"prodotto":"Prodotto9","Descrizione":"Prodotto numero 9","Prezzo":49,"promozione":True},
        {"prodotto":"Prodotto10","Descrizione":"Prodotto numero 10","Prezzo":145,"promozione":True},
        ]
    es3_df_prodotti=pd.DataFrame(es3_prodotti)
    es3_conn=sqlite3.connect("es3_articoli.db")
    es3_df_prodotti.to_sql("pd_prodotti",es3_conn,if_exists="replace", index=False)

if True:
    print("----------------------------------------")
    print("----------- LETTURA FILES --------------")
    print("----------------------------------------")

    #
    #CSV
    # 
    file=Path(r".\es3_vendite.csv")
    if not file.exists():   
        raise FileNotFoundError (f"File: {file} non trovato.")
    #leggo il file con chunk per file di grandi dimensioni
    chunks=pd.read_csv(file,parse_dates=["data"],chunksize=500,usecols=["negozio","data","prodotto","qta","cliente"])

    agg_list=[] #lista di chunk
    for chunk in chunks:
        chunk["negozio"]=chunk["negozio"].astype("category")
        chunk["prodotto"]=chunk["prodotto"].astype("category")
        chunk["cliente"]=chunk["cliente"].astype("category")
        #chunk["qta"]=pd.to_numeric(chunk["qta"].astype("int32"))
        #print(chunk)
    agg_list.append(chunk) #aggiorno lista

    #UNIONE dei chunck con concat                                     
    df_vendite=pd.concat(agg_list)
    print(f"vendite: \n{df_vendite.head(3)}")
    #
    #JSON
    #
    file=Path(r".\es3_clienti.json")
    if not file.exists(): 
        raise FileNotFoundError(f"File: {file} non trovato.")
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        #print(data)
    # data["customers"] è la lista dei clienti
    #df_clienti = pd.json_normalize(data["customers"],record_path="indirizzi", meta=["codice", "ragione_sociale"])
    df_clienti = pd.json_normalize(data["customers"], meta=["codice", "ragione_sociale"])
    #riordino le colonne
    print(df_clienti)
    df_clienti = df_clienti[["codice", "ragione_sociale"]]
    print(f"clienti: \n{df_clienti.head(3)}")
    #
    #SQL
    #
    conn=sqlite3.connect("es3_articoli.db")
    df_prodotti=pd.read_sql_query("select prodotto, descrizione, prezzo, promozione from pd_prodotti",conn)
    print(f"prodotti: \n{df_prodotti.head(3)}")

    #concateno tutto
    df_tot = pd.merge(df_vendite, df_clienti,left_on="cliente", right_on="codice", how="left")
    df_tot = pd.merge(df_tot,df_prodotti, on="prodotto", how="left")
    df_tot["ricavo"]=df_tot["Prezzo"]*df_tot["qta"]-df_tot["promozione"].apply(lambda x: 20 if x == 1 else 0)
    df_tot = df_tot.drop(columns=["codice", "ragione_sociale"])
    print(df_tot.head())
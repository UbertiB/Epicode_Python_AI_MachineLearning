"""
ESERCIZIO 1
* Crea un df con n righe di dati fittizi (vendite, prodotto, regione, prezzo)
Salva in csv, Parquet, Feather e HDF5
Misura i tempi di lettura per ciascun formato e confrontali

ESERCIZIO 2
* Crea un subset filtrati su base condizionale (es. prezzo>100 o regione="Nord)
e salvali in tutti e quattro i formati. Misura la velocità di lettura e calcola
il totale vendite dei subset

ESERCIZIO 3
* Salva due o più subset diversi per lo stesso file HDF5 usando chiavi diverse.
Leggere solo un subset e calcolare la media del prezzo, poi leggere solo le prime 50 
righe dello stesso subseet usando slicing diretto

ESERCIZIO 4 
* Crea un subset dei dati con vendite elevate e salvandolo in Feather.
Leggerlo più volte in loop e misurare il tempo totale, per dimostrare 
l'efficienza nei trasfserimenti tra processi o calcoli ripetuti

"""


import pandas as pd
import numpy as np
import time #per misurare i tempi di lettura

startd = np.datetime64("2025-01-01")
endd = np.datetime64("2026-01-01")  # limite escluso, così includi tutto il 2025

n=1_000_000
df=pd.DataFrame({
    "vendite":np.random.randint( 0,(endd - startd).astype(int),size=n),
    "prodotto":np.random.choice(["Prodotto A","Prodotto B","Prodotto C","Prodotto E"],size=n),
    "regione": np.random.choice(["Nord","Centro","Sud","Isole"],size=n),
    "prezzo":np.random.randint(100,1000,size=n)
})
#print(df)
file_csv="07_Esercizio1.csv"
file_parquet="07_Esercizio1.parquet"
file_featfher="07_Esercizio1.feather"
file_hdf="07_Esercizio1.hdf"

"""
ESERCIZIO 1
* Crea un df con n righe di dati fittizi (vendite, prodotto, regione, prezzo)
Salva in csv, Parquet, Feather e HDF5
Misura i tempi di lettura per ciascun formato e confrontali
"""
if False:
    print("----------------------------")    
    print("-------ESERCIZIO 1----------")    
    print("----------------------------")    
    #salvo il df in csv
    df.to_csv(file_csv,index=False)
    df.to_parquet(file_parquet,index=False)
    df.to_feather(file_featfher)
    df.to_hdf(file_hdf,index=False,key="tutto",mode="a")

    start=time.time()
    df_csv=pd.read_csv(file_csv)
    print(f"Tempo lettura CSV: {time.time()-start}")
    
    start=time.time()
    df_parquet=pd.read_parquet(file_parquet)
    print(f"Tempo lettura Parquet: {time.time()-start}")    

    start=time.time()
    df_feather=pd.read_feather(file_featfher)
    print(f"Tempo lettura Feather: {time.time()-start}")    

    start=time.time()
    df_hdf=pd.read_hdf(file_hdf)
    print(f"Tempo lettura HDF: {time.time()-start}")    

"""
ESERCIZIO 2
* Crea un subset filtrati su base condizionale (es. prezzo>100 o regione="Nord)
e salvali in tutti e quattro i formati. Misura la velocità di lettura e calcola
il totale vendite dei subset
"""    
if False:
    print("----------------------------")    
    print("-------ESERCIZIO 2----------")    
    print("----------------------------")  
    df_filtrato = df[(df["prezzo"] > 500) & (df["vendite"] > 100)].copy()
    #salvo il df in csv
    df_filtrato.to_csv(file_csv,index=False)
    df_filtrato.to_parquet(file_parquet,index=False)
    df_filtrato.to_feather(file_featfher)
    df_filtrato.to_hdf(file_hdf,index=False,key="tutto",mode="a")

    start=time.time()
    df_csv=pd.read_csv(file_csv)
    totale_csv=df_csv["prezzo"].sum()
    print(f"Tempo vendite: {totale_csv}, totale tempo lettura CSV: {time.time()-start}")
    
    start=time.time()
    df_parquet=pd.read_parquet(file_parquet)
    totale_parquet=df_parquet["prezzo"].sum()
    print(f"Tempo vendite: {totale_parquet}, totale tempo lettura PARQUET: {time.time()-start}")

    start=time.time()
    df_feather=pd.read_feather(file_featfher)
    totale_feather=df_feather["prezzo"].sum()
    print(f"Tempo vendite: {totale_feather}, totale tempo lettura FEATHER: {time.time()-start}")

    start=time.time()
    df_hdf=pd.read_hdf(file_hdf)
    totale_hdf=df_hdf["prezzo"].sum()
    print(f"Tempo vendite: {totale_hdf}, totale tempo lettura HDF: {time.time()-start}")

"""
ESERCIZIO 3
* Salva due o più subset diversi per lo stesso file HDF5 usando chiavi diverse.
Leggere solo un subset e calcolare la media del prezzo, poi leggere solo le prime 50 
righe dello stesso subseet usando slicing diretto
"""
if False:
    print("----------------------------")    
    print("-------ESERCIZIO 3----------")    
    print("----------------------------")     

    df[df["prezzo"]>500].to_hdf("filtrato_hdf.hdf",key="maggiore",mode="w")
    df[df["prezzo"]<500].to_hdf("filtrato_hdf.hdf",key="minore",mode="a")

    maggiore=pd.read_hdf("filtrato_hdf.hdf",key="maggiore",start=0,stop=50)
    print(maggiore)

"""
ESERCIZIO 4 
* Crea un subset dei dati con vendite elevate e salvandolo in Feather.
Leggerlo più volte in loop e misurare il tempo totale, per dimostrare 
l'efficienza nei trasfserimenti tra processi o calcoli ripetuti      
"""
if True:
    print("----------------------------")    
    print("-------ESERCIZIO 5----------")    
    print("----------------------------")  
    df1=pd.DataFrame({"Prodotto": np.random.choice(["Prodotto A","Prodotto B","Prodotto C","Prodotto D"],size=n),
                      "Quantita": np.random.randint(1,60,n),
                      "Prezzo": np.random.randint(100,1000,n)
        })
    df1.to_feather("esercizio4.feather")

    start=time.time()

    for _ in range(1,100):
        df1_riletto=pd.read_feather("esercizio4.feather")
    print(f"Tempo lettura Feather: {time.time()-start}")            

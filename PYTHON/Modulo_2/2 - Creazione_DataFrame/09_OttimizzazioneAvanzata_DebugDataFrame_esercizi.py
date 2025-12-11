"""
ESERCIZIO 1 
- crea un df con 2_000_000 di righe simulando vendite (ID, Prodotto, Prezzo, Quantita,
Regione, Categoria
- Ottimizzare i tipi e misurare la memoria
- Filtrare righe con ValoreTotale>500 usando .copy() e calcolare la media,
somma emax di ValoreTotale
- Salvare il dataset su CSV e leggere in chunk 200_000 righe
- Per ogni chunk creare una nuova colonna con Prezzo_scontato del 10%
e sommare il valore totale
- Misurare il tempo totale di elaborazione e confrontarlo con il tempo
necessario se si fosse caricato l'intero dataset
- Implementare un debug step-by-step
- Stampare info, memoria e statistiche descrittive per ogni chunk
- Identificare  eventuali colonne che possono essere convertite in tipi
più efficienti.
- Ottimizzare il dataset e salvare in Parquet chunk, verificando il tempo
di scrittura e dimensione finale del file
-Creare un subset delle vendite solo per categoria A e regione="Napoli"
- Misurare  memoria e tempo di elaborazione usando sia il caricamento totale
che chunking
- Dimostrare l'efficienza dei chunk confrontando i due approcci.

"""
import pandas as pd
import numpy as np
import time
import os
from pathlib import Path


N=2_000_000
CHUNK=200_000
np.random.seed(42)
csv_path="sales_2M.csv"
parquet_path="sales_2M.parquet"
parquet_chunk="parquet_chunk"

def GeneraBig_DF(n_righe:int):
    n_prodotti=20
    prodotti=[f"Prodotto_{i+1}" for i in range(n_prodotti)]
    n_categorie=10
    categorie=[f"Cat_{i+1}" for i in range (n_categorie)]
    regioni=["Nord","Centro","Sud"]
    df=pd.DataFrame({
        "ID": np.arange(n_righe+1),
        "Prodotto": np.random.choice(prodotti,size=n_righe+1),
        "Prezzo":np.round(np.random.uniform(low=10,high=100,size=n_righe+1),2),
        "Quantita":np.random.randint(10,25,n_righe+1),
        "Regione":np.random.choice(regioni,n_righe+1,),
        "Categoria":np.random.choice(categorie,n_righe+1)
    })
    return(df)

df=GeneraBig_DF(1_000_000)
#print(df)
print(f"Memoria iniziaele (MB): {df.memory_usage(deep=True).sum()/1_048_576}")
#ottimizza i tipi
df["ID"]=df["ID"].astype("int16")
df["Prodotto"]=df["Prodotto"].astype("category")
df["Prezzo"]=df["Prezzo"].astype("float16")
df["Quantita"]=df["Quantita"].astype("int16")
df["Regione"]=df["Regione"].astype("category")
df["Categoria"]=df["Categoria"].astype("category")
print(f"Memoria dopo ottimizzazione tipi (MB): {df.memory_usage(deep=True).sum()/1_048_576}")

#Filtrare righe con ValoreTotale>500
df["Valore"]=df["Prezzo"]*df["Quantita"]
subset_alto=df[df["Valore"]>500].copy()
media_subset=subset_alto["Valore"].mean()
max_subset=subset_alto["Valore"].max()
min_subset=subset_alto["Valore"].min()
sum_subset=subset_alto["Valore"].sum()
#print(len(df))
#print(len(subset_alto))
print(f"Subset con Importo>500: min: {min_subset} - max: {max_subset} - somma: {sum_subset} - media: {media_subset}")

#Salvare il dataset su CSV 
nomefile_csv="09_vendite.csv"
df.to_csv(nomefile_csv,sep=";",index=True)

#caricamento senza chunk
start=time.time()
df_csv=pd.read_csv(nomefile_csv,sep=";")
print(f"Tempo totale caricamento diretto: {time.time()-start}")

#caricamento in chunk 200_000 righe
chunk_size=200_000
chunk_count=0
importo_scontato=0
chunk_list=[]
start=time.time()
for chunk in pd.read_csv(nomefile_csv,sep=";",chunksize=chunk_size):
    start_chunk=time.time()
    chunk_count+=1
    chunk["ID"]=chunk["ID"].astype("int16")
    chunk["Prodotto"]=chunk["Prodotto"].astype("category")
    chunk["Prezzo"]=chunk["Prezzo"].astype("float32")
    chunk["Quantita"]=chunk["Quantita"].astype("int16")
    chunk["Regione"]=chunk["Regione"].astype("category")
    chunk["Categoria"]=chunk["Categoria"].astype("category")
    chunk["Prezzo_scontato"]=np.round(chunk["Prezzo"]*0.9,2)
    chunk["Valore_scontato"]=np.round(chunk["Prezzo_scontato"]*chunk["Quantita"],2)
    importo_scontato+=chunk["Valore_scontato"].sum()
    print(f"  chunk {chunk_count}: rows={len(chunk)}, memory={chunk.memory_usage(deep=True).sum() / (1024**2):.2f} MB, processing_time={(time.time()- start_chunk):.3f}s")
    chunk["n_chunk"]=chunk_count
    chunk["tempo_caricamento"]=time.time()-start_chunk        
    chunk_list.append(chunk)
print(f"Tempo totale caricamento con chunk (ed ottimizzazione memoria): {time.time()-start}")
# Nota: chunking evita picco memoria ma può avere overhead I/O; i tempi dipendono dall'I/O e CPU

df = pd.concat(chunk_list, ignore_index=True)
#print(df.head())

#Ottimizzare il dataset e salvare in Parquet chunk, verificando il tempo di scrittura e dimensione finale del file
nomefile_parquet="09_vendite.parquet"
df.to_parquet(nomefile_parquet,index=False)
start=time.time()
df_parquet=pd.read_parquet(nomefile_parquet)
print(f"Tempo lettura file PARQUET totale: {time.time()-start}")







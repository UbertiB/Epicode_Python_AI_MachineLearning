"""
Serializzazioni efficienti
Quando si lavora con tanti dati una cosa importante è letture e scrittura dati.
Formati come csv o xls possono diventare lenti quando i dati aumentano.
Per questo è necessario conoscere tecniche di serializzazione efficiente.
Ovvero modi di caricare e salvare dati in maniera efficiente.
La serializzazione dei dati consente nel trasformare un dataset in un formato che
può essere scritto sul disco e letto successivamente in memoria.

NON SOLO CCSV
CSV può risultare utile quando abbiamo dati non di grandi dimensioni, negli altri 
casi diventa lento e preferibile utilizzare altre soluzioni
PARQUET
formato colonnare open source, adatto a dataset grandi, esssendo colonnare consente
di caricare solo le colonne necessarie
velocità: buona
Spazio: ottimo (compressione avanzata)
Uso: con big data, archiviazione efficiente
FEATHER
formato progettato per massima velocità di scrittura e lettura.
velocità: eccellente
spazio: media
uso: Utile quando si devono trasferire dati da processi o per prototipazione
Non ha compressione avanzata come parquet
HDF5
E' un formato gerarchico simile ad un filesystem all'interno di un singolo file
Permette di salvare dataset multipli con strutture diverse e supporta
compressione e slicing diretto dei dati
velocità: media
spazio:buona
uso: Utile quando si gestiscono dataset molto grandi e strutturati con più tabelle
correlate tra di loro e per archiviazione scientifica
CONFRONTO
le varie tecniche possono essere combinate tra di loro
bilanciando velocità compressione compatibilità
"""
import pandas as pd #per dataframe
import numpy as np #per generare dati casuali
import time #per misurare i tempi di lettura

df_piccolo=pd.DataFrame({
    "ID": np.arange(100),
    "Valore": np.random.rand(100),
    "Categoria": np.random.choice(["A","B","C","D"],size=100)
})

df=pd.DataFrame({
    "ID": np.arange(5_000_000),
    "Valore": np.random.rand(5_000_000),
    "Categoria": np.random.choice(["A","B","C","D"],size=5_000_000)
})

#confronto tempi di lettura tra CSV e Pandas
print ("-------------------------------------")
print ("-----TEMPI LETTURA CSV->PARQUET------")
print ("--------(dataset piccolo)------------")

#trasformiamo il dataframe in csv con il metodo to_csv
df_piccolo.to_csv("dati_piccolo.csv",index=False)
df_piccolo.to_parquet("dati_piccolo.parquet",index=False)
start=time.time()
df_piccolo_csv=pd.read_csv("dati_piccolo.csv")
print(f"Tempo lettura CSV: {time.time()-start}")
start=time.time()
df_piccolo_parquet=pd.read_parquet("dati_piccolo.parquet")
print(f"Tempo lettura PARQUET: {time.time()-start}")

print ("-------------------------------------")
print ("-----TEMPI LETTURA CSV->PARQUET------")
print ("--------(dataset grande)-------------")

#trasformiamo il dataframe in csv con il metodo to_csv
df.to_csv("dati.csv",index=False)
df.to_parquet("dati.parquet",index=False)
start=time.time()
df_csv=pd.read_csv("dati.csv")
print(f"Tempo lettura CSV: {time.time()-start}")
start=time.time()
df_parquet=pd.read_parquet("dati.parquet")
print(f"Tempo lettura PARQUET: {time.time()-start}")

print ("-------------------------------------")
print ("----FILTRAGGIO ED AGGREGAZIONE CON PARQUET------")
print ("-------------------------------------")

df[df["Categoria"]=="A"].to_parquet("categoria_A.parquet",index=False)
df_A=pd.read_parquet("categoria_A.parquet")
media_valore=df_A["Valore"].mean()
print(f"Media valore Categoria A: {media_valore}")

print ("-------------------------------------")
print ("--FEATHER PER TRASFERIMENTI RAPIDI---")
print ("-------------------------------------")

subset=df[df["Valore"]>0.99].copy()
subset.to_feather("subset_valore.feather")
start=time.time()

subset_letto=pd.read_feather("subset_valore.feather")
print(f"Tempo per lettura Feather: {time.time()-start}")
print ("-------------------------------------")
conteggio=subset_letto["Categoria"].value_counts()
print(conteggio)

print ("-------------------------------------")
print ("------------HDF5-----------")
print ("-------------------------------------")

#divido il file in due key
df[df["Categoria"]=="A"].to_hdf("dati.h5",key="cat_A",mode="w")
df[df["Categoria"]=="B"].to_hdf("dati.h5",key="cat_B",mode="a")

#recupero solo i dati con key=cat_A
#è obbligatorio indicare una key, non è possibile recuperare senza alcuna key
cat_A=pd.read_hdf("dati.h5",key="cat_A")
media_valoreA=cat_A["Valore"].mean()
print(cat_A)
print(type(cat_A))







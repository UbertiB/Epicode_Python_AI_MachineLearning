"""
Quando i dati sono tanti 
chungking e striming

CHUNKING
Ci permette di leggere un dataset in porzioni o blocchi di dimensioni controllate.
Possiamo elaborare ogni chunk separatamente ed aggregare poi tutti dati, già filtrati
Divodi un dataset in blocchi, ogni chuck è un dataframe indipendente ed infine posso unire tutti i chunck
posso elaborare dataset con dimensioni superiore alla ram disponibile
STREAMING
ci permette di leggere i dati riga per riga ed è utilie per file molti grandi o con flussi continui di dati
Ha un approccio simile al chunck ma è più flessibile, posso leggere dasti da file, api o flussi in tempo reale.

Il tutto per evitare problemi di memoria
"""

import pandas as pd
import numpy as np

#
#Creazione dataset enorme
#
n_righe=5_000
np.random.seed(42)
prodotti=[f"Prodotto_{i}" for i in range(1,101)]
regioni=["Nord","Sud","Est","Ovest"]

df=pd.DataFrame({
    "ID": np.arange(1,n_righe+1),
    "Prodtto":np.random.choice(prodotti,n_righe),
    "Prezzo": np.round(np.random.uniform(5,500,n_righe),2),
    "Quantita": np.random.randint(1,20,n_righe),
    "Regione": np.random.choice(regioni, n_righe)
})
#print(df)

#Creazione file
file_csv="vendite_1M.csv"
df.to_csv(file_csv,index=False)
print(f"File {file_csv} creato.")

print("----------------------------------")
print("--------LETTURA A CHUNK-----------")
print("----------------------------------")
#Lettura a chunk
chunk_size=100
prezzi_medi=[]

for chunk in pd.read_csv(file_csv,chunksize=chunk_size):
    prezzo_medio=chunk["Prezzo"].mean()
    prezzi_medi.append(prezzo_medio)

print(f"Numero di chunck: {len(prezzi_medi)}")
print(f"Media massima dei prezzi per chunck: {max(prezzi_medi):.2f}")
print(f"Media minima dei prezzi per chunck: {min(prezzi_medi):.2f}")

print("----------------------------------")
print("--------LETTURA A HDF5------------")
print("----------------------------------")

#utilizzare HDF5, salvare lo stesso dataset in più chiavi (una per ogni regione)
#leggere solo un subset alla volta, calcolando la somma totale delle vendite

file_hdf="vendite_regioni.h5"
#Salvataggio per regione in chiavi diverse per ragione
for regione in regioni:
    subset=df[df["Regione"]==regione].copy()
    subset.to_hdf(file_hdf,key=regione,mode="a", format="table")
    subset["TotaleVendite"]=subset["Prezzo"]*subset["Quantita"]
    somma=subset["TotaleVendite"].sum()
    print(f"Somma vendite per regione {regione}: {somma:.2f}")

#
#salvare in file PARQUET
#

file_parquet="vendite_parq.parquet"
totale_filtrati=0
chunk_filtrati=[]
for chunk in pd.read_csv(file_csv,chunksize=chunk_size):
    filtrati=chunk[chunk["Prezzo"]>50].copy()
    if not filtrati.empty:
        chunk_filtrati.append(filtrati)
        totale_filtrati+=len(filtrati)
if chunk_filtrati:
    df_filtrato=pd.concat(chunk_filtrati,ignore_index=True)
    df_filtrato.to_parquet(file_parquet,index=False)
    print(f"Salvato Parquet incrementale con {totale_filtrati:,} righe filtrate.")
else:
    print("Nessuna riga filtrata")

#
#implementare uno STREAMING
#
def streaming_sum(file_csv):
    totale_quantita=0
    with open(file_csv,"r",encoding="utf-8") as f:
        next(f) #salta header
        for line in f:
            parts=line.strip().split(",")
            try:
                quantita=int(parts[3]) #colonna quantita
                totale_quantita+=quantita
            except (ValueError,IndexError):
                continue
    return totale_quantita

totale=streaming_sum(file_csv)
print(f"Somma cumulativa Quantita (streaming simulato): {totale}")
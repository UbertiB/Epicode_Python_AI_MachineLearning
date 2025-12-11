"""
Come scrivere codice efficiente e scalabile
quando il dataset cresce non basta più sapere come manipolare le tabella
bisogna anche capire come sfruttare al meglio le risorse del sistema.
- Scegliere il tipo di dato più adatto per le colonne
- differenza tra vettorizzazione loop e le operazione vettorializzate sono preferibili
- filtrare, ridurre i dati: non selezionano solo i dati ma anche a migliorare le performance
- dubug indispensabile per capire dove il codice rallenta
- tecniche avanzate per combinare tutti i concetti

-GESTIONE DELLA MEMORIA
-uno dei colli di bottiglia principali è spesso la memoria. Pandas, in default, usa 
int64 e float64, ma spesso non servono. Molti dati possono essere "compressi"
con il downcasting (int64->int32, float64->float32, object->category (per valori ripetuti) )
La scelta del tipo corretto può fare differenza enorme in termini di velocità ed utilizzo memoria
La conversione dei tipi, deve essere fatta con attenzione, per non perdere i dati o precisione.
- Pandas è progettato per operazioni vettoriali che sono preferibili a operazioni riga per riga.
Inoltre molte operazioni di Padas accettano il parametro inplace=true che permettono di fare una copia 
risparmiando tempo e memoria
-Il debug ed il profile delle operazioni è importanto per controllare l'utilizzo della memoria tramite
metodi come info e memoryusage e verificare statistiche sintetiche dei dati come describe.
Strumenti esterni come Memory e Profiler permettono di misurare l'uso delle memoria riga per riga.
Mentre time It consente di profilare il tempo di esecuzione di ogni singola operazione.
- combinando tutte queste tecniche insieme è indispensabile per ottimizzare la memoria e la velocità

"""

import pandas as pd
import numpy as np
import time

n_righe=1_000_000

df=pd.DataFrame({
    "ID":np.random.rand(n_righe),
    "Prezzo":np.random.rand(n_righe)*100,
    "Categoria":np.random.choice(["A","B","C","D"],size=n_righe),
    "Quantita": np.random.randint(1,100,size=n_righe)
})

#controllo memoria di tipi ottimizzati
print(f"Memoria originale (MB): {df.memory_usage(deep=True).sum()/1_048_576}")
#ottimizo i tipo
df["Quantita"]=df["Quantita"].astype("int16")
df["Categoria"]=df["Categoria"].astype("category")
df["Prezzo"]=df["Prezzo"].astype("float32")
print(f"Memoria dopo ottimizzazione tipo (MB): {df.memory_usage(deep=True).sum()/1_048_576}")

#operazioni vettoriali
df["Valori_totale"]=df["Prezzo"]*df["Quantita"]
#cancellazione colonne non necessarie
df.drop(columns=["ID"],inplace=True)

subset=df[df["Valori_totale"]>200].copy()

start=time.time()
media_valore=subset["Valori_totale"].mean()
end=time.time()
print(f"Media valore totale: {media_valore}")
print(f"Tempo di calcolo: {end-start} secondi")
print(f"Memoria dopo ottimizzazione (MB): {df.memory_usage(deep=True).sum()/1_048_576}")

#combiniamo con chung e serializzazione
df.to_csv("vendite.csv",index=False)
totale_valore=0
for chunk in pd.read_csv("vendite.csv",chunksize=10_000):
    chunk["Prezzo"]=chunk["Prezzo"].astype("float32")
    chunk["Quantita"]=chunk["Quantita"].astype("int16")
    chunk["Valore_totale"]=chunk["Prezzo"]*chunk["Quantita"]

totale_valore+=chunk["Valore_totale"].sum()
print(f"Totale vendite: {totale_valore}")


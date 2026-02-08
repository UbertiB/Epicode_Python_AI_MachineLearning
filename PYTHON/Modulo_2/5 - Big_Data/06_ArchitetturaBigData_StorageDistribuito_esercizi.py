"""
ESERCIZIO 1
* Crea un dataset di grandi dimensioni e salvalo sia in formato CSV che in formato Parquet,
confrontando la dimensione dei file e i tempi di lettura
ESERCIZIO 2
* Salvare lo stesso dataset in formato ORC e confrontare il tempo di caricamento con
Parquet
ESERCIZIO 3
* Implementare una semplice architettura simulata con più file Parquet per rappresentare 
un piccolo Data Lake, quindi leggere solo alcune colonne specifiche per analisi mirate
"""

import pandas as pd
import numpy as np
import time
import pyarrow.orc as orc
import pyarrow as pa
import dask.dataframe as dd

"""
ESERCIZIO 1
* Crea un dataset di grandi dimensioni e salvalo sia in formato CSV che in formato Parquet,
confrontando la dimensione dei file e i tempi di lettura
"""
df=pd.DataFrame({
    "id":np.arange(1,1_000_001),
    "categoria": np.random.choice(["A","B","C"],1_000_000),
    "valore": np.random.uniform(10,1000,1_000_000)
})

#scrittura file csv
t1=time.time()
df.to_csv("dati_gradi2.csv")
t2=time.time()
#scrittura file parquet
t3=time.time()
df.to_parquet("dati_grandi2.parquet",compression="snappy")
t4=time.time()

print(f"Scrittura CSV {t2-t1:.3f}s | Scrittura Parquet {t4-t3:.3f}s")

#lettura file csv
t5=time.time()
df_csv=pd.read_csv("dati_gradi2.csv")
t6=time.time()
#lettura file parquet
t7=time.time()
df_parquet=pd.read_parquet("dati_grandi2.parquet")
t8=time.time()

print(f"Lettura CSV {t6-t5:.3f}s | Lettura Parquet {t8-t7:.3f}s")

"""
ESERCIZIO 2
* Salvare lo stesso dataset in formato ORC e confrontare il tempo di caricamento con
Parquet
"""
#scrittura file ORC
t9=time.time()
df.to_orc("dati_grandi2.orc")
t10=time.time()
print(f"Scrittura Parquet {t4-t3:.3f}s | Scrittura OCR {t10-t9:.3f}s")

#lettura file ORC
t11=time.time()
table=pa.Table.from_pandas(df)
with open("dati_grandi2.orc","wb") as f:
    orc.write_table(table,f)
t12=time.time()

print(f"Lettura Parquet {t8-t7:.3f}s | Scrittura ORC {t12-t11:.3f}s")

"""
ESERCIZIO 3
* Implementare una semplice architettura simulata con più file Parquet per rappresentare 
un piccolo Data Lake, quindi leggere solo alcune colonne specifiche per analisi mirate
"""
df = pd.DataFrame({
    "id": np.arange(1, 1_000_001),
    "categoria": np.random.choice(["A","B","C"], 1_000_000),
    "sottocategoria": np.random.choice(["A","B","C"], 1_000_000),
    "quantita": np.random.uniform(10, 1000, 1_000_000),
    "prezzo": np.random.uniform(10, 1000, 1_000_000),
    "sconto": np.random.uniform(0, 0.5, 1_000_000),
})

chunks = np.array_split(df, 5)
for i, part in enumerate(chunks, start=1):
    part.to_parquet(f"dati_grandi3_{i:02d}.parquet", compression="snappy", index=False)

#lettura più file parquet con colonne specifiche
ddf = dd.read_parquet("dati_grandi3_*.parquet", columns=["categoria", "prezzo", "sconto"])    
print(df.head())
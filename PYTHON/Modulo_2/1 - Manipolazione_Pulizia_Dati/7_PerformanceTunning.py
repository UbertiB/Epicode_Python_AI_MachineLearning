"""
Con il performance tunning con tipi categorici e ottimizzazione
della memoria.
- Analisi dello stato iniziale del dastaset
- Conversione dei tipo
- downcasting numerico
- uso di variabili categoriche
Ci sono strumenti per automatizzare questa parte delle operazioni.
Quando si lavora con dataset di grandi dimensioni,uno dei problemi principali è l'uso della memoria
Ottimizzare il consumo di memoria è fondamentale sia per ridurre i tempi di esecuzione, 
sia per ottimizzare gli algoritmi di ml
Bisongna quindi capire quando spazion sta usando il nostro dataset, info e memori_usage
Uno dei modi più efficaci per ridutte l'uso di memoria è definire il tipo di dato con la sua dimensione
Le stringhe possono essere trasformate in categoria, se non hanno centinaia di elementi
Anche il downcasting, per i valori numerici, è fondamentale per ridudrre lo "spreco" di memoria.
Le categorie sono ottime per valori ripetitivi ma non se i valori unici crescono in modo continuo

"""

import pandas as pd
import numpy as np

df1=pd.DataFrame({
    "id":np.arange(1,1_000_001),
    "prezzo": np.random.uniform(1,100,1_000_000)
})
print("1) Consumo iniziale di memoria in (MB):",
      df1.memory_usage(deep=True).sum()/1024**2)

#facciamo il DOWNCASTING
df1["id"]=pd.to_numeric(df1["id"], downcast="integer")
df1["prezzo"]=pd.to_numeric(df1["prezzo"], downcast="float")
print("1) Consumo di memoria in (MB) dopo downcasting:",
      df1.memory_usage(deep=True).sum()/1024**2)

#ottimizzazione tramite tipi categorici
df3=pd.DataFrame({"categoria": np.random.choice(["A","B","C","D"], size=1_000_000)})
print("2) Consumo iniziale di memoria in (MB) dopo downcasting:",
      df3.memory_usage(deep=True).sum()/1024**2)
df3["categoria"]=df3["categoria"].astype="category"
print("2) Consumo di memoria in (MB) dopo category:",
      df3.memory_usage(deep=True).sum()/1024**2)

#cast study con più colonne con versione automatica
df4=pd.DataFrame({
    "user_id": np.random.randint(1,2_000_000,1_000_000),
    "product_category":np.random.choice(["abbigliamento","elettronica","giocattoli","libri"], size=1_000_000),
    "purcharse_amount":np.random.uniform(5,500,1_000_000),
    "purchase_date": pd.date_range("2020-01-01",periods=1_000_000,freq="T").astype(str)
})
print("3) Consumo iniziale di memoria in (MB):",
      df4.memory_usage(deep=True).sum()/1024**2)
df4["user_id"]=pd.to_numeric(df4["user_id"], downcast="integer")
df4["product_category"]=df4["product_category"].astype("category")
df4["purcharse_amount"]=pd.to_numeric(df4["purcharse_amount"],downcast="float")
df4["purchase_date"]=pd.to_datetime(df4["purchase_date"])
print("3) Consumo di memoria in (MB) dopo category:",
      df4.memory_usage(deep=True).sum()/1024**2)

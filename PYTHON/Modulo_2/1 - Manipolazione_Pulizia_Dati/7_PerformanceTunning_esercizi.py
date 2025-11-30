"""
ESERCIZIO 1
- calcola la memoria occupato dal df con colonne int64 e float64
- riduci i tipi numerici con il downcasting
- confronta memoria prima e dopo, spiegando quali colonne hanno beneficiato di più

ESERCIZIO 2
- misura la memoria occupata da una colonna object con valori ripetuti
- converti la colonna in category e calcola la nuova memoria
- spiega perchè la conversione porta vantaggi significativi in questo caso
ESERCIZIO 3
- Analizza la memoria iniziale di un dataset con int64, flot64, object e date in stringa
- applica ottimizzazioni
   - downcast di interi e float
   - conversione di colonne testuali in category
   - conversione di date in datetime64
- Misura la memoria finale e discuti i trade-off delle scelte fatte
"""

import pandas as pd
import numpy as np

print("-------------------------")
print("ESERCIZIO 1")
print("-------------------------")

data1={"numero1": np.random.randint(1,500,1_000_000), 
       "numero2":np.random.rand(1_000_000)}
df1=pd.DataFrame(data1)
#print (df1.head())
print("Esercizio 1) Consumo iniziale di memoria in (MB):",
      df1.memory_usage(deep=True).sum()/1024**2)
df1["numero1"]=df1["numero1"].astype("int16")
df1["numero2"]=df1["numero2"].astype("float32")
#print (df1.head())
print("Esercizio 1) Consumo iniziale dopo astype (MB):",
      df1.memory_usage(deep=True).sum()/1024**2)
#si passa da circa 11mb a circa 5mb, la conversione dei tipi, con il downcasting ove possibile
#senza perdere i dati, occupa meno memoria, rendendo il df performante

print("-------------------------")
print("ESERCIZIO 2")
print("-------------------------")

class Persona:
    def __init__(self, nome, eta):
        self.nome=nome
        self.eta=eta
    def __str__(self):
        return f"Nome: {self.nome} - eta: {self.eta}"
p1=Persona("Mario",50)
p2=Persona("Ettore",40)
p3=Persona("Anna",20)
p4=Persona("Maria",15)
data2={"persona": np.random.choice([p1, p2, p3, p4], size=1_000_000)}
df2=pd.DataFrame(data2)
print("Esercizio 2) Consumo iniziale di memoria in (MB):",
      df2.memory_usage(deep=True).sum()/1024**2)
df2["persona"]=df2["persona"].astype("category")
print("Esercizio 2) Consumo dopo category di memoria in (MB):",
      df2.memory_usage(deep=True).sum()/1024**2)


print("-------------------------")
print("ESERCIZIO 3")
print("-------------------------")

rng_date = pd.date_range("2020-01-01", "2025-01-01", freq="D")
data3={"persona": np.random.choice([p1, p2, p3, p4], size=1_000_000),
       "numero1": np.random.randint(1,500,1_000_000,dtype=np.int64),
       "numero2": np.random.rand(1_000_000),
       "data": (np.random.choice(rng_date, size=1_000_000,)).astype("str")}
df3=pd.DataFrame(data3)
print("Esercizio 3) Consumo iniziale di memoria in (MB):",
      df3.memory_usage(deep=True).sum()/1024**2)
df3["persona"]=df3["persona"].astype("category")
df3["numero1"]=df3["numero1"].astype("Int16")
df3["numero2"]=df3["numero2"].astype("float16")
df3["data"]=pd.to_datetime(df3["data"], format="ISO8601")

print("Esercizio 3) Consumo dopo pulizia di memoria in (MB):",
      df3.memory_usage(deep=True).sum()/1024**2)
#print (df3.head())



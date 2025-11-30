import numpy as np
import pandas as pd
import hashlib

"""
ESERCIZIO 1:    Genera un dataset di 500.000 righe con colonne id, name, salario e ufficio. 
                Carica solo le colonne necessarie, elimina duplicati e valori nulli, applica anonimizzazione su name e imposta id come indice. 
                Misura la memoria e i tempi di ricerca prima e dopo le ottimizzazioni.
"""
df1=pd.DataFrame({"Id": np.arange(1,500_001, dtype=np.int64),
                 "Nome": np.random.choice(['Alice', 'Bob', 'Carla', 'David','Charlie', 'David', 'Barbara','Carla','Carlo','Anna','Erika','Erik','Luigina','Giorgia','Giorgio','Mattia','Palmiro','Giovanna','Giovanni','Franco','Franca','Gianfranco','Gianfranca'], size=500_000),
                 "Salario": np.random.uniform(30000, 120000, size=500_000),
                 "Ufficio": np.random.choice(['Roma', 'Milano', 'Torino', 'Napoli'], size=500_000)
                })
print(f"\n DataFrame Iniziale:\n {df1.head()}")

#informazioni sulla memoria occupata prima delle ottimizzazioni
mem_usage = df1.memory_usage(deep=True).sum()
print(f"Memoria occupata prima delle ottimizzazioni: {mem_usage} byte.")

#salvo su csv e ricarico SOLO COLONNE NECESSARIE
df1.to_csv("data_esercizio.csv",index=False)
df1=pd.read_csv("data_esercizio.csv",usecols=["Id","Nome","Salario"])
#pulizia dati ELIMINO DUPLICATI (dulicates()) E VALORI NULLI (dropna())
df1=df1.drop_duplicates().dropna(subset=["Salario"])    
#DOWNCASTING numerico
df1["Id"]=df1["Id"].astype(np.int32) #riduco da int64 a int32
df1["Salario"]=df1["Salario"].astype(np.float32) #riduco da float64 a float32
#ottimizzazione CATEGORIA
df1["Nome"]=df1["Nome"].astype("category") #converte in tipo categorico
#anomizzazione DATI SENSIBILI con hash  hmac
salt="esercizio_salt"
df1["Nome_hmac"]=df1["Nome"].apply(lambda x: hashlib.sha256((salt+x).encode()).hexdigest())
#rimozione dati sensibili originali 
df1.drop(columns=["Nome"],inplace=True)
print(f"\n DataFrame Ordinato per Indice:\n {df1.head()}")
#imposto la COLONNA ID come indice
df1.set_index("Id",inplace=True)    

#informazioni sulla memoria occupata
mem_usage = df1.memory_usage(deep=True).sum()
print(f"Memoria occupata dopo le ottimizzazioni: {mem_usage} byte.")

"""
ESERCIZIO 2:    Crea un data set di 1.000.000 di righe, includendo colonne numeriche con valori grandi. 
                Applica downcasting a int32 e float 32 e confronta l'uso della memori. 
                Poi esegui un'aggregazione complessa (groupby e sum) e confronta i tempi prima e dopo il downcasting.
"""
df2=pd.DataFrame({"Numero1": np.random.uniform(1_000_000, 100_000_000, size=500_000),
                 "Numero2": np.random.uniform(1_000_000, 100_000_000, size=500_000),
                 "Numero3": np.random.uniform(1_000_000, 100_000_000, size=500_000),
                })
print(f"\n DataFrame Iniziale:\n {df2.head()}")
#informazioni sulla memoria occupata prima delle ottimizzazioni
mem_usage = df2.memory_usage(deep=True).sum()
print(f"Memoria occupata prima delle ottimizzazioni: {mem_usage} byte.")
#DOWNCASTING numerico
df2["Numero1"]=df2["Numero1"].astype(np.int32) #riduco da int64 a int32
df2["Numero2"]=df2["Numero2"].astype(np.float32) #riduco da float64 a float32
print(f"\n DataFrame Iniziale:\n {df2.head()}")
#informazioni sulla memoria occupata prima delle ottimizzazioni
mem_usage = df2.memory_usage(deep=True).sum()
print(f"Memoria occupata prima delle ottimizzazioni: {mem_usage} byte.")
#aggregazione complessa con groupby e sum
agg_result=df2.groupby(df2["Numero1"]%10).sum()
print(f"\n Risultato Aggregazione:\n {agg_result}")

"""
ESERCIZIO 3:    Genera un dataset misto con colonne id, name, salario, citta, ufficio, con valori ripetuti e mancanti casuali. 
                Applica pulizia, anonimizzazione dei nomi, indicizzazione avanzata e conversioni di colonne categoriche.
"""
df3=pd.DataFrame({"Id": np.arange(1,500_001, dtype=np.int64),
                 "Nome": np.random.choice(['Alice', 'Bob', 'Carla', 'David','Charlie', 'David', 'Barbara','Carla','Carlo','Anna','Erika','Erik','Luigina','Giorgia','Giorgio','Mattia','Palmiro','Giovanna','Giovanni','Franco','Franca','Gianfranco','Gianfranca'], size=500_000),
                 "Salario": np.random.uniform(30_000, 30_010, size=500_000),
                 "Ufficio": np.random.choice(['Roma', 'Milano', 'Torino', 'Napoli'], size=500_000)
                })
#salvo su csv e ricarico SOLO COLONNE NECESSARIE
df3.to_csv("mudulo2_lezione7_1.csv",index=False)
df3=pd.read_csv("mudulo2_lezione7_1.csv",usecols=["Id","Nome","Salario"])
#DOWNCASTING numerico
df3["Id"]=df3["Id"].astype(np.int32) #riduco da int64 a int32
df3["Salario"]=df3["Salario"].astype(np.float32) #riduco da float64 a float32
#anomizzazione DATI SENSIBILI con hash  hmac
salt="esercizio3_salt"
df3["Nome_hmac"]=df3["Nome"].apply(lambda x: hashlib.sha256((salt+x).encode()).hexdigest())
#rimozione dati sensibili originali
df3.drop(columns=["Nome"],inplace=True)
#imposto la COLONNA ID come indice
df3.set_index("Id",inplace=True)    
print(f"\n DataFrame Finale:\n {df3.head()}")
#informazioni sulla memoria occupata
mem_usage = df3.memory_usage(deep=True).sum()
print(f"Memoria occupata dopo le ottimizzazioni: {mem_usage} byte.")
#aggregazione complessa con groupby e sum
agg_result=df3.groupby("Nome_hmac").sum()
print(f"\n Risultato Aggregazione:\n {agg_result.head()}")

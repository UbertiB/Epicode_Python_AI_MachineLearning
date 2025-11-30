""""
INDICIZZAZIONE AVANZATA e GESTIONE SICURA DEI DATI
garantire la coeerenza dei valori e proteggere valori personali
Indici permettono di accedere direttamente alle righe

INDICIZZAZIONE
indicizzazione è il cuore di qualsiasi df efficiente, la scelta dell'indice
appropriato permette di accedere alla righe in modo diretto
riducendo il tempo di filtraggio, aggregazione, join e merge
Migliora le performace ma anche oraganizza logicamente i dati
Inoltre Pandas supporta indici multilivello (con + colonne)
facilitando aggregazioni complesse su più colonne
Un df senza un indice appropriato può diventare lento quando il dataframe cresce
poiche le operazioni di ricerca richiedono la scansione sequenzale di tutte le righe
con l'indice invece si accede direttamente alla riga desiderata
Con tanti dati l'ottimizzazione della memoria diventa fondamentale
Un primo approccio può essere caricare solo le colonne necessarie con usecols
poi rimuovere duplicati
rimuovere valori nulli o sistemare
downcasting numerico, converte colonne int64 in int32 op 16, oppure float
riduce l'uso della memoria
Idem per le colonne testuali con pochi valori distinti che possono convertite in category
Poi la combinazione di indicizzazione e gestione della memoria permette di ottimizzare operazioni
complesse come group by
 
SICUREZZA DEI DATI
Anominizzazione quando il dataset contiene info personali come noi, mail o codicei identificativi
Si possono utilizzare funzion di anonimizzazione come sha-256 (combinato con un salt)
Questo permette di condurre analisi senza esporre dati sensibili
La gestione sicura dei dati è obbligatoria anche per normativa

"""

import numpy as np
import pandas as pd
import hashlib

df=pd.DataFrame({"id": np.arange(1,1000001, dtype=np.int64),
                 "Nome": np.random.choice(['Alice', 'Bob', 'Carla', 'David','Charlie', 'David'], size=1000000),
                 "Categoria": np.random.choice(['CATEA', 'CATEB', 'CATEC', 'CATED','CATEE', 'CATEF'], size=1000000),
                 "Salario": np.random.uniform(30000, 120000, size=1000000),
        })
                 
#
#CARICAMENTO SELETTIVO con usecols
#
df.to_csv("data.csv",index=False)
df=pd.read_csv("data.csv",usecols=["id","Nome","Salario"])  #carico solo le colonne necessarie

#
#informazioni sulla MEMORIA OCCUPATA
#
print(f"\n Informazioni Iniziali sul DataFrame:\n {df.memory_usage(deep=True).sum()/1024**2} MB.")
#
# PULIZIA CANCELLAZIONE DUPLICATI E VALORI NULLI con dropduplicates
#
df.drop_duplicates() #elimino duplicati
df.dropna(subset=["Salario"]) #elimino righe con valori nulli nella colonna salario

#
#OTTIMIZZAZIONE NUMERICA CON DOWNCASTING
#
df["id"]=df["id"].astype(np.int32) #riduco da int64 a int32
#OPPURE
#df["id"]=pd.to_numeric(df["id"], downcast="integer")  #riduce da int64 a int32 o int16 a seconda del valore massimo

df["Salario"]=df["Salario"].astype(np.float32) #riduco da float64 a float32
#OPPURE
#df["Salario"]=pd.to_numeric(df["Salario"], downcast="float") #riduce da float64 a float32

#
#OTTIMIZZAZIONE CATEGORIE
#
df["Nome"]=df["Nome"].astype("category") #converte in tipo categorico
#df["Categoria"]=df["Categoria"].astype("category")


print(f"\n Informazioni Iniziali sul DataFrame:\n {df.memory_usage(deep=True).sum()/1024**2} MB.")



#
#INDICIZZAZIONE con .set_index
#
#df.set_index("id", inplace=True)  #imposto la colonna id come indice


#
#GESTIONE SICURA DEI DATI
#

#anomizzazione dati sensibili con hashah
salt="mysalt123"  #caratteri che aggiunge al valore originale per rendere più sicuro l'hash
df["Nome_hmac"]=df["Nome"].apply(lambda x: hashlib.sha256((salt+x).encode()).hexdigest())
print(f"\n DataFrame con Dati Anonimizzati:\n {df[['Nome','Nome_hmac']].head()}")
#rimozione dati sensibili originali
df.drop(columns=["Nome"],inplace=True)
print(f"\n DataFrame Finale:\n {df.head()}")

#
#INDICIZZAZIONE
#
df=df.set_index("id")  #imposto la colonna id come indice

#
#OPERAZIONI VELOCI
#
print(df.loc[500]) #avendo indice posso accedere direttamente alla riga 500
mean_salari=df.groupby("Nome_hmac")["Salario"].mean() #calcolo salario medio per nome
print(f"\n Salario Medio per Nome Anonimizzato:\n {mean_salari.head()}")
#df.sort_index(inplace=True) #ordino il dataframe in base all'indice
#print(f"\n DataFrame Ordinato per Indice:\n {df.head()}")
#df.reset_index(inplace=True) #reimposto l'indice di default
#print(f"\n DataFrame con Indice Reimpostato:\n {df.head()}")



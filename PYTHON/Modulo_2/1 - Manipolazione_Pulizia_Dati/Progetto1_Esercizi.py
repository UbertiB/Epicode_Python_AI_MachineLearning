import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

"""
ESECIZIO 1:    DATASET CLIOENTI:
               * Nome, Email, Data_nascita, Eta, Stipendio, Citta
               * Pulisci stringhe e email, valida pattern email
               * Converti le date in datetime e calcola l'età reale
               * Inputa valori mancanti con media/mediana
               * Identifica outlier nelle colonne numeriche.
               * Trasforma colonne ripetute in tipo categorico
"""
data1={"Nome":["Mario Rossi","  LUIGI BIANCHI","anna verdi","CaRlA NeRi", "Mario Rossi"],
      "Email": ["mario.rossi", " luigi@gmail", "   anna@gmail.com  "," gmail com",None],
      "Data_nascita": ["1985-05-15", "1990-08-22", None, "1978-12-30", "1985-05-15"],
      "Eta": [38, None, 33, 45, 38],
      "Stipendio": [50000, 60000, None, 80000, 50000],
      "Citta": ["Roma", "Milano", "Torino", None, "Roma"]
      }
df1=pd.DataFrame(data1)
print(df1)

df1["Nome"]=df1["Nome"].str.strip().str.title().fillna("Sconosciuto")
df1["Email"]=df1["Email"].map(lambda x: x.strip().lower() if pd.notnull(x) else x)
df1["Email_valida"]=df1["Email"].str.contains(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",na=False)
df1["Data_nascita"]=pd.to_datetime(df1["Data_nascita"],errors="coerce")
df1["Eta_reale"]=pd.Timestamp.now().year-df1["Data_nascita"].dt.year.astype("Int32")
df1["Eta"]=df1["Eta"].fillna(pd.Timestamp.now().year - df1["Data_nascita"].dt.year).astype("int32")
df1["Stipendio"]=df1["Stipendio"].fillna(df1["Stipendio"].median().astype("float32"))
df1["Citta"]=df1["Citta"].str.strip().str.title().fillna("Sconosciuta")
df1["Citta"]=df1["Citta"].astype("category")      


print(df1)
"""
ESERCIZIO 2:    DATASET VENDITE:
                * Colonne: Prodotto, Categoria, Prezzo, Quantita, Data_vendita
                * Pulizia stringhe e uniformattazione categorie
                * Conversione data1 e calcolo giorni della prima vendita
                * Rilevamento outlier e calcolo giorni dalla prima vendita
                * Creazione di feature: ricavo totale, log del prezzo, interazioni tra quantita e mese
  
"""
data2={"Prodotto": ["Prodotto A", " prodotto b ", "Prodotto C", "Prodotto A", "Prodotto B"],
       "Caategoria:": ["Elettronica", "elettronica", "Casa", "Elettronica", "casa"],
       "Prezzo": [199.99, 299.99, 49.99, 189.99, 59.99],
       "Quantita": [1, 2, 5, 1, 3],
       "Data_vendita": ["2023-01-15", "2023-02-20", "2023-01-25", "2023-03-10", None]
       }
df2=pd.DataFrame(data2)
print(df2)
df2["Prodotto"]=df2["Prodotto"].str.strip().str.title()
df2["Prodotto"]=df2["Prodotto"].astype("category")
df2["Categoria"]=df2["Caategoria:"].str.strip().str.title().fillna("Sconosciuta").astype("category")
df2["Prezzo"]=df2["Prezzo"].astype("float32")
df2["Quantita"]=df2["Quantita"].astype("int32")
df2["Data_vendita"]=pd.to_datetime(df2["Data_vendita"],errors="coerce")
data_minima=df2["Data_vendita"].min()
df2["Giorni_dalla_prima_vendita"]=(df2["Data_vendita"]-data_minima).dt.days.fillna(-1).astype("int32")
df2["Ricavo_totale"]=(df2["Prezzo"]*df2["Quantita"]).astype("float32")
#outlier detection con IQR su Prezzo
Q1=df2["Prezzo"].quantile(0.25)
Q3=df2["Prezzo"].quantile(0.75)
IQR=Q3-Q1
limite_basso=Q1-1.5*IQR
limite_alto=Q3+1.5*IQR
df2["Outlier_prezzo"]=(df2["Prezzo"]<limite_basso)|(df2["Prezzo"]>limite_alto)
df2["Log_prezzo"]=np.log(df2["Prezzo"]+1)

print(df2)


"""
PARTE 3:        DATASET COMPLETO MIXATO:
                * Colonne: Nome, Email, Data_iscrizione, Eta, Stipendio, Citta, Prodotto, Categoria, Vendite, Girni_attivi
                * Applica pipeline completa: pulizia stringa, validazione, gestione valori mancanti, gestione outlier, feature
                * Usa apply map e lambda per creare  almeno due colonne derivate 
"""
df3=df1.merge(df2,left_index=True,right_index=True,how="outer")
df3["Email"]=df3["Email"].where(df3["Email_valida"],other="")
df3=df3.drop(columns=["Email_valida", "Eta", "Data_nascita"])
#df3 = df3.drop(columns=["Eta"])
print(df3)

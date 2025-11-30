import pandas as pd
import numpy as np

#pulizia e validazione contatti mail, rilevando mail non valide

data={"Nome":["Mario Rossi","  LUIGI BIANCHI","Anna Verdi","Carla Neri"],
        "Email":["  mario@mail.com  ","LUCA@",None, "paolo@mail.com"],
        "Eta":[28,34,29,40],
        "Paese":["Italia","Italia","Francia","Italia"]}
df=pd.DataFrame(data)
print("DataFrame Iniziale:\n",df)
#Pulizia colonna nome
df["Nome"]=df["Nome"].str.strip().str.title()
df["Nome"]=df["Nome"].map(lambda x : x.strip().capitalize() if pd.notnull(x) else x)
#Pulizia colonna email
#rimuovo spazi bianchi e converto in minuscolo
df["Email"]=df["Email"].map(lambda x: x.strip().lower() if pd.notnull(x) else x)
#valido email con regex
#email_pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#df["Email_valida"]=df["Email"].str.match(email_pattern)
#oppure con funzione
df["Email_valida"]=df["Email"].str.contains(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",na=False)
print("\nDataFrame con Validazione Email:\n",df)
#formattazione colonna eta
df["Eta"]=df["Eta"].fillna(df["Eta"].median()).astype(int)
df["Paese"]=df["Paese"].str.strip().str.title()
df["Paese"]=df["Paese"].astype("category")
summary=df.isna().sum().to_dict()
print(df)
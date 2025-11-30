"""
Feature engineering, variabili cioè alle colonne di un dataset che utiliziamo per addestrare
un modello.
Comprende tutte quelle creazione, gestione, trasformazioni di variabili, che ci permette di estrarre informazioni
Il feature engineering i dati grezzi sono trasformati in dati più utili per rappresentare le
informazioni e per essere passati ai modelli predittivi
Etrae cononoscenza dai dati

Creazione di nuove feature derivate da variabili esistenti
Vari tipi di feture
- Creazione di nuove feature da variabili già presenti
- Trsformazione di feature già esistenti
- Codifica di variabili categoriche in numeriche per consentire l'uso nei modelli
- aggregazioni su gruppi di dati per cogliere dei pattern ricorrrenti
- riduzione dimensionale per diminuire il rumore
- Costruire nuove feature che derivano da iterazione di due o più variabili con modelli predittivi
Le fature devono essere confrontabili tra di loro in termini di scala
- standarizzazione
- normalizzazione, porta i valori in un range (esempio 0 e 1)
- logaritmo , riduca la variabilità
Tecniche di feature selection permettono di tenere solo le feature che servono
"""

import pandas as pd
import numpy as np

data={"Altezza_cm":[170,165,180,175],
       "Peso_kg":[65,70,80,75],
       "Data_rilevamento":["2023-01-01","2023-01-02","2023-01-03","2023-01-04"]
    }   

df=pd.DataFrame(data)
df["Data_rilevamento"]=pd.to_datetime(df["Data_rilevamento"])   

#CREAZIONE NUOVA FEATURE (feature derivata): INDICE DI MASSA CORPOREA (BMI)
# dati grezzi trasformati in data ipiù utili (feature)
df["BMI"]=df["Peso_kg"]/(df["Altezza_cm"]/100)**2   
print(df)
#NORMALIZZAZIONE DELLE FEATURE (Min-Max Scaling)
df_normalized=(df-df.min())/(df.max()-df.min()) 
print("\nDataFrame Normalizzato:\n",df_normalized)
#STANDARDIZZAZIONE DELLE FEATURE (Z-score Standardization)
df_standardized=(df-df.mean())/df.std() 
print("\nDataFrame Standardizzato:\n",df_standardized)
#CREAZIONE FEATURE BINARIE: SOVRAPPESO (BMI>25)
df["Sovrappeso"]=(df["BMI"]>25).astype(int)
print("\nDataFrame con Feature Binarie:\n",df)
#CREAZIONE FEATURE CATEGORICA: CATEGORIA PESO
def categoria_peso(bmi):
    if bmi<18.5:
        return "Sottopeso"
    elif 18.5<=bmi<25:
        return "Normopeso"
    elif 25<=bmi<30:
        return "Sovrappeso"
    else:
        return "Obeso"  
df["Categoria_Peso"]=df["BMI"].apply(categoria_peso)
print("\nDataFrame con Feature Categoriali:\n",df)


data2={"Colore":["Rosso","Blu","Verde","Giallo"],
       "Prezzo":[100,150,200,450]}
df2=pd.DataFrame(data2)
#ONE-HOT ENCODING PER VARIABILI CATEGORICALI
df2_onehot=pd.get_dummies(df2, columns=["Colore"])
print("\nDataFrame con One-Hot Encoding:\n",df2_onehot)
#BINNING PER VARIABILI CONTINUE: CATEGORIE PREZZO
bins=[0,120,200,300,999999]
labels=["Economico","Moderato","Costoso","Lusso"]
df2["Categoria_Prezzo"]=pd.cut(df2["Prezzo"], bins=bins, labels=labels)
print("\nDataFrame con Binning:\n",df2)
#FEATURE INTERAZIONE: PREZZO SCONTATO
df2["Sconto"]=0.1  #10% di sconto
df2["Prezzo_Scontato"]=df2["Prezzo"]*(1-df2["Sconto"])
print("\nDataFrame con Feature di Interazione:\n",df2)

data3={"Data":["2023-01-01","2023-01-02","2023-01-03","2023-01-04","2023-01-05","2023-01-06"],
         "Vendite":[10,15,14,20,18,25]}
df3=pd.DataFrame(data3)
df3["Data"]=pd.to_datetime(df3["Data"])

df3["Mese"]=df3["Data"].dt.month
df3["Vendite_log"]=df3["Vendite"].apply(lambda x: np.log1p(x))  #per ridurre l'impoatto dei valori grandi

df3.set_index("Data", inplace=True)
print(df3)
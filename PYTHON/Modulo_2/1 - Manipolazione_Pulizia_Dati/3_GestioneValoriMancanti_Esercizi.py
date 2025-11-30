
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer

"""
ESERCIZIO 1:    Creare un dataframe con 10 righe e una colonna con valori numerici e alcuni NaN. 
                Sostituisci i mancanti con un valore costante, ad esempio 0
"""
data1={"Valori":[15,13,None,14,13,None,18,10,8,None,25]}
np1=pd.DataFrame(data1)
np1_corretto1=np1.fillna(np1.mean())
print(f"Valori originali: \n{np1} \nsostituzione con costante media: {np1["Valori"].mean()} \n {np1_corretto1}")
np1_corretto2=np1.fillna(0)
print(f"\nsostituzione con costante: 0 \n {np1_corretto2}")
np1_corretto3=np1.fillna(np1.median())
print(f"\nSostituzione con mediana: {np1["Valori"].median()} \n{np1_corretto3}")

"""
ESERCIZIO 2:    Genera un dataframe con 3 colonne numeriche e alcuni valori mancanti. 
                Sostituisci i mancanti della prima colona con la media, 
                quelli della seconda con la mediana e 
                quelli della terza con la moda
"""
data2={"Numero1":[15,85,None,64,85,100],
       "Numero2":[64,66,67,68,None,69],
       "Numero3":[15,80,5,None,55,None]}
df2=pd.DataFrame(data2)
df2_corretto=df2[:]
df2_corretto["Numero1"]=df2_corretto["Numero1"].fillna(df2_corretto["Numero1"].mean())
df2_corretto["Numero2"]=df2_corretto["Numero2"].fillna(df2_corretto["Numero2"].median())
df2_corretto["Numero3"]=df2_corretto["Numero3"].fillna(df2_corretto["Numero3"].mode())
print(df2_corretto)

"""
ESERCIZIO 3:    Usa KNNImputer su un dataset con almeno due colonne numeriche e valori mancanti. 
                Prova diversi valori di n_neighbors e confronta i risultati ottenuti.
"""
data3={"Numero1":[15,15,None,15,15],
       "Numero2": [8,100,1550,None,50],
       "Numero3": [12,10,13,11,None]}
df3=pd.DataFrame(data3)

imputer1=KNNImputer(n_neighbors=1)
imputer2=KNNImputer(n_neighbors=2)
imputer10=KNNImputer(n_neighbors=10)
df3_corretto_1=pd.DataFrame(imputer1.fit_transform(df3),columns=df3.columns)
df3_corretto_2=pd.DataFrame(imputer2.fit_transform(df3),columns=df3.columns)
df3_corretto_10=pd.DataFrame(imputer10.fit_transform(df3),columns=df3.columns)
print(f"n_neighbors=1 \n{df3_corretto_1}")
print(f"n_neighbors=2 \n{df3_corretto_2}")
print(f"n_neighbors=10 \n{df3_corretto_10}")



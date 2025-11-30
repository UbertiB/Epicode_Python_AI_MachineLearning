import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

"""
ESERCIZIO 1:    Crea un dataframe con almeno 10 valori numerici e 
                individua gli outlier usando la deviazione standard (soglia 2)
"""
data1={"Valori": [10,12,120,13,15,12,200,800,10,12,13,14,9,10,13,15,900,14]}
df1=pd.DataFrame(data1)

media=df1["Valori"].mean()
dev_std=df1["Valori"].mean()
df1["Outlier"]=(abs(df1["Valori"]-media)>2*dev_std)  # è un outlier se valore-media è maggiore  di d*deviazione standard (outlier=true)

if True:
    print(df1)

"""
ESERCIZIO 2:    Genera un dataset di 20 valori, 
                applica il metodo IQR e rimuovi le righe con outlier. 
                Mostra il dataset pulito.
"""
data2={"Valori":[10,12,120,13,15,12,200,800,10,12,13,14,9,10,13,15,900,14]}
df2=pd.DataFrame(data2)

#Quantile 1
Q1=df2["Valori"].quantile(0.25)
#Quantile 3
Q3=df2["Valori"].quantile(0.75)
#IQR
IQR=Q3-Q1

limite_basso=Q1-1.5*IQR
limite_alto=Q3+1.5*IQR
print(f"limite basso: {limite_basso}, limite alto: {limite_alto}")

df2["Outlier"]=(df2["Valori"]<limite_basso)|(df2["Valori"]>limite_alto)

if True:
    print(df2)

"""
ESERCIZIO 3:    Usa IsolationForest su un dataset con due colonne numeriche 
                (es. Altezza e Peso). 
                Individua gli outlier e 
                visualizza i risultati in un dataframe con una 
                colonna aggiuntiva che+ indichi i valori anomali
"""
data3={"Altezza":[150,153,182,160,174,200,168,250],
       "Peso":[66,180,90,88,66,50,210,None]}
df3=pd.DataFrame(data3)

df3["Rapporto"]=(df3["Altezza"]/df3["Peso"]).where(df3["Peso"]!=0) 
df3["Rapporto"]=df3["Rapporto"].fillna(df3["Rapporto"].mean())
model=IsolationForest(contamination=0.2, random_state=42)
df3["Outlier"]=model.fit_predict(df3[["Rapporto"]])

if True:
    print(df3)

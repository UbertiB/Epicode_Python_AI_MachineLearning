#calcolo della deviazione standard

import pandas as pd
import numpy as np



np.random.seed(0)

dati1=({"Valore":np.random.normal(5,10,15)})
df1=pd.DataFrame(dati1)
media=df1["Valore"].mean()
dev_std=df1["Valore"].std()

print (f"Media: {media}, deviazione standard: {dev_std}")

#Individuo applaier, valori che sono agli estermi e possono distorcere la distribuzione
#utili per individuare errori

soglia=2
df1["Outlier"]=(abs(df1["Valore"]-media)>2 *dev_std)
print(df1)



print ("IQR")
#q1 valore che si trova al di sotto del 25% dei dati
#q3 valore che si trova al di sopra del 75% dei dati
#limite inferiore=q1, limite superiore= 3

#creazione dataset
df2=pd.DataFrame({"Valori":np.random.randint(20,30,100)})
#aggiungo outlier
df2.loc[100]=300
df2.loc[101]=2
print(df2)
q1=df2["Valori"].quantile(0.25)
q3=df2["Valori"].quantile(0.75)
IQR=q3-q1 #intervallo interquartile
print(f"Q1: {q1}, Q3: {q3}, IQR: {IQR}")
limite_inferiore=q1 - 1.5*IQR
limite_superiore=q3 + 1.5*IQR
print(f"Limite inferiore: {limite_inferiore}, Limite superiore: {limite_superiore}")
df_clean=df2[(df2["Valori"]>=limite_inferiore) & (df2["Valori"]<=limite_superiore)]
print("Dataset senza outlier:")
print(df_clean)




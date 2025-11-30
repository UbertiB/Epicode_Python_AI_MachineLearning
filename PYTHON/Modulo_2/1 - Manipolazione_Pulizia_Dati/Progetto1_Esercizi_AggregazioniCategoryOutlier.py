import pandas as pd
import numpy as np

data={"Store":["S1","S2","S1","S3","S2","S1"],
      "Prodotto":["A","B","A","C","B","C"],
      "Data": ["2023-01-01","2023-01-02","2023-01-03","2023-01-04","2023-01-05","2023-01-06"],
      "Vendite":[100,150,200,130,170,160]}
df=pd.DataFrame(data)

df["Data"]=pd.to_datetime(df["Data"])
df["Store"]=df["Store"].astype("category")
df["Prodotto"]=df["Prodotto"].astype("category")
df=df.set_index("Data")
settimanale=df.groupby(["Store","Prodotto"]).resample("W")["Vendite"].sum()
mensile=df.groupby(["Store","Prodotto"]).resample("M")["Vendite"].sum()
print("Vendite Settimanali:\n",settimanale)
print("\nVendite Mensili:\n",mensile)
Q1=mensile.quantile(0.25)
Q3=mensile.quantile(0.75)
IQR=Q3-Q1
soglia_superiore=Q3+1.5*IQR
soglia_inferiore=Q1-1.5*IQR
outliers=mensile[(mensile<soglia_inferiore) | (mensile>soglia_superiore)]
print("\nOutliers nelle Vendite Mensili:\n",outliers)
df["Vendite"]=pd.to_numeric(df["Vendite"],downcast="integer")
print("\nDataFrame con Tipi Ottimizzati:\n",df.info())
print("\nDataFrame:\n",df)
df.reset_index(inplace=True)
print("\nDataFrame con Indice Reimpostato:\n",df)

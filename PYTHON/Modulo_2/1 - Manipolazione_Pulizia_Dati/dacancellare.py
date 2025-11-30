
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer

data1={"Settimana":[1,2,3,4,5,6,7],
     "Vendite":[100,200,150,None,350,100,None],
     "Quantita":[50,55,60,42,70,80,np.nan]}
df1=pd.DataFrame(data1)
print(df1)

#Creazione di categorie
#df1["Categoria"]=["Alto" if x>300 else "Basso" for x in df1["Vendite"]]
#oppure
if False:
    df1["Categoria"] = np.where(df1["Vendite"] > 300, "Alto", "Basso")

    #Creazione di dati
    df1["Prezzounitario"]=df1["Quantita"]/df1["Vendite"]

#
#VALORI MANCANTI
#
print(f"Valori mancanti: \n{df1.isna().sum()}")

#sostituzione con valore fisso da statistica
df1["Vendite"]=df1["Vendite"].fillna(df1["Vendite"].mean()) #mediana

#KNNImputer
imputer=KNNImputer(n_neighbors=2) #elementi più simili e vicini agli elemnti mancanti per stimare valore (considera 2 elementi più vicini)
df1_imputer=pd.DataFrame(imputer.fit_transform(df1),columns=df1.columns)
print(f"imputer: \n{df1_imputer}")
#
# GRAFICO
#
media_vendite=df1["Vendite"].mean()
colori=np.where(df1["Vendite"]<media_vendite,"red","blue")

plt.bar(df1["Settimana"],df1["Vendite"], color=colori)
plt.axhline (media_vendite,color="red",linestyle="--")
plt.xlabel("Settimana")
plt.ylabel("Vendite")
plt.title("Vendite settimanali")
plt.legend()
plt.show()

if True:
    print (media_vendite)
    print(df1)





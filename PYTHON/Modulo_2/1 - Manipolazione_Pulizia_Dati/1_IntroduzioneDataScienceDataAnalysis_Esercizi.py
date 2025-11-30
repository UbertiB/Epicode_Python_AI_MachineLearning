
"""
Qual'è la settimana con vendite massime?
Aggiungi un grafico a linee sopra quello a barre 
    per la visualizzare meglio il trend
Cambia i colori alle barre in base a una soglia:
    rosso se sotto la media, verde se sopra
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dati={"Giorno":["lunedi","martedi","mercoledi","giovedi","venerdi","sabato","domenica"],
      "Vendite": [200,250,220,300,280,350,180]}

df=pd.DataFrame(dati)
media_vendite=df["Vendite"].mean()
print(f"media della settimana: {media_vendite}")

plt.bar(df["Giorno"],df["Vendite"],color="skyblue")
plt.axhline(media_vendite,color="red",linestyle="--",label="Media")
plt.xlabel("Giorni")
plt.ylabel("Vendite")
plt.legend()
plt.show()

massimo_vendite=df["Vendite"].mean()
print(f"settimana massima: {massimo_vendite}")

#colori=df["Vendite"].apply(lambda x :"red" if x<=media_vendite else "green")
#alla lambda preferire operazioni vettoriali, come segue:
colori=np.where(df["Vendite"] <= media_vendite, "red", "green")

plt.bar(df["Giorno"],df["Vendite"],color=colori)
plt.axhline(media_vendite,color="red",label="Media",linestyle="--")
#plt.axhline(massimo_vendite,color="yellow",label="Massimo",linestyle="--")
plt.xlabel("Giorno")
plt.ylabel("Vendite")
plt.legend()
plt.show()

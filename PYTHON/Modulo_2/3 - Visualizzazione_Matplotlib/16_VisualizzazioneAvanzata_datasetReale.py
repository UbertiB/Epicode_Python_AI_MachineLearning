"""
CASO DI STUDIO
Dataset reale, applicare tecniche di visualizzazione avanzata per estrarre inside significativi
- Preparare dati 
- Creare grafici
- Identificare patetrne stagionali nelle prenotazioni
- Evidenziare outlier e anomalie

- caricamento dati
- selezione colonne utili
- gestire dati nulli 
- pulizia dati (rimuovere outlier estermi)
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df=pd.read_csv("AB_NYC_2019.csv")
#PULIZIA DEI DATI (tolgo i record che non voglio analizzare)
df=df[df["price"]<1000]


if False:
    
    print (df.head())
    plt.figure(figsize=(8,5))
    sns.boxplot(x="room_type",y="price",data=df,palette="viridis")
    plt.title("Distribuzione prezzi per tipo di alloggio")
    plt.xlabel("Tipo di alloggio")
    plt.ylabel("Prezzo in dollari")
    plt.show()
#grafico con 3 tipi di stanza, i punti indicano le mediana, i quartili ed i valori anomali di ogni 
#tipo di alloggio

if False:
    #MAPPA GEOSPAZIALE
    plt.figure(figsize=(8,6))
    sns.scatterplot(x="longitude",y="latitude",hue="neighbourhood_group",data=df.sample(5_000),alpha=0.5,s=30)
    plt.title("Distribuzione geospaziale degli annunci Airnb di NYC")
    plt.xlabel("Longitudine")
    plt.ylabel("Latitudine")
    plt.legend(title="Borough",loc="upper right")
    plt.show()
    #releva una forte concentrazione in determinate zone

if True:
    #scatter con regressione, per verificare se esiste una relazione tra numero di recensione e prezzo
    plt.figure(figsize=(8,5))
    sns.regplot(x="number_of_reviews",y="price",data=df[df["number_of_reviews"]<200],scatter_kws={"alpha":0.5,"s":30},line_kws={"color":"red"})
    plt.title("Relazione tra numero di recensioni e prezzo")
    plt.xlabel("N. di recensioni")
    plt.ylabel("Prezzo in dollari")
    plt.show()
    #la popolarità di un annuncio non è legata al prezzo




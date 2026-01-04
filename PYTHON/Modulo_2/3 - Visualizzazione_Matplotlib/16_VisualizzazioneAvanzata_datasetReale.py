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
df=df[df["price"]<1000]

if False:
    
    print (df.head())
    plt.figure(figsize=(8,5))
    sns.boxplot(x="room_type",y="price",data=df,palette="viridis")
    plt.title("Distribuzione prezzi per tipo di alloggio")
    plt.xlabel("Tipo di alloggio")
    plt.ylabel("Prezzo in dollari")
    plt.show()

if True:
    plt.fig
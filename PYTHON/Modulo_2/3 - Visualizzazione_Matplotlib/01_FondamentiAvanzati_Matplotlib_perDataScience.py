"""
Visualizzazione avanzata dei dati con Matplotlib

è una delle librerie più potenti e versatili di Python per la visualizzazione avanzata dei dati.
Grafici 2D, grafici 3D figure iterative, visualizzazioni complesse e personalizzabili. 
Integrandosi con librerie scientifiche come numpy e pandas.
La sua flessibilità consente di produrre grafici semplici ma anche figura avanzate per pubblicazioni scientifiche, ecc
2 Modalità principali di utilizzo
- pyplot API (comoda per creare grafici veloci), 
- object orient API, preferibile in contesti avanzati (permette un controllo completo).
Quando si lavora con dataset di grandi dimensioni matplotlib si integra perfettamente con datafram pandas, sfruttando aggregazioni, filtraggi, 
inoltre l'utilizzo di array np vettorializzati permette di costruire grafici estremamente efficienti evitando loop ridondanti.

Grafici di tipo lineare, scatter, barre, istrgrammi, boxplot, grafici a torta, 3d, superfici, headmap.
Permette personalizzazione estetica, gestione di colori, e palette, stili di linea, market, trasparenza, colormap condizoinali
ed annotazioni dinamiche basate su valori calcolati.
Importante per rendere i grafici informativi, leggibile ed immediatamente interpretabili.

Separazione tra la logica dei dati e logica di visualizzazione. In ambienti reali i dati subiscono trasformazioni (aggregazioni, merge
normalizzazioni, imputazioni, ecc) matplotlib permette di utilizzare il risultati di questi dati direttamente.

La gestione di figure multi-plot consente di controllare visivamente più metriche o categorie contemporaneamente (gridspec o subplots)

L'approcio modulare e riutilizzabile è fondamentale per sviluppatori avanzati, funzioni o classi dedicate alla greazione dei grafici
possono accettare dataframe e parametri restituendo figure pronte per reportistica, esportazione o dashboard.
Questo garantisce coerenza tra visualizzazioni, riduce la scrittura di codice.

Alla fine matplotlib non è solo una libreria per creare grafici è uno strumento professionale per la visualizzazione di dataset complessi.


"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dates=pd.date_range("2023-01-01",periods=30)
sales=np.random.randint(50,200,size=30)
df=pd.DataFrame({
    "Date":dates,
    "Sales":sales
}).set_index("Date")
#print(df)
#
#GRAFICO LINEARE 
#
if False:
    fig,ax=plt.subplots(figsize=(10,5))
    ax.plot(df.index, df["Sales"],color="blue",linestyle="-",marker="o",label="Vendite giornaliere")
    ax.set_title("Vendite giornaliere - Gennaio 2025")
    ax.set_xlabel=("Data")
    ax.set_ylabel("Vendite")
    ax.grid(True)
    ax.legend()
    plt.show()

forecast=df["Sales"]*np.random.uniform(0.9,1.1,size=len(df))
df["Forecast"]=forecast

if False:
    fig,ax=plt.subplots(figsize=(10,6))
    ax.plot(df.index,df["Sales"],color="blue",linestyle="-",marker="o",label="Vendite reali")
    ax.plot(df.index,df["Forecast"],color="orange", linestyle="--", label="Forecast")
    ax.fill_between(df.index,df["Sales"],df["Forecast"],color="gray",alpha=0.2)
    ax.set_title("Confronto Vendite reali vs Forecast")
    ax.set_xlabel("Data")
    ax.set_ylabel("Vendite")
    ax.grid(True)
    ax.legend()
    plt.show()

df["Revenue"]=df["Sales"]*np.random.randint(10,20,size=len(df))
df["Units"]=np.random.randint(5,15,size=len(df))

if True:
    fig,axs=plt.subplots(2,2,figsize=(12,8))
    
    axs[0,0].plot(df.index,df["Sales"],color="blue")
    axs[0,0].set_title("Vendite")

    axs[0,1].bar(df.index,df["Units"],color="green")
    axs[0,1].set_title("Unita Vendute")

    axs[1,0].plot(df.index,df["Revenue"],color="red")
    axs[1,0].set_title("Fatturato")

    axs[1,1].scatter(df["Sales"],df["Revenue"],color="purple")
    axs[1,1].set_title("Vendite vs Fatturato")

    #per ogni grafico ruoto le etichette dell'asse x e aggiungo una griglia
    for ax in axs.flat:
        ax.grid(True) #griglia
        ax.tick_params(axis="x",rotation=45) #asse x ruotato
    plt.tight_layout()

    ax.grid(True)
    ax.legend()
    plt.show()    




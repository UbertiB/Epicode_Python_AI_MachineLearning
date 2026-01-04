"""
Consumo energetico: dati di consumo domestico in watt con outlier. Individua e rimuovi
valori fuori scala plausibile, crea un istogramma con asse y in scala log, definisci ticks a
step di 100W e analizza come la scala log evidenzi le code della distribuzione
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if False:
    #Creazione dataset fittizio
    np.random.seed(0)
    consumo_base = np.random.normal(loc=300, scale=50, size=1000)  # Consumo normale intorno a 300W
    outliers = np.random.choice([50, 1500, 2000], size=10)  # Outlier estremi
    nulli=[None,None] # valori nulli
    consumo_totale = np.concatenate([consumo_base, outliers,nulli])   
    print(len(consumo_totale))

    df=pd.DataFrame({"consumo_watt":consumo_totale})
    #print(df.head(15))

    #Rimozione outlier
    df_pulito=df[(df["consumo_watt"]>=100) & (df["consumo_watt"]<=1000)]
    print(f"Dati originali: {len(df)}, Dati puliti: {len(df_pulito)}")   
    df_pulito=df_pulito.dropna()
    print(f"Dati puliti dopo rimozione NaN: {len(df_pulito)}")

    max_consumo=df_pulito["consumo_watt"].max()

    #Istogramma con asse y in scala logaritmica
    fig,ax=plt.subplots(figsize=(10,6))
    ax.hist(df_pulito["consumo_watt"], bins=30, color="blue", alpha=0.7)
    ax.set_yscale("log")
    ax.set_title("Distribuzione consumo energetico domestico (dati puliti)")
    ax.set_xlabel("Consumo")
    ax.set_ylabel("Frequenza (scala logaritmica)")
    ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _:f"{int(x)} freq."))
    ax.set_xticks(np.arange(100, max_consumo+100, 100))  # Ticks a step di 100W
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(100))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _:f"{int(x)} W"))
    ax.grid(True, which="both", linestyle="--", alpha=0.5)

    
    plt.legend()
    plt.show()

"""
Concenttrazioni chimiche: dataset con misure in ppm e ppb. Uniforma le unità, calcola la metrice di correlazione
e crea una heatmap impostando entrambi gli assi in scala log per rappresentare ordini di grandezza diversi. 
Personalizza i ticks in notazione scientifica e interpreta i pattern evidenziati.
"""

if True:
    import seaborn as sns

    #Creazione dataset fittizio
    np.random.seed(0)
    n_samples=100
    sostanza_A_ppm=np.random.uniform(0.1,1000,size=n_samples)  #in ppm
    sostanza_B_ppb=np.random.uniform(100,1_000_000,size=n_samples)  #in ppb

    df_chem=pd.DataFrame({
        "sostanza_A_ppm":sostanza_A_ppm,
        "sostanza_B_ppb":sostanza_B_ppb
    })

    #Uniformare le unità (convertiamo ppb in ppm)
    df_chem["sostanza_B_ppm"]=df_chem["sostanza_B_ppb"]/1000

    #Calcolo matrice di correlazione
    corr_matrix=df_chem[["sostanza_A_ppm","sostanza_B_ppm"]].corr()
    print(corr_matrix)
"""
ESERCIZIO 1
Bilanci aziendali: dataset con bilanci da microimprese a multinazionali. Normalizza 
le unità (migliaia vs milioni), rimuovi valori mancanti, crea un grafico a barre prima
in scala lineare e poi in scala logaritmica. Definisci ticks per milioni e miliardi
con abbreviazioni (M,B) e scrivi una breve analisi sulle differenze di leggibilità 
tra le due scale

ESERCIZIO 2
Serie epidemica: pulisci date e rimuovi duplicati in un dataset giornaliero di nuovi casi.
Traccia i nuovi casi in scala logaritmica, imposta ticks temporali solo all'inizio di 
ogni settimana e aggiungi ticks verticali per soglie cliniche (100,1000,10000)
Confronta la percezione della crescita tra scala lineare e log

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

if False:

    #NOTAZIONE SCIENTIFICA: 1e3=1.000, 1e6=1.000.000, 1e9=1.000.000.000
    
    # Creazione dataset 
    Tipo_Azienda = ["Micro", "Piccola", "Media", "Grande", "Multinazionale"]
    Bilancio = [500_000, 2000_000, 50_000_000, 200_000_000, 5_000_000_000]  # valori corrispondenti alle unità

    df = pd.DataFrame({"Azienda": Tipo_Azienda, "Bilancio": Bilancio})
    print(df)

    fig,axes=plt.subplots(2,1,figsize=(10,8))

    axes[0].bar(df["Azienda"],df["Bilancio"])  #(df["Bilancio"],color="blue",linestyle="-",marker="o",label="Bilanci")
    axes[0].set_title("Bilanci per tipo di azienda (dati reali)")
    axes[0].set_xlabel("Tipo azienda")
    axes[0].set_ylabel("Bilancio (Eur)")
    axes[0].grid(True)
    axes[0].legend()

    axes[1].bar(df["Azienda"],df["Bilancio"])  #(df["Bilancio"],color="blue",linestyle="-",marker="o",label="Bilanci")
    axes[1].set_title("Bilanci per tipo di azienda (dati logaritmi)")
    axes[1].set_xlabel("Tipo azienda")
    axes[1].set_ylabel("Bilancio (Eur)")

    axes[1].set_yscale("log")  #SCALA LOGARITMICA

    def thousands(x,pos):
        if x>=1e9: return f"{x/1e9:.1f}B"  #b=miliardi
        if x>=1e6: return f"{x/1e6:.1f}M"   #m=milioni
        if x>=1e3: return f"{x/1e3:.1f}K" #k=mila
        return f"{int(x)}"
    
    axes[1].yaxis.set_major_formatter(ticker.FuncFormatter(thousands)) #FORMATTER PERSONALIZZATO    
    #oppure:
    #ticks_log = [1e3, 1e6, 1e9] #PERSONALIZZO I TICKS
    #ticks_log = [1_000, 1_000_000, 1_000_000_000] #PERSONALIZZO I TICKS    
    #labels_log = ["1K", "1M", "1B"]
    #axes[1].set_yticks(ticks_log)
    #axes[1].set_yticklabels(labels_log)

    axes[1].grid(True)
    axes[1].legend()

    plt.show()

if True:

    # Creazione dataset fittizio
    date = pd.date_range("2025-01-01", periods=60, freq="D")
    nuovi_casi = np.random.poisson(lam=200, size=60) + np.linspace(0, 2000, 60).astype(int)
    df = pd.DataFrame({"date": date, "nuovi_casi": nuovi_casi})

    # Pulizia e rimozione duplicati
    df.drop_duplicates(subset="date", inplace=True)
    df.sort_values("date", inplace=True)
    #print(df)

    fig,axes=plt.subplots(2,1,figsize=(10,8))

    axes[0].bar(df["date"],df["nuovi_casi"])
    axes[0].set_title("Nuovi casi")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel("Casi")
    axes[0].grid(True)
    axes[0].legend() 

    df_epidemic = pd.DataFrame({"date": date, "new_cases": nuovi_casi})

    axes[1].bar(df["date"],df["nuovi_casi"])
    axes[1].set_title("Nuovi casi")
    axes[1].set_xlabel("Date")
    #axes[1].xaxis.set_major_locator(ticker.MultipleLocator(7))
    axes[1].set_xticks(df_epidemic["date"][::7])
    axes[1].set_xticklabels([x.strftime("%Y-%m-%d") for x in df_epidemic["date"][::7]], rotation=45)
    for threshold in [100, 1000, 10000]:
        axes[1].axhline(threshold, color='red', linestyle='--', alpha=0.7)
    axes[1].set_ylabel("Casi")
    axes[1].grid(True)
    axes[1].legend()     

    plt.tight_layout()
    plt.show()   





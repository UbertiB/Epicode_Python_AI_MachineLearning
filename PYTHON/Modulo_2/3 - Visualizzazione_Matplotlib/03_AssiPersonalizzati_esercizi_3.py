#ESERCIZI SU ASSI PERSONALIZZATI
#SCALE LOGARITMICHE E NOTAZIONE SCIENTIFICA
#TICKS PERSONALIZZATI

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

if False:
    data={
        "Azienda":["A","B","C","D","E"],
        "Capitalizzazione":[1.2e6,None,5.5e9,3.4e3,2.1e11]
    }
    df=pd.DataFrame(data)
    df_clean=df.dropna() #per eliminare i valori mancanti, non è sempre la soluzoine migliore perchè rischia di compromettere la verificità del dataset
    print (df_clean)

    fig,ax=plt.subplots()
    ax.bar(df_clean["Azienda"],df_clean["Capitalizzazione"],color="skyblue",edgecolor="black")
    ax.set_yscale("log")  #scala logaritmica

    def billions(x,pos):
        if x>=1e9:
            return f"{x/1e9:.1f}B"  #B=miliardi
        if x>=1e6:
            return f"{x/1e6:.1f}M"   #M=milioni
        if x>=1e3:
            return f"{x/1e3:.1f}K" #K=mila
        return f"{int(x)}"  

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(billions)) #FORMATTER PERSONALIZZATO
    ax.set_title("Capitalizzazione di mercato (scala logaritmica)")
    ax.set_xlabel("Azienda")
    ax.set_ylabel("Capitalizzazione (notazione scientifica)")
    plt.show()

if True:

    date_rng=pd.date_range(start="2025-01-01",end="2025-02-28",freq="D")
    cases=np.exp(np.linspace(0.1,0.5,len(date_rng)))*100

    df=pd.DataFrame({"data":date_rng,"casi":cases.astype(int)})
    #print(df)

    fig,ax=plt.subplots(figsize=(10,5))
    ax.plot(df["data"],df["casi"],marker="o",color="red")

    ax.set_yscale("log")  #SCALA LOGARITMICA
       
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0)) #TICKS PERSONALIZZATI SULL'ASSE X
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d")) 

    ax.set_yticks([100,1_000,10_000,100_000]) #TICKS PERSONALIZZATI SULL'ASSE Y
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _:f"{int(x):,}")) #FORMATTER PERSONALIZZATO SULL'ASSE Y

  
    ax.set_title("Crescita giornaliera dei casi (scala logaritmica)") 
    ax.set_xlabel("Data")
    ax.set_ylabel("Numero di casi")
    ax.grid(True,which="both",linestyle="--")   

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
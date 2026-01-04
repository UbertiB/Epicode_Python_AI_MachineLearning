"""
VISUALIZZAZIONE SERIE TEMPORALI COMPLESSE
Le serie temporali sono dati molto diffusi in ogni ambito.
Problemi comuni includono:
* Dati che coprono ordini di grandezza diversi
* Necessità di evidenziare soglie critiche o trend
* Annotazioni per spiegare eventi chiave
Questo modulo mostra tecniche avanzate per gestire questi aspetti

* Spesso i dati temporali arrivano con frequenze diverse (giorni, ore, settimane,ecc). 
Se riportati insieme senza accorgimenti, questi dati possono generare confuzioni.
Il resampling (ricampionatura dei dati) è una tecnica utile per uniformare le serie temporali e portarli
ad una granularita comune (esempio disaggregare volori mensili in settimanali o annuali in quote mensili).
Le serie temporali normali sono spesse piene di rumori, oscillazioni improvvise, valori anomali.
L'applicazione di finestre mobili (esempio media mobile calcolata su un periodo di 7 giorni) 
attenua la variabilità quotidiana e mette in evidenza i trend.
Allo stesso modo le mediana mobili è più robusta ai valori estremi 
Mentro lo smoothing (levigatura) esponenziale attibuisce maggior peso ai dati recenti
e aiuta a ridurre il rumore mantenendo la forma generale della serie, 
attribuisce maggior peso ai dati più recenti.
L'aspetto importante è non confondere la serie "smussata" con i dati originali. Un grafico ben progettato 
mostra entrambe le serie di grandezza.
E' buona prassi specificare nella legenda quale tecnica è stata utilizzata.

Un'altra sfida tipica delle serie temporali è il confronto di variabili con unità di misure diverse (esempio l'aumento della
temporatura dell'ambiente con il consumo di energia elettrica in kw), in questo caso si ricorre spesso ai doppi assi verticali
uno a sinistra ed uno a destra, ogni serie deve essere bene etichettata. 
E' fondamentale rendere le etichette estremamente chiare e usare colori coerenti per legare ogni serie al proprio asse.
Un'alternativa più sicura è normalizzare i dati portandoli ad una scala comune.
Questo approccio è utilie per capire quando due fenonomi seguono andamenti simili o diverenti
Tuttavia perde informazioni sul livello reale delle variabili, per questo spesso si indica anche un grafico con i valori assoluti.
Un'altra pratica è la gestione del colore, usare colori differenti e linee differenziate per ogni serie.

E' importante documentare le scelte fatte per la visualizzazione, in modo che il lettore possa interpretare correttamente i dati.
Questi piccoli dettagli visivi hanno un impatto enorme sulla comprensione delle serie temporali complesse.
E' importante anche considerare il pubblico di destinazione e adeguarsi di conseguenza.
La leggibilità va testata anche su diversi dispositivi (esempio monitor, stampa bianco nero, pdf, cellulare, ecc).
Le annotazioni permettono di evidenziare eventi chiave all'interno della serie temporale, aiutando il lettore.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#SERIE CON GRANULARITA DIVERSE
if False:
    #serie giornaliera
    date_rng=pd.date_range(start="2025-01-01",end="2025-06-30",freq="D")
    consumo=np.random.randint(100,500,size=(len(date_rng)))
    #serie mensile
    data_months=pd.date_range(start="2025-01-01",end="2025-06-30",freq="M")
    produzione=np.random.randint(2000,6000,size=(len(data_months)))

    df_daily=pd.DataFrame(data={"data":date_rng,"consumo":consumo})
    df_monthly=pd.DataFrame(data={"data":data_months,"produzione":produzione})

    #il grafico risultante non è di immediata lettura
    # ho produzione mensile e consumo giornaliero (con valori molto più bassi)
    #Plot
    fig,ax=plt.subplots(figsize=(10,5))

    ax.plot(df_daily["data"],df_daily["consumo"],marker="o",label="Consumo giornaliero", alpha=0.6,color="blue")
    ax.scatter(df_monthly["data"],df_monthly["produzione"],marker="s",label="Produzione Mensile",color="red")
    ax.set_title("Serie con granularità diverse (poco leggibile)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Valori")
    ax.legend()
    plt.show()

#Media mobile e smoothing
if True:
    
    date_rng=pd.date_range(start="2025-01-01",end="2025-03-31",freq="D")
    vendite=np.linspace(100,500,len(date_rng))+np.random.normal(0,30,len(date_rng))
    df=pd.DataFrame({"Data":date_rng,"Vendite":vendite})
    #media mobile per 7 giorni
    df["MA7"]=df["Vendite"].rolling(window=7,min_periods=1).mean() #calcolo la media mobile settimanale
    #media mesile
    df["MA30"]=df["Vendite"].rolling(window=30,min_periods=1).mean() #calcolo la media mobile mensile
    #Plot
    fig,ax=plt.subplots(figsize=(10,5))
    ax.plot(df["Data"],df["Vendite"],marker="None", label="vendite", color="blue")
    ax.plot(df["Data"],df["MA7"],marker="o",label="Media mobile 7", color="red")
    ax.plot(df["Data"],df["MA30"],label="Media mobile 30",color="green",linewidth=2)
    ax.set_title("Smussamento con media mobili")
    ax.set_xlabel("Data")
    ax.set_ylabel("Vendite")
    ax.legend()
    plt.show()



# #Resampling mensile
# df_daily_resampled=df_daily.resample("M",on="data").sum().reset_index()
# df_merged=pd.merge(df_daily_resampled,df_monthly,on="data",how="inner")
# #Merge dei due dataset
# #print(df_merged.head())




"""
VISUALIZZAZIONE SERIE TEMPORALI COMPLESSE
Le serie temporali sono dati molto diffusi in ogni ambito.
Problemi comuni includono:
* Dati che coprono ordini di grandezza diversi
* Necessità di evidenziare soglie critiche o trend
* Annotazioni per spiegare eventi chiave
Questo modulo mostra tecniche avanzate per gestire questi aspetti

Spesso i dati temporali arrivano con frequenze diverse (giorni, ore, settimane,ecc). 
Se riportati insieme senza accorgimenti, questi dati possono generare confusioni.
l'occhio tende a sovrapportli anche se la base temporale non è la stessa

RESAMPLING (cambi la frequenza del tempo)
Il resampling (ricampionatura dei dati) è una tecnica utile per uniformare le serie temporali diverse
e portarle ad una granularita comune (esempio disaggregare volori mensili in settimanali o annuali in quote mensili,
portare valori settimanali a mensili, ecc).
Porti le serie su un nuovo calendario (più grosso o più fine) e poi devi aggregare o riempire. Esempio passi
da dati giornalieri a settimanali, oppure con UNSAMPLING da dati mensili a giornalieri (ma qui devi scegliere
come riempire)
In Pandas .resample("W"), .resample("M"), .resample("15min"), ecc e poi .sum(), .mean(), .count(), ecc.
mensile = df.set_index("data")["pezzi"].resample("M").sum()

ROLLING
Le serie temporali reali sono spesse piene di rumori, oscillazioni improvvise e valori anomali.
Con il rooling tieni la stessa frequenza temporale, ma calcoli su una finestra che scorre.
Non cambi il calendario, resti per esempio su 'giorni', ma per ogni giorno calcoli qualcosa 
(media, mediana, ecc) usando gli ultimi N giorni
L'applicazione di finestre mobili (esempio media mobile calcolata su un periodo di 7 giorni attenua
la variabilità quotidiana e mette in evidenza il trende).
Allo stesso modo le mediana mobili è più robusta ai valori estremi 
In Pandas è rolling(window=7).mean()
oee_ma7 = df.set_index("data")["oee"].rolling(window=7, min_periods=3).mean()

SMOOTHING
Esistono diverse tecniche di smoothing, tra le quali la media mobile ne è una
1) Media mobile (SMA): è rooling. Buona per rumore casuale, ma introduce ritardo (io trend appare dopo)
   .rolling(...).mean(), .rolling(...).median(), .rolling(...).sum()
2) Media mobile esponenziale (EWMA/EMA): pesa di più i dati recenti, quindi reagisce più in fretta ai cambi.
   In Pandas la trovi come finestre “Exponentially Weighted”.
3) Altri filtri (gaussiani, ecc): rari in azienda, utili se fai analisi 'segnale (sensori)
Esempio
# smoothing esponenziale: più peso al recente
oee_ewm = df.set_index("data")["oee"].ewm(span=7, adjust=False).mean()
Smoothing non è verità, è un filtro, puoi nascondere picchi che invete interessano (fermate, scarti improvvisi),
puoi far sembrare stabile un processo che in realtà è instabile

Mentro lo smoothing (levigatura) esponenziale attibuisce maggior peso ai dati recenti
e aiuta a ridurre il rumore mantenendo la forma generale della serie, 
attribuisce maggior peso ai dati più recenti.
L'aspetto importante è non confondere la serie "smussata" con i dati originali. 
Un grafico ben progettato mostra entrambe le serie di grandezza (serie originale e serie smussata).
E' buona prassi specificare nella legenda quale tecnica è stata utilizzata, per dare al lettore la possibilità
di interpretare correttamente il grafico.

Riassumendo:
- Resampling: cambia l'asse del tempo (nuovi 'bucket' temporali). Da utilizzarsi quando devi confrontare
  serie temporali diverse (giornaliera con mensile, ecc), quando devi regionare per un determinato periodo (
  esempio settimana piuttosto che mese), quando devi fare KPI per un certo periodo (esempio pezzi/mese, 
  scarti/settimana)
- Rooling: non cambia l'asse del tempo, cambia il valore in ognu punto usanto una finestra scorrevole. Da 
  utilizzarsi quando vuoi trend e stabilità senza perdere il dettaglio temporale

DOPPI ASSI VERTICALI
Un'altra sfida tipica delle serie temporali è il confronto di variabili con unità di misure diverse 
(esempio l'aumento della temporatura dell'ambiente con il consumo di energia elettrica in kw), 
in questo caso si ricorre spesso ai doppi assi verticali uno a sinistra ed uno a destra, ogni serie deve 
essere bene etichettata. 
E' fondamentale rendere le etichette estremamente chiare e usare colori coerenti per legare ogni serie al proprio asse.
Un'alternativa più sicura è NORMALIZZARE I DATI portandoli ad una scala comune, il confronto visivi si concentrarà
di più sui pattern e non sui singoli valori.
Questo approccio è utilie per capire quando due fenonomi seguono andamenti simili o divergenti
Tuttavia perde informazioni sul livello reale delle variabili, per questo spesso si combina la normalizzazione con
un secondo grafico dove vengono riportati i valori assoluti, offrendo al lettore entrambe le prospettive.
Un'altra pratica è la gestione del colore, usare colori coerenti e linee differenziate per ogni serie.

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
if True:
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
    ax.set_title("Serie con granularità diverse - DA SISTEMARE ILLEGGIBILE -")
    ax.set_xlabel("Data")
    ax.set_ylabel("Valori")
    ax.legend()
    plt.show()

    """
    In questo caso ho dati con granularità diversa (giornaliera e mensile), confrontare questi dati così 
    come arrivano diventa di difficile lettura e facilmente porta fuori strada il lettore.
    Il consumo giornaliero ha sicuramente importi più piccoli rispetto alla produzione mensile
    Una tecnica per rendere i dati tra loro confrontabili consiste nell'applicare lo smoothing
    """

#MEDIA MOBILE (SMOOTHING)
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




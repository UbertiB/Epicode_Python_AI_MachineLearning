"""
NUMPY CALCOLA, PANDAS ORGANIZZA, MATPLOTLIB MOSTRA

La viasualizzazione dei dati è il cuore dell'analisi quantitativa.
Matplotlib è già potente con la sua libreria ma la sua integrazione con Pandas e Numpy ci permette di passare da dati grezzi
a rappresentazioni visive molto più avanzate che semplicemente Pandas o Matplotlib in modo efficiente e flessibile.

NUMPY ci permette di gestire array multidimensionali eseguendo calcoli numerici complessi ed operazioni vettorializzate
molto più comode e veloci rispetto alle classiche iterazione di python riducendo i tempi rispetto ai classici cicli for

PANDAS offre delle strutture di data tabellari (dataframe) e serie temporali (series) ad alte prestazioni. permettendo 
selezione di filtri ed aggregazioni avanzate

MATPLOTLIB può convertire queste strutture in grafici leggibili personalizzabili e professionali. con annotazioni, colori
market ed anche stili sofisticati.

Vediamo come combinare queste 3 librerie per creare delle visualizzazioni avanzate passando da semplice array numerici 
a grafici analisi avanzate.

Numpy rappresentazione la base della computazione scientifica in pytyhon
Gli array multidimesnionali consentono di eseguire operazioni matematiche complesse in modo efficiente, quando integriamo questa
lireria a matplotlib possiamo generare dati sintetici con funzioni matematiche, rumore casuale o simulazioni. Possiamo anche
applicare trasformazioni numeriche (scaling,normalizzazioni, logaritmi, funzione trigonometriche) prima della visualizzazione
La visualizzazione può sfruttare direttamente gli array, linplot, scatter, barplot, ed itmap.
Un vantaggio chiave della libreria di np è la vettorializzazione, permettendo di lavorare con dataset di grandi dimensioni
senza rallentamenti.

Pandas porta la gestione dei dati ad un livello superiore, le strutture df e series rendenono semplici operazioni come
l'organizzazione dei dati etichettati e multidensionali, gestire indici temporali e dati mancanti, ed effetture aggregazioni
e trasformazioni avanzate in pochi minuti.

L'integrazione con matplotlib ci permette di visualizzare le colonne di un df direttamente con il metodo plot.
Automatizzare la gestione degli assi, dei titoli e legenda e di combinare più serie temporali in un unico grafico
Un df di pandas può derivare da dati reali, csv, databse, simulazioni, invece np gestisce la transizione dal calcolo alla 
visualizzazone in modo immediato, combinando le 3 libreria possiamo avere una potenza di calcolo (np), 
gestione flessibile dei dati (pansad) e visualizzazione avanzata (matplotlib).
Ad es. posso generare una serie temporale sintetica (np) memorizzarla in un df (con pandas) e con colonne multiple, fare 
calcolo statistici (media mobilem, deviazione stanrdar, percentuale) e visualizzare dati reali e delle metriche
calcolate in un grafico combinato con matplotlib.

*
NUMPY - IL MOTORE MATEMATICO
*
NP lavora con array numerici monodimensionali ed omogenei.
E' veloce, vettoriale, pensato per il calcolo

Esempio
import numpy as np
vendite=np.array([100,120,80,90])
media=vendite.mean()

NP non sa nulla di articoli, mesi, colonne, indici, gestisce SOLO numeri

*
PANDAS - IL CERVELLO TABELLARE
*
Pandas prende np e gli aggiunge:
etichette, righe e colonne, simantica (articolo, data, kpi)
Cioè questi numeri (np) appartengono a questi articoli in questi mesi

Esempio
import pandas as pd
df=pd.DataFrame({
    "Articolo":["A01","A02","A03","A04"],
    "Vendite":[100,200,80,90]})

Dentro Pandas i dati sono ancora NumPy, Pandas li organizza e li rende leggibili.
Quando fai:
df["Vendite"].mean()
Pandas chiama NumPy sotto il cofano

*
MATPLOTLIB - LA FINESTRA SUI DATI
*
Matplotlib prende array np, oppure df/series di Pandas e li trasforma in 1) linee 2) barre 3) heatmap

Esempio
import matplotlib.pyplot as plt
plt.bar[df["Articolo"],df["Vendite"]
plt.show()

Matplotlib non calcola, non organizza, disegna ciò che gli dai

COME LAVORANO INSIEME
Numpy calcola, Pandas struttura, Matplotlib visualizza

#NUMPY: CALCOLO
qta=np.array([100,120,80,90])
indice_rotazione=qta/qta.mean

#PANDAS: STRUTTURA
df=pd.DataFrame({
    "Articolo":["A01","A02","A03","A04"],
    "Rotazione": indice_rotazione})

#MATPLOTLIB: VISUALIZZAZIONE
plt.bar(df["Articolo"],df["Rotazione"])
plt.axhline(1,linestyle="-")
plt.show()

Spesso non ci si accorge dell'integrazione perchè Pandas usa np internamente, espone metodi "amichevoli"
Quando scrivi:
df.corr()
Stai usando pd per la struttura, np per il calcolo, plt per il grafico
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#
#LINEPLOT DA NUMPY  (NUMPY E MATPLOTLIB)
#
t=np.linspace(0,10,300)
y=np.sin(2*t)+0.2*np.random.randn(300)
plt.figure(figsize=(10,5))
plt.plot(t,y,label=("Segnale rumoroso"))
plt.title("Line plot generato da numpy")
plt.xlabel("Tempo")
plt.ylabel("Valore")
plt.show()

#DATAFRAME  (NUMPY, PANDAS, MATPLOTLIB)
dates=pd.date_range("2025-01-01","2025-02-28",freq="D")
sales=np.random.randint(50,200,len(dates))
df=pd.DataFrame({"Data": dates, "Vendite":sales})
df.plot(x="Data", y="Vendite", marker="o", linestyle="-", color="blue", figsize=(10,5))
plt.title("Serie temporale di vendite giornaliere")
plt.xlabel("Data")
plt.ylabel("Vendite")
plt.grid(True)
plt.show()

dates=pd.date_range("2025-01-01","2025-03-31",freq="D")
sales=100+10*np.sin(np.linspace(0,8,len(dates)))+np.random.random(len(dates))*5
df=pd.DataFrame({"Data":dates,"Vendite":sales})
df["MA7"]=np.random.randn(len(df)) #media mobile
df["STD7"]=df["Vendite"].rolling(7).std() #finestra temporale 7 giorni deviazione standard (.std)
plt.figure(figsize=(12,6))
plt.plot(df["Data"],df["Vendite"],alpha=0.5,label="Vendite giornaliere")
plt.plot(df["Data"],df["MA7"],color="red",label="Media modbile 7 giorni")
plt.fill_between(df["Data"],df["MA7"]-df["STD7"],df["MA7"]+df["STD7"],color="red",alpha=0.2,label="")
plt.title("Vendite e trand smussato con banda di deviazione")
plt.xlabel("Data")
plt.ylabel("Vendite")
plt.legend()
plt.show()






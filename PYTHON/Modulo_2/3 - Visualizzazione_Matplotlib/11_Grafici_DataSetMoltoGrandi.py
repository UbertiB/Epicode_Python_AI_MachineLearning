"""
Gestione di grafici per dataset molto grandi o flusso continui in arrivo.
In questi casi visualizzare tutti i dati in un unico grafico non è pratico ed utile (lento, difficile da leggere, non evidenzia
i pattern importanti)

Si utilizzano due strategie fondamentali
- Sampling (prendendo solo un sottoinsieme rappresentativo dei dati)
- Straming (aggiornare i grafici man mano che i dati arrivano, mostrando solo gli ultimi punti rilevanti)

Queste tecniche permettono di avere grafici veloci, leggibili ed informativi anche quando abbiamo un  dataset
troppo grande per essere visualizzato integralmente.
Il primo problema per dataset enormi è legato alle performance ed alla leggibilità, può rendere illegibile
il grafico, rallentare matplotlib, o bloccare l'intero sistema (per troppi dati).

Per affrontare questi problemi è fondamentale capire quali dati siano davvero necessari e quali possono
essere sintetizzati o ridotti senza perdere informazioni significative.
Un approccio consiste nel lavorare in un sottoinsieme rappresentativo dei dati stessi.
Concentrandosi sui trend di distribuzioni invece di visualizzare ogni singolo punto.
Questo concetto introduce la necessità di tecniche come sampling e lo streaming 
Ridurre la quantità dei dati (sempling) o aggiornare i grafici man mano che i dati arrivano (streaming)

SAMPLING 
selezionare un sottoinseieme dei dati che rappresenta fedelmente l'intero dataset, senza compromettere la
qualità dell'informazione, esistono diverse stategie di campionamento:
- campionamento casuale (etrae punti a caso)
- campionamento stratificato (preserva le proporzioni tra diverse categorie)
- campionamento sistematico (seleziona punto secondo regole fisse)
La scelta dei dati da campionare è fondamentale, troppi pochi punti rischiano di distorcere le distribuzioni
mentre troppi punti non risolvono i problemi di lentezza
L'obbiettivo del sampling è trovare un equilibrio tra leggibilità e la comunicazione in modo che il grafico continui
a comunicare correttamente i dati originali
Pandas offre degli strumenti per effetturare il sampling con metodi come
.sample (numero) (numero fisso di dati)
.sample (frazione di dati)
grazie a questi due motodi è possibile etrarre un numero fisso, o una frazione di dati in modo casuale.

Per dataset con valori categoriali il caricamente stratificato permette di mantenere le proporzioni costanti
tra le varie categorie evidando di introdurre dei bais.
Questo per l'espolorazione iniziale dei grafici o per generare grafici statici su dataset troppo grandi, 


lo STREAMING consiste nel visualizzare i dati che arrivano PROGRESSIVAMENTE, quindi quando i dati
non sono disponibili tutti insieme ma vengono raccolti generati o raccolticontinuamente 
(come nel caso dei sensori, log di sistema)
Non visualizzano tutti i dati contemporaneamente, ma solo i più recenti e aggiornati dinamicamente.
Spesso si utilizzano pattern circolari che conservano solo un certo numero di punti.
Matplotlib ci consente di implementare lo streaming tramite diverse strategie.
- aggiornando di grafici (linee o scatterplot) già esistenti con i dati che arrivano in tempo reale, 
senza ridisegnare completamente il grafico (func animation per aggioranre la figura in tempo reale 
o il metodo pose per aggiornamenti incrementali)
esempio aggiornare la figura ad intervalli regolare oppure refresh incrementali.
Consigliabile utilizzare buffer circolari in cui vengono mantenuti solo gli ultimi N punti visualizzati.
Riduce l'uso di memori e mantiene costante le performance.

Regole da seguire sia per dataset grandi o in streaming:
- Ridurre il numero dei punti da visualizzare (sempling casuale o stratificato o aggregazioni statistiche)
- importante anche scegliere grafici adatti al tipo di dato (scaterplot con trasparenza, liner aggiornati incrementale
i haemap per dati densi)
- Nel caso dello streaming conviene aggiornare le linee o i punti modificati evitando il ridisegno completo 
del grafico.
- tutte le trasformazioni devono essere documentate chiaramente, indicando se il grafico rappresenta solo un campione
una media dei dati originali.

Nell'area dei big dati i dataset possono diventare molto grandi, visualizzarli tutti può diventare impossibile.
Obbiettivo è produrre grafici veloci ed informativi

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#
# ESEMPIO SAMPLING (selezioniamo un sottoinsieme rappresentativo dei dati)
#

x=np.linspace(0,100,1_000_000)
y=np.sin(x)+np.random.normal(0,0.5,len(x))

df=pd.DataFrame({"x":x,"y":y})
#prendo 1% di valori e con random_state mi assicuro che i valori presi sono sempre gli stessi
df_sample=df.sample(frac=0.1, random_state=42)  #SAMPLE 1%

plt.figure(figsize=(10,5))
plt.scatter(df_sample["x"],df_sample["y"],alpha=0.6)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Sampling casuale del 1%")
plt.show()

#
# ESEMPIO STREAMING (visualizzare i dati man mano che arrivano)
#
from matplotlib.animation import FuncAnimation

x_data, y_data = [], [] #creo due array per il momento vuoti
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2) #creo una linea con due array ora vuoti
#definisco i limiti degli assi per evitare che si aggiornino automaticamente in base ai dati (anche perchè parte con una liena vuota)
ax.set_xlim(0, 100) #visualizza i dati da 0 a 100 (gli altri non spariscono, non sono nel grafico)
ax.set_ylim(-2, 2)

def init():
    line.set_data([], []) #parte con linea vuota e restituisce la linea
    return line,

def update(frame): #aggiorna la linea
    x_data.append(frame)
    y_data.append(np.sin(frame/5) + np.random.normal(0,0.1))
    if len(x_data) > 100:  # buffer circolare 
        #se ci sono più di 100 punti elimina il primo, quello più vecciho (in questo modo ho sempre 100 punti)
        x_data.pop(0)
        y_data.pop(0)
    line.set_data(x_data, y_data)
    return line,

#blit=true ridisegna il grafico solo le parti che cambiano
anim = FuncAnimation(fig, update, frames=np.arange(0,200), init_func=init, blit=True, interval=50)

plt.show()







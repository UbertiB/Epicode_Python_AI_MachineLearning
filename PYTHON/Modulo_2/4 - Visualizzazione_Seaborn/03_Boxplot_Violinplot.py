"""
BOXPLOT e VIOLINPLOT personalizzati per le ANALISI CATEGORICHE

Visualizzare la distribuzione dei dati in relazione a categorie qualitative è fondamentale 
per comprendere differenze e simmetrie ed outlier
I grafici come boxplot e violinplot offronto strumenti visivi potenti per sintetizzare la viaribilità
la mediana, i quartili e la densità dei dati.

BOXPLOT 
mostrano mediana, quartili e outlier e valori estremi (boxplot tradizionali). Fornenedo una istantanea
compatta della distribuzione dei dati, tuttavia con la personalizzazione  si possono evidenziare 
colori diversi per categoria, aggiungere annotazioni e gestire outlier in modo più leggibile.
Con il boxplot non si guardano ai singoli valori, ma come sono distribuiti
Nel boxplot le informazioni che da sono:
- Linea centrale: mediana, valore tipico, il 50% dei dati sta sopra il 50% sotto.
- Bordo inferiore box: percentile 25, il 25% dei valori è sotto questo punto
- Bordo superiore box: percentile 75, il 25% dei valori è sopra questo punto
- Baffi: estensione dei dati "normali" (50%), indicano la dispersione
- Pallini fuori:outlier, valori anormali, non errori
- Il box contiene il 50% centrale dei dati
La Mediana è la prima cosa da guardare, poi si guarda l'altezza dei box 
(box alto=molta variabilità, box basso=valori più stabili), successivamente si guardano i baffi
(baffi linghi=casi estermi frequenti, baffi corti=compartamente più controllato).
Si guardano gli outlier e ci si chiede: sono eccezioni o segnali di problema?
Mediana=livello tipico, mi dice 'quanto va bene'
Altezza box=affidabilità del processo
Outlier=campanelli d'allarme

VIOLINPLOT
Combinano informazioni di boxplot e densità offrendo un'idea più completa della forma della
distribuzione e permettendo di confrontare più categorie contemporaneamente.
La linea centrale indica la mediana, le altre linee i quartili, la larghezza del violino indica 
la densità (quanto valori stanno li).
L'altezza del violino dice 'quanto', la larghezza dice 'quanto spesso', un violino largo a un valore
dice che li ci sono molti dati, un violino stretto: pochi dati. Le pance del violino sono zone di alta
concetrazione, i colli invece sono zone 'rare'

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#punteggio di soddisfazione dei clienti diviso per giorno, fascia oraria
np.random.seed(42)
giorni=["lun","mar","mer","gio","ven"]
fasce=["Mattina","Pomeriggio","Sera"]
data={
    "giorno":np.random.choice(giorni,300),
    "fascia":np.random.choice(fasce,300),
    "soddisfazione":np.concatenate([
        np.random.normal(7,1,100),
        np.random.normal(5,1.5,100),
        np.random.normal(6,0.8,100)
    ])
    }
df=pd.DataFrame(data)

#
#BOXPLOT
#

#il boxplot consente di visualizzare rapidamente mediana, quartili, intervallo interquartile e outlier
#possiamo personalizzare i colori per categoria, aggiungere annotazioni, modificare larghezza e lo stile dei box

plt.figure(figsize=(8,5))
sns.boxplot(data=df,x="giorno",y="soddisfazione",hue="fascia",palette="Set2",linewidth=2,fliersize=5, order=["lun","mar","mer","gio","ven"])
plt.title("Boxplot personalizzaato della soddisfazione per giorno e fascia")
plt.xlabel("Giorno della settimana")
plt.ylabel("Punteggio di soddisfazione")
plt.legend()
plt.show()

#
#VIOLINPLOT
#

#combinano boxplot e stima di densità delle distribuzione, mostrnado non solo i quartili ma anche la
#forma completa dei dati, possiamo regolare larghezza, colori e orientamento, per ottenere visualizzazioni
#più intuitive
plt.figure(figsize=(8,5))
sns.violinplot(data=df,x="giorno",y="soddisfazione",hue="fascia",palette="Pastel1",split=True, inner="quartile")
plt.title("Violinplot avanzato della soddisfazione per giorno e fascia")
plt.xlabel("Giorno della settimana")
plt.ylabel("Punteggio di soddisfazione")
plt.legend()
plt.show()

#la combinazione di x ed hue permette di confrontare più categorie su un unico asse, esempio soddisfazione 
#per fascie orario ogni giorno della settimana
plt.figure(figsize=(10,6))
sns.violinplot(data=df,x="fascia",y="soddisfazione",hue="giorno",palette="Set3",split=False, inner="stick")
plt.title("Confronto tra fasce orarie per giorno (Violinplot)")
plt.xlabel("Fascia oraria")
plt.ylabel("Punteggio di soddisfazione")
plt.legend(title="Giorno")
plt.show()

#per rendere i grafici più leggibili possiamo regolare trasparenza, larghezza violini, orientamento
#orizontale, verticale e combinare violinplot e boxplot nello stesso grafico
#L'uso di palette coerente permette di distinguere categorie
plt.figure(figsize=(8,6))
sns.violinplot(data=df,x="giorno",y="soddisfazione",palette="coolwarm",cut=0, inner=None)
sns.boxplot(data=df,x="giorno",y="soddisfazione",palette="Set2",width=0.1,showcaps=True, boxprops={'facecolor':'none'})
plt.title("Boxplot sovrapposto a violinplot")
plt.xlabel("Giorno")
plt.ylabel("Soddisfazione")
plt.legend()
plt.show()



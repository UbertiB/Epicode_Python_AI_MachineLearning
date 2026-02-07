"""
HEATMAP AVANZATE con annotazioni statistiche

Le heatmap sono uno strumento fondamentale per la sintesi e l'interpretazione di grandi 
quantità di dati numerici. E' uno degli strumenti più efficaci per sintetizzare grandi quantita
di dati numerici.
Consentono di rappresentare matrici di valori codificati attraverso una scala di colori, 
rendendo immediata l'individuazione di pattern, relazioni, concentrazioni e anomalie. 
Nella loro forma più semplice, le heatmap forniscono una rappresentazione puramente descrittiva
matrice di valori codificata con una scale di valori; tuttavia, un utilizzo avanzato 
permette di integrare informazioni statistiche e strutturali, 
trasformandole in uno strumento di analisi più potente (p values, cluster e relazioni
complesse tra variabili).

Le heatmap avanzate consentono di arricchire la visualizzazione includendo metriche derivate, 
annotazioni statistiche, p-value, misure di dispersione e strutture di clustering. 
Questo approccio permette di unire analisi descrittiva e inferenziale in un'unica figura 
compatta, facilitando la lettura anche in presenza di molte variabili.

Tali tecniche sono ampiamente utilizzate in ambiti come la ricerca scientifica, la bioinformatica, 
l'economia, la data analysis e il machine learning, dove è frequente dover analizzare simultaneamente 
numerose variabili. 
Comprendere come costruire e interpretare correttamente heatmap avanzate è essenziale per trarre 
conclusioni affidabili e per evitare interpretazioni fuorvianti.

MATRICE DI CORRELAZIONE
Una delle applicazioni più comuni delle heatmap è la rappresentazione delle MATRICE DI CORRELAZIONE. 
In questo caso, ogni cella mostra il coefficiente di correlazione tra una coppia di variabili numeriche. 
Tuttavia, visualizzare esclusivamente i coefficienti di correlazione può essere insufficiente, 
poiché un valore elevato non implica necessariamente una relazione statisticamente significativa.
Non tutte le correlazioni osservate sono significative, per questo motivo è possibile arricchire 
la heatmap di correlazione con annotazioni di significatività statistica, basate sui p-value 
associati ai test di correlazione. 
I livelli di significatività vengono spesso indicati tramite simboli grafici, come le stelle:
*** indica p < 0.001
**  indica p < 0.01
*   indica p < 0.05

Questo sistema consente di distinguere rapidamente le correlazioni robuste da quelle potenzialmente 
dovute al caso, combinando informazione numerica e statistica, distinguendo relazioni forti da casuali.

Seaborn, in combinazione con librerie statistiche come SciPy, permette di calcolare automaticamente 
sia i coefficienti di correlazione sia i relativi p-value per ciascuna coppia di variabili. 
Così da creare matrici annotate.
Le heatmap annotate risultanti hanno un elevato valore comunicativo: le informazioni statistiche sono 
integrate direttamente nel grafico, rendendo la lettura accessibile anche a utenti non esperti di statistica.

Nelle matrici di correlazione i valori sopra e sotto la diagonale principale sono simmetrici. 
Visualizzare entrambe le metà della matrice è quindi ridondante. 

HEATMAP TRIANGOLARI
Le heatmap triangolari mostrano solo una metà della matrice, generalmente quella inferiore, 
migliorando la leggibilità e lasciando più spazio alle annotazioni aggiuntive (come p-values
e le stelle di significatività). 
Questo risultato si ottiene applicando una maschera booleana alla matrice di correlazione che nasconda
la parte superiore o inferiore della matrice. L'aggiunta dei p values permette di valutare simultanemente
la forza e la significatività di ciascuna correlazioni. E' possibele colorale le celle in base ai p values.

Le heatmap triangolari sono particolarmente utili quando si lavora con dataset ad alta dimensionalità, 
poiché riducono il sovraccarico visivo e permettono di concentrarsi sulle relazioni rilevanti. 
In alcuni casi, i coefficienti di correlazione possono essere visualizzati come testo all'interno 
delle celle, mentre il colore dello sfondo rappresenta l'intensità del valore, offrendo un ulteriore 
livello di chiarezza. Alcuni analisti preveriscono inserire il coefficente di correlazione
all'interno della cella come testo, colorando lo sfondo in base al p values.

CLUSTERED HEATMAP
Un'evoluzione delle heatmap tradizionali è rappresentata dalle clustered heatmap. 
In questo caso, righe e colonne vengono riordinate automaticamente in base alla somiglianza 
tra variabili o osservazioni. Questa tecnica utilizza algoritmi di clustering gerarchico per 
individuare gruppi omogenei e visualizzare la struttura dei dati tramite dendrogrammi affiancati 
alla matrice.

In Seaborn, le clustered heatmap permettono di controllare la metrica di distanza e il metodo di 
collegamento, offrendo flessibilità nella definizione dei criteri di similarità. 
Questo tipo di visualizzazione è ampiamente utilizzato nell'analisi di geni, clienti o prodotti, 
dove la similarità tra elementi rappresenta un'informazione chiave. 

Un ulteriore utilizzo avanzato delle heatmap consiste nella rappresentazione di valori aggregati, 
come medie o deviazioni standard di più osservazioni, al posto dei dati grezzi. 
Possiamo calcolare indicatori riassuntivi per ogni combinazioni di categorie ed esporli in grafico.
In questo caso, i dati vengono aggregati per combinazioni di variabili categoriali e il valore 
risultante viene visualizzato tramite una mappa di colore. 
Questa tecnica è particolarmente efficace per confrontare prestazioni, punteggi medi, tassi di successo 
o indicatori quantitativi simili.

La deviazione standard può essere visualizzata come annotazione testuale all'interno delle celle 
oppure come heatmap separata, consentendo di valutare rapidamente la variabilità interna ai gruppi. 
Le heatmap della dispersione completano l'analisi descrittiva, fornendo informazioni fondamentali 
sulla stabilità o variabilità dei dati.

Quando si calcolo decine o centinaio di correlazioni aumenta il rischio di trovare correlazioni
apparentemente significativi (solo per effetto del caso), per questo motivo è opportuno applicare 
una correzione per cofronti multipli come bonferroni o fdr, per controllare la probbabilità di errori di tipo 1
Dopo aver applicato la correzione, possiamo evidenziare le celle significative modificando il 
loro colore, aggiungendo contorni o simboli specifici , in questo modo la headmap mostra l'affidabilità 
statistica, permettendo di concentrare l'attenzione sui partner robusti piùttosto che relazioni casuali.
Questa tecnica è utilizzata in data scienze avanzata, è la sintesi perfetta tra calcolo e percezione visiva
L'integrazoine tra analisis statistica e visualizzazione grafica rende le heatmap avanzate uno strumento indispensabile
per l'analisi esplorativa dei dati e la comunicazione efficace dei risultati.

"""

import seaborn as sns
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

np.random.seed(0)
df=pd.DataFrame(np.random.randn(50,5),columns=list("ABCDE"))
#print(df)

#
#matrice di correlazione
#
#Il coefficiente di correlazione misura quanto due variabili si muovono insieme in modo
#lineare e in che direzione, le due variabili devono muoversi insieme su una retta (correlazione lineare)
#Se non si indivisua una correlazione lineare, il coefficiente di correlazione di Pearson non è adatto.
#Non significa che non esiste una relazione tra le due variabili, ma solo che non è lineare.
#Potrebbe esserci una relazione non lineare (ad esempio quadratica, esponenziale, logaritmica, ecc)
#Possibili valori del coefficiente di correlazione di Pearson:
# +1 = relazione lineare pefetta positiva (x aumenta y aumenta)
# -1 = relazione lineare perfetta negativa (x aumenta y diminuisce)
#  0 = nessuna relazione lineare (ma potrebbero esserci relazioni non lineari)
#La diagonale della matrice di correlazione è sempre 1 (ogni variabile è perfettamente correlata con se stessa)

corr=df.corr() #Matrice di correlazione di Pearson (che è quella di default) tra tutte le colonne numeriche del df
#
#Test di Pearson
#ricalcolo la matrice di correlazione applicando la funzione del test di Pearson
#usi Person non per scoprire se due variabili sono collegate, ma per verificare se sono collegate
#in modo lineare

#Il test di Pearson restituisce una coppia di valori 
# r [0] = r (coefficiente di correlazione): misura quanto due variabili si muovono insieme 
# in modo lineare (direzione ed intensità) -1 0 +1
# r [1] = p-values: indica la significatività statistica del legame (della correlazione)
#un p values basso indica che la correlazione osservata è improbabile che sia dovuta al caso
#tipicamente si usa una soglia di 0.05 per considerare una correlazione
#significativa (cioè con meno del 5% di probabilità che sia dovuta al caso)
#se faccio molti test di correlazione (ad esempio 1000) è probabile che alcuni risultati
#siano significativi solo per caso, per questo motivo si applicano correzioni per confronti multipli

#calcolo/creo una matrice di p values
pvals=df.corr(method=lambda x,y: stats.pearsonr(x,y)[1]) -np.eye(len(df.columns)) #np.eye azzera la diagonale (che altrimenti avrebbe p value = 0 per la correlazione con se stessa)
#creo la maschera per prendere solo la metà della matrice di correlazione (l'altra parte è uguale alla prima)
mask=np.triu(np.ones_like(corr,dtype=bool)) #triu prende solo la parte diagonale superiore (per nascondere metà della matrice simmetrica) Creo una maschera triangolare superiore

sns.heatmap(corr,mask=mask,annot=True,cmap="coolwarm",fmt=".2f") #annot=True scrive i valori numerice nelle celle
plt.title("Heatmap triangolare delle correlazioni")
plt.show()

#il risultato oscilla tra -0.11 e +0.23 identifica che non esistono correlazioni forti.
#questo dataset è realmente indipendente, o troppo piccolo, o troppo rumoroso, o simulato con random 
# (come nel mio caso)
#Che non ci sia una correlazione lineare lo si vede anche nello scatterplot che poi andrò a visualizzare
#tra a e b, a e c, a e d, b e c, b e d, c e d lo scatterplot evidenzia nubi, non c'è una direzione 
#pertanto non c'è un correlazione lineare (Pearson funziona solo con correlazioni lineari)
#potrebbe esserci un altro tipo di correlazione non lineare, ma Pearson non la individua

sns.scatterplot(x=df["A"], y=df["B"])
plt.title("Scatter A - B")
plt.show()
sns.scatterplot(x=df["A"], y=df["C"])
plt.title("Scatter A - C")
plt.show()
#, ecc per tutte le combinazioni, sicuramente fare il test di Pearson è più veloce che testare tutte
#le correlazioni

#
#CLUSTERED HEATMAP CON DENDOGRAMMI
#
#combina la heatmap con i dendogrammi, con la heatmap nell'esempio sotto vedo che le variabili non 
#hanno una relazione lineare forte, non hanno dipendenze, tutte coerenti con dati casuali. 
# I valori oscillano tra 0.11 e 0.28 confermando la mancanze di dipendenza lineare.
#Alla Heatmap si aggiungono i dendogrammi, che raggruppa le variabili solo in base a somiglianze relative
#dei pattern, non ha relazioni forti.
#questa visualizzazione è utile per indivisuare gruppi di variabili correlate tra di loro
sns.clustermap(corr, cmap="vlag", center=0, annot=True)
plt.suptitle("Clustered Heatmap con dendrogrammi", y=1.05)
plt.show()

#
#HEATMAP DI MEDIA CON MEDIA DEVIAZIONE STANDARD (per ogni combinazione di categorie/gruppi)
#

data=pd.DataFrame({
        "categoria":np.repeat(["A","B","C"],10),
        "gruppo":np.tile(["X","Y","Z"],10),
        "valore": np.random.rand(30)*10
})
pivot=data.pivot_table(values="valore",index="categoria",columns="gruppo",aggfunc=[np.mean,np.std])
print(pivot)
sns.heatmap(pivot["mean"],annot=True,cmap="ylGnBu")
plt.title("Heatmap delle medie per categorie e gruppo")
plt.show()

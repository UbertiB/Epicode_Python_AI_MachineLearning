"""
Analisi bivariata = analisi di due variabili alla volta (X e Y) per capire se c'è una relazioni e come
questa è fatta. 

L'analisi può essere:
- descrittiva: guardi forma, trend, outlier, gruppi
- inferenziale: fai un test o un modello,calcoli correlazioni, regressioni, test statistici
E' un modo per rispondere alla domande tipo "quando X aumenta, Y come si comporta?"

La SCELTA DEL GRAFICO dipende dal tipo di variabili (continue, categoriali) e dallo scopo dell'analisi
- NUMERICA VS NUMERICA (es. %sconto vs %margine): scatterplot (è il punto di partenza, ogni riga del dataset
  è un punto x,y, se vedi una 'nuvola' inclinata c'è una relazione, se vedi una curva non è lineare, 
  se vedi due nuvole, hai segmenti diversi), joinplot (scatter + distribuzioni marginali, utile perchè
  mostra subito se una variabile è 'strana', supporta diversi 'kind' scatter, reg, hex, kde, hist, resid), 
  regplot/implot (serve per capire tendenza lineare e per smascherare caso dove Pearson sembra alto ma
  guidato da pochi outlier), kde bivariato
- CATEGORIALE VS NUMERICA (es. fornitore vs leadtime): boxplot (confronta mediana, dispersione, outlier), 
  violinplot (come boxplot ma mostra anche la densita), stripplot (mostra i valori reali), 
  swarmplot (mostra i valori reali senza sovrapposizioni), barplot/pointplot (confronta la media, 
  spesso con intervallo di confidenza)
  Plot di confronto vuol dire: un grafico che confronta la distribuzione di una variabile numerica 
  tra più gruppi (categorie). Misuri e confronti la variabile numerica mentre, la variabile categoriale, 
  serve solo per 'tagliare' i dati in gruppi distinti.
- CATEGORIALE VS CATEGORIALE (es. sesso vs preferenza colore): heatmap di contingenza, clustered heatmap, count
  Qui l'analisi bivariata  diventa: contare le combinazioni e capire se le due variabili sono indipendenti
  o associate (test del chi quadro)

L'analisi bivariata si concentra sull'esplorazione delle relazioni tra due variabili, identificando
pattern, trend e correlazione e osservando eventuali differenze tra gruppi.
Visualizzare due variabili contemporaneamente può permettere di individurae relazioni lineari o no
ma anche di individuare cluster naturali o outlier che potrebbero influenzare l'analisi statistica successiva.

Due strumenti utili per visualizzare queste relazioni sono il jointplot e i vari comparison plot (come il pairplot) di Seaborn.

Il jointplot combina un grafico di dispersione (scatter plot) con istogrammi marginali per mostrare la distribuzione di ciascuna variabile.

Il pairplot estende questo concetto creando una matrice di grafici di dispersione per tutte le coppie di variabili in un dataset, insieme a istogrammi marginali per ogni variabile.
Questi grafici aiutano a identificare correlazioni, tendenze e pattern tra le variabili.

JOINPLOT (analisi bivariata numerica vs numerica)
Strumento versatile per visualizzare due variabili insieme
Nel pannello centrale mostra la relazione tra due variabili x e y (scatter plot, regplot, o un grafico kde bidimensionlae)
mentre lungo i margini vengono visualizzare le distribuzioni indivisuali di ciascuna variabile (istogrammi
o KDE, a seconda del tipo).
Questa combinazione permette di osservare contemporaneamente la forma generale dei dati e la loro densita
identificando tendenze lineari o non lineari e la presenza di valori estremi.
In molti casi le distribuzioni marginali offrono informazioni importanti sulle caratteristiche del dataset
come asimmetrie o concentrazioni di valori.
Può essere arrichito in diversi modo per analisi più approfondite:
- Parametro HUE consente di distinguere i dati in base ad una variabile categoriale rendendo visibili
differenze tra gruppi direttamente all'interno dello stesso grafico
- e' possibile scegliere il tipo di grafico centrale: uno scatterplot (scatter) mostra la relazione diretta, buono
per vedere forma, cluster, outlier 
un regplot (reg) scatter + retta di regressione permette di stimare una regressione lineare o polimoniale, 
un kde bidimensionale evidenzia aree di maggiore densita
- le distribuzioni marginali possono essere personalizzate (istogrammi, kde, rug plot) con parametri
come bendhid o ragplot per enfatizzare dettagli dei dati
Questo funzionalità rendono il joinplot un ottimo strumento per osservazioni esplorative avanzate
combinando informazioni di relazione e densità in una singola figura

Quando si vuole confrontare due variabili continue gli scatterplot rimane la scelta più immediata 
ed intuitiva, l aggiunta di hue permette di visualizzare gruppi distinti, mentre l'uso del parametro
size consente di introdurre una terza variabile continua, questo arrichisce il grafico e permette di
valutare simultaneamente 3 dimensioni di informazione

Gli scatterplot utili per indivisuare correlazioni lineari, raggruppamenti nauturali e outlier
Uso di trasparenza, palette e temi per migliorare la leggibilità, soprattutto quando il dataset è numeroso
o quando i punti si sovrappongono

Se una delle varibili è categoriale, scastterplot e regressione possono diventare poco chiari
In questi caso è consigliabile usare grafici come boxplot, violinplot, stripplot o swarmplot
che sono specificamente progettati per visualizzare distribuzioni di dati categoriali
Strumenti che sintetizzano informazioni statistiche delle distribuzioni.
il boxplot mostra mediana, quartili e outlier
il violinplot aggiunge la stima della densità dei dati evidenziando forme più complessi di distribuzione
Combinare questi grafici con stripplot o swarmplot permette di visualizzare i singoli punti sovrapposti
consente di visualizzare i singoli dati insieme ai riassunti statistici, migliorando l'interpretazione
Utile per confronti tra più categorie, per osservare pattern nascosti nelle distribuzioni.

Quando si hanno più categorie o gruppi da confrontare facetgrd permette di creare una griglia di 
grafici separati per ogni combinazione di categorie
E' possibile mappare scatterplot, boxplot, violinplot o altri tipi di grafici su questa griglia, usando
row e col per due variabili categoriale e hue per una terza variabile categoriale all'interno di ogni grafico

Grazie a facetgrid si possono esplorare dataset complessi senza creare grafici separati, confrondando
più livelli di catagorie in un'unica visualizzazione strutturata.

"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.random.seed(0)
df = pd.DataFrame({
    "altezza": np.random.normal(170, 10, 200),
    "peso": np.random.normal(65, 15, 200),
    "sesso": np.random.choice(["M", "F"], 200),
    "gruppo": np.random.choice(["A", "B"], 200)
})

#
#Esempio 1 JOINPLOT
#
#nel pannello centrale viene mostrata la relazione tra due variabili x e y (scatter plot, regplot, o un grafico kde bidimensionlae)
#mentre lungo i margini vengono visualizzare le distribuzioni indivisuali di ciascuna variabile (istogrammi o KDE, a seconda del tipo).
#Questa combinazione permette di osservare contemporaneamente la forma generale dei dati e la loro densita
#identificando tendenze lineari o non lineari e la presenza di valori estremi

sns.jointplot(data=df, x="altezza", y="peso", hue="sesso", kind="kde", fill=True, alpha=0.5)
plt.show()

sns.jointplot(data=df, x="altezza", y="peso", hue="sesso", kind="scatter", alpha=0.5)
plt.show()

#Esempio 2  COMPARISON PLOT
plt.figure(figsize=(8,5))
sns.violinplot(data=df, x="sesso", y="peso", inner=None, palette="Pastel1")
sns.boxplot(data=df, x="sesso", y="peso", width=0.2, palette="Set2")
sns.stripplot(data=df, x="sesso", y="peso", hue="gruppo", dodge=True, size=4, alpha=0.7)
plt.title("Comparison Plot combinato: violin + box + punti")
plt.show()

#Esempio 3  FACETGRID
#crea una griglia di grafici separati per ogni combinazione di categorie
g = sns.FacetGrid(df, col="gruppo", row="sesso", height=4)
g.map_dataframe(sns.scatterplot, x="altezza", y="peso", hue="sesso", alpha=0.7) #hue sesso è ridondante perchè già presente nel facet, andrebbe utilizzata un altra variabile categoriale
g.map_dataframe(sns.kdeplot, x="altezza", y="peso", levels=4, color="r", alpha=0.3)
g.add_legend()
plt.show()
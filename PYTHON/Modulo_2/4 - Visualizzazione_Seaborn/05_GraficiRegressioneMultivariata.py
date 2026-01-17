"""
Un GRAFICO DI REGRESSIONE mostra
- una relazione tra variabili numeriche
- più una linea (o superficie) che stima questa relazione
Rispondono alla domanda: 'Se X cambia, come tende a cambiare Y'
Permette di individuare relazioni tra variabili e di costruire modelli predittivi.

Correlazione=misura quanto due variabili si muovono insieme
Regrassione=metodo per modellare la relazione tra una variabile dipendente (Y)
ed una indipendente (X) ma anche più variabili indipendenti. Serve sia per previsoine
sia per spiegazione (stimare l'effetto di X su Y)

La regressione permette di individuare relazioni tra variabili e costruire modelli predittivi.
Seaborn fornisce un indieme di funzioni per rappresentare relazioni lineari e multivariate.
Capire come costruire ed interpretare consente di validare ipotesi ma anche di comunicare risultati
statici in modo chiaro.
Il punto di partenza per creare una relazione lineare è la funziona lmplot combina la potenza statistica
di regplot con la flessibilità di facet grid. 
lmplot disegna automaticamente una liena di regrwessione insieme ai punti di dati, idale per analizzare 
la relazione tra due variabili continue e la tendenza generale.
Possiamo controllare il grado delle regressione o disattivare la linea di confidenza.
Utile per valutre correlazioni lineari, per varificare se una relazione segue un modello semplice o
richiede analisi più complesse.
Spesso desideriamo analizzare come  una variabile categoriale influenzi la relazione tra due variabili 
continue, questo è possibile con heu e permette di verificare contemporaneamente più gruppi osservando
come varia la relazione tra le variabili.
Oltre a hue ho diversi stili di linea e marker per rendere il grafico più intuitivo
Utile per analizzare dati complessi dove i le informazioni categoriali influenza le variabili numeriche.
E' possibile aggiungere ulteriori informazioni visive al grafico attraverso i parametri col e row
possiamo divedere il grafico in tanti sottografici, osservando contemporaneamente l'effetto di più
variabili (esempio regione e genere)

Quando le variabili da analizzare sono 3 o più e tutte continue è possibile passare a visualizzazioni
tridimensionali. Questi variabili permette di considerare come una variabile dipendente varia in 
funzione a due altre variabili indipendenti.
Utili in contesti di modellazione predittiva, dove più fattori numerici numerici integagiscono simultaneamente
(esempio nella definizione dei prezzi di vendita) 

Esempio
x=ore lavorate
y=produttività
Il grafico dice: in media Y si muove così quando X cambia
La Relazione vedo che due variabili 'si muovono insieme'
La Regressione stima una funzione che descrive questa relazione

GRAFICO DI REGRESSIONE SEMPLICE/LINEARE (UNIVARIATA)
Ho una X ed una Y domanda: 'all'aumentare di X, Y aumenta o diminuisce?'
Visivamente sul grafico:
- punti: dati reali
- linea: stima della relazione
- spessore banda: incertezza della stima
lmplot combina la potenza statistica di regplot con la flessibilità di facetgrid, consentendo di creare grafici
complessi con poche righe di codice
lmplot disegna una linea di regressione insieme ai punti di dati mostrando l'andamento medio 
e l'intervallo di confidenza. 
Ideale per analizzare la relazione tra due variabili continue e per osservare la tendenza generale.
Ad esempio la crescita di una variabile dipendente di una funzione e di una indipendente
Possiamo controllare il grafico di regressione o la linea di confidenza.
Perticolarmente utile per valutare correlaizoni lineare e se la relazione segue un modello semplice o
richiede analisi più complesse. Spesso oltre alle variabili numeriche, desideriamo analizzare come una 
variabile categoriale influenzi la relazione tra due variabile continue, lmplot consente di fare ciò grazie
al parametro hue che differenzia i punti e le linee di regressione per categoria utilizzando colori diversi.
Permette di confrontare contemporaneamente più gruppi (come generi, regioni, fascie di eta) osservando
come varia la relazione tra le stesse variabili. Seaborn disegna una linea di regressione per ciascun gruppo
Oltre al parametro hue possiamo utilizzare diversi stili di linea e marker


GRAFICO DI REGRESSIONE MULTIVARIATA
Y è spiegata da più variabili X
esempio:
X1: carico di lavoro
X2: fascia oraria
X3: giorno
Y: Soddisfazione
Qui il grafico diventa una proiezione, perchè non puoi vedere tutto insieme facilmente
Metodi comuni (Seaborn):
1) Segmentazione (hue):
   - stessa X-Y
   - regressione separata per gruppo
2) Facet (row/col):
   - una regressione per sottogruppo
3) Superfici / contour
   - rari in contesto business
Esempio concettuale:
'La relazione tra X e Y cambia a seconda della fascia?'

Una delle caratteristiche più potenti è quella di poter aggiungere ulteriore dimensioni visive attravaerso 
i parametri col e row possiamo suddividere i grafici in sottofrafici (o facet) in base a uno o più
parametri categoriali.
In questo modo osserviamo contemporaneamente l'effetto di più variabili
L'aggiunta di dimensioni extra trasforma il grafico in una matrice informativa completa, tecnica fondamentale
per analisi esplorative e permette di visualizzare relazioni complesse.
Quando le variabili da analizzare sono 3 o più e tutte continue la rappresentazione bidimensionale può
risultare limitata, in questi casi è possibili passare alla visualizzazione 3d
Questo grafici permettono di visualizzare come una variabile indipendente varia in fuzione di due
variabili dipendenti.
La regressione multivariata 3d è utile in contesti di modellazione predittiva come pricing o analis economica
Tutta via è importante non sovracaricare la visualizzazione e scegliere colori ed angolazione che rendono
la lettura intuitiva.

Fondamentale seguire alcune buone pratiche
- assicurarsi che i dati siano puluti senza valori mancanti o anomali che potrebbero distorcere la linea di regressione
- normalizzare o scalare le variabili quando hanno ordini di grandezza diversi. 
- Conviene mantenere una palette coerenze e limitare il numero di categoria visualizzate simultaneamwente
- Controllo della trasparenza con alpha e la dimensione dei punti contribuisce ad una buona lettura
- Integrare la parte visiva con la parte descrittiva breve relazione statistica

Potente strumento per comprendere relazioni complesse tra variabili.
La forza di questi strumenti risiede nella capicità di condensare grandi quantita di dati in un grafico leggibile.
Ideal per la comunicazione dei risultati di data science
Le tecniche apprese costituiscono una base solida per analizi più avanzate e per la costruzione di modelli predittivi
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df=pd.DataFrame({
    "ore_studio":[5,10,15,8,12,7,14,9,11,16],
    "voto": [22,26,30,24,28,23,29,25,27,30],
    "corso":["Informatica","Economia","Ingegneria","Informatica","Economia","Ingegneria","Informatica","Economia","Informatica","Informatica"],
    "genere":["M","F","M","F","M","F","M","F","M","F"],
    "anno":[1,1,2,2,3,3,1,2,3,1],
})
print(df)

# REGRESSIONE SEMPLICE
sns.lmplot(data=df,x="ore_studio",y="voto",height=5,aspect=1.2,ci=95,scatter_kws={"s":40,"alpha":0.6})
plt.title("Relazione lineare tra ore di studio e voto")
plt.xlabel("Ore di studio settimanali")
plt.ylabel("Voto finale")
plt.tight_layout()
plt.show()
#ci=intervallo di confidenza del 95% attorno alla linea di regressione. 
#Quanto siamo sicuri della stima ottenuta
#scatter_kws={"s":40,"alpha":0.6} dimensione e trasparenza dei punti


#REGRESSIONE MULTIVARIATA con variabili categoriali (hue)
#ora dimostriamo quanto è forte la relazione tra ore di studio e voto
sns.lmplot(data=df,x="ore_studio",y="voto",hue="corso",height=5,aspect=1.3,ci=None)
plt.title("Regressione per corso di laurea")
plt.xlabel("Ore di studio settimanali")
plt.ylabel("Voto medio")
plt.tight_layout()
plt.show()

#dimensioni estra con col e row
#utile per analizzare relazioni complesse
sns.lmplot(data=df,x="ore_studio",y="voto",hue="corso",col="genere",row="anno",height=4)
#plt.subtitle("Regressioni multiple per genere e anno")
plt.tight_layout()
plt.show()
#otteniamo una matrici di grafici con un regressione per ognuno





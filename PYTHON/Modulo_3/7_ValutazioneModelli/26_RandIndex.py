"""
RAND INDEX

Metrica riservata al problema del clustering
Il Rand Index (RI) serve per valutare un clustering confrontandolo con una “verità a terra”. 
Senza etichette vere, il RI non ha senso. Questo già taglia metà degli usi.
Non guarda i singoli punti. Guarda le coppie di punti.

Il Rande Index è una metrica usata per valutare la qualità di un clusering quando si dispone di una 
suddivisione 'ideale' dei dati a cui fare riferimento.
Attraverso questa metrica possiamo capire quanto i gruppi trovati dall'algoritmo (cluster) siano coerenti 
rispetto alle vere appartenenze dei punti.
Il risultato è un numero compreso tra 0 e 1, dove:
    - 0 indica un disaccordo totale
    - 1 indica una corrispondenza perfetta.
Per questo motivo il RI è una misura semplice da interpretare e molto utile per confrontare diversi modelli 
di clustering.

Nei problemi di clustering non si hanno quasi mai etichette che dicono a quale gruppo ogni punto appartenga
realmente. 
Quando però le ETICHETTE SONO PRESENTI (es. in contesti didattici, o in casi in cui il dataset è già 
classificato) il Rand Index permette di verificare quanto l'algoritmo sia riuscito a rispettare questa
struttura.
Inoltre evita l'ambiguità dei nomi dei cluster, perchè considera solo la coerenza delle relazioni tra punti,
indipendentemente da come i cluster vengono etichettati.

Il Rand Index ragiona sulle coppie di punti.
Per ciascuna coppia controlla se i due punti appartengono allo stesso cluster oppure a cluster diversi,
sia nella soluzione stimata che in quella reale.
Più coppie sono classificate in modo concorde tra clustering reale e clustering calcolato, più Rand Index
risulta elevato e vicino a 1.
L'intuizione è semplice: un buon clustering deve preservare le relazioni tra i punti.

Quando si analizzano due partizioni, è possibile classificare ogni coppia di punti in quattro diverse
situazioni, in cui le prime due contribuiscono al punteggio finale, mentre le altre lo penalizzano:
    - Concordanza positiva: quando due punto sono insieme nel clustering reale e insieme in quello stimato
    - Altra forma di concordanza: quando due punti sono separati in entrambe le partizioni
    - Errore di frammentazione: quando due punti devono stare insieme ma l'algoritmo li separa.
    - Errore di aggregazione: quando due punti devono stare separati ma l'algoritmo li unisce.
La domanda è: due punto stanno insieme o separati nel clustering? e nella realtà stanno insieme o separati?
Conta quante volte sei coerente tra effettivo e clustering

Supponendo di avere un dataset D e due partizioni:
    - una è quella reale, indicata con R
    - l'altra è quella ottenuta dall'algoritmo, indicata con S
Analizzando ogni coppia di punti di D, è possibile verificare se i due punti sono assegnati allo stesso
cluster oppure a cluster diversi in entrambe le partizioni.
Si indica:
    - con a il numero di coppie che risultano insieme sia in R sia in S
    - con b il numero di coppie che invece risultano correttamente separate in entrambe

Il Rand Index si ottiene confrontando queste coppie 'corrette' con il numero totale di possibili coppie
di tutto il dataset, che corrisponde al coefficiente binomiale, dove n è il numero totale di punti.
In questo modo otteniamo un valore normalizzato compreso tra 0 e 1 che esprime il livello di somiglianza
tra le due partizioni.
In altre parole, più coppie risultano coerenti tra clustering reale e clustering stimato, più il Rand Index
sarà vicino a 1, indicando una maggiore qualità del modello

RI = (coppie corrette) / (coppie totali)

Questo rapporto normalizza il risultato nel range tra 0 e 1 facilitando il confronto tra algoritmi diversi 
o tra varie configurazioni dello stesso modello.

Immaginiamo un dataset estremamente piccolo, composto da quattro soli punti.
Potrebbero esistere sei coppie possibili tra questi punti.
Se l'algoritmo di clustering ne assegna correttamente soltanto una, perchè sbaglia la struttura dei gruppi,
allora il Rand Index sarà molto basso, vicino a 0.
Questo semplice esempio mette in evidenza quanto la metrica sia rigorosa nel valutare le partizioni.

In generale, un Rand Index vicino a 1 indica che il clustering è molto fedele alla suddivisione reale.
Valore medi, intorno a 0.5, suggeriscono che l'algoritmo ha catturato parte delle struttura, ma con errori
non trascurabili.
Quando invece il valore scende sotto 0.3, si può ragionevolmente dedurre che i cluster ottenuti non 
riflettano la realtà e che il modello vada migliorato o sostituito.

In skitlearn, il Rand Index si calcola facilmente con metrics.rand_score.
La funzione rand_score richiede due vettori: le etichette reale e le etichette predette dal clustering.
Restituisce sempre un valore compreso tra 0 e 1 che misura la similarità tra le due assegnazioni.
E' possibile, e anche consigliato, integrare il calcolo in pipeline di clustering per valutare 
automaticamente diversi modelli o parametri.
Questa funzione è particolarmente utile per confrontare clustering diversi senza dover costruire manualmente
matrici di contingenza o contare coppie concordanti/discordanti.

"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.metrics import rand_score

data=load_digits()
X=data.data
y=data.target

df=pd.DataFrame(X,columns=data.feature_names)
df["target"]=y
#print(df)
#1800 righe per 65 colonne
#target 10 classe diverse numerate da 0 a 9 

K=10
kmeans=KMeans(n_clusters=K, random_state=42)
y_pred=kmeans.fit_predict(X)

ri=rand_score(y,y_pred)
print(f"Random Index:\t{ri:.3f}")

#0.95 il clustering ha ricostruito molto bene le coppie di numeri tra etichette reali e clustering

"""
Vantaggi
Immediatezza di spiegazione e interpretazione anche a persone non epserte di ml.
E' una metrica generale, applicabile a qualsiasi algoritmo di clustering, e permette di confrontare modelli
diversi sullo stesso dataset
Poichè utilizza tutte le combinazioni di punti disponibili (tutte le coppie), fornisce una visione globale 
e non si base su misurazioni locali o parziali
Svantaggi
Nonostante la sua abilità/utilità, la metrica può essere fuorviante quando il numero di coppie cresce 
rapidamente, come accade nei dataset molto grandi: anche un piccolo errore può tradursi in un peggioramento 
significativo del punteggio.
Inoltre tende ad assegnare valori alti a clustering che creano molto gruppi piccoli o addirittura con un
solo elemento, pur essendo soluzioni poco significative.
Per questi motivi spesso si affianca ad altre metriche di valutazione.

Considerazione
Questa metrica è utilizzata quando si desidera verificare la qualità di un clustering su dati per cui
esiste una classificazione nota: ad esempio nella segmentazione di clienti già etichettati, nella 
diagnosi medica su patologie già diagnosticate, oppure nel raggruppamento di testi con categoria editoriale
predefinita.
E' lo strumento ideale per capire se sviluppi o aggiornamenti di un modello portano un reale miglioramento.

Il Rand Index rappresenta un metodo chiaro ed affidabile per stabilire quanto un clustering sia 
coerente con la realtà dei dati.
La sua forza ridiede nella semplicità di interpretazione e nella capacità di confrontare in modo equo
molte soluzioni diverse.
Tuttavia, è bene non usarlo come unica metrica: combinarlo con altre misure permette una valutazione
più completa e robusta della qualità dei cluster.
"""
"""
SOFT CLUSTERING

Il soft clustering è un approccio di apprendimento non supervisionato.
L'obiettivo è sempre raggruppare i dati in cluster.
A differenza dell'hard clustering, un dato può appartenere a più cluster contemporaneamente.
L'appartenenza viene espressa tramite una probabilità o un grado di confidenza.
Questo lo rende più flessibile e adatto a scenari complessi con confini non definiti.

Ogni punto ha un'appartenenza parziale a tutti i clusetr. Un punto potrebbe appartenere ad un clusetr A con una
probabilità del 70% e ad un cluster B con il 30%
Questo riflette la realtà di molti dati in cui i confini non sono rigidi.
L'algoritmo non impone una scelta netta, ma fornisce un quadro più completo tramite le % di probabilità
L'output è un insieme di probabilità per ogni punto e per ogni cluster.

Processo
Gli algoritmi di soft clusering lavorano per massimizzare la probabilità che i dati appartengono ai cluster.
L'algoritmo calcola la probabilità di appartenenza di ogni punto a ogni cluster.
I parametri dei cluster (come la posizione e la vicinanza/varianza) vengono aggiornati all'aggiunta di un 
nuovo punto.
Il processo si ripete finchè le probabilità non si stabilizzano.
L'obiettivo è trovare la migliore combinazione di cluster che di adatti ai dati

La probabilità è quindi il concetto chiave che distingue l'approccio hard da quello soft.
L'algoritmo assegna una 'fiducia' a ogni punto rispetto a ciascun cluster.
Un punto con una probabilità alta (es. 99%) è considerato un 'membro forte' del cluster.
Un punto con una probabilità distribuita (es. 50% e 50%) si trova al confine tra due cluster.
Questo fornisce un'informazione aggiuntiva che l'hard clusetring non può fornire, ossia definisce una sfumatura
che l'hard non può offrire.

Vantaggi
il principale vantaggio del soft clustering, è la capacità di gestire i confini sfumati.
E' più informativo perhcè fornisce il gradi di appartenenza di ogni punto al cluster.
E'più robusto agli outlier, perchè un punto anomalo non influenza un solo cluster.
Un outlier avrà una bassa probabilità di appartenenza a tutti i cluster, senza spostare il centro.
Funziona bene quando i dati non formano cluster separati in modo netto.

Svantaggi
L'interpretazione dei risultati può essere più complessa rispetto all'hard.
Invece di una semplice etichetta, si ha una distribuzione di probabilità
Gli algoritmi sono spesso più lenti dal punto di vista computazionale.
La scelta dei parametri può essere difficile
Se i cluster sono già ben separati, un approcio hard può essere più che sufficiente.

Algoritmi:
    - Gaussian Mixture Model (GMM): il più diffuso, modella i clusetr come distribuzione di probabilità.
        Per la stima dei parametri del GMM si utilizza un altroalgoritmo EM (Expectatione-Maximization)
    - Fuzzy C-Means: che usa gradi di appartenenza per raggruppare i dati, l'obiettivo è sempre lo stesso:
        trovare la struttura sottostante con un approccio probabilistico

Algoritmo GMM (Gaussian Mixture Model)
Assume che i dati siano generati da una combinazione di più distribuzioni gaussiane.
Ogni cluster è rappresentato da una gaussiana con media, varianza e peso propri.
Ogni data point nello spazio dei dati ha una probabilità di appartenere a ciascuna di queste gaussiane.
Durante l'addestramento, il modello cerca i parametri che massimizzano la probabilità complessiva dei dati 
osservati di appartenenza a ciasun cluster.
In questo modo il clusetring diventa una problema di stima statistica delle componenti che spiegano meglio
la distirbuzione

Il GMM offre una rappresentazione flessibile dei dati, capace di modellare i cluster di forma ellittica e 
con densità differenti.
A differenza di metodi come K-Means, non assume che i cluster abbiano la stessa dimensione o distribuzione.
L'approccio probabilistio consente di gestire incertezza e sovrapposizione tra gruppi, offrendo una visione
più realistica della struttura dei dati.
Grazie all'algoritmo EM, il modello si adatta progressivamente, trovando la combinazione di gaussiane che 
meglio descrive la popolazione osservata (dati).
Il risultato non è solo un insieme di etichette, ma una mappa di probabilità che rivela quanto ogni punto
appartiene ai diversi cluster.

Algoritmi EM
L'algoritmo EM è il cuore del processo di stima nei modelli probabilistici come GMM.
Si articola in due passaggi che si ripetono finchè il criterio di arresto non è incontrato (il modello converge):
    - nella fase di Expectation, il modello calcola la probabilità che ogni punto appartenza a ciascun cluster
    - nella fase di Maximization, i parametri delle gaussiane (media, varianza e peso) vengono aggiornati
        sulla base di questo probabilità ricalcolate
Ogni iterazione migliora la stima dei parametri, portando a una rappresentazione più accurata di tutti i cluster.

Esempi di utilizzo
Analisi genetica

Parametri
Come nell'approccio hard, è necessario definire il numero di cluster k a priori.
E' fondamentale scegliere il modello di distribuzione di probabilità (es. gaussiana).
Si devono impostare anche i parametri di convergenza
Le inizializzazioni iniziali dei parametri possono influenzare il risultato finale.
L'interpretazione dei risultati dipende fortemente da queste scelte.

Interpretazione dei risultati
La valutazione si concentra sulla coerenza interna e sulla separazione dei cluster.
L'interpretazione delle probabilità richiede un'analisi più approfondita
Si possono visualizzare le distribuzioni di probabilità per comprendere i risultati.
Le metriche di valutazione sono più complesse, ma l'analisi visiva rimane fondamentale.
E' importante valutare se il risultato ha senso nel contesto del problema 

Valutazione
Anche se non si sono etichette, esistono metriche per valutare la qualtà di un clustering.
Due concetti importanti sono:
    - Coesione: quanto i punti interni ad un cluster sono vicini
    - Separazione: quanto i cluster sono distanti tra di loro
Anche se nelle prime fasi può bastare  una valutazione qualitativa visiva, esistono metriche comunemente usate
per questo scopo come Silhouette Score, Random Index o Adjusted Random Index
Osservare i cluster graficamente è spesso sufficiente per capire se il risultato ha senso.


"""
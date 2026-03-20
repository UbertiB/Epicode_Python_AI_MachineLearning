"""
K-Means

K-Means è uno degli algoritmi più semplici ed allo stesso tempo più usati nel machine learning.
Serve per fare clustering, cioè per dividere dati non etichettati in gruppi simili tra loro.
Unsupervised hard clustering
Non prevede una variabile target come nella regressione o classificazione. Qui i dati non
hanno etichette. L'algoritmo cerca strutture interne nei dati.
Guardando il grafico di un dataset si potrebbero vedere che alcuni punti tendono a raggrupparsi.
Alcuni sono vicini tra loro, altri lontani. L'idea del clustering è trovare questi gruppi
automaticamente.

K-Means prende i dati e li divide in k gruppi distinti, ogni gruppo è chiamato clusetr. 
K indica il numero di cluster che si vuole ottenere.
L'algoritmo cerca i punti centrali dei gruppi, chiamati CENTROIDI, e assegna ogni osservazione 
al centroide più vicino.
L'obiettivo è minimizzare la distanza dei punti dal centro del loro cluser, questo centro è
chiamato centroide, e rappresenta la media aritmetica di tutti i punti assegnati a quel gruppo.

Il funzionamento è iterativo, Succede sempre la stessa sequenza di operazioni:
- all'inizio si scelgono k centroidi casuali. Non sono ancora buoni, sono solo punti iniziali.
  Poi l'algoritmo fa due passi che si ripetono fino a stabilizzarsi
- Primo passo: ogni punto viene assegnato al centroide più vicino, usando la distanza euclidea.
- Secondo passo: aggiornamento, per ogni gruppo si ricalcola il centroide, facendo la media dei
  punti assegnati al cluster.
  K-Means significa media dei punti del cluster.
Questi due passaggi continuano finchè i centroidi non cambiano più oppure cambiano pochissimo.
Questo metodo è detto Lloyd's algorithm ed è la versione più comune di K-Means.
Quindi l'algoritmo minimizza la somma delle distanze quadrate tra i punti e centro del cluster.
Questa quantità di chiama INERTIA in sklearn.
Alla convergenza dell'algoritmo, i punti di ciascun clusetr risulta vicini tra loro e lontani
da quelli di altri cluster.
L'algoritmo tende quindi a creare gruppi compatti e bene separati nello spazio delle feature.
Questo tipo di struttura è particolarmente efficacie quando i dati sono distribuiti in regioni
quasi sferiche.

K-Means non conosce la classi reali del dataset. Divide i dati solo per somiglianza geometrica.

Primo limite: bisogna scegliere k prima. L'algoritmo non lo sa, Spesso si usa il metodo
    dell'elbow. Si calcola l'intertia per diversi valori di k e si cerca il punto dove il 
    miglioramento rallenta.
Secondo limite: funziona bene solo con cluster sferici e simili come dimensione. Se i cluster
    hanno forme strane l'algoritmo sbaglia
Terzo limite: è molto sensibile alla scala della variabili. Se una variabile ha valori molto
    piu grandi delle altre, domina la distanza. Per questo quasi sempre si fa standarizzazione
    prima del clustering
Quarto limite: dipende dall'inizializzazione dei centroidi. Per questo sklearn esegue più
    inizializzazioni. Questo con il parametro n_init

K-Means lavora sempre su feature numeriche in uno spazio geometrico. Quando fai PCA o t-SNE 
prima del clustering stai solo cambiando lo spazio in sui i punti sono rappresentati.
Se PCA mantiene bene la sturttura dei dati, il clustering funziona ancora.

Quando aumentano le dimensioni dei dati (le feature), la distanza tra i punti perde significato.
K-Means vive proprio per distanze. Se le distanze diventano poco significative, il clustering
peggiora. Questo distrugge l'efficacia di algoritmi basati sulle distanze come: 
- K-Means - KNN -DVSCAN

Per questo motivo spesso si fa riduzione dimensionale prima del clustering (es. PCA).

La parte critica di questo algoritmo è la scelta dei centroidi iniziali, poichè influisce sul
risultato finale.
Un''inizializzazione casuale può condurre a cluster di bassa qualità o a convergenze premature.
Per questo si usa spesso il metodo k-means++, che seleziona i centroidi iniziali più distanti
tra loro.
Questo approccio ridue la probabilità di convergere a soluzioni subottimali.
Nelle librerie moderne, come skleanr, k-means++ è l'impostazione predefinita

Scelta del k
K è il parametro più importante e rappresenta il numero di cluster.
Non esiste una regola unica per sceglierlo, ma spesso si usa l'elbow method (scree plot k-WCSS)
Questo metodo analizza la variazione della funzione obiettivo WCSS al crescere di k
Il punto in cui la riduzione di WCSS rallenta visibilmente seggerisce un buon compromesso.
Esistono anche altre tecniche come il Silhoutte Score o l'Information Criterion

In Python K-means è implementato tramite la libreria sklearn.cluster.KMeans
Parametri:
    - n_clusters: imposta il numero (k) di cluster desiderati e va scelto con criterio
    - init: definisce come inizializzare i centroidi: k-means++ è raccomandato e quello di default
    - max_iter: limita il numero massimo di iterazioni per garantire la convergenza del metodo
    - n_init: stabilisce quanto inizializzazioni eseguire, scegliendo poi la migliore (defaul auto)
    - random_state: permette di replicare i risultati tra esecuzioni differenti, tipicamente 
        settato a 0 o 42
    - tol: controlla la soglia di convergenza: se i centroidi cambiano meno di tol, l'algortmo
        si ferma
    - algorithm: può essere 'lloyd' (classico e default) o 'elkan' più efficiente per cluster 
        già ben separati
    - verbose: consente di monitorare il processo di addestramento stampando le informazioni 
        intermedie.

Vantaggi:
- efficiente dal punto di vista computazionale
- facile da implementare e interpretare, perfetto per analisi esplorative
- si adatta bene a dataset di grandi dimensioni e a spazi di moderata dimensionalità
- offre una rappresentazione compatta dei dati tramite i centroidi
- può essere un ottimo punto di partenza per algoritmi più complessi
Svantaggi
- richiede di conoscere in anticipo il numero k di cluster
- è sensibile alla scelta dell'inizializzazione e può convergere a minimi locali
- non gestisce bene cluster a forma non sferica o di densità diversa
- è influenzato dalla presenza di outlier, che possono spostare i centroidi
- richiede che le feature siano su scala simile per funzionare correttamente

Conviene eseguire l'algoritmo più volte con diversi parametri e scegliere il migliore

"""
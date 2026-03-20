"""
UNSUPERVISED LEARNING

Apprendimento non supervisionato, è il secondo approccio di apprendimento automatico di Machine Learning.
Il modello impara da dati non etichettati.
Ogni dato è composto solo da input (X), cioè le sue featur ma non sono presenti le label (y), infatti
non c'è niente da predire.
L'obiettivo è quello di scoprire pattern, strutture o relazioni nascoste nei dati.
Il modello non 'impara a predire', ma organizza e comprende la distribuzione dei dati meglio di come lo 
farebbe un umano.
Viene spesso usato per esplorare dataset complessi o non strutturati.
Può essere un primo passo per generare insight utili per problemi successivi.

Non ci sono risposte corrette fornite in anticipo: il modello non ha esempi da imitare.
L'algoritmo cerca somiglianze, gruppi o associazoni tra i dati.
I risultati di questa ricerca, possono variare a seconda delle tecniche usate (es. clustering, 
riduzione dimensionale, regole associative).
L'apprendimento non supervisionato non mira a generalizzare su dati futuri ma ad estrarre struttura e
insigh latenti tra i dati.
Viene spesso combinato con tecniche supervisionate per miglioare i modelli predittivi e la loro accuratezza.

Ci sono due principali applicazioni dell'unsupervised learning:
- CLUSTERING: Usato per raggruppare dati simili in base a caratteristiche comuni, senza etichette predefinite
    L'obiettivo è scoprire strutture o pattern nascosti, identificando gruppi omogenei all'interno del dataset
    Permette di semplificare e interpretare dati complessi in modo non supervisionato.
    Utile per segmentazione cliente, analisi di mercato, rilevamento anomalie e organizzazione automatica dei dati
- ASSOCIATION: Usato per scoprire relazioni e dipendenze tra variabili in grandi insieme di dati.
    L'obiettivo è identificare regole frequenti del tipo 'se X accade, allora Y è probabile'
    Non predice valori, ma estrae conoscenza utile per descrivere comportamenti o pattern ricorrenti.
    Utile per analisi di carrelli della spesa, raccomandazioni di prodotti e analisi comportamentale.

CLUSTERING

E' una tecnica di apprendimento non supervisionato che consiste nel raggruppare i dati in insiemi, chiamati
appunto cluster, in base alle somiglianze che esistono tra i dati.
L'obiettivo è che i punti di uno stesso cluster siano simili tra loro ma diversi dai punti appartenenti
ad altri cluster.
Non vengono usate etichette note: è il modello a 'scoprire' le strutture nei dati.
E' molto usato in analisi esplorativa, segmentazione di utenti, compressione di dati e pre-processing
per altri modelli ML.

Anche nel clustering serve una funzione obiettivo per misurare la qualità dei gruppi che il modello ha trovato.
A differenza del supervised learning, non c'è un'etichetta di verità, quindi il modello non va a predire
dei risultati sulla base di valori reali, ma l'errore misura quanto sono 'compatti' i cluster e quanto 
sono separati tra loro.
Queste funzioni di perdita sono classificate tramite misure di distanza:
    - intra-cluster: quanto i punti devono stare vicini al centro del cluster
    - inter-cluster: quanto i cluster devono essere distinti e ben separati.
L'obiettivo del clustering è quello di minimizzare la variabilità interna tra i dati all'interno dello
stesso cluster, e massimizzare la separazione di tutti i cluster trovati

Esistono diverse tipologie di clustering:
    - Hard clustering (chiamato anche partizionale): ogni data point appartiene a un solo cluster, 
        algoritmi: K-Means
    - Gerarchico: si costruisce una gerarchia di cluster usando strutture dati chiamati alberi (dendrogramma)
    - Density Based: cluster formati da aree ad alta densità di punti e separati da aree a bassa densità
        algoritmi: DBSCAN
    - Soft clustering: i punti appartengono a più cluster con probabiltà diverse, 
        algoritmi: Gaussian Mixture Model

        
ASSOCIATION

L'association è una tecnica di unsupervised learning usata per trovare relazioni interessanti tra variabili
di grandi dataset.
E' particolarmente utile in analisi co-occorrenza, cerca pattern del tipo 'se X allora Y', questo pattern
viene chiamata regola.
L'esempio classico è l'analisi del carrello della spesa: capire quali prodotti vengono spesso acquistati insieme.
Non prevede etichette di output: l'algoritmo scopre regole in autonomia.
Le regole trovate possono supportare decisioni strategiche, marketing, o raccomandazioni automatiche.

L'association non usa loss function tradizionale, ma metriche per valutare la qualità delle regole:
    - Support: la frequenza con cui la regola appare nel dataset
    - Confidence: probabilità che Y sia presente quando X è presente.
    - Lift: quanto la presenza di X aumenta la probabilità di Y rispetto la caso casuale.
        L<1: associazione negativa
        L=1: associazione indipendente tra X e Y
        L>1: associazione positiva.
L'obiettivo è massimizzare supporto e confidenza, e lift > 1 indica una correlazione interessante.
Le metriche aiutano a filtrare e mantenere solo regole significative e utili.

Esistono diversi algoritmi per estrarre regole:
    - APRIORI: trova insieme frequenti di item e genera regole a partire da questi (utilizzato da Spottify)
    - ECLAT: simile ad Apriori ma usa un approccio basato su set verticali, più efficiente in certi casi
    - FP-Growth: costruisce un albero compatto (FP-tree) per trovare regole più velocemente e con meno scansioni
La scelta dell'algoritmo dipende dalla dimensione e dalla densità del dataset e dal contesto.
Queste tecnciche sono ampiamente usate in e-commerce, retail, e analisi comportamentale.
"""
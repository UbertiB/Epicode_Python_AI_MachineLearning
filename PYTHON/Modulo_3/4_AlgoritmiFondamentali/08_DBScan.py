"""
DBSCAN

DBSCAN è un tipo di clusetring basato sulla densità, raggruppa i dati in base alla concentrazione
dei punti nello spazio
I cluster vengono definiti come regioni ad alta densità e vengono separate da regioni a bassa 
densità di dati.

A differenza dell'hard clustering, un punto può rimanere isolato se non appartiene a nessuna
regione densa

DBScan costruisce i cluster cercando aree con un'elevata concentrazione di punti tutti vicini 
tra loro. Ogni grupppo rappresenta una regione dello spazio in cui i punti sono densamente
distribuiti. 
Le aree a bassa densità vengono considerate come rumore o punti anomali.
Questo permette di individuare cluster di qualsiasi forma, anche non lineari.
Il risultato è un insieme di gruppi/punti coerenti e realistici dal punto di vista della 
distribuzione dei dati.

Il nome significa Density-Based Sparial Clustering of Applicazions with Noise, clustering basata
sulla densità dei punti nello spazio.
Quindi non ragiona in termini di 'centri' ma in termini di densità locale.
Immagina un piano con punti sparsi. In alcune zone i punti sono molto vicini tra loro, in altre
sono isolati. DBSCAN dice: se una zona ha abbastanza punti vicini, allora quella zona è un cluster.

Questo porta a due vantaggi:
- può trovare cluster con forme irregolari
- identifica automaticamente rumore e outlier
Non è necessario indicare quanti cluster si vogliono

Consente di isolare il cluster dal rumore.

DBSCAN ha due parametri fondamentali:
1) eps (epsilon): è il raggio massimo entro il quale due punti vengono considerati vicini. 
   Se due punti sono entro questa distanza, sono considerati vicini, altrimenti fanno parte 
   di cluster diversi o uno di esse è outlier.
2) min_samples: numero minimo di punti necessari per formare una zona densa (numero di punti
   minimo necessari per definire un core point). 
   Se dentro il raggio eps ci sono abbastanza punti, allora siamo in una regione di cluster.

La scelta corretta di questi due valori determina la qualità e la granularità dei cluster ottenuti
Valore inadeguati possono produrre troppi cluster o, al contrario, un unico grande cluster, 
generalizzando troppo.

Geometricamente, eps definisce l'ampiezza del 'vicinato' di ciascun punto nello spazio
Se all'interno di questa sfera si trovano almeno min_samples punti, quel punto viene 
considerato denso.
Cluster diversi nascono dove esistono più regioni di densità sufficientemente alta.
Un valore di epsilon troppo piccolo porta a molti punti isolati, mentre uno troppo grande
fonde cluster separati.
min_samples controlla la sensibilità del modello alla presenza di rumore, all'interno del cluster.

La selezione di eps e min_samples è una aspetto cruciale del modello.
Un approccio comune è utilizzare il grafico delle distanze k-esime per trovare eps, 
serve a trovare il punto in cui le distanze crescono bruscamente (punto in cui i dati passano da 
zone dense a zone più sparse), questo punto, detto gomito.
Questo valore suggerisce la soglia di distanza oltre la quale le regioni diventano meno dense.
min_samples può essere scelto in relazione alla dimensionalità del dataset (spesso pari al
doppio della dimensione, quindi numero feature * 2)
Valori mal scelti possono generare cluster errati o eccessivamente frammentati.

Se trovi troppi noise: eps troppo basso
Se trovi un solo cluser gigante: probabile eps è troppo alto
Se trovi cluster frammentati: min_samples è troppo basso
Se non trovi cluster: min_samples troppo alto o eps troppo basso

Tipi di punti
DBScan classifica ogni punto in base  ha quanti vicini ha entro eps e li divide in tre categorie:
1) Core point: un punto con almeno min_samples vicini entro distanza eps. E' il cuore di un 
   cluster. Sono punti interni ai cluster, circondati da un numero minimo di vicini. Si tratta
   di un punto dentro una zona densa. E' il punto che genera il cluster, da lui parte l'estensione
2) Border point: punti che hanno meno di min_samples vicini ma dentro il raggio eps di un
   core point. Da solo non è denso abbastanza, ma è vicno a una zona densa, vicno a un core point.
   Viene assegnato al cluster, ma non espande il cluster
3) Noise point (o outlier): punto isolato, è considerato rumore o outlier. Punto che non è un 
   core point e non è border point. E' un punto isolato, che non appartiene a nessun cluster
Questo è un punto molto potente dell'algoritmo: identifica automaticamente outlier, separando
automaticamente cluser e rumore.

- Un punto è detto density-reachable da un altro se può essere raggiunto attraversando una 
  catena di core points
- Due punti appartenenti alla stessa catena fanno parte dello stesso cluster
- Questo meccanismo crea regioni continue di alta densità all'interno dei dati
- I punti non raggiungibili (density unreacheble) rimangono esclusi dai cluster principali.
- In questo modo DBSCAN costruisce gruppi coerenti senza dipendere da un numero prestabilito di
  cluster.

Processo dell'algoritmo
1. si sceglie un punto
2. si controllano i punti entro distanza eps
3. se ce ne sono abbastanza (min_samples) nasce un cluster
4. il cluster si espande includendo punti vicini
5. i punti isolati diventano rumore.
Il cluster nasce come una macchia d'olio che si espande nelle zone dense.

Confronto con K-Means
K-Means:
* devi scegliere k
* cluser sferici
* ogni punto deve appartenere a un cluster
* non gestisce bene outlier
DBSCAN:
* non serve scegliere numero di cluster
* cluster di qualsiasi forma
* rileva automaticamente rumore
* funziona male se densità dei cluster è molto diversa.

DBScan è molto usato in:
- geolocalizzazione
- analisi di anomalie
- clusering spaziale

Nel mondo ERP è utile per:
Rilevare anomalie (esempi clienti con comportamenti anomali, movimenti di magazzino anomali, ecc)

Limite importante
DBSCAN ha un problema serio, se i cluster hanno densità molto diversa può fallire.
Esempio un cluster molto denso ed un cluster molto sparso, con un solo valore eps non riesce a 
separarli bene, per questo esiste un algoritmo più avanzato chiamato HDBSCAN

In Python questo algoritmo è disponibile tramite
sklearn.cluster.DBSCAN
Dopo l'addestramento, l'attributo labels_ restituisce l'indice del cluster assegnato a ciuascun
punto.
I punti con etichetta -1 sono considerati rumore (noise point).
L'attributo core_samples_indices_ permette di identificare i punti centrali di ciascun cluster.

L'oggetto DBSCAN di sklearn riceve parametri come:
- eps: controlla la distanza massima tra due punti affinchè siano considerati connessi
- min_samples: stabilisce quanti punti servono per formare una regione densa
- metric: definisce la misura di distanza, solitamente Euclidea ma personalizzabile
- algorithm: identifica il metodo di ricerca dei vicini, come ball_tree o kd_tree

Vantaggi
- non necessita di conoscere in anticipo il numero di cluster
- gestisce efficientemente il rumore e gli outlier, escludendoli dai gruppi principali
- riesce a individuare cluster di forme irregolari e di densità variabile
- è relativamente semplice da implementare e interpretare visivamente
- si adatta bene a problemi di analisi spaziale e a dati bidimensionali
Svantaggi
- la scelta dei parametri eps e min_samples è delicata e dipende fortemente dalla scala dei dati
- in presenza di cluster con densità molto diverse, può confonderli o unirli erroneamente
- le prestazioni peggiorano rapidamente con l'aumentare della dimensionalità del dataset
- in dataset molto grandi, il costo computazionale può diventare rilevante
- L'algoritmo non fornisce una metrica diretta per valutare la qualità del clustering

"""
"""
SUPERVISED VS UNSUPERVISED

Entrambi i metodo sono potenti, ma il vero valore emerge quando vengono combinati insieme in modo stretegico.

I dati etichettati sono spesso costi da ottenere e difficili da raccogliere in quantità sufficienti
per addestrare modelli complessi.
In molti contesti reali, l'etichettatura richiede l'intervento umano o competenze specialistiche,
rendendo il processo lento, oneroso e soggetto a errori.
Di conseguenza, solo una parte ridotta del dataset risulta etichettata, mentre una grande quantità di dati
rimane inutilizzata perchè priva di etichette.
Per ovviare a questa limitazione, si può sfruttare l'enorme disponibilità di dati non etichettati per 
supportare l'apprendimento supervisionato e migliorare la capacità predittiva del modello.
Un modo efficiente per farlo è utilizzare i dati non etichettati come fase preliminare di pre-processing,
attraverso tecniche di apprendimento non supervisionato che consentono di individuare strutture, patterm
o gruppi nascosti nei dati che sono inzialmente non visibili.
L'unsupervised learning può, ad esempio, ridurre la dimensionalità, estrarre caratteristiche significative
o costruire rappresentazioni più compatte dei dati da fornire successivamente a un modello supervisionato.

In questo modo, anche senza etichette, il modello riesce a comprendere meglio la distribuzione e la struttura
dello spazio dei dati, migliorando le prestazioni complessive per problemi di supervised learning.
Negli ultimi anni si è visto che la combinazione di apprendimento supervisionato e non supervisionato
porta spesso a risultati superiori rispetto all'uso di una singola tecnica.
Esistono diversi approcci per integrare le due modalità di apprendimento per rafforzare i modelli supervisionati.

In generale è comunque possibile e spesso raccomandabile sfruttare questa combinazione per sfruttare appieno
sia la potenza predittiva dei modelli supervisionati, sia la capacità esplorativa e strutturale di quelli 
non supervisionati.
Questo approccio ibrido consente di costruire sistemi più flessibili, efficienti, e adattabili anche in
scenari in cui i dati etichettati sono scarsi, ma l'informazione non etichettata è abbondante.

Si usa il clustering (unsupervised) come freature engeniring, per assegnare un'etichtta di gruppo (esempio
cluster id) ai dati non etichettati.
L'ID del cluster (esempio cliente tipo A) diventa una nuova feature categorica X
Questa nuova feature X viene utilizzata per migliorare le prestazioni del modello di classificazione (
supervised)
Esempio:
prevedere l'abbonamento di un cliente: prima di addestrare il classificatore, si raggruppano i clienti in 
base al comportamento (tempo speso, prodotti acquistati), probabilmente utilizzando K-Means, per segmentare 
i clienti rispetto alle loro abitudini rispetto al prodotto/servizio che offre l'azienda.
L'appartenenza a un cluster ( es. 'basso utilizzo') migliora significativamente l'accuratezza delle previsioni di 
churn rate (abbandono di un cliente)

Il semi-unsupervised learning è un approccio intermedio tra l'apprendimento supervisionato e quello 
non supervisionato.
Si basa sull'idea di sfruttare una grande quantità di dati non etichettati insieme a un piccolo insieme
di dati etichettati per addestarre il modello in modo più efficiente.
Nella pratica, il modello utilizza i dati non etichettati per comprendere la struttura generale dello spazio
dei dati, individuando pattern, relazioni e gruppi naturali.
Successivamente, le poche etichette disponibili vengono usate per affinare i confini tra le classi e rendere
il modello capace di distinguere correttamente le categorie.

Questo processo consente di ottenere prestazioni simili a quello di un modello supervisionato addestrato con
molto più dati etichettati, ma con un costo molto inferiore.
Un semi-supervised learning è praticamente utile in tutti quei contesti in cui l'etichettatura è lenta,
complessa o molto costosa, come nel riconoscimento di immagini mediche, nell'analisi linguistica o nella
classificazione di documenti.
In questi casi, sfruttare anche i dati non etichettati permette di ampliare la conoscenza del modello
e di generalizzare meglio, pur partendo da un numero limitato di esempi con etichetta.

La riduzione dimensionale è una delle applicazioni più comuni dell'apprendimento non supervisionato, come
fase di pre-processing per modelli supervisionati.
In pratica si parte da un insieme di dati con molte caratteristiche o faeture, spesso ridondanti o poco
informative, e si cerca di ridurle da x a un numero minore.
Questa trasformazione permette di conserverare l'informazione più rilevante dei dati, eliminando rumore e
correlazioni inutili.
Avere un minor numero di feature significa ridurre la complessità computazionale del modello, rendendo
l'addestramento più rapido ed efficiente.

Inoltre un input più semplice, a dimensione ridotta, aiuta a diminuire il rischio di overfitting, poiche
il modello si concentra sui pattern fondamentali piuttosto che sui dettagli irrelievanti.
Il nuovo insieme di dati ridotto, indicato come X1, viene poi utilizzato come input per un modello supervisionato
ad esempio una regressione o una classficazione.
In questo modo, la fase non supervisionata prepara il terreno e migliora la qualità dell'apprendimento
supervisionato, creando un flusso integrato tra i due approcci.

Scikit-learn
Scikit-learn è la libreria di python di riferimento per il Machine Learning classico.
La sua forza è l'interfaccia uniforme e coerente per la maggior parte degli algoritmi che ne semplifica
l'utilizzo e l'integrazione di approcci ibridi.
Mette a disposizione la maggior parte degli algoritmi di ML utilizzati ad oggi.
Inoltre comprende già dei dataset 'giocattolo' per esercitarsi ad allenare dei propri modelli senza
scaricare file online.

Ogni modello, sia supervisonato che non supervisionato, segue una logica comune di tra passaggi fondamentali:
1) Inizializzazoine
2) Addestramento
3) Applicazione
Imparare a padroneggiare questo workflow standarizzato è la chiave per poter utilizzare efficacemente qualsiasi
algoritmo all'interno della libreria.
Tutti gli algoritmi (oggi della libreria) condividono un'interfaccia comune di tra metodi principali, migliorando
la coerenza del codice:
1) .fit(): è proprio l'addestramento del modello sui dati
2) .predict(): che restituisce una previsione (etichetta/cluster) post-addestramento
3) .transform(): che modifica la rappresentazione dei dati

Per la regressione, si usa l'oggettop LinearRegression in cui l'obiettivo è minimizzare il MSE. Il modello
addestrato espone coefficienti che definiscono la retta o l'iperpiano di previsione.
Per la Classificazione, si usa l'oggetto LogisticRegression:
    - .fit(X,y) utilizza sia le feature X che le etichette y
    - .predict(X):  prende un data di feature e restituisce le previsioni y
    - Dopo l'addestramento:
        - .score(X,y) calcola l'accuratezza in percentuale delle previsioni effettuate sul dataset 
        - .predict_proba() fornisce le probabilità di classificazione soft
Entrambi gli oggetti fanno parte del modulo sklearn.linear_model 

Per l'hard clustering, l'oggetto KMeans richiede il numero esatto di cluster k
    - .fit_predict(x) ritorna l'array di indici di appartenenza dei punti ai cluster
Invece DBSCAN non richiede k, ma due parametri: epc (rappresenta il raggio di ricerca, distanza massima tra 
due campioni) e min_samples (densità minima, numero minimo di campioni in un cluster)
    - .fit_predict(X) assegna ogni punto a un cluster o lo etichetta come rumore
Per il soft clustering, anche l'oggetto GaussianMixture richiede a priori il numero di cluster k
    - .predict_proba(X) restituisce la probabilità di appartenenza dei dati a ciascun cluster, offrendo
    un'analisi più ricca

"""
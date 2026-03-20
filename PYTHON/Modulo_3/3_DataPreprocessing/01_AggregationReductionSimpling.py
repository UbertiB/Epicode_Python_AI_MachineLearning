"""
AGGREGATION REDUCTION SIMPLING

DATA PREPROCESSING
La fase di preparazione dei dati grezzi per i metodi statistiche ed algoritmi di ml.
Rende i dati odonei al processo di apprendimento, nessun modello può correggere la 
qualità dei dati, che pertanto va fatta prima di passare i dati agli algoritmi.
L0bbiettivo è garantire dati idenei al processo di apprendimento.
Le tecniche si concentrano su volume, dimensione e coerenza dei dati.
Il processo mira a trasformare i dati in un formato pulito, coerente e numerico.
risolvendo problemi di volume, qualità e formato dei dati.
Migliora l'efficienta del training,
aumenta la robustessa e l'accuratezza del modello finale
migliora la capacità del modello di generalizzare su dati nuovi.
Le tecnniche principali sono:
1) Data cleaning: fase iniziale che assicura la qualità ed accuratezza dei dati, 
   consiste nel rimuovere e/o ignorare i dati mancanti e nel riempire valori vuoti
   con le loro medie o valori più probabili
2) Data Reduction: riduce la cardinalità del database per migliorare l'efficienza e
   la scalabilità, 
   consiste nella riduzione del volume, riduzione per righe (riducendo cardinalità
   e si ottiene tramite Aggregation o Sampling)
   e consiste nel Dimensionality Management, riduzione feature (ridurre la  
   carinalità delle feature tramite Feature Selection e Feature Engineering o PCA)

Le tecniche principali del data prepocessing sono:
    1) Data Transformation: fase in cui si convertono i dati in un formato numerico
    e standarizzato, idonei per l'analisi e l'elaborazione
        * Normalization: scalare dati di una colonna o di una riga, in range 0-1
        * Standarization: fondamentale per modelli che si basano sulla distanza
        (k-mean, svm, ecc) è lo scaling dei dati per portare la loro distribuzione
        a media 0 e varianza unitaria
        * Discretization: conversione di dati numerici in categorici per l'analisi
        più facile

Vantaggi
Migliore qualità dei dati, migliori performance del modello, analisi efficiente dei
dati, migliore processo decisionale

Svantaggi
Richiede tempo, richiede risorse, potenziale perdita di dati e informazioni, complessità

DATA CLEANING
Pulizia dei dati
Fondamentale per garantire qualità ed effidabilità del dataset, per dati accurati
completi e consistenti.
Il modello di ML può imparare pattern ma non può correggere errori gravi nei dati
e potrebbe imparare anche dagli errori, per questi vanno 'sistemati' prima di 
essere dati in pasto al modello.
La pulizia si concentra su tra aree principali di anomalia:
1) Completezza: valori mancanti e dati incompleti
2) Accuratezza: errori, rumore e outlier
3) Coerenza: incosistenze e ridondanze nei dati.
Ognuno dei 3 punti precedenti richiede un approccio risolutivo specifico che ora vediamo

1) COMPLETEZZA
I valri mancanti è il problema più comune e può distorcere il risultato dell'analisi
Molti algoritmi di ML non sono in grado di elaborare record con dati mancanti.
Alcune soluzioni sono:
    - Rimozione record/feature con dati mancanti: accettabile solo se la quantità
    dei dati è piccola, la rimozione non introduce distorsione nel campione di dati
    e se troppi dati non mancano. Abbiamo a disposizione 3 soluzioni:
        1) imputazione manuale
            *) possibile solo se il dataset è piccolo e il data scientist ha profonda
               conoscenza del dominio
            *) sostituzione valori mancanti con media, mediana o moda della colonna
            *) la mediana è preferibile alla media in presenza di outlier perchè robusta
               (dipende solo dalla quantità dei dati, ma non dal loro valore numerico)
        2) usare un altro modello di ML per predire il valore mancante
           * si usa la Regressione Lineare per stimare un valore numerico mancante 
             basandosi sulle altre feature del record
           * approccio più accurato ma computazionalmente più costoso
2) ACCURATEZZA
Le minaccie per l'accuratezza dei dati si divisono in tre; rumore, errore, ed outlier
    1) RUMORE: Il rumore sui dati è un errore casuale o la varianza che si introduce nel processo di
       raccolta dei dati (es errori di misurazione, data entry) che modifica il valore 
       originale dei dati
       Rende difficile per il modello distinguere i pattern reali
       L'obbiettivo è livellare (smoothing) queste fluttuazioni.
       Si usano tecniche come:
            * Binning (raggruppare i dati ordinati in bin o fasce) per livellare il rumore
            * Uso della regressione per adattare i dati ad una linea o curva, attenuando
       l'effetto delle fluttuazioni casuali
    2) OUTLIER: Gli outlier sono valori che di discostano significativamente dalla 
    maggior parte degli altri dati. Possono essere dovuti a errori di misurazione
    o eventi reali e rari (casi corner). A volte possono essere rumore da identificare
    oppure il fine della ricerca (esempio rilevamento introsioni, frodi bancarie, ecc)
    Per identificarli si usano metodi di visualizzazione come i BoxPlot
    Una volta identificati, gli outlier possono essere gestiti con diverse strategie
        * eliminare il record (se è un chiaro errore)
        * mettere un limite (limitare il valore ad una soglia prestabilita)
        * oppure usare un metodo robusto (mitigare l'impatto con funzioni di perdita come
        MAE o Huber Loss)
3) COERENZA
La terza area di competenza di un data cleaning è la coerenza del dato. Si divide
tra inconsistenze e ridondanze.
    * Le INCONSISTENZE si verificano quando i valori sono validi ma non sono coerenti tra 
    di loro o con regole di dominio o quando sono in formati diversi (esempio m o maschio)
    E' molto comune quando si fondono dati da fonti diverse (data integration) e questo
    problema si risolve rendendo i dati uniformi.
    E' necessario allineare schemi, definizioni e unità di misua, spesso usando un 
    database di metadati che aiutano a tracciare e correggere la provenienza e la validità
    delle informazioni
    * Le RIDONDANZE si verificano quando esistono dati duplicati o sovrapposti (dividendosi
    a sua volta tra record identici o feature strettamente correlate che misurano
    la stessa cosa). Si gestiscono identificando ed eliminando i duplicati, che altrimenti
    andrebbero ad aumentare il costo computazionale.

SIMILARITà E DISSIMILARITà
La similarità è una misura numerica che indica quanto due oggetti sono simili 
tra di loro.
La dissimilarità misura quanto due oggetti sono diversi.
Queste grandezze ventono misurate utilizzando metriche di distanza che si possono
applicare per confrontare due oggetti.
Sono concetti fondamentali perchè permettono di stabilire un criterio per raggruppare
(clustering) o confrontare (classificazione) i dati.
Proprietà rilessiva/identità: la distanza tra un punto e se stesso è 
Proprietà positiva: la distanza fra due punti distinti è una quantita positiva
Proprietà simmetria: la distanza tra a e b èuguale la distnaza tra b e a
Proprietà disuguaglianza triangolare: la distanza dell'ipotenusa è minore o uguale
alla distanza tra i due cateti (teorema di pitagora)
La distanza che si usa in generale è la distanza di MinKowski
"""
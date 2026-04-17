"""
K-FOLD

Suddividere il dataset in un singolo training set e un validation set può essere rischioso quando lo 
split risulta sfortunato.
In alcuni casi il validation set potrebbe non rappresentare correttamente la distribuzione dei dati.
Questo problema diventa più evidente con dataset di piccole dimensioni, dove poche osservazioni possono
influenzare molto la stima.
Per ridurre l'effetto degli split 'sfortunati' si cerca di suddividere i dati più volte in maniera
casuale.
La media delle performance sui diversi split permette di ottenere una stima più affidabile dell'errore
di generalizzazione.

K-Fold Cross Validation è una tecnica utilizzata per stimare la capacità di generalizzazione di un
modello.
Permette di mediare le performance su diversi training e validation split.
E' utile quando un singolo split potrebbe risultare 'sfortunato'.
Riduce la varianza della stima dell'errore di validazione
La procedura consiste nel suddividere il dataset in k blocchi o fold di dimensione simile

I dati vengono suddivisi in k fold di dimensione approssimativamente uguale.
In ciascuna iterazione un fold viene utilizzato come validation set e gli altri k-1 come training set.
Si addestra il modello su ogni training fold e si valuta sul corrispondente validation fold.
Alla fine si calcolano gli errori medi su tutti i k fold.
Questo produce una stima più robusta dell'errore di generalizzazione rispetto a un singolo split

L'errore di training corrisponde alla media della loss empirica sul k training fold.
L'errore di validazione corrisponde alla media della loss empirica su k validation fold.
Entrame le misure permettono di rilevare fenomeni di overfitting o underfitting.
La media sui k fold riduce l'impatto di split particolarmente sfortunati.
Consente di confrontare diversi modelli in maniera più affidabile.

Il numero di fold, k, rappresenta un iperparametro importante.
I training fold devono essere sufficientemente grandi per evitare overfitting.
I validation fold devono essere abbastanza ampi per fornire stime affidabili.
Valori comuni sono k=5 o k=10, ma la scelta dipende dalla dimensione del dataset.
Un numero maggiore di fold aumenta la precisione della stima ma richiede più calcoli.

K-Fold CV richiede un metodo per suddividere correttamente i dati in fold.
Il metodo più semplice consiste nel dividere i dati in k blocchi di uguale dimensione.
Questa soluzione funziona se i dati sono i.d.d cioè ordinati in maniera casuale.
Se i dati presentano gruppi o ordine temporale, la divisione casuale può essere inadeguata.
In questi casi si utilizzano tecniche speciali di splitting

Dataset piccoli possono generare stime instabili dell'errore.
Split sfortunati possono sovrastimare o sottostimare le performance.
Classi sbilanciate possono portare validation fold senza esempi di alcune categorie.
Dati ordinati temporalmente possono causare leakage se non viene rispetata la sequenza.
Questi problemi richiedono varianti di K-Fold adattate alla struttura dei dati.

Alcuni dataset presentano classi sbilanciate, con molto più osservazioni di alcune classi rispetto 
ad altre.
Altri dasti presentano una struttura a gruppi, con esempi correlati tra loro o raccolti insieme.
Dati temporali presentano punti raccolti in sequena, con autocorrelazioni tra osservazioni consecutive.
La divisione casuale può rompere queste strutture importanti.
Per ottenere stime affidabili si utilizzano tecniche di cross-validation che preservano proporzioni,
gruppi o sequenze. 

In scikit-learn si utilizza la classe KFold del modulo model_seleciont.
Si definisce il numero di fold tramite l'argomento n_splits, specificando quante suddivisioni creare.
Il metodo split(X) genera gli indici dei fold, che possono essere usati per separare training set e 
validation set.
Durante ogni iterazione si addestra il modello sui dati di training e si valuta sui dasti di validation
ottenuti dagli indici forniti.
Es.
    kf=KFold(n_splits=5).split(X)

    
STRATIFIED K-FOLD

Una prima variante di k-fold mantiene le proporzioni delle classi in ciascun fold.
E' particolarmente utile quando le classi sono sbilanciate.
Ogni fold ha una distribuzione simile di etichette (target) rispetto al dataset originale.
Si evita che alcune classi siano assenti in fold di validazione.
Questa tecnica permette di ottenere stime di performance più realistiche per modelli classificatori.

Gli esempi vengono raggruppati in base alla classe.
Si suddividono proporzionalmente in k fold.
Ogni fold riceve un numero equilibrato di esempi di ciascuna classe.
La procedura viene ripetuta k volte per ottenere fold diversi come validation set.
In questo modo si preserva la distirbuzione delle classi in ogni iterazione.

In scikit-learn si utilizza StratifiedKFold dal modulo model_selection
Si specifica il numero di fold desiderato tramite n_splits=k
Il metodo split (X,y) restituisce gli indici di training e validation
Questa tecnica funziona solo per problei di classificazione, in quanto richiede le etichette y.
Es.
    skf=StratifiedKFold(n_splits=5).split(X,y)
    (prende in ingresso sia feature che target)

    
GROUP K-FOLD

Group K-Fold preserva l'integrità dei gruppi durante la suddivisione in fold.
E' utile quando esempi dello stesso gruppo non devono comparire contemporanemaente in training e 
validation.
Ad esempio si applica a dati raccolti da soggetti diversi o batch sperimentali distinti.
Garantisce che non ci sia leakage tra training e validation dovuto a correlazioni tra gruppi.
Ogni gruppo intero viene assegnato a un singolo fold.

I gruppi a cui appartengono gli esempi vengono identificati
I gruppi vengono suddivisi in k fold invece dei singoli esempi
Gli esempi di un gruppo non vengono mai separati tra training e validation.
Questo garantisce indipendenza tra i fold
La tecnica riduce il rischio di overfitting dovuto a correlazioni interne ai gruppi.

In scikit-learn si utilizza GroupFold dal modulo model_selection
Si specifica n_splits=k e si forniscono i gruppi associati agli esempi.
Il metodo split (X,y,gropus) restituisce gli indici di training e validation rispetto i gruppi.
Permette di gestire dastaset con gruppi correlati senza creare leakage

Es.
    gkf=GroupKFold(n_splits=5).split(X,y,groups)
    (prende in ingresso feature, target e gruppi)

    
TIMESERIES-SPLIT

TimeSeriesSplit rispetta l'ordine temporale o dati sequenziali.
E' adatto per serie temporali o dati sequenziali.
Non mescola i dati in maniera casuale, ma crea fold successivi nel tempo
In questo modo si evita il leakage futuro-passato che potrebbe falsare la stima.
Rappresenta una generalizzazione di K-Fold per dati temporali.

Si definiscono k fold successivi in ordine temporale.
Ogni fold di training include tutti i dati fino a un certo punto nel tempo
Il fold di validation include i dati immediatamente successivi al training.
La tecnica simula scenari realistici di predizione futura.
La dimensione dei fold può essere fissa o crescente a seconda delle esigenze e dal contesto dei dati.

In scikit-learn si utilizza TimeSeriesSplit dal modulo model_selection
Si specifica n_splits=k
Il metodo split(X) restituisce indici di training e validation rispettando l'ordine cronologico.
Non richiede etichette o gruppi particolari.
Es.
    tscv=TimeSeriesSplit(n_splits=5).split(X)

    
RIEPILOGO VARIANTI.
La scelta della variante corretta dipende dalla struttura del dataset.
    - Standard K-Fold: funziona bene con dati i.i.d (indipendenti e identicamente distribuiti), 
      ed è indicato per dataset bilanciati;
    - Stratified K-Fold: mantiene  le proporzioni della classi, utile per problemi di classificazione
      con classi sbilanciate;
    - Group K-Fold: preserva l'indipendenza dei gruppi, utile quando i dati contengono gruppi correlati;
    - TimeSeriesSplit: rispetta l'ordine temporale dei dati, necessario per dati temporali e/o sequenziali

Vantaggi
Migliora la stima dell'errore su dataset complessi
Riduce il rischio di overfitting dovuto a split casuali
Mantiene le strutture importanti dei dati come classi, gruppi o sequenze
Facilita il confronto affidabile tra modelli diversi
Rappresenta una best practice consolidata nel machine learning supervisionato
Svantaggi
Più fold aumentano il tempo di calcolo necessario
Stratified o Group K-Fold richiede informazioni aggiuntive come etichette o gruppi
TimeSeriesSplit non mescola i dati, qundi fold possono avere dimensioni diverse
Alcune combinazioni complesse di vincoli non sono supportate direttamente
E' sempre necessario analizzare la struttura dei dataset prima di scegliere la CV

Importante varificare semper la distribuzione delle classi nei fold
Controllare che i gruppi non vengano spezzati tra training e validation
Nei dati temporali rispettare rigorosamente l'ordine cronologico
Testare diversi valori di k per bilanciare precisione della stima e costo computazionale
Documentare chiaramente la scelta della variante CV adottata.
"""
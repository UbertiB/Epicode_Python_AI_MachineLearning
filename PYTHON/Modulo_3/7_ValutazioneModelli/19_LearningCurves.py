"""
PERFORMANCE METRICS: LEARNING CURVES

Le learning curves rappresentano uno strumento fondamentale per valurare come cambia la prestazione di 
un modello in funzione della quantità di dati di addestramento disponibile.
Questi GRAFICI mettono in relazione la DIMENSIONE DEL TRAINING SET con una METRICA DI PERFORMANCE
come l'accuratezza o l'errore di generalizzazione.
Grazie alla loro interpretazione possiamo comprenere se aggiungere ulteriori dati si realmente
utile o se il modello ha già raggiunto il massimo del suo potenziale.
In pratica, aiutano a capire l'impatto della crescita del dataset sul comportamento globale del 
modello dal punto di vista del training.

Le learning curves consentono di identificare problemi strutturali nell'addestramento del modello,
come under/over fitting.
Analizzando queste curve è possibile capire se servono più dati, se è necessario cambiare modello, 
o modificarne gli iperparametri.
Riducono quindi il rischio di tentativi a caso duranto lo sviluppo del modello.
Sono essenziali per ottimizzare tempi e risorse nella fase di training, evitando di sprecare tempo su
dataset enormi quando non è necessario.
Permettono anche di confrontare strategie di pre-processing e scelte delle feature con un riscontro
visivo immediato.

Tipicamente una learning curve mostra due linee:
    - una per la performance sul TRAINING set
    - una per la performance sul VALIDATION/TEST set.
Man mano che aumentano i dati, la curva del training tende di solito a peggiorare leggermente, perchè
il modello ha più esempi da rispettare.
La distanza geometrica tra le due cure è l'indicatore principale da osservare per la diagnosi sul 
comportamento del training.
Al contrario, la curva di validazione migliora, perchè più dati aiutano la capacità di generalizzazione.
Quando entrambe le curve vanno a convergere, diminuisce quindi la loro distanza, anche il modello sta 
convergendo, cioè sta raggiungendo la migliore performance ottenibile con quella configurazione.

Per realizzare una learning curve occorre definire una progressione crescente di DIMESIONI del dataset
di addestramento.
Per ogni sottoinsieme SI ALLENA UN MODELLO DA ZERO e si misura la performance anche su dati non visti.
Ripetendo questo processo si ottengono coppie (dimensione dati, performance) che formano la curva.
E' un procedimento computazionalmente costoso, perchè richiede molti addestramenti distinti.
Tuttavia fornisce una visione estremamente chiara e pratica delle potenzialità dei dati.

La scelta del modo in cui campionare i dati, influenza l'affidabilità della curva.
Serve una STRATEGIA DI SAMPLING CASUALE che eviti gruppi di esempi troppo simili e quindi misure distore.
Occorre inoltre fissare un NUMERO DI STEP che sia rappresentativo della crescita reale del dataset.
Più step significano curve più dettagliate ma anche più costi computazionali.
La stabilità del campionamento garantisce una maggiore coerenza dei risultati ottenuti in fasi ripetute.

Quando la dimensione del training è molto bassa, il modello tende ad imparare poco e male, con 
performance instabili.
La curva del training è inizialmente elevata perchè il modello può memorizzare pochi esempi, ma quella 
di validazione è molto bassa.
In questa regione delle curve, l'errore varia molto, perchè bastano piccole variazioni di dati 
per cambiare drasticamente le performance del training.
E' possibile osservare una forte varianza nel modello e una stima poco affidabile della sue reali 
capacità.
Questa fase della curva è utile per capire quanto il modello sia sensibile al numero iniziale di campioni

AGGIUNGENDO più dati il modello si trova ad apprendere strutture più generali e meno legate ai singoli
casi di esempio.
La performance su validation migliora stabilmente e la curva del training scende leggermente.
Se il modello ha sufficiente capacità rappresentativa, entrambi gli indicatori convergono a una zona
stabile.
In molti casi più dati portano benefici consistenti, specialmente in dataset complessi o rumorosi.
Si può valutare se investire nella raccolta di nuovi dati sia una scelta sensata, per rendere il 
modello più performante.

UNDERFITTING

Significa che il modello 'memorizza' non generalizza
Train: basso (esempio 70%)
Validation: basso (esempio 68%)
Modello troppo semplice, non capisce i dati
Se entrambe le curve risultano piuttosto basse e vicine, significa che il modello non riesce ad
apprendere la struttura del problema nei dati.
Anche aumentando i dati di training il miglioramento è minimo e si rimane in una zona di scarse 
prestazioni.
Questo fenomeno è tipico di modelli o sono troppo semplici o sono mal configurati.
In questo caso non serve aggiungere dati, ma cambiare modello o applicare feature engineering o
il feature selection.
La learning curvers mostrano chiaramente quando serve una maggiore complessità computazionale.

Un modello presenta underfitting se non riesce a catturare la complessità del problema, cosa che 
accade quando le curve mostrnao un errore elevato sia sul training che sul validation set.
Per AUMENTARE LA CAPACITà DI APPRENDIMENTO affinchè le curve mostrino un miglioramento progressivo
con più dati:
    - aumentare la COMPLESSITà DEL MODELLO con algoritmi più espressivi (es. reti neurali)
    - arricchire l'input con NUOVE FEATURE utili (feature engineering o transformation)
    - RIDURRE LA REGOLARIZZAZIONE presente, perchè potrebbe limitare eccessivamente la flessibilità
    del modello

In caso di overfitting posso avere le due curve in due situazioni distinte:
    - curva validation molto alta
    - curva training molto basse
    le due curve rimangono alla stessa altezza e non si avvicinano mai
Un altro caso di overfitting è quando la curva della loss del validation set non aumenta mai, in questo
caso il modello non sta imparando da nuovi dati

OVERFITTING

Come diagnosticare un caso di overfitting
Train score: molto alto (es. 99%)
Validation: molto più basso (es. 80%)
Grande distanza tra le curve
Il modello 'memorizza' non generalizza
Se il modello presenta overfitting, la curva di training rimane molto più alta di quella di validazione.
Ciò indica che il modello sta 'memorizzando' i propri dati invece di generalizzare.
In questo caso aggiungere più dati (aumentare il training set) potrebbe aiutare a ridurre la distanza, 
ma spesso e volentieri non è sufficiente.
Potrebbe essere necessario, invece, applicare regolarizzazione o ridurre la complessità del modello.
La learning curves rendo questa criticità evidente in modo rapido ed intuitivo.

Se le curve mostrano un'alta accuratezza sul training set ma prestazioni scarse sul validation set,
il modello ha appreso troppo i dettagli del training e non è in grado di generalizzare.
In questo scenario aggiungere ulteriori dati può essere molto vantaggioso, perchè aumenta la diversità
degli esempi e riduce la distanza tra le curve.
E' inoltre utile applicare regolarizzazione, come L1/L2 o dropout, per limitare la complessità effettiva
del modello.
Se possibile, conviene semplificare l'architettura o ridurre il numero di parametri, così da evitare 
memorizzazione superflua.
Lo scopo è avvicinare le due curve (ridurre la distanza) e ottenere prestazioni più stabili su dati
mai visti.

In caso di overfitting la curva di validation rimane più in alto (rispetto alla curva di train) con 
l'aumentare dei dati, e quella di train va sempre a perdere.

GOOD GENERALIZATION

Come diagnosticare un caso di buona generalizzazione
Esempio train 93% e validation 92%
Modello equilibrato, buona generalizzazione
Poca distanza tra le curve
Quando le due curve convergono stabilmente, ciò significa che il modello ha raggiunto il limite della 
sue capacità con quei dati.
Ulteriori dati possono portare vantaggi minimi o nulli.
E' il caso ideale perchè indica equilibrio tra variabilità e generalizzazione.
La convergenza guida le scelte per evitare sprechi di tempo nell'addestramento futuro.
Questo comportamento è tipico dei modelli ben progettati con dataset sufficientemente ampio

Le due curve convergono (si toccano)

Diagnosi

La forma delle learning curves è un ottimo strumento diagnostico qualitativo delle strategie di 
machine learning.
    - Un grande divario tra le curve implica overfitting
    - Due curve basse suggeriscono undefitting
    - Una convergenza lenta suggerisce potenzialmente scarsa efficienza del modello
    - Forme irregolari indicano forte varianza e dati insufficienti.
Grazie a questo strumento possiamo prendere decisioni motivate e non casuali sulle ottimizzazioni.

Asse X: numero di dati di training
Asse Y: performance (accuracy, errore, ecc)
Ho sempre due linee: 
    1) training score: quanto il modello è bravo sui dati di train
    2) validation score:_quanto generalizza sui dati nuovi

scikit-learn tramite learning_curve
La funzione richiede come input
    - un modello estimator
    - i training set X e y (tranne per clustering)
La n_jobs è possibile sfruttare la paralelizzazione per eseguire i vari addestramenti su più core,
riducendo i tempi necessari.
I parametri train_sides, cv, e shuffle determinano profondamente la qualità statistica dei risultati
ottenuti.
Una buona configurazione di questi elementi garantisce curve più lisce e interpretabili, utili per
diagnosticare correttamente i problemi del modello.
Il parametri cv, controlla la strategia di validazione incrociata e, aumentando il numero di fold, si
ottine una stima più stabile al costo di maggiore tempo computazionale.
trin_sizes stabilisce in quali punti misurare le prestazioni del modello, e una suddivisione ben 
distribuita permette di osservare correttamente il trend di apprendimento.
Attivare shuffle=True prima di effettuare le suddivisioni è fondamentale per evitare strutture anomale
nei dati che possono alterare le stime.
Dopo aver raccolto le prestazioni, si visualizzano le medie e le deviazioni standard per rappresentare
anche l'incertezza statistica dell'apprendimento.

Vantaggi
Capacità di mostrare in modo immediato e visivo se i problemi del modello dipendono dai dati o dalla 
sua struttura interna.
Guidano interventi mirati evitando sprechi di risorse
Permettono di pianificare con precisione l'espansione del dataset
Svantaggi
Costo computazionale elevato per la generazione: si deve addestrare molto volte lo stesso modello.
Le stime possono risultare variabili se:
    - se i dati sono pochi
    - il campionamento non è progettato correttamente

Considerazini
Le learning curves dovrebbero essere introdotte nelle prime fasi del workflow quando si esplorra il 
comportamento del modello e si vuole evitare di investire tempo in soluzioni improduttive.
Sono particolarmente utili quando si sospettano problemi di generalizzazione, come undefitting e
overfitting, ma anche quando dobbiamo valutare se la raccolta di più dati porterebbe reali benefici.
Permettono una revisione strategica delle scelte operative, dal tipo di modello, alla complessità
computazionale delle techiche adottate.
La corretta interpretazione dei risultati è cruciale per capire se servono più dati, un nuovo modello,
modifiche nella tecniche di regolarizzazione o applicazioni di feature engineering.
Per ottenere buoni risultati è fondamentale scegliere metriche coerenti e valutare eccuratamente la
statistica delle curve.
In definitiva, le learning curves rappresentano un riferimento costante per guidasre l'intero ciclo
di sviluppo del Machine Learning dalla prototipazione alla produzione.


"""

"""
Hyperparameters Tuning

Hyperparameters Tuning è il processo con cui scegli i parametri che non vengono appresi automaticamente 
dal modello.

Il modello impara i PARAMETRI, mentre gli IPERPARAMETRI sono da scegliere
Per esempio in Logistic Regression imposto C e penality (questi sono iperparametri) mentre il modello
trova i pesi (coefficienti) delle varie features (questi sono parametri)
Con gli iperparametri decide le regole del gioco, il modello trova i valori di parametri migliori 
dentro le regole dati dagli iperparametri
Esempio
    LogisticRegression(C=1)
    Stai dicendo quanto può adattarsi il modello ai dati con l'iperparametro C (c basso: modello 
    semplice; c alto: modello complesso)
    Il modello trova i coefficienti migliori per minimizzare l'errore.
    y=ax+b
    a,b sono parametri che trova il modello
    tipo di modello (lineare) è un iperparametro
NON imposti direttamente il comportamento finale del modello, imposti quanto il modello è libero
di imparare
Nel mondo reale sia abituati a controllare tutto, nel ML invece controlli solo indirettamente

GLI IPERPARAMETRI DEFINISCONO IL COMPORTAMENTO DEL MODELLO, MENTRE I PARAMETRI VENGONO APPRESI
AUTOMATICAMENTE DURANTE IL TRAINING

Serve il tunning perchè ogni dataset è diverso da tutti gli altri e gli stessi parametri danno 
risultati diversi

Ci sono diversi modi per fare TUNNING

1) GRID SEARCH: Provi tutte le combinazioni
    from sklearn.model_selection import GridSearchCV
    param_grid = {"model__C": [0.1, 1, 10, 100]}
    grid = GridSearchCV(pipeline, param_grid, cv=5)
    grid.fit(X, y)
    print(grid.best_params_)
2) RANDOM SEARCH: Provi combinazioni random
    Più veloce su dataset grandi
3) BAYESIAN OPTIMIZATION: Non provi a casi ma impari dalle prove precedenti

L'HYPERPARAMETER TUNNING CONSENTE DI OTTIMIZZARE LE PRESTAZIONI DEL MODELLO INDIVIDUANDO LA 
COMBINAZIONE DI IPERPARAMETRI PIU' ADATTA AL DATASET

Con Hyperparameters Tuning vengono provate tante combinazioni di iperparametri per scegliere quella che
funziona meglio sui dati.
Non è 'provare a caso' è un ciclo strutturato

Nel ML, il comportamento finale di un modello dipende non solo dai dati e dai parametri appresi, ma
anche dagli iperparametri. Questi valori controllano aspetti come la complessità del modello, 
il numero di iterazioni o la regolarizzazione.
Una scelta non adeguata può portare a modelli inutili e sovradimensionati.
Il tuning degli iperparametri è quindi un passaggio fondamentale per ottenere prestazioni ottimali.
L'obiettivo è trovare la configurazione che massimizza la generalizzazione su dati non visti.

Gli iperparametri sono valori decisi a priori e non vengono appresi direttamente dall'algoritmo durante
l'addestramento.
Esempi comuni includono il numero di alberi in un Random Forest, il learning rate un una rete neurale
o il parametro C in una SVM.
In scikit-learn questi vengono passati come argomenti al costruttore dell'estimatore.
La loro scelta influisce direttamente sui bias-variance trade-off del modello.
Per questo vanno analizzati e ottimizzati in modo sistematico.

La configurazone predefinita degli algoritmi raramente è la migliore per una datasetreale.
Senza un tuning si può ottenere un modello fortemente undefittato o eccessivamente overfittago.
Ricercando nello spazio degli iperparametri si cerca di massimizzare le prestazioni di validazione,
che fungono da indicatore della capacità di generalizzazione del modlelo.
Un tuning corretto permette di sfruttare al massimo la potenzialità del modello.
Questo processo garantisce sia maggiore accuratezza che maggiore stabilità nelle predizioni.

Per valutare gli iperparametri non basta guardare le perfomance sui dati di training, ma serve un metodo
di validazione.
Si usa quindi la validation set o più spesso la cross-validation, che fornisce una stima più robusta.
Ogni configurazione viene testata su più suddivisioni del dataset, riducendo il rischio di effetti casuali.
La metrica di valutazione usata pidende dal problema: può essere l'accuracy, F1-score, o AUC.
L'obiettivo è sempre migliorare la perfomance sui dati mai visti.

VALIDATION CURVE
La prima di queste tecniche per mettere in atto il tuning degli iperparametri è la ValidationCurve
Una Validation Curve mostra come variano training score e validation score al modificarsi di un singolo 
iperparametro.
La sua analisi fornisce indicazioni immediate su quando il modello è troppo semplice o eccessivamente 
complesso.
Prendo un imperparametro lo cambio, per ogni valore dell'iperparametro alleno il modello.
E misura due cose:
    1) Training score: quanto il modello è bravo su dati che ha usato per imparare (fit sui dati di 
        training, score sugli stessi dati)
    2) Validation score: quanto il modello è bravo su dati che NON ha mai visto (fit sui dati di 
        training, score su validation set)
Un valore ottimale si ottiene quando le due curve risultano bilanciate e abbastanza alte.
La curva deve essere letta anche in combinazione con metriche quantitative aggiuntive.
E' uno strumento diagnostico essenziale per capire la sensibilità del modello a un parametro specifico 

UNDERFITTING
Training score: BASSO
Validation score: BASSO
Se entrambe le curve presentano valori bassi, il modello non sta imparamendo abbastanza.
Il modello è troppo semplice, non capisce. Esempio decision Tree profondità=1
In questo caso di parla di underfitting, e ciò indica che l'iperparametro va regolato per aumentare
la capacità del modello
Può essere utile anche aumentare la complessità, come più feature o profondità maggiore di un 
albero decisionale.
Si osserva una distanza ridotta tra le curve ma a livelli di performance insoddifacenti.
La validation curve aiuta a individuare esattamente il range in cui il modello è troppo debole.

OVERFITTING
Training score: ALTO
Validation score: BASSO
Il modello ha imparato troppo bene i dati di training, perdendo la capacità di generalizzazione.
Esempio decisione tree profondita=50
Questo è sintomo di overfitting.
In tal caso l'iperparametro va regolato per ridurre la complessità o aggiungere regolarizzazione.
La validation curve permette di identificare il punto in cui il modello inizia a degradare.
Lo scopo è minimizzare la distanza tra training e validation curve mantenendo alte prestazioni

SITUAZIONE BUONA
Trainig score: ALTO MA NON PERFETTO
Validation score: ALTO E VICINO A TRAINING
Il modello è ben equilibrato

Tipicamente Training curve scende leggermente e Validation curve sale e poi scende. Il punto giusto è dove
la validation è massima. Inizialmente la distanza geometrica tra le curve di trainig e validation, man mano
che si aumenta la grandezza del training set le due curve convergono e si arriva in un momoento di good fit
cioè il momento in cui il modello riesce a raggiungere una buona generalizzazione.

Una validation Curve analizza un solo iperparametro per volta e ignora possibili interazioni con altri parametri.
Per questo le conclusioni potrebbero essere parziali se il modello ha molti controlli.
Inoltre la cross-validation per ogni valore può essere computazionalmente molto pesante.
Serve una scelta intelligente dei valori da testare, evitando livelli inutili.
Nonostante ciò rimane uno strumento prezioso di diagnosi.

Per analizzare l'effetto di un singolo iperparametro sulle prestazioni in scikit-learn si può utilizzare la
funzione model_selection.validation_curve che calcola contemporaneamente gli score di training e di validazione
tramite una procedura di cross-validation.
E' necessario specificare:
    - estimator: il modello da analizzare
    - param_name: il nome esatto dell'iperparametro da variare
    - param_range: una lista di possibili valori che può assumere il parametro.
La funzione restituisce due matrici contenenti gli score per ciascuna fold della cross-validation, una 
per il training e una per la validazione, che devono essere mediati e accompagnati dalla deviazione standard
per una rappresentazione grafica chiara e informativa.
Una pratica comune consiste nel visualizzare i risultati tramite un grafico che pone sull'asse delle ascisse (X)
i valore dell'iperparametro e sull'asse delle ordinate (Y) gli score, così da facilitare l'identificazione di
situazioni di underfitting (score bassi e vicini) o overfitting (score molto diversi tra training e validation)

Vantaggi
Fornisce una stima della qualità del fitting
Analisi grafica dei risultati immediata e intuitiva
Valutazione delle performance più robusta rispetto a una semplice singola suddivisione traing-test.
Svantaggi
Analizza un solo iperparametro per volta.
Non tiene conto delle iterazioni tra più parametri che a volte possono influenzarsi a vicenda.
Costo computazionalmente elevato, specialmente se il modello è costoso.

GRID SEARCH

Un'atra tecnica per fare il tuning degli iperparametri chiamata GRID SEARCH
Grid Search prova tutte le combinazioni possibili degli iperparametri e sceglie quella con performance
migliore (di solito cross-validation)
Grid Search non è inteliggente, è sistematico, funziona perchè prova tutto.
Hai un modello con più iperparametri
Esempio Random Forest:
    - n_estimator: numero di alberi
    - max_depth: profondità
    - min_samples_split: quando splittare
Non sai i valori giusti, quindi crei una griglia e provi tutte le possibili combinazioni
Per ogni combinazione Grid Search 
- allena il modello
- fa cross validation (es. 5 fold)
- calcola score medio
- salva il risultato
Alla fine prende la combinazione con score migliore.
Scikit-learn restituisce automaticamente sia il migliore score che il modello ri-addestrato con la configurazione
ottimale.
La valutazione combinata di parametri multipli permette di trovare la configurazione ottimale.
Il problema diventa una ricerca guidata in uno spazio spesso molto grande.
Il tuning corretto richiede equilibrio tra costo computazionale e qualità della soluzione trovata.
E' particolarmente utile quando si conosce già un intervallo ben preciso da esplorare.
E' uno dei motodi più utilizzati nelle pipeline di tuning automatico.

GridSearchCV è l'implementazione ufficiale in scikit-learn del Grid Search con cross-validation integrata.
Il parametro param_grid definisce la griglia degli iperparametri tramite un dizionario Python
cv stabilisce il numero di fold
Il parametro n_jobs permette di parallelizzazione per ridurre i tempi di calcolo.
La metrica è controlata dal parametro scoring, adattabile a classificazione o regressione.
L'addestramento finale del modello migliore è automatico se si imposta refit=True

Vantaggi
Semplicità di configurazione e interpretazione anche per chi è alle prime armi
Offre una ricerca sistematica e completa nello spazio definito.
Garantisce il miglio modello possibile nei limiti della griglia.
Produce risultati ripetibili
E' lo standard per benchmark e sperimentazioni accademiche.
Svantaggi
Costo computazionale proporzionale al numero di iperparametri.
Richiede una buona conoscenza preliminare del range sui cui cercare i valori ottimali
Poco efficiente quando la funzione è piatta in molte regioni dello spazio dei parametri.
Per modelli complessi o dataset molto grandi diventa difficile da applicare.

RANDOMIZED SEARCH

Un'atra tecnica per fare il tuning degli iperparametri chiamata RANDOMIZED SEARCH
Con Radomized Search testa solo un numero limitato di combinazioni estratte da distribuzioni predefinite
degli iperparametri.
Invece di provare tutte le combinazioni di iperparametri, ne prova solo alcune scelte casualmente.
Quindi Grid Search è eseustivo, prova tutte le possibili combinazioni, mentre Random Search fa un campionamento
prendo solo N combinazioni a caso.
Questo riduce notevolmente i tempi.
E' particolarmente efficace quando non si conoscono a priori i range più promettenti da passare a Grid Search.
Spesso si usa come primo step prima di una Grid Search più mirata

Oltre a questi 3 metodi standard, esistono altri approcci più sofisticati BAYESIAN SEARCH, GENETIC ALGORITHMIS e
HYPERBAND.
Questi algoritmi cercano di modellare la funzione di costo per scegliere in modo più intelligente quale 
combinazione testare dopo in seguito.
Sono molto efficaci quando il costo computazionale dell'addestramento è elevato.
Offrono un compromesso tra esplorazione e sfruttamento dello spazio dei parametri.
Sono disponibili in librerie dedicate come Optuna, Ray Tune e Scikit-Optimize

Il Tuning degli iperparametri è una fase necessaria in qualsiasi progetto di Michene Learning, che voglia 
raggiungere performance competitive.
Va però bilanciato con il costo computazionale, specialmente quando si lavora con dataset molto grandi.
Gli strumenti come Validation Curve, Grid Search e Randomized Search devono essere utilizzati in modo strategico,
pertendo dall'analisi diagnostica fino all'ottimizzazione finale.
La scelta della metrica e della strategia di validazione influenzano pesantemente il risultato.
Con un workflow ben progettato, si ottengono modelli migliori e decisioni più affidabili.





"""
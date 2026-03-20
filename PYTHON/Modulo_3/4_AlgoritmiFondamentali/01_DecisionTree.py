"""
DECISION TREE

Un DecisionTree è uno degli algoritmi più intuitivi del machine learning. Funziona esattamente 
come un albero decisionale logico: una sequenza di domande che divede i dati fino ad 
arrivare a una previsione.
fai una domanda, poi un'altra, ed un'altra ancora, così via, finchè arrivi alla causa.
Imita il ragionamento umano, passo dopo passo con se-allora.
Un Decision Tree serve a separare i dati in gruppi sempre più omogenei fino a poter fare una
previsione. La parola 'divisione' significa prendere il dataset, spezzarlo in due gruppi usando
una regola. Se succede questo vai di qui, altrimenti vai di la, ecc
Il modello deve scegliere la variabile e la soglia, due decisioni:
1) quale variabile usare: esempio uso la colonna eta
2) quale valore della variabile usare come taglio: esempio 30
Eta>30?
Ogni scelta crea una divisione. Il modello prova molte possibilità e sceglie quella che sapara
meglio i dati
L'algoritmo di Decision Tree costruisce automaticamente le domande migliori
Il modello prende ogni feature e prova a usarla per dividere i dati. Per ogni colonna prova
diverse soglie. Ogni soglia crea due gruppi, e su ognuno calcola quando sono 'puri'. Se un
gruppo contiene solo 'si' o solo 'no' sono puri=0. Il modello sceglie la divisione con 
impurità più bassa. Confronta tutte le divisioni possibili su tutte le colonne. La migliore
diventa il suo albero decisionale. Questo processo si chiama Recuersive Binary Splitting (il 
dataset viene continuamente diviso in due)

Un albero è composto da 3 elementi:
1) Nodo radice (root): è il primo punto dove il dataset viene diviso
2) Nodi interni (decision nodes): contengono una condizione logica su una variabile
3) Foglie (leaf nodes): sono il risultato finale, una classe o un valore numerico.

I Decision Tree possono gestire punti dati con variabili numeriche e categoriche, rendendoli 
flessibili. Le etichette possono essere arbitrariamente numerate: ciò che conta non è il numero
ma la classe stessa.

Bisogna distinguere tra tipo di target (y), cioè cosa vuoi prevedere, e tipo di feature (x) 
cioè il tipo di colonne.

Classificazione in base al tipo di target (continua o discreta) essistono due categorie 
principali di decision tree:
1) Decision Tree per classificazione (DecisionTreeClassifier): prevede una classe. 
   Esempio email: spam/non spam. 
   Algoritmo: sklearn
2) Decision Tree per regressione (DecisionTreeRegressor): prevete un valore numerico. 
   Esempio prevedere il prezzo di una casa. 
   Algoritmo sklearn

Scikit-lean non accetta feature con tipo stringhe direttamente, ma vanno trasformate con encoding, 
esempio con one-hot encoding.
Non tutti i Decision Tree richiedono encoding, algoritmi moderni gestiscono categorical feature
nativamente. 
Questi algoritmi sono:
- CatBoost: molto usato usa dati aziendali
- LighGBM
- XGBoost (parzialmente)

I Decision Tree non  hanno bisogno di scaling, non confrontano più categorie tra di loro,
quindi standarizzazione, normalizzazione, e log scaling non servono. 

La rappresentazione grafica dei Decision Tree è quella di un flow-chart, con nodi decisionali,
rami e  foglie.

Tutti gli algoritmi di Decisoin Tree utilizzano una strategia greedy cioè ad ogni passo 
selezionano l'attributo 'migliore' per lo split, in modo locale, non cercano un ottimo globale:
la decisione è presa nodo per nodo, basata su una misura di purezza.
Questo significa che l'algoritmo sceglie la divisione migliore in quel momento, senza sapere
se quella scelta porterà alla soluzione migliore alla fine dell'albero. 
Una decisione globale significherebbe provare tutte le possibile strutture di albero e scegliere
qualla che da il risultato migliore alla fine. Questo è computazionalmente impossibile

Questo approccio greedy, rapito e locale, consente di costruire alberi in tempi brevi, 
ma richiede attenzione al rischio di overfitting e non garantisce la soluzione ottimale globale.

Come si risolve questo limite dato dall'approccio greedy?
Nel machile learning moderno si usano molti alberi insieme, questo ridue il problema delle
decisioni locali.
I metodi più importanti sono: 
1) Random Forest: costruisce centinaia di alberi su dataset leggermente diversi e poi fa la media
2) Gradient Boosting: costruisce alberi in sequenza, ogni albero cerca di correggere gli 
   errori del precedente

Scikit-learn offre la funzione plot_tree che serve per visualizzare graficamente la struttura
dell'albero. E' utile per capire come il modello prende decisioni e quali feature contribuiscono
maggiormente agli split.
Ogni nodo mostra la condizione di divisione, il numero di campioni e la distribuzione delle 
classi o dei valori.
Parametri:
- filled=True colorano i nodi in base alla purezza o al valore medio della foglia.
- feature_names e class_names permettono di rendere la visualizzazione più leggibile e informativa

Molti parametri controllano la complessità e la profondità del modello, prevedendo l'overfitting:
L'albero tende naturalmente a crescere troppo e a memorizzare i dati. I parametri servono
quasi sempre, a controllare la crescita dell'albero:

- max_deph: limita la profondità massima dell'albero, cioè il numero di livelli, 
  valore raccomandato da 3 a 10 per dataset medi
  Livello 0 root
  Livello 1 split
  Livello 2 split
  ...
  Livello ultimo foglie
  Se non si limita la profondità (max_deph=None) l'albero cresce finchè separe quasi perfettamente
  i dasti con il rischio di overfitting
- min_samples_split: impone un numero minimo di campioni/osservazioni per fare uno split,
  tipo valore 2-10
  significa se un nodo contiene meno di n campioni allora non può più dividersi, serve per
  evitare divisioni su campioni troppo piccoli
- min_samples_leaf: stabilisce il numero minimo di campioni in una foglia,
  consigliato 1-5 per generalizzazione migliore
- max_features: regola quante feature vengono considerate per ogni split, 
  spesso impostasto a sqrt o log2
  max_features=None usa tutte le colonne
- random_state: assicura la riprocucibilità del modello, utile per fare confronti o esperimenti
- splitter: definisce la strategia di divisione, può avere due valori:
  - best: sceglie lo split più informativo, prova tutti gli split possibili
  - random: introduce casualità, prova split casuali tra quelli disponibili
- criterion: serve per decidere come valutare la qualità di una divisione.
  Per la classificazione puoi usare:
    - gini
    - entropy
    - log_loss

Il tuning di questi parametri è fondamentale per ottenere un equilibrio tra accuratezza e 
interpretabilità: albero troppo profondi tendono a sovra-adattarsi (overfitting), 
mentre alberi troppo limitati perdono capacità predittiva.

DECISION TREE CLASSIFICATORE

DecisionTreeClassifier: usato per problemi di classificazione supervisionata, dove il target
è discreto/categorico (cioè appartiene a un insieme finito di classi).
Prevede una classe
Se il fatturato lo divido in classi (esempio basso, medio, alto) anche label numeriche possono
essere risolte con una classificazione e quindi DecisionTreeClassifier
Un decision Tree per classificazione è un modello che utilzza una struttura ad albero per 
dividere i dasti in base a condizioni sulle feature.
Ogni nodo interno rappresenta un test condizionale su un attributo:
    Esempio eta>30? o colore=rosso? 
Ogni ramo di ogni nodo rappresenta il risultato del test (vero/falso, oppure le possibili 
categorie)
Ogni foglia finale rappresenta una classe assegnata ai campioni che vi giungono
In sostanza, è un modello composto solo da istruzioni condizionali, senza l'utilizzo di 
funzioni troppo complesse
parametri:
    - criterion: serve per decidere quale divisione è migliore, può essere:
        - gini: impurita di Gini
        - entropy: guadagno informativa, 
    - Entropy tende a produrre alberi più bilanciati, ma gini è più veloce o spesso simile
        in prestazioni
    - class_weight: permette di bilanciare classi sbilanciate assegnando più importanza a 
        quelle moeno rappresentate
    - max_leaf_nodes: impone un numero massimo di foglie per controllare la complessità del
        modello e della struttura ad albero.
Valori raccomandati criterion='gini' e max_depht= tra 4 e 8 
offrono spesso buoni compromessi.

DECISION TREE REGRESSORE

DecisionTreeRegressor è la versione del decision tree usata quando il target non è una classe
ma un valore numerico continuo. In altre parole serve per problemi di regressione.
Funzionano in modo analogo a quelli di classificazione, la differenze è che ogni foglia
va a predire un VALORE NUMERICO MEDIO, piuttosto che una classe.
Le regole di split si basano sulla minimizzazione dell'errore di predizione anzichè dell'impurità
di classe.
parametri:
    - criterion: può assumere valori come:
        - squared_error (MSE): è il più comune e produce stimi stabili ma sensibili agli outlier
        - absolute_error (MAE) è più robusto ai valori anomali, utile in presenza di dati rumorosi
        - frieman_mse o poisson
    - max_depth e min_samples_leaf: controllano la complessità e aiutano a prevenire l'overfitting
Valori raccomandati come punto di partenza max_depth=5 e min_samples_leaf=2

Vantaggi 
Interpretabilità: si può seguire ogni percorso di decisione
Presenta un linguaggio semplice e naturale per condividere risultati con persone non tecniche
Adattabilità a contesti regolamentati o dove serve trasparenza (es medicina, finanza)
Svantaggi
Overfitting: è un rischio ricorrente un albero troppo profondo tende a memorizzare il rumore 
del set di training, compromettendo la generalizzazione
Instabilità: piccoli cambiamente nei dati possono generare alberi radicalmente diversi
Ortogonalità: delle regole generate rispetto agli assi delle feature (non sempre ottimale
in spazi complessi)

Casi d'uso
Scelta ottimale nella fase iniziale di EDA e generazione di baseline di data scientics
Utile anche quando abbiamo variabili miste (numeriche e categoriche) e vogliamo una soluzione 
rapida.
In workflow completo, possono fungere da modello base prima di passare a soluzioni più complesse
Spesso vengono usati come building block per ensemble (es. random forest) per migliorarne la
stabilità e le prestazioni.
Ricorda però che occorre controllare la complessità e tenere d'occhio la generalizzazione.


"""
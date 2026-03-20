"""
RANDOM FOREST

E' uno degli algoritmi più usati nel machine learning, anche in contesti aziendali ERP, perchè 
è robuto, richiede poca pulizia dei dati e gestisce bene relazioni non lineari.
Il difetto principale del Decision Tree è che sono instabili, piccole modifiche nei dati, 
portano ad un albero completamente diverso; inoltre fanno spesso overfitting.
Qui nasce l'idea: non fidarti di un solo albero, fai votare molti alberi diversi.
Random Forest significa letteralmente Foresta casuale di alberi decisionali.
Invece di avere un decisoin tree ne crea centinaia.
Ogni albero vede i dati leggermente diversi, vede feature diverse. Poi si fa una media delle
decisioni. Questo riduce drasticamente l'errore.
Questa tecnica (combinazione di più modelli deboli per creare un modello più forte) è detta
ensemble learning; il concetto fondamentale è che un gruppo di alberi (foresta), se addestrato 
correttamente, commette meno errori di un singolo alberto
Il processo ha 3 passaggi:
1) Bootstrapping (campionamento casuale dei dati)
   Ogni albero viene addestrato su un campione casuale del dataset.
   Esempio albero di 1000 righe, ogni albero estrae 1000 righe casuali con ripertizone, quindi
   alcuni record compaiono più volte ed altri non compaiono. Questo genera alberi diversi.
2) Random feature selection
   Quando l'albero deve fare uno split, non considera tutte le feature, ne prende solo un
   sottoinsieme casuale.
   Esempio dataset con 10 variabili, ad ogni split l'albero scegliere casualmente 3 feature 
   su 10 e decide il miglio split. Questo rende gli alberi meno correlati tra loro.
3) Aggregazione finale
   Alla fine si combinano i risultati:
   - Classificazione: voto di maggioranza
   - Regressione: media delle predizioni
Dati diversi e feature diverse permettono ad ogni albero di ridurre la correlazione tra i 
singoli modelli e migliorare la capacità di generalizzazione.
Quando arriva un nuovo dato da classificare, ogni albero fornisce la propria previsoine
e la foresta prende la decisione finale.
Per problemi di classificazione si prende il majority voting, mentre per la regressione si 
calcola la media delle previsioni.

Parametri principali comuni:
    n_estimators: numero di alberi, più alberi più stabilità ma anche più calcolo. 
        valori tipici 100 - 300, offrono un buon equilibrio tra accuratezza e tempo di calcolo
    max_depth: profondità massima degli alberi, evita overfitting (impedendo che l'albero di
        adatti troppo ai dati)
    max_features: numero di feature da valutare per split, mantenendo la diversità tra gli alberi
        valore tipico sqrt(numero_feature)
    min_samples_split: numero minimo di record per fare uno split, serve per evitare alberi
        troppo complessi
    min_samples_leaf: quanti record/campioni devono trovarsi in ogni foglia

    boostrap: determina se usare il bagging classico, cioè campionamento casuale con rimpiazzo
    random_state: permette di ottenere sempre gli stessi risultati, utile per la riproducibilità
        degli esperimenti
    oob_score: attiva la stima delle prestazioni tramite i campioni non usati in addestramento, 
        è un modo interno di validazione senza separare i dati
    n_jobs: indica quanti core della CPU usare per parallelizzare il calcolo, rendendo 
        l'addestramento più veloce.

Parametri classificatore
    - criterion: definisce la misula di purezza dei nodi, di solito gini, o entropy, e 
        influenza come vengono scelti gli split
    - class_weight: serve per dare più importanza alle classi minoritarie nei dataset sbilanciati,
        migliorando l'equilibrio del modello
    - max_samples: indica la frazione di campioni usata per addestrare ogni albero, utile
        per ridurre tempi di calcolo su dataset molto grandi
    In generale, per problemi comuni si usano circa 200 alberi, profondità massima tra 10 e 30
    e sqrt per max_feature

Parametri regressione
    - criterion: controlla la misura dell'errore nei nodi, di solito impostato su squared_error
    - max_features: regola quante variabili testare per ogni split, e valori come sqrt o 0.8
        sono spesso buone scelte di partenza
    - boostrap: può essere disattivato per usare tutti i campioni ma attivarlo migliora la
        diversità del modello
    In genere, di ottengono buoni risultati con 200-500 alberi e profondità massima tra 20 e 40

I Random Forest funzionano meglio dei Decision Tree perchè riducono la varianza (molti alberi
mediati-modello stabile); Riduce overfitting (gli alberi sono addestrati su dati diversi, con
feature diverse); Funziona bene senza pre-processing (non richiede scaling, gestisce relazioni
non lineari, gestisce iterazioni tra variabili)

Uno dei punti di forza della Random Forest è la sua capacità di gestire dataset molto
grandi e con feature eterogenee.
Non richiede una normalizzazione accurata dei dati (perchè le feature non vengono confrontate 
tra di loro) e può lavorare sia con variabili numeriche sia con variabili categoriche.

Difetti:
Non è perfetto, modello poco interpretabile, lento (più alberi più lento), non eccelle con 
dataset molto grandi

FEATURE IMPORTANCE
Una cosa molto ultile del Random Forest più dirti quando conta ogni variabile, questo è
utilissimo per analisi predittive.
Permette di capire quali variabili hanno il maggior peso nella decisione.
Osservando la distribuzione delle importanze, si possono individuare le feature più influenti
e ridurre la dimensionalità del dataset.
Questo rende la Random Forest non solo un modello predittivo, ma anche uno strumento di 
interpretazione dei dati. 
Le feature più influenti possono essere rappresentate in un grafico a barre, per mostrare il 
loro contributo complessivo.

In Python la Random Forest si implementa grazie alle classi:
- RandomForestClassifier: per classificazione
- RandomForestRegressor: per regressione
del modulo sklearn.ensemble

Sebbene un Random Forest contenga molti alberi, è possibile esplorare la struttura di uno
di essi per capire come ragione il modello.
Con la funzione plot_tree si può disegnare uno degli alberi per visualizzare i nodi di decisione,
le soglie di split, e le classi finali.
Questa rappresentazione aiuta a comprendere il comportamento del modello anche in un contesto
complesso.
Ogni albero rappresenta una regola decisionale leggermente diversa, derivata dal campionamento
casuale sui dati e sulle feature.
Osservando più alberi si può notare come la diversità interna della foresta contribuisce a un
risultato più stabile.


"""
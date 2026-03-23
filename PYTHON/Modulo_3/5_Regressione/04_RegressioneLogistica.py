"""
REGRESSIONE LOGISTICA

Serve per prevedere una classe (0/1) non un numero continuo.
E' un modello statistico utilizzato per risolvere problemi di classificazione.
A differenza della regressione lineare, è usata quando la variabile dipendnete (il target) è categorico.
Il modello stima la probabilità che un'osservazione appartenga a una determinata classe, solitamente
0 o 1.
La funziona di base è la sigmoide, che trasforma una previsione continua in una probabilità compresa
tra 0 e 1.
La forma della sigmoide è importante, poichè introduce la non linearità necessaria per la classificazione

Esempio prevedere: cliente paga/non paga, ordine evaso/non evaso, cliente abbandona/resta
0=no
1=si
Rispetto alla regressione lineare, dove output è un numero, nella regressione logistica l'output è una 
probabiltà (esempio 0.82)
z= w1*x1+w2*x2....+b
b è l'intercetta e w1, w2, ecc sono i coefficienti delle variabili indipendenti.
L'obiettivo finale è stimare tutti questi n parametri in modo di massimizzare la probabilità di assegnare
correttamente le classi. Il risultato finale è una probabilità che ogni osservazione appartenza alla 
classe 1
output tra 0 e 1
z<0.5 classe 0
z>0.5 classe 1

Esattamente come la regressione lineare, regredisce un valore continuo, ma poi, con la sigmoide diventa
una probabilità (tra 0 e 1) ed infine, stabilendo una soglia (>0.5 allora 1 altrimenti 0) diventa una
classificazione
regressione (calcolo z) -> sigmoide (probabilità) - > soglia -> classe (0 o 1)
Non si chiama classificazione perchè nasce come modello statistico di regressione, poi viene usato per
classificare, quindi regressione nel metodo, classificazione nel risultato.
Rispetto ad un algoritmo di classificazione ha informazioni in più data dalla probabilità (0.51 incerco,
0.99 molto sicuro)

Valutazione modello
La funzione di costo nella regressione logistica è la log-loss o entropia incrociata, che misura la
distanza tra probabilità previste e reali.
Quindi non si usa MAE (come in regressione lineare) ma si usa ACCURACY model.score(X,y)
L'obiettivo è minimizzare questa funzione, cioè ridurre la distanza tra le probabilità predette e quelle
reali. Quando le probabilità previste sono vicine ai valori reali, la log-loss è bassa.
Questa funzione consente di allenare il modello per ottenere una previsione corretta della classe.

In Python
La regressione logistica può essere implementata con sklearn.linear_model.LogisticRegression.
Si adatta ai dati con il metodo .fit. (sui dati di traning) Per fare previsioni sulle etichete si 
utilizza .predict (con il set di test) 
Le probabilità di appartenenza a ciascuna classe possono essere ottenute con .predict_proba

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X, y)
y_pred = model.predict(X)
y_prob = model.predict_proba(X)
model.predict_proba(X)
.predict (restituisce [prob_classe_0, prob_classe_1] esempio [0.2,0.8] 80% probabilità classe 1)

Alcuni parametri chiave includono:
    - penalty: tipo di penalizzazione da applicare, tipicamente L2 regularization
    - tol: soglia per la quale di determinare la convergenza durante l'ottimizzazione di questo algoritmo
    - C: parametro di regolarizzazione, controlla l'intensità della penalizzazione sui coefficienti
    - max_iter: numero massimo di iterazioni consentivo per la convergenza, si usa quando si vuole limitare 
      l'uso computazionale delle risorse in presenza di dataset con dimensionalità alta
    - solver: il tipo di algoritmo di ottimizzazione (es lbfgs, newton-cg)

Vantaggi:
Semplice da implementare è interpretare, sia dell'algoritmo che dei coefficienti che trova
Non richiede grosse risorse computazionali, adatta anche per dataset medio/grandi
E' efficace per problemi di classificazione binaria.
Il modello è probabilistico, quindi fornisce anche la probabilità di appartenenza alla classe positiva
o negativa.
Facilmente interpretabile, utile quando è necessario spiegare le decisioni del modello, la trasparenza è
un suo punto di forza.

Svantaggi:
La regressione lineare presuppone che le classi siano separabili linearmente, il che può non essere 
sempre vero.
Non gestisce bene situazioni con forti interazioni tra variabili senza trasformazioni specifiche.
La performance può degradaere con grandi datasete soprattutto se sbilanciati.
E' sensibile agli outlier che possono distorcere la decisione del modello.
In caso di correlazioni elevate tra variabili, il modello può soffrire di multicollinearità

La regressione logistica è soggetta all'overfitting, specialmente quando il numero di variabili è elevato.
La regolarizzazione, tramite L1 (Lasso), o L2 (Ridge), aiuta a controllare l'overfitting e migliorare la
generalizzazione.
La regolarizzazione penalizza i coefficienti più grandi, riducendo la complessità del modello.
Il parametro C controlla il livello di regolarizzazione:
    - valori troppo bassi potrebbero portare a un underfitting
    - valori troppo alti potrebbero causare overfitting

La regressione logistica è ampiamente usata in medicina per diagnosticare o prevedere la risposta a 
trattamenti; in finanza viene impiegata per stimare la probabilità di default di un prestito; nel 
marketing aiutare a prevedere se un cliente acquisterà un prodotto o meno; utilizzata nel riconoscimento
facciale, spam detection, e analisi del sentimente.
La sua versatilità la rende un ottimo strumento per risolvere problemi di classificazione binaria.

La regressione logistica è uno degli algoritmi più importanti e versatili nel campo del Machine Learning.
Pur essendo relativamente semplice, offre una potente base probabilistica per problemi di classificazione.
La sua interpretabilità è uno dei motivi per cui viene spesso preferita in scenari in cui è necessario
spiegare le decisioni del modello.
Un uso corretto della regolarizzazione e della scelta dei parametri è essenziale per ottenere buone prestazioni.
Comprendere a fondo la regressione logistica fornisce le basi per apprendere modelli più avanzati e complessi

"""
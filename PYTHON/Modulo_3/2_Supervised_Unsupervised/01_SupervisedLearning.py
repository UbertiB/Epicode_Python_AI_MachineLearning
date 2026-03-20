"""
SUPERVISED LEARNING

Esistono due paradigmi, principi, di apprendimento:
1) Supervised: il training dataset (dataset di apprendimento) contiene anche sia feature che le label 
dei dati, si supervisiona come il modello apprende le relazioni e predice correttamente le etichette
2) Unsupervised: Il training dataset (dataset di apprendimento) non contiene nessuna label, si lascia 
decidere al modello i gruppi CLUSTER di dati con similarità, senza supervisione.
Nel primo caso il data scientics conosce l'output corretto nel primo caso, nel secondo invece si lascia 
completa autonomia al modello.


SUPERVISED LEARNING
L'apprendimento supervisionato è un approccio di Machine Learning in cui il modello impara da dati già 
etichettati.
Ogni dataset è composto dalle feature (X) e da label (y).
L'obiettivo è imparare una funzione f che sappia predire correttamente la laberl y anche per nuovi dati, 
mai visti prima.
Questo è possibile 'addestrando' il modello su un insieme di esempi noti (training dataset)
La qualità del modello dipende sia dai dati ma anche dalla scelta della funzione ipotizzata, quindi dal
algoritmo che il modello implementa.
L'obiettivo finale è costruire una funzione f che approssimi i label y a partire dalle feature X (f(X)=y)
Questa funzione deve generalizzare, cioè funzionare bene anche su dati non presenti nel training set.
Un buon modello non 'memorizza', ma apprende i pattern sottostanti ai dati.
La qualtà della generalizzazione è misurata tramite errori sui dati di test.
La scelta della funzione, dei dati, e della loss è fondamentale per buone prestazioni.

Le principali categorie di applicazione dell'apprendimento supervisionato sono due:

    REGRESSIONE: Usata per prevedere un output valori numeri continui.
        L'obbiettivo è trovare una funzione che descriva al meglio la relazione tra input e output,
        minimizzando l'errore tra valori predetti e osservati.
        Utile per probemi come previsioni economiche, metereologiche, o analisi di trend.

    CLASSIFICAZIONE: Usata per assegnare etichette discrete e/o categoriche a nuovi dati.
        L'obiettivo è imparare un confine decisionale che separi correttamente le classi nello spazio di ipotesi.
        Utile per riconoscimento di immagini, spam detection, disgnosi mediche e molte altre applicazioni


REGRESSIONE

La regressione è un campo di apprendimento supervisionato che mira a prevedere un valore numerico continuo.
L'obiettivo è costruire un modello che apprenda la relazione che esiste tra le feature (input) 
e le laber, cioè target (output)
Il modello cerca di stimare una funzione f di previsione che minimizzi l'errore tra i valori previsti
e quelli reali.
Esempi tipici sono:
- Previsione prezzi
- Stima consumi energetici
- Previsioni di vendita o di domanda

Per addestare un modello di regressione si misura quanto le previsioni che ha affettuato differiscono dai 
valori reali tramite la funzione di perdita.
La loss function influenza direttamente la qualità del modello.
Le loss più utilizzate sono:
    - Mean Squared Error (MES): penalizza fortemente gli errori trandi, 'trascurando' quelli più piccoli, 
        utile quando si vogliono evitare outlier lontani
    - Mean Absolute Error (MAE): misura la distanza media assoluta, più robusta agli outlier
    - Huber Loss: combina vantaggi di MES e MAE, quadratica per errori piccoli, e lineare per errori grandi.

Esistono diversi tipi di modelli di regressione, ognuno adatto a scenari differenti:
    - LINEARE: il modello apprende una relazione lineare tra le feature e target
    - POLINOMIALE: la relazione è non lineare ma approssimata tramite trasformazioni polinomiali.
    - LASSO/RIDGE: tipo di regressione che va a regolarizzare i dati per evitare overfitting
    - NON LINEARE: modelli più complessi per pattern più articolati
Ogni scelta del modello implica compromessi tra accuratezza statistica , interpretabilità e 
complessità computazionale.

CLASSIFICAZIONE

La classificazione è un compito di apprendimento supervisionato in cui l'obiettivo del modello 
è assegnare un'etichetta discreta a ogni dati di input.
I dati in input sono rappresentati da vettori di caratteristiche (le feature), ma le etichette appartengono 
a un insieme finito di categorie.
Il modlelo va a stimare una funzione h(x) che predice la classe corretta per un nuovo esempio.
La classificazione può essere binaria (la label assume al massimo due valori) oppure multi-classe (n valori
ma n numero finito)

Per addestrare un modello di classificazione si minimazza la funzione di perdita che misura quanto le 
predizioni si discostano dalle etichette reali.
Le più comuni sono:
    - 0/1 loss: indica semplicemente se la predizione è corretta o no, nel primo caso la perdita sarà 0 nel
        secondo caso la perdita sarà completa quindi 1
    - Logistic loss: usata in regressione logistica, misura qunto il modello si senti sicuro nel classificare
        una classe (misura la confidenza)
    - Hinge Loss: usata nei modelli SVM, penalizza fortemente la classificazioni sbagliate quelle con bassa
        confidenza.

Esistono due tipi di classificazione (binaria, multi-classe):
1) Binaria: quando le etichette sono due (esempio positivo/negativo, spam/non spam)
    Algoritmi: Logistic Regression, Decision Tree, Support Vector Machine (SVM)
2) Multi-classe: quando ci sono più di due classi e ogni esempio appartiene ad una sola classe (es. riconoscimento
   di cifre, classificazione di immagini in categorie).
   Algoritmi: Random Forest, K-Nearest Neighbors (k-NN), Naive Bayes
In generale la classificazione si differenzia in due categorie sul come il modello sceglie l'appartenenza
di un dato ad una classe e sono: classificazione hard e soft: in cui il modello sceglie:
    - Hard: una classe definitiva
    - Soft: una probabiltà/confidenza per ciascuna classe (Logistic Regression)






"""
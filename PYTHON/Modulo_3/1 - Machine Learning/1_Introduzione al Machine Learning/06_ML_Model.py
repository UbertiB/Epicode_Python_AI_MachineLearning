"""
MACHINE LEARNING PROCESS: DATA, MODEL, LOSS

MODELLO
Un modello rappresenta in modo concreto la funzione f, che è la funzione che va ad approsimare meglio una 
label y a partire dalle sue feature x. 
In pratica il modello cerca di riprodurre il comportamento del fenomeno reale osservando nei dati.
Addestrare un modello significa trovare i parametri ottimali di f affinche f(x)=y anche per i nuovi dati.
Il modello è la traduzione formale della nostra ipotesi su come i dati sono generati, e come vengono
legati alle label.
Ogni modello rappresenta un insieme di possibili funzioni f, chiamate ipotesi.
Una singola ipotesi h è una possibile approssimazione della reale funzione f(x)=y.
Durante l'addestramento di un modello, si sceglie sempre un'ipotesi h che è quelle che meglio 
approssima i dati osservati.
Lo spazio delle ipotesi H è l'insieme di tutte le relazioni che legano x a y, ed è un insieme molto grande.
L'insieme di tutte le ipotesi che un modello può generare è chiamato spadio di impotesi H.
Il modello impone dei vincoli su come i dati possono essere rappresentati, riducendo il numero di funzioni
possibili e rendendo l'apprendimento più gestibile e generalizzabile.
- Modello lineare, chiamato regressione linerare. (somma di monomi)
- Modello polinomiale, anche esso lineare, non è più una retta ma un insieme di curve (somma di monomi
    ma in questo caso le feature sono elevate a potenze)
- Decision Tree
- Artificial Neural Network: rete di tutte regressioni lineari

QUALE MODELLO SCEGLIERE?
Scegliere un modello significa anche scegliere le funzioni che esso può apprendere. 
E' necessario un bilanciamento tra complessità e capacità di generalizzare.
Un modello:
    - troppo piccolo: ciaò un modello che offre una spazio di ipotesi troppo ristretto, è incapace di 
        rappresentare i pattern (underfitting), incapace di apprenderli
    - troppo grande: apprende anche rumore ed outliers (overfitting)
Un modello deve essere sufficientemente grande da contenere una buona ipotesi.
Esempio dati non lineari non possono essere rappresentati da una retta ma hanno bisogno di modelli polinomia
o comunque non lineari.
Se il modello è troppo semplice, l'errore sarà molto elevato su dati complessi.
Un modello troppo grande, è sempre difficile da addestrare ed interpretare e laborioso a livello computazionale.
Un modello non deve essere troppo complesso, altrimenti rischi di imparare anche il rumore e gli outlier dai dati
anzichè i pattern reali.
Modelli eccessivamente grandi portano ad overfitting: ottime prestazioni sui dati di learning (apprendimento)
scarsa capacità di generalizzare.
Un modello più semplice è invece meno computazionalmente costoso da addestrare, più efficiente da eseguire,
più interpretabile.

Per scegliere un modello bisogna fare un compromesso tra l'interpretabilità accuratezza statistica e la
compelssità comutezionale.
Il trade-off si trova bilanciando queste caratteristiche in base agli scopi, vincoli e contesto.

Ogni tentativo di minimizzare l'errore del modello (migliorare l'accuratezza statistica) si scontra con una
competizione tra due fonti di errore:
- Bias: è la distorsione, l'errore di semplificazione che deriva dall'utilizzo di un modello troppo semplice, 
    modelli con bias elevato tendono all'underfitting indipendentemente dalla qualità e quantità dei dati
    di apprendimento
- Varianza: è l'errore di sensibilità che deriva da un modello troppo grande, complesso e sensibile alle 
    fluttuazioni, modelli con elevata varianza tendono all'overfitting, adattandosi eccessivamente anche al
    rumore ed outlier.

"""
"""
SVM: SVC (per la classificazione) e SVR (per la regressione)

Le SVM sono modelli supervisionati utilizzati per la classificazione e la regressione.
Si basano sull'idea di trovare un confine ottimale che separi le classi nel modo più netto possibile.
Questo confine è detto iperpiano e rappresenta la frontiera di decisione tra le categorie.
L'obiettivo principale è massimizzare il margine, cioè la distanza tra l'iperpiano e i punti più 
vicini ad esso per ogni classe
I punti più vicini al margine prendono il nome di vettori di supporto

Una SVM cerca di dividere lo spazio dei dati nel modo più pulito possibile.
Le osservazioni ai margini sono quelle che determinano la posizione dell'iperpiano ottimale.
Il modello non si concentra su tutti i dati, ma solo sui punti chiave che vanno a definire
la separazione tra le classi.
Questa caratteristica rende SVM particolarmente robusto a dati rumorosi o ridondanti.
L'idea del margine ampio centrale per andare a ridurre la possibiltà l'overfitting e migliorare la 
generalizzazione.

In uno spazio bidimensionale, l'iperpiano è una semplice retta che separa le due classi.
In spazi con più dimensioni, diventa un piano o un iperpiano.
L'iperpiano ideale è quello che va a massimizzare la distanza dai punti più vicini di ciascuna classe.
Matematicamente, SVM risolve un problema di ottimizzazione vincolata per trovare tale confine.
Questo approccio garantisce la migliore separazione possibile tra le classi nei training set

Il margine è definito come la distanza tra l'iperpiano e i vettori di supporto.
Un margine ampio implica maggiore robustezza alle variazioni dei dati.
I vettori di supporto sono gli unici punti che influenzano realmente il confine d separazione.
Rimuovere o modificare altri punti non cambia la posizione dell'iperpiano.
Questa proprietà rende SVM efficinete e molto meno sensibile al ruomore rispetto ad altri modelli.

Quando i dati sono linearmente separabili, SVM trova un iperpiano esatto che divide le classi.
L'obiettivo è massimizzare il margine mantenendo corretta la classificazione di tutti i punti.
In questo scenario, la funzione obiettivo si risolve con vincoli di uguaglianza lineare.
Questo tipo di SVM è detto hard-margin perchè non ammette errori di classificazione.
E' un modello efficace solo quando i dati sono ben separati senza sovrapposizioni, 
cioè sono linearmente separabili

Nella pratica, molti dataset non sono perfettamente separabili da una linea o da un piano.
Per questi motivo si va ad introdurre un parametro di tolleranza agli errori tramite il parametro C
C controlla il compromesso tra massimizzazione del margine e penalizzazoine degli errori, valori di C 
- valori di C alto riducono gli errori ma restringono il margine
- valori di C basso consentono un margine più ampio ma con maggiore tolleranza agli errori.

Per gestire i dati non linermente separabili SVM utilizza la tecnica del kernel trick
L'idea è quella di proiettare i dati in uno spazio di dimensioni superiori dove deventano separabili interamente
In questo spazio trasformato, la separazione si ottiene tramite un iperpiano lineare.
Il kernel consente di eseguire questa trasformazione in modo implicito e computazionalmente efficiente.
Le SVM con kernel sono così' in grado di modellare relazioni complesse e non lineari.

Il SVM con un kernel lineare disegna una retta che divide i dati
Il SVM con un kernel non lineare (esempio RBF) disegna una curva gaussiana che divide i dati ed un 
minor errore.

SVM risolve un problema di ottimizzazione quadratica con vincoli lineari
La funzione obiettivo minimizza la norma del vettore dei pesi sottetta a vincoli di classificazione corretta.
Nei casi non lineari, la funzione di perdita introduce variabili di slack per gestire errori.
Il kernel consente di calcolare i prodotti scalari nello spazio trasformato senza esplicitarlo.
Questo approccio mantiene la complessità gestibile anche per i dati ad alta dimensionalità

Nel contesto della classificazione questo algoritmo (SVM) costruisce un iperpiano che separa le classi.
Per problemi multiclasse, scikit-learn implementa strategia one-vs-one e one-vs-rest.
Ogni sottoproblema binario determina un confine locale tra due categorie.
La predizione finale combina i risultati di tutti i classificatori binari.
Questa estensione permette a SVM di affrontare problemi complessi con molto etichette. Principalmente
consiste nel confrontare una sola classe con il resto delle altre, creando così, nel caso di 3 classi, 
due problemi binari e gestendo meglio la classificazione.

Nel caso della regressione si ha a che fare con la Support Vector Regression (SVR) che si base sugli 
stessi principi.
SVR cerca una funzione che si discosta dai dati di meno di un certo margine. I punti entro questo margine
non contribuiscono all'errore complessivo del modello.
Il parametro C controlla la penalità per le deviazioni superiori al margine.
Questo approccio consendte di modellare relazioni non lineari anche nella regressione.

Parametri:
    C: controlla il compromesso tra ampiezza del margine e accuratezza sul training set.
    Kernel: determina la funzione di trasformazione usata per separare i dati, e si imposta in base
        alla complessità dei dati
    gamma: regola l'influenza di ogni singolo punto di training nel kernel RBF
    degree: è rilevante per i kernel polinomiali e definisce il grado del polinomio, da questo parametro
        dipende anche il costo computazionale per allenare il modlelo.
Perametri come c o gamma, devono essere ottimizzati tramite cross validation o grid search
Un c troppo alto porta a modelli rigiti e overfittati
Un gamma elevato crea confini molto complessi che catturano anche il rumore.
E' importante bilanciare questi parametri per mantenere un buon margine di generalizzazione.
L'uso di metriche come accuracy o F1-score aiuta a valutare la bontà della scelta dei parametri.

I kernel più comuni sono: lineare, polimoniale, RBF (Radial Basis Function) e sigmoidale.
Il kernel lineare è adato a dati già ben separabili
Il kernel RBF è il più usato e misura la similarità tramite una funzione gaussiana, più usato.
Il kernel polinomiale crea confini più flessibili ma può essere costoso computezionalmente.
La scelta del kernel è determinante per la qualità del modello e deve riflettere la natura dei dati.

Ho dati divisi in classi
Esempio: clienti buoni pagatori, clienti pessimi pagatori. Ho alcune feature. esempio: giorni di ritardo,
numero di insoluti, fatturato, voglio capire da che parte cade un nuovo cliente.

SVM cerca una linia (o piano) che separa le classi, ma non  una qualsiasi, quella migliore possibile.
Quidn a SVM non basta separare, vuole massimizzare la distanza dai punti più vicini, questa distanza
si chiama margine.

SVM non usa tutti i dati, usa solo i punti che sono più vicini alla linea, quelli sono i support
vectors. Sono i punti critici, che decidono il modello (a dx o asx)

Differnza con k-NN
k-NN guarda i vicini, decide ogni volta
SVM costruisce un confine, decide con una regola globale

Nella maggior parte dei casi, non puoi tracciare un linea perfetta, SVM fa due cose: 1. accetta errori
(soft margin) 2. cerca comunque il miglior compromesso.
Parametro C:
    C alto: meno errori, rischio overfitting
    C basso: più tolleranza, più generalizzazione

E se non basta una linea per separe i dati, SVM usa kernel
Kernel= trasformazione dei dati
porta i dati in uno spazio più complesso, dove diventano separabili (esempio in 2d non separi, in 3D si)

Tipi principali:
- Linear: linea
- RBF: curva (il più usato)
- Polynomial: polinomio

Vantaggi:
SVM è efficace in spazi ad alta dimensionalità
robuta al rumore
si concentra solo sui punti più rilevanti per la decisione
offre una buonva generalizzazione anche con  un numero limitato di campioni
i kernel permettono di gestire relazioni complesse senza espandere esplicitamente lo spazio
Ha solide basi matematiche e teoriche nel campo dell'ottimizzazione convex
Svantaggi:
Il costo computazione può essere elevato per dataset molto grandi
La scelta dei parametri e del kernel richiede attenzione ed esperienza
La probabilità predetta non è nativa e richiede calibrazione separata.
Non è facilmente interpretabile come un albero decisionale o una regressione lineare.
Le prestazioni possono peggiorare su dataset con molto feature irrilevanti o rumorose, si consigli un 
pre-processing.

Le SVM uniscono rigore matematico e grande capacità predittiva.
La massimizzazione del margine garantisce modelli stabili e generalizzabili
La possibilità di usare kernel rende SVM adattabile a una vasta gamma di problemi.
Richiede un tuning accurato dei parametri per ottenere le migliori prestazioni
Rimane una delle tecniche più solide e versatili nell'apprendimento supervisionato moderno.
"""
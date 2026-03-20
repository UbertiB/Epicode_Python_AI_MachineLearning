"""
KERNEL PCA

La PCA è una tecnica di riduzione dimensionale di dati che possono essere rappresentati 
in modo lineare.
K-PCA invece è una tecnica di riduzione dimensionale con dati non lineari.
Oltre alla K-PCA, un'altra tecnica di riduzione dimensionale non lineare è la tSNE (vedremo
più avanti)

La PCA tradizionale è uno strumento estremamente utile, ma funziona bene solo quando i dati
seguono relazioni lineari.
Nella realtà però molti fenomeni non si comportano in modo lineare: le variabili possono 
interagire in modo complesso presentando delle curve.
Quando questo accade, la PCA perde parte della sua efficacia, perchè non riesce a cogliere
la vera struttura dei dati.
L'obiettivo della Kernel PCA è proprio superare questo limite offrendo una versione non 
lineare della PCA.
Inoltre permette di scoprire pattern nascosti e strutture complesse che la PCA classica non 
è in grado di rappresentare.

La PCA cerca combinazioni lineari delle variabili che vanno sempre a massimizzare la varianza, 
ma questa ipotesi lineare è anche il suo principale limite.
Quando le relazioni tra i dati non sono rettilinee, la PCA fatica a rappresentarne in modo
significativo.
Se ad esempio, i punti si dispongono lungo una curva o su una superficia chiusa, la PCA tende
a schiacciarli su un asse che non conserva la loro forma.
La riduzione ottenuta può sembrare informativa ma in realtà perde le relazioni più importanti.
Questo caso mostra la necessità di un'estensione di questo algoritmo che sappia adattarsi 
a strutture più complesse.

Esempio: un insieme di punti disposti lungo un cerchio o una spirale, in questo caso la PCA 
lineare proietta i punti su un asse e li comprime in una linea, perdendo completamente la forma
circolare.
I punti che nel piano erano lontani possono finire vicini, e viceversa.
In termini geometrici, la PCA ha ridotto la dimensione ma ha distrutto la geometrica del
dataset, andando a perdere un'informazione importante dei dati.
Per mantenere la struttura originale (non lineare) servirebbe una trasformazione capace
di "srotolare" il cerchio e renderlo lineare in uno spazione diverso.

KERNEL PCA
Il principio fondamentale della Kernel PCA è molto elegante:
trasformare i dati in uno spazio di dimensione più alta dove le relazioni diventano lineari.
In quello spazio, ciò che nel piano originale appariva curvo o intrecciato può diventare più 
semplice e lineare.
Una volta mappati i dati nel nuovo spazio, si può applicare la PCA classica per individuare
le direzioni di massima varianza.
Il problema è che questa trasformazione potrebbe anche essere enorme, persino infinita, 
e quindi impossibile da calcolare esplicitamente.
Per fortuna esiste un modo per sfruttarla senza calcolare davvere la trasformazione: il 
kernel trick

Un kernel è una funzione che misura la similarità tra due punti in modo da riflettere la loro
vicinanza in uno spazio trasformato.
Invece di calcolare la posizione di ogni punto in quello spazio, il kernel calcola direttamente
quanto due punti si assomigliano.
E' come lavorare  con le distanze e non con le coordinate.
Il kernel permette quindi di lavorare implicitamente in spazi di dimensione molto alta, 
o addirittura infinita, senza doverli mai costruire.
Questo approccio apre la strada a metodi capaci di catturare relazioni non lineari mantenendo
la semplicità di calcolo.

Esistono diversi tipi di kernel:
    * Il kernel lineare: è il più semplice e corrisponde alla PCA classica, perchè misura
      solo il prodotto scalare tra i vettori dei dati
    * Il kernel polinomiale: eleva quel prodotto a una potenza e introduce così una sensibilità
      a interazioni di ordine superiore
    * Il kernel gaussiano (o RBF): è il più flessibile: valuta la similarità in base alla 
      distanza e privilegia le relazioni locali similarità in base alla distanza e privilegia 
      relazioni locali.
Ogni kerel definisce una diversa 'geometrica' dei dati e quind un diverso modo di catturare
le relazioni.
Scegliere il kernel giusto, significa scegliere la prospettiva più adatta per osservare il 
fenomeno in esame

Il kernel trick è l'idea di base che rende tutto questo possibile.
Permette di calcolare prodotti scalari nello spazio trasformato senza mai effetturare la 
trasformazione.
Invece di calcolare le nuove coordinate, si lavora con la matrice dei kernel, che contiene 
tutte le similarità tra le coppie di punti.
Questa matrice sostituisce i dati originali e divanta l'oggetto su cui applicare la PCA

Il kernel trick è l'idea di base che rende tutto questo possibile
Permette di calcolare prodotti scalari nello spazio trasformato senza mai effettuare 
la trasformazione.
Invece di calcolare le nuove coordinate, si lavora con la matrice dei kernel, che contiene 
tutte le similarità tra le coppie di punti.
Questa matrice sostituisce i dati originali e diventa l'oggetto su cui applicare la PCA.
Così la complessità del mapping resta nascosta, ma l'effetto non lineare è pienamente sfruttato.

La Kernel PCA parte costruendo la matrice dei kernel e centrando i suoi valori per eliminare
effetti di traslazione.
Poi calcola gli autovalori e gli autovettori di quella matrice, proprio come fa la PCA con la
matrice di covarianza.
Gli autovettori rappresentano le nuove componenti principali nello spazio trasformato.
Ogni dato può essere proiettato su queste componenti, ottenendo una nuova rappresentazione 
non lineare.
Il risultato è una proiezione capace di mettere in evidenza strutture che la PCA lineare
non avrebbe mai potuto mostrare

Se si applica la PCA lineare a dati disposti in forma circolare, i punti appaiono tutti 
lungo una linea indistinta.
Usando invece la kernel PCA (es. RBF), la struttura circolare riemerge chiaramente nella nuova
rappresentazione.
Punti appartenenti a regioni diverse dal cerchio restano separati, come se lo spazio fosse 
stato 'raddrizzato'
Questo mostra come un cambiamento di prospettiva possa trasformare completamente l'analisi.
Un confronto grafico tra i due risultati, rende immediata l'istruzione di quanto la Kernel PCA
sia più flessibile.

* La PCA tradizionale trova direzioni di massima varianza che sono rette nello spazione dei dati.
* La kernel PCA, invece, trova direzioni che corrispondono a curve o superfici nel piano originale.
* E' come se piegasse lo spazio in modo che relazioni complesse diventano lineari nel nuovo 
ambiente.
Questo concetto di 'spazio piegato' aiuta a visualizzare perchè la Kernel PCA riesce a 
rappresentare strutture così diverse.
In sostanza, la geometrica dei dati viene reinterpretata attraverso una mappa più ricca e non 
lineare.

La Kernel PCA appartiene alla stessa famiglia di tecniche che utilizzano kernel, come la SVM
o la regressione kernel ridge.
Tutte condividono l'idea di lavorare in uno spazio trasformato per risolvere problemi che nel  
piano originale sarebbero troppo complessi.
Nel caso della PCA, lo scopo non è classificare o predire, ma rappresentare i dati in modo più
informativo.
Questo la rende uno strumento potente anche come passo preliminare per altri modelli di 
apprendimento.
In molti casi la Kernel PCA migliora la separabilità dei dati, facilitando l'analisi successiva.

Non esiste una regola universale per scegliere quel'è il kernel migliore in assoluto.
In molti casi si prova una gamma di kernel e si osservano i risultati, regolando parametri
come il grado del polinomio o la larghezza della gaussiana.
La scelta dipende fortemente dalla natura dei dati e dall'obiettivo dell'analisi.
Un kernel:
    * troppo rigido può perdere dettagli rilevanti
    * troppo flessibile può adattarsi eccessivamente al rumore, andando incontro al overfitting
Trovare l'equilibrio giusto è spesso una questione di esperienza e sperimentazione.

Vantaggi
- capacità di catturare strutture altamente non lineare senza dover esplicitare la trasformazione
- conserva l'intuizione geometrice della PCA ma la estende a scenari molto più complessi.
- Rappresenta relazioni intricate tra le variabili ed è in grado di scoprire pattern nascosti.
- Utile per l'estrapolazione e preprocessing per altri algoritmi di classificazione e/o clustering.
Svantaggi
- Necessità di scegliere il kernel giusto e impostare correttamente i parametri.
- Una scelta indadeguata può portare a risultai fuorvianti o difficili da interpretare.
- La matrice dei kernel cresce quadraticamente con il numero di osservazioni, rendendo il metodo
pesante per dataseet molto grandi.
- Il risultato della Kernel PCA sono sempre meno interpretabili in termini di variabili 
originali, a differenza della PCA.

Applicazioni
La Kernel PCA è stata applicata con successo in molti ambiti dove la linearità non basta:
- Nel riconoscimento facciale, ad esempio, consente di distinguere volti con variazioni
  di luce o posa
- In bioinformatica, aiuta a individuare pattern complessi nei dati genetici o proteici.
- In robotica e visione artificiale è utile per analizzare forme e movimenti non lineari.

In Python: KernelPCA di sklearn.decomposition

"""
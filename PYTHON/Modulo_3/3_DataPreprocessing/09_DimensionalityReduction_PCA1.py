"""
DATA PREPROCESSING
DIMENSIONALITY REDUCTION CON PCA1 (PRINCIPAL COMPONENT ANALYSIS)

La visualizzazione dei dati multivariati (plotting) è un problema significatiper per l'analisi.
Mentre i dati 1D (righe o colonne) e 2D (matrici e tabelle in generale) sono facili 
da rappresentare (un punto o un piano X-Y), le cose si complicano velocemente.. aumentando 
le dimensioni.
Un plot 3D può essere visualizzato ma con qualche difficoltà, dati con 4D richiedono tecniche 
più complesse come un plot ternario con codifica a colori.
Quando si arriva a 5D, 6D o più, la visualizzazione intuitiva diventa quasi impossibile.
E' anche inefficiente tentare di analizzare tutte le coppie di attributi di un dataset con 
queste dimensioni.

E' qui che interviene la Dimensionality Reduction che impara una mappa e trasforma la rappresentazione
di un dati in un set di feature complesse.
Questo crea una rappresentazione compressas del dato originale.
In sintesi, la dimensionality reduction consiste nel ricostruire i dati originali da un numero
ridotto di feature.
In generale, ridurre il numero di feature permette di:
    - catturare l'informazione importante in modo più efficiente rispetto agli attributi originali
    - migliorare la generalizzazione dei modelli, riducendo anche la possibilita di overfitting,
    - ridurre la quantità di tempo e memoria richiesti dagli algoritmi quindi migliorare le
    prestazioni computazionali del modello
    - eliminare feature irrilevanti e/o ridurre il rumore nei dati

Le principali tecniche per applicare una riduzione di dimensionalità sono:
* Singular Value Decomposition (SVD)
* Linear Discriminant Analysis (LDA)
* Principal Component Analysis (PCA)
* Techinche non lineari:
    - K-PCA: kernel PCA
    - t-SNE: t-distributed Stochastic Neighbor Embedding

Applicare la dimensinality reduction si parte da un dataset con n variabili, da dati grezzi
e già puliti, si vuole compensare questo dataset, tramite una funzione generica h per portarlo
ad un numero di variabili p inferiore a n.
Queste nuove feature, queste nuove informazioni, possono essere ricostruite a partire da una
funzione generica g, questa ricostruzione mantiene la forma che portava il dataset originale
a partire da tutte quelle feature già compresse

La prima tecnica per applicare la dimensionality reduction è la 
PRINCIPAL COMPONENT ANALYSIS (PCA), analisi del componente principale
ed è anche una delle più comuni, più esate e popolari.

La PCA è la tecnica fondamentale e più diffusa per la riduzione di dimensionalità.
Fu introdotta per la prima volta, da Karl Pearson nel 1901 per descrivere la variazione in un
set di dati multivariati.
Rappresenta uno strumento di preprocessing essenziale in moltissimi ambiti della Data Science, 
del Machine Learning e dell'analisi statistica.
Consente di semplificare i dataset multidimensionali mantenendo la maggior parte delle
informazioni rilevanti.
In pratica, ci permette di riassumere i dati in un numero minore di dimensioni, rendendo
più facile visualizzarli, analizzarli e interpretarli.

Nei dataset con molte variabili, spesso, alcune di esse, contengono informazioni ridondanti o
sono correlate tra loro.
La PCA individua un nuovo modo di rappresentare i dati, mettendo in evidenza le direzioni più 
informative senza perdere la struttura principale del dataset.
Le principali utilità della PCA sono:
    - Ridurre il numero di dimensioni nel dataset, semplificando analisi e modelli
    - Trovare pattern nascosti in dati ad alta dimensionalità
    - Visualizzare dati complessi in 2D o 3D, facilitando l'interpretazione e la comunicazione.

L'idea centrale della PCA è trasformare le variabili originali, spesso correlate, in un nuovo
insieme di variabili X1 completamente scorrelate.
Algebricamente equivale a cercare una nuova base di assi all'interno dello spazio dei dati, dove:
    - gli assi sono ortogonali (perpendicolari tra loro)
    - ogni asse rappresenta una direzione di massima variabilità
Ogni componente principale (PC) è definita come una combinazione lineare delle variabili originali,
ponderata in modo ottimale per catturare quanta più informazione possibile.
Se abbiamo n variabili osservate, la PCA può estrarre fino a n omponenti principali, ma 
spesso solo le prime p spiegano una quantità significativa di varianza.

con p intendendo  un numero di feature, o comunque varibili, minore del totale.

La PCA è particolarmente utile quando:
    - esisten ridondanza tra le variabili (alcune variabili sono correlate)
    - I vati non riempono completamente lo spazio d-dimensionale.
In questo condizioni, possiamo ridurre il numero di variabili osservate, a un numero minore
di componenti artificiali senza osservare un numero minore di componenti artificiali senza
perdere la maggior parte dell'informazione.

La PCA è più utile quando esiste ridondanza nelle variabili, il che signirica che alcune
variabili sono correlate tra loro.
E' utile anche quando i dati non coprono l'intero spazio n-dimensionale.
I componenti principali PC risultanti, spiegano la maggior parte della varianza delle
variabili osservate.
Tuttavia, spesso solo i primi pochi componenti p (p<=n) spiegano una quantià significativa 
di varianza.
In queste condizioni è possibile ridurre il numero di variabili osservate in un numero minore 
di componenti artificiali.

La prima definizioe di PCA è trovare un sottospazio di dimensionalità inferiore.
La proiezione ortogonale dei punti dati su questo sottospazio, deve massimizzare la varianza dei
punti proiettati.
Se la varianza è massimizzata, l'asse ha catturato la massima dispersione possibile dei dati.

Una definizione alternativa, è matematicamente equivalente, si base sulla minimizzazione 
dell'errore. Questo approccio minimizza la somma dei quadrati degli errori di proiezione.
In pratica si cerca la linea che meglio si adatta ai dati, riducendo al minimo la distanza
ad ogni punto.


"""
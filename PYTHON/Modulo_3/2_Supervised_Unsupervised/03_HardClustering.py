"""
HARD CLUSTERING

L'hard clustering è una tecnica di apprendimento non supervisionato che mira a raggruppare i dati in insiemi 
coerenti detti cluster.
A differenza di altri approcci più complessi, in questo caso ogni dato che viene elaborato, viene assegnato 
in modo netto e univoco a un solo cluster.
Non ci sono probabilità o appartenenze parziali: un punto è 'dentro' un cluster oppure 'fuori'
Questo rende il metodo molto intuitivo da comprendere e interpretabile da visualizzare graficamente.
E' spesso il primo approccio che si utilizza quando si vuole eseguire un'analisi esplorativa sui dati per
scoprire pattern nascosti.

Un CLUSTER è un raggruppamento di dati che mostrano tra loro un alto grado di somiglianza e un basso grado
di somiglianza con elementi appartenenti ad altri cluster.
L'obiettivo è identificare strutture naturali all'interno dei dati, senza che queste siano fornite in 
partenza (senza output o label).
In un approccio hard, ogni dato viene etichettato rigidamente con un solo cluster.
L'idea alla base è che i dati simili si trovano vicini nello spazio delle feature, e quindi appartengono
allo stesso gruppo.
Questa definizione è semplice ma molto potente, perchè permette di costruire segmentazioni chiare
e facilmente interpretabili.

Il processo di hard clustering si basa su un ciclo di assegnazione e aggiornamento che mira a migliorare
progressivamente la qualità dei cluster.
In genere si inizia specificando il numero desiderato di cluster k, a priori, e scegliendo delle posizioni 
iniziali per i centroidi (i centri di gravità per ogni cluster).
Ogni punto viene quindi assegnato al cluster il cui centroide è più vicino, secondo una certa metrica di distanza.
Una volta assegnati tutti i punti, i centroidi vengono aggiornati calcolando la posizione media dei punti 
assegnati per ciascun cluster.
Questo processo di riassegnazione e aggiornamento dei centroidi si ripete finchè non si raggiunge una 
situazione stabile (convergenza), in cui i cluster non cambiano più.

Vantaggi:
- semplicità concettuale e operativa
- facile da spiegare, da implementare e interpretabile nella visualizzazione, il che lo rende perfetto 
    per introdurre il concetto di clustering.
- Quando i dati presentano cluster ben separati, i risultati sono già spesso ottimi e stabil, ciò significa
    che non c'è più bisogno di applicare altre tecniche per migliorarli o interpretarli
- Gli algoritmi hard, come K-Means, sono inoltre molto efficienti dal punto di vista computazionale. Questo
    li rende adatti a dataset di dimensioni medio-grandi

Svantaggi e limiti:
- L'approccio hard non gestisce bene i dati con confini sfrumati tra cluster, perchè impone una scelta netta
    ed univoca di assegnazione ad un cluster.
- Non è adatto a situazioni in cui un dato potrebbe appartenere a più gruppi contemporaneamente.
- Inoltre, richiede di conoscere il numero di cluster k a priori, cosa che nella pratica spesso non è banale.
- E' anche sensibile agli outlier: pochi punti anomali possono influenzare fortemente la posizione dei centroidi
    e sbilanciare così tutto il calcolo e la convergenza del processo (centroidi)
- Per questo motivo, va utilizzato con attenzione, valutando bene i dati di partenza e applicando varie
metriche di pre-processing per rendere il dataset più uniforme possibile.

Algoritmi
L'algoritmo hard più famoso è K-Means, che funziona tramite assegnazione iterativa dei dati ai centroidi, 
nell'aggiornamento delle coordinate dei centroidi, sensibili agli outlier.
Una variante importante è K-Medoids, che utilizza punti reali come centroidi, rendendolo più robusto agli outlier
Anche Hierarchical Clustering (clustering gerarchico) può essere usato in versione hard, creando una 
struttura ad albero ma con assegnazione netta.
Tutti questi algoritmi condividono lo stesso principio: ogni dato deve essere assegnato in modo esclusivo
a un gruppo.
La scelta dell'algoritmo che si va ad implementare dipende dal tipo di dati e dagli obiettivi dell'analisi

Parametri necessari
Il parametro più importante è il numero di cluster K, che deve essere scelto a priori e scelto con molta
attenzione in base al contesto.
Anche l'inizializzazione dei centroidi può avere un impatto notevole sul risultato finale.
E' poi necessario decidere la metrica di distanza e la condizione di arresto (numero di iterazioni o convergenza)
Alcune versioni avanzate dell'algoritmo usano strategie di inizializzazione intelligenti per migliorare la
stabilità e minimizzare l'errore di inizializzazione.
In genere, l'interpretabilità dei risultati è fortemente legata solo a queste scelte iniziali.

Interpretazione dei risultati
Dopo l'esecuzione dell'algoritmo ogni clusetr è rappresentato da un centroide.
I punti vicini al centroide rappresentano i casi più tipici di quel cluster, ovvero tutti i dati che hanno
somiglianze tra di loro.
I punti lontani, invece, possono essere considerati outlier o casi speciali.
Analizzare la posizione e la distribuzione dei punti rispetto ai centroidi è fondamentale per trarre insight 
utili
Questo tipo di interpretazione è uno dei motivi per cui l'hard clustering è molto usato in pratica.

L'hard clustering è un approccio di tipo unsupervised, perchè non richiede etichette per funzionare.
Questo lo differenzia dai metodi supervisionati, che invece imparano da dati già etichettati.
In molti casi pratici, però, le due cosa possono essere combinate. Ad esempio, si possono usare i cluster
ottenuti dell'applicazione di un algoritmo come K-means per creare nuove feature da usare in un modello 
supervisionato. Oppure il cluster può essere utilizzato per andare a rilevare gli outlier
Questo approccio ibrido è molto usato nella costruzione di sistemi complessi di machine learning perchè la prima
parte permette di fare un primo setting applicando queste tecniche il la seconda parte di modelling può
utilizzre questi cluster.

Valutazione risultato finale
Anche se non ci sono delle etichette, esistono delle metriche per valutare la qualità di un clustering.
Due concetti importanti sono:
    - Coesione: misura quanto i punti interni ad un cluster sono vicini (quanto sono coesi) . Può anche essere
        visto come misura di densità di punti all'interno di un cluster
    - Separazione: misura quanto i cluster sono distinti/distanti tra loro, quanto è netta la separazione
        tra i cluster
Anche se nella prime fasi può bastare una valutazione qualitativa visiva, esistono metriche comunemente
usate per questo scopo, come Silhouette Score (quanto un cluster è magro, quanto i punti sono vicini tra
loro e non sparsi), Random Index o Adjusted Random Index.
Osservare i cluster graficamente è spesso sufficiente per capire se il risultato ha senso


"""
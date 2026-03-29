"""
k-NN & SVM

Algoritmo supervisionato basato sulla similarità tra punti.
Se devo classificare qualcosa e non so la regola, guardo i casi simili già visti.
Esempio: voglio capire se un cliente è 'buon pagatore', guardo i clienti simili (fatturato, settore,
storico pagamenti))
Questo è k-NN (k-Nearest Neighbors)
Il principio alla base è che punti simili (vicini) tendono ad avere etichette simili

k-NN è un algoritmo detto lazy (pigro), perchè non impare un trend (una formula), memorizza i dati, 
quando arriva un nuovo caso, cerca i k casi più simili, decide in base a loro.
Tutta l'elaborazione avviene in fase di predizione, analizzando i vicini più prossimi.
Questo rende il modello flessibile ma computazionalmente costoso

Il concetto chiave è la distanza, che definisce quanto due istanze sono simili
Distanze comuni sono: Euclidea, Manhattan, Minkowski

Ci sono due utilizzi:
1) clasificazione: la classe che si assegna ad ogni dato è quella più frequente tra i vicini, 
   esempio previsione cliente rischioso
2) regressione: il valore previsto è la media o mediana, dei vicini più prossimi, 
   esempio previsne vendite

Funziona bene in spazi di dimensione modesta e con feature numeriche scalate.
Spesso utilizzata come baseline per confrontare modelli più complessi.

Come funziona:
1. Scegli k (numero di vicini): consigliato prendere numero dispari, per evitare pareggi nella classificazione. 
   Un valore troppo piccolo di k rende il modello troppo sensibile al rumore (il modello segue troppo 
   da vicini i dati di training), mentre un valore troppo grande porta il modello ad essere più stabile 
   ma generalizza troppo, perdendo i dettagli locali. 
   Utile valutare diverse scelte di k, tramite la cross validation. k dipende dalla densità e dalla
   distribuzione dei dati (quanto sono sparsi nello spazio)
2. Calcoli la distanza del punto da prevedere con tutti gli altri punti(di solito medoto Euclidea).
3. Ordini per distanza in ordine crescente.
4. Prendi i k più vicini.
5. Decidi output: piu frequente per classificazione, media/mediana per regressione.
6. Restituisci il risultato come predizione finale.

k-NN dipende dalla scala dei dati e dalla scelta di k.
Feature irrilevanti possono distorcere o peggiorare la classificazione. In uno spazio con molte feature
la distanza tra i punti minimizza.
Se non standarizzi/normalizzi, sbaglia i risultati

Distanza Euclidea: misura la lunghezza della linea retta tra due punti (classica distanza geometrica).
Distanza Manhattan: somma le differenze assolute lungo ogni dimensione
Distanza Minkowski: generalizza entrambe ed introduce un parametro di potenza p
La scelta della metrica di distanza influenza fotemente la forma delle regioni di decisione (vicini)

Vantaggi
Semplicissimo, nessun training (non richede addestramento, riducendo la complessità iniziale), 
funziona bene con pochi dati, intuitivo, gestisce bene relazioni non lineari tra le feature, può adattarsi
a nuovi dati senza riaddestramento completo, utile come baseline o modelli a bassa complessità.
Svantaggi
lento su dataset grandi (confronta tutti i punti con tutti altri punti), sensibile al rumore, soffre
dimensioni alte, cioè troppe feature (curse of dimensionality), devi scegliere k bene, consuma 
parecchio risorse, predizone lenta con dataset grandi, sensibile alla presenza di rumore ed outlier,
non fornisce una funzione esplicita che descrive la relazione tra variabili.

k-NN spesso usato per analisi esplorativa, richiede pochi parametri, difficilmente utilizzato in
produzione, non crea un modello ma ha in ram tutti i valori precedenti, ed ad ogni nuova previsone
confranta sempre tutto con lo storico, i tempi pertanto esplodono.
Quindi k-NN spesso usato per capire i dati, non per soluzione finale da mettere in produzione

Confronto con altri algoritmi
k-NN vs Logistic Regression
- Logistic trova una formula
- k-NN guarda i vicini
Usa Logistic per pattern semplici

Parametri:
- n_neighbors: imposta il numero di vicini
- weights: determina compe ponderare i vicini (uniforme o in base alla distanza)
- metric: definisce la metrica di distanza (default Euclidea)
- p: controlla l'esponente della distanza Minkowski
Questi parametri consentono di adattare il modello a differenti geometrie dei dati.
- leaf_size: regola la dimensione dei nodi nelle strutture di ricerca
- n_jobs: consente di sfruttare più core per il calcolo parallelo
- algorithm: specifica il metodo di ricerca dei vicini (auto, ball_tree, kd_tree, brute)

"""
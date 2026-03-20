"""
LOSS FUNCTIONS E EMPIRICAL RISK MINIMIZATION

Funzioni di perdita (Loss functions)
Dopo aver scelto il modello è necessario un metodo per valutare quando bene esso stia imparando dai dati.
Questo metodo è la funzione di perdita (loss function L) che misura la differenza tra le predizioni del modello
e i valori reali dei dati (label).
E' il metro di errore utilizzato durante l'addestramento per migliorare la qualità del modello.
In quest'ottica, l'obiettivo è minimizzare la perdita per ottenere previsioni sempre più accurate.
Le loss function è una misura quantitativa dell'errore di predizione ottenuto quando si usa un'ipotesi
h per predire una label y di un data point descritto dalle feature x.
Formalmente è una funzione L (x,y) che restituisce un valore numerico dell'errore.
Più grande è l'errore L, peggiore è la predizione.
Costituisce un feedback guidando il processo di apprendimento e permettendo al modello di aggiornare
i propri parametri per ridurre l'errore di predizione.
Rappresenta la distinza della label dal valore effettivo

Esistono diverse tipologie di funzioni di perdita, ma ognune di essa è adatta a un diverso tipo di problema
e modello.
La scelta della loss function influenza direttamente l'apprendimento determinandno quali errori
vengono penalizzati.
Capire le differenze è fondamentale per decidere e progettare modelli robusti agli eerrori ed efficienti
nell'effettuare predizioni.
Le funzioni più comuni sono:
- 0/1 loss: utilizzata per classificazioni binarie, misura direttamene se la predizone del modello è corretta
    (l'errore è 0) o sbagliata (l'errore è 1). E' una funzione intuitiva, facile da interpretare, ma non 
    differenziabile, non pò esser usata per l'ottimizzazione durante l'addestramento.
- Absolute Error Loss (L1): misura la differenza assoluta tra la predizione del modello ed il valore reale.
    Penalizza in maniera lineare gli errori: un errore doppio produce una loss doppia. E' particolarmente
    utile quando si vuole che il modello sia robusto agli outlier, perchè grando scosamenti non dominano
    l'errore totale. Ottimizzare l'errore assoluto guida il modello a predire la mediano dei valori.
- Squared Error Loss (L2):misura il quadrato della differenza tra la predizione del modello ed il valore reale.
    Gli errore grandi vengono penalizzati molto più severamente agli errori piccoli, per via del quadrato
    della differenza. Pertanto non è una funzione robusta agli outlier, che possono avere un impatto
    sproporzionato sul modello. E' la loss più comune per problemi di regressione.
- Huber Loss: combina i vantaggi dell'absolute loss e della squared loss: quadratica per errori piccoli e 
    lineare per errori grandi. Il parametro stabilisce quando la loss passa da assoluta a quadratica.
    Mantiene entranbbi i vantaggi delle due funzioni loss precedenti.

Quale è la funzione migliore loss da scegliere? dipende da diversi fattori del problema, aspetti statistici,
aspetti computazionali, interpretabilità
La decisione non è mai banale e richiede di bilanciare esigenze statistiche, pratiche e interpretative.
La scelta della loss function che direge il modello, è la bussola che guida l'intero processo di apprendimento.
Scegliere la funzione di perdita significa definire il tipo di errore che si desidera minimizzare:
    - Squred Error loss: spinge il modello verso la media (più veloce ma sensibile outlier)
    - Absolute Error loss: spinge il modello verso la mediana (per lenta ma garantisce maggior robustezza ai dati rumorosi)
La scelta finale deve esssere allineata all'obiettivo di business: si preferisce l'accuratezza media
o la robustezza agli estemi?

Ci sono 3 punti di vista differenti da cui analizzare un problema di ml
1) dati: qualità, quantità, preprocessing e rappresentazione dei dati
2) modelli: scelta del modello per spazio di ipotesi e complessità di calcolo
3) perdite: misura dell'errore e guida all'ottimizzazione del modello.



"""
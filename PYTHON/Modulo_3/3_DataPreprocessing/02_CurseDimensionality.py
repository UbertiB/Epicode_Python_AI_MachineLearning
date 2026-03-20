"""
CURSE OF DIMENSIONALITY
Data reduction

La data reduction è una fase del preprocessing che ha come obbiettivo qualla di 
generare una reppresentazione del dataset più piccola in termini di volume.
Questo significa che si cerca di conservare solo le informazioni realmente utili
all'analisi, eliminando ridondanze e dettagli superflui che non aggiugono valore
ai dati.
E' una fase fondamentale per la scalabilità dei modelli di machine learning, perchè
consente di lavorare in modo efficiente anche con dataset molto grandi.
Ridurre i dati significa poter addestrare modelli più rapidamente, utilizzare meno
memoria e ottenere risultati anche più stabili.
E' particolarmente importante nel contesto dei big dati, dove processare tutto il set
completo può risultare impraticabile.
La data reduction è possibile su due fronti:
1) riducendo la cardinalità del set (righe)
2) riducendo il numero di attributi (colonne o feature)
Le tecniche principali sono Aggregation e Sampling (campionamento) per le righe,
e la Feature Selection/Extraction per le colonne.
E' importante sottolineare che la riduzione deve essere intelligente, il risultato
finale devo conservare le proprietà essenziali del dataset originale, così da garantire
risultati analitici simili, anche se si opera con meno dati.

Meno dati irrilevanti significano un apprendimento più stabile e previsioni
più affidabili, inoltre un dataset ridotto è più facile da interpretare e da
visualizzare permettendo un'analisi più intuitiva ed interpretabile dei risultati.

Un altro vantaggio della data reduction è il miglioramento della qualtà dei dati
riducendo osservazioni rumorose, incomplete o ridondandi.
Quando si rimuovono duplicati, fuori scala o incosistenti, il dataset diventa più
coerente ed il modello puo imparare realazioni più pulite.
In molti casi, un dataset più piccolo ma pulito, da risultati migliori rispetto 
ad un dataset enorme e disordinato.

Nel contesto dei big data, la data reduction è una necessità perchè alcuni database
sono impossibili da elaborare integramente (per problemi di grandezza dei dati)
In questi casi tecniche di sampling intelligente o aggregazione dinamica, permettono
di ottenere risultati analitici affidabili in tempi più brevi.
Ad esempio, nei sistemi di monitoraggio in tempo reale, si utilizzano tecniche di
stream sampling, dove i dati vengono 'campionati al volo' man mano che arrivano, 
mantentendo un set rappresentativo aggiornato.
Questo consente di prendere decisioni rapide senza dover attende l'alaborazione 
completa del flusso dati.

Ogni processo di riduzione comporta inevitabilmente un trade-off, cioè un compromesso.
Ridurre troppo può portare alla perdita delle informazioni utili, mentre ridurre poco
potrebbe non avere alcun effetto sull'efficienza.
La sfida quindi è trovare il punto di equilibrio tra dimensione del dataset e qualità
delle informazioni mantenute.
Un buon approccio è partire da una riduzione graduale e valutare come cambiano
le metriche di performance del modello: se i risultati restano stabili, la riduzione
è efficace.
Questa logica è molto simile al principio dell'empirical risk minimizazion dove
si cerca il punto in cui l'errore di generalizzaiozne è minimo.

AGGREGATION
E' una delle tecniche più utilizzate per gestire l'eccessivo volume dei dati
Consiste nel combinare due o più record (righe) o colonne (feature) in una singola
unità riassuntiva.
Si tratta di un processo di riassunto controllato dei dati, dove più osservazioni
vengono sintetizzate attraverso funzioni come media, somma, massimo o conteggio.
Questo processo riduce la cardinalità del set, cioè il numero di record da 
analizzare, o consente di concentrare l'attenzione sulle tendenze generali piuttosto
che sui dettagli lcoali.
L'aggregazione stabilizza il comportamento del sistema poiche diminuisce la variabilità
ed il rumore statistico
Uno degli obbiettivi principali dell'aggregazione è il cambio di scala: unendo unità
più piccole in entità più grandi, si passa da un livello micro ad uno più macro.
Questo consente al modello di concentrarsi sul quadro generale e di catturare
relazioni strutturali più stabili.

Il vantaggio è che i dati così aggregati sono più facili da interpretare, piu leggeri
da elaborare e meno soggetti a oscillazioni casuali.
Ovviamente bisogna sempre bilanciare la riduzione con la perdita di dettaglio: aggregare
troppo può nascondere informazioni utili:
    - nelle analisi geografiche si aggregano città in regioni, le regioni in stati, ecc
    - nei dati ambientali misurazioni orarie possono diventare medie giornaliere, mensili,
    annuali
    - nelle vendite si possono sommare transazioni giornaliere per negozio, così da
    analizzare l'andamento genearle, anzichè di ogni singolo acquisto

In un''aggregazione fatta bene la deviazione standard prima e dopo laggregazione non
dovrebbe cambiare, la distribuzione deve avere lo stesso andamento pur cambiando la
dimensione del dataset

SAMPLING 

(o campionamento)
Il sampling è la principale tecnica di riduzione del numero di record o istanze.
E' essenziale quando il dataset è così vasto che un'analisi intera diventa troppo
costosa o complessa dal punto di vista computazionale.
L'obbiettivo del sampling è crare un sottoinsieme rappresentativo del dataset originale, 
abbastanza piccolo da poter essere gestito facilmente, ma abbastanza informativo
da garantire risultati affidabili.

Il sampling è molto utlie non solo nelle fasi di analisi preliminare, ad es. per 
esplorare rapidamente la distribuzione dei dati, ma anche nell'analisi finale, 
soprattutto in applicazioni reali dove la quantità dei dati può raggiungere milioni 
di record/righe.
I principi chiave di un campionamento efficace sono:
    * se un campione è rappresentativo, il suo utilizzo funzionerà quasi altrettanto
    bene quanto l'utilizzo dell'intero dataset
    * un campione è rappresentativo se ha approssimativamente le stesse proprietà
    (di interesse per la ricerca) del dataset originale.

Esistono due tipi di sampling (simpe random sampling e sampling stratiticato)
1) SIMPLE RANDOM SAMPLING (SRS): è il metodo più semplice ma non garantisce la 
rappresentatività in caso di dataset sbilanciati; ogni record ha una probabilità
perfettamente uguale di essere selezionato. Può essere:
    - senza rimpiazzo: ogni volta che viene selezionato, in modo random un record, 
    viene anche rimosso dal dataset
    - con rimpiazzo: gli oggetti/record non vengono rimossi dal dataset, e lo 
    stesso oggetto può essere selezionato più di una volta.
2) SAMPLING STRATIFICATO: usato per assicurare la rappresentatività in presenza
di sottogruppi importanti. Si divide il dataset in partizioni omogenee (strati) in
base a una variabile chiave e poi si estraggono campioni casuali da ogni strato, 
mantenendo le proporzioni originali del dataset

Il sampling è vitale per i problemi di classi sbilanciate (es. frodi, malattie rare)
si usa spesso l'OVERSAMPLING, cioè duplicare i record delle classi minoritarie per
bilanciare i campioni e prevenire che il modello ignori la classe rara.

Conclusione.
La data reduciont è una strategia fondamentale per rendere l'analisi dei dati più
efficiente e gestibile, senza rinunciare alla qualità dei risultati
Le tecniche di aggregation e sampling sono solo le più comuni, ma rappresentano due
strumenti potentissimi per ridurre i dati mantenendo la loro essenza informativa.
In molti casi, un dataset ridotto, può portare a modelli più veloci, più interpretabili
e meno soggetti a overfitting, perchè si eliminano rumore e ridondanze inutili.
Ridurre i dati, quindi, non significa 'perdere informazione', ma ottimizzare
il contenuto per ottenere risultati più chiari e affidabili.

"""
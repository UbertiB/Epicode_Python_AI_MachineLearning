"""
ENCODING

Gli algoritmi di ml, per quanto sifisticati, non capiscono il linguaggio
umano: tutto ciò che non è numero deve essere tradotto in una forma che la macchina
possa elaborare.
Questa traduzione, o encoding, è un pò come insegnare a un computer una lingua
semplificata fatta solo di numeri.
Gli algoritmi di ML lavorano esclusivamente con valori numerici e non sono in grado
di processare stringhe di testo.
L'encoding è quindi un processo fondamentale che trasforma le variabili categoriche
(come nomi di città, colori, generi) in valori numerici.
In generale, la codifica è una forma di "data transformation", ma con un obiettivo
specifico: rendere leggibili le variabili testuali mantentendo il significato 
informativo.

Se non si codificano correttamente le categorie, il modello potrebbe interpretare
relazioni che non esistono.
Esempio se a rosso, verde, blu, assegniamo i valori 1, 2 e 3 l'algoritmo penserà
che blu>verde>rosso, cioè un ordine inesistente.
E' per questo che servono tecniche dedicate, pensate per rappresentare le
categorie senza introdurre ordini gerarchie o distanze artificiali.

Le principali tecniche per gestire variabili nominali sono:
    * One-Hot Encoding
    * Dummy Coding
    * Effect Coding
Queste trasformazioni evitano di introdurre relazioni inesistenti e aiutano a 
mantenere la coerenza statistica dei dataset.
Nei dataset codificati con tecniche come one-ho coding, questo accade perchè la 
somma delle colonne è costante: conoscere tutte tranne una permette di ricostruire
l'ultima.
La scelta del metodo di encoding, dipende anche dalla necessità di gestire la
multicollinearità, cioè la ridondanza tra le colonne.

La multicollinearità si verica quando una o più variabili sono altamente correlate
tra loro o addirittura prevedibili linearmente con le altre.
Gli effetti principali sono:
- Instabilità nei coefficienti dei modelli lineari o logistici (piccole variaizoni
  nei dati portano a grandi variazioni nei risultati)
- Perdita di interpretabilità, perchè non è più chiaro quale variabile spiega 
  realmente l'effetto.

Tecniche come Dummy Coding o Effect Coding vengono progettate proprio per rompere
queste dipendenze e garantire modelli stabili.

ONE-HOT ENCODING

Il One-Hot encodign è il metodo più intuitivo: trasforma ogni categoria in una
colonna separata, accendendo un interrutore (1) per la categoria attiva e lasciando
spento (0) tutti gli altri.
In pratica, si costruisce una matrice di interruttori binari:
- ogni riga descrive un'osservazione
- ogni colonna indica se quella riga appartiene a una determinata categoria.
E' un approccio estremamente chiaro: uno solo acceso (1), tutti gli altri spenti (0).

Il vantaggio è che ogni categoria è indipendente, non c'è rischio di imporre un
ordine o un legame numerico.
Tuttavia il numero di colonne può crescere rapidamente: un problema noto come
dimensionality explosion
In dataset reali, con centinaio di categorie (come città o codici prodotto), il
numero di colonne può diventare ingestibile.
Inoltre, poichè la somma delle colonne per ogni riga è sempre 1, si introduce
una dipendenza perfetta tra le colonne, creando la multicollinearità perfetta (una
può essere ottenuta dalle altre)

Vantaggi
- metodo più sicuro perchè elimina il rischio di imporre un ordine fittizio tra le categorie
- I dati mancanti possono essere codificati tramite vettori con tutto 0
Svantaggi
- Genera k nuove colonne per k categorie, creando un problema di alta dimensionalità
- il difetto principale è la multicollinearità perfetta (k gradi di libertà)

DUMMY CODING

Risolve il probelma del one-hot encoding eliminando una colonna, cioè scegliendo una
categoria di riferimento. 
Questa categoria funge da baseline: le altre colonne indicano quanto ogni categoria
'di discosta' dalla baseline. Si sceglie la colonna di riferimento.
In pratica, se omettiamo la categoria/colonna 'rosso', le colonne 'verde' e 'blu' 
saranno 0 solo quando l'osservazione 'rosso'
Questo piccolo trucco matematico rompe le dipendenza perfetta tra le categorie e 
permette al modello di stimare coefficienti stabili.
Se le categorie totali sono k: con one-hot crea k colonne, invece Dummy crea solo 
k-1 colonne.

I coefficienti non sono più assoluti, ma relativi rispetto alla categoria di 
riferimento. E' molto usato nelle regressioni lineari e logistiche, dove 
interpretare i coefficienti in termini di 'quanto cambia rispetto alla categoria
base' è più utile che in valore assoluto.
Ma bisogna fare attenzione alla scelta della categoria di riferimento: se ne scegli
una poco rappresentativa, il modello può sembrare 'squilibrato'.
Un modo intelligente per scegliere la categoria rappresentativa è scegliere la 
colonna più frequente o più neutrale.

Vantaggi
si previene la multiollinearità perfetta, migliorando la stabilità statistca dei
modelli come la Regressione (fondamentale per l'interpretazione dei coefficienti)
Svantaggi
Si introduce un bias di riferimento, poichè l'effetto di ogni categoria viene 
misurato relativamente alla categoria omessa (quella codificata con tutti 0), pertanto
i coefficienti non sono interpretabili in modo assoluto.
Inoltre non gestisce facilmente i dati mancanti (vettori tutti 0 sono già presenti
con la categoria di riferimento), mentre in on-hot encoding in presenza di valori
mancanti tutti i valori delle k categorie erano settati a 0

EFFECT CODING

L'effect coding è molto simile al Dummmy Coding, ma la categoria di riferimento 
viene rappresentata da un vettore di tutti valori settati a -1
Questo cambia il significato dei coefficienti del modello
L'effetto di una categoria non viene misurato rispetto a una baseline arbitraria (0,0),
ma rispetto alla media complessiva di tutte le categorie.

l'effect coding parte dallo stesso principio del Dummy Coding, ma cambia la logica
di riferimento.
Invece di confrontare ogni categoria con una baseline arbitraia, le confronta con 
una media generale di tutte le categorie
Questo approccio è particolarmente utile quando non esiste una categoria di riferimento 
'giusta', o quando tutte le categorie sono ugualmente importanti.
Ad es. in un sondaggio su più brand, non c'è un brand di riferimento: interessa
piuttosto capire se ciascun brand si comporta meglio o peggio della media complessiva.

E' una tecnica più interpretativa che predittiva, perchè offre una visione più
bilanciata degli effetti di ogni categoria.
Tuttavia, è meno immediata da leggere, perchè le colonne contengono valori -1 e 1:
l'intuizione del 1=si e 0=no viene meno
Inoltre può essere meno efficiente in contesti con molte categorie o grandi dataset
L'effect coding è molto apprezzato in statistica sperimentale, dove interessa capire 
quando ogni gruppo si discosta dalla media globale, non rispetto a un singolo gruppo

Vantaggi
Previne la multicollinearità perfetta
L'interpretazione dei coefficienti è più informativa, poichè misura la deviazione
di una categoria dalla media generale degli effetti (l'effetto principale): utile 
quando non esiste una categoria di riferimento logica
Si possono gestire i valori mancanti
Svantaggi
Può essere meno intuitivo da interpretare per chi non ha famigliarità con le 
statistiche, a causa dei valori negativi.
Il vettore con tutti -1 è costoso sia per l'archiviazione che per la computazione

Non esiste un metodo di encoding migliore in assoluto. La scelta dipende dall'algoritmo
usato e dalla necessità di interpretabilità dei coefficienti.
Per applicare nella pratica questi metodi di codifica si ua l'oggetto 
ONEHOENCODER di sklearn-prepocessing

Nei modelli interpretativi (come regressione) è fondamentale evitare la multicollinearita
quindi si preferisce Dummy o l'effect coding.
Nei modelli puramente predittivi (come le reti neurali o gli alberi decisionali), 
l'one-hote è spesso la scelta standard, perchè l'algoritmo non soffre la collinearità
nello stesso modo.
E' importante sottolineare che un encoding scorretto può annullare completamente
l'efficacia di un modello, anche molto sofisticato.
La fase di encoding deve sempre essere coerente tra trainig e nuovi dati: le stess
categorie devono essere trasformate nello stesso mdoo, pena errori in fase di
predizione.
"""
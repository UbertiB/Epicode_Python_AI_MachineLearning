"""
DATA TRANSFORMATION, DISCRETIZAZIONE, BINARIZATION

DATA TRANSFORMAZION
E' la fase in cui di adattano i valori delle feature per renderli idonei e 
comprensibili all'algoritmo.
E' una fase obbligatoria, poichè i dati gressi raramente sono pronti per l'apprendimento
automatico.
L'obbiettivo principale è garantire che l'input sia numerico e standarizzato,
trasformando i dati e cambiando la loro rappresentazione.
Un altro obiettivo è minimizzare i bias e migliorare la stabilità del processo di
training.
Inoltre risolvere i problenim lasciati aperti dalle fasi di Cleaning e Feature Engineering.

Spesso è qui che molto progetti falliscono: valori mancanti, stringhe o codifiche
incoerenti, possono impedire all'algoritmo di funzionare correttamente: come una
ricetta di cucina con ingredienti non puliti/tagliato o lavorati per quella ricetta.

TRASFORMAZIONI

Molti algoritmi di ML assumono che i dati seguano una certa distribuzione o abbiano
scale uniformi, soprattutto basati sulle metriche di distanza.
La trasformazione garantisce che queste assunzioni matematiche siano soddisfatte.
Le trasformazioni possono essere classificate in base al loro scopo:
- Trasformazioni di FUNZIONE: modificando la distribuzione dei dati (esempio logaritmica)
- Trasformazioni di STRUTTURA: cambiando tipo di variabile (es. continua in discreta)
- Trasformazioni di SCALA: uniformando i range dei valori (es. normalizzazione/standarizzazione)

TRASFORMAZIONI DI FUNZIONE

TRASFORMAZIONE LOGARITMICA
La Trasformazione Logaritmica (log(x)) è una trasformazione potente per correggere 
l'assimetria (skewness) nelle distribnuzioni dei dati.
Viene utilizzata quando i dati sono concentrati su valori bassi e hanno una lunga 
coda verso destra.
Rende la distribuzione più vicina a una forma normale, il che è cruciale per i 
modelli che assumono normalità, come la Regressione Lineare
La trasformazione logaritmica serve principalmente a comprimere valori grandi e
ridurre le differenze estreme tra i numeri.
In pratica si applica il logaritmo ai dati, invece di usare i valori originali.
Log(x)
questo cambia la scala dei dati
Esempio dati originali: 1,10,100,1000 dopo log(x) diventano 0,1,2,3
Passare da 1000 a 2000 è simile passare da 1 a 2 perchè sono più raddoppi.
Il log trasforma i raddoppi in incrementi quasi lineari.

La trasformazione logaritmica permette:
- Ridurre la skewness: molti dataset hanno distribuzione asimmetrica (esempio oridni cliente
  10,20,30,40,5000, il valore 5000 rovina la distribuzione e domina il modello). 
  Rende la distribuzione più vicina ad una forma normale
- Ridurre l'impatto degli outlier
- Rende lineari relazioni non lineari: molte relazioni sono esponenziali, se si applica
  il log, diventa una retta, e i modelli lineari funzionano meglio 
- Stabilizzare la varianza: molti modelli statistici funzionano meglio quando la
  varianza è costante.

Ricordarsi che la funzione log non accetta valori zero o negativi, per questo
spesso si usa log(1+x) in Python np.log1p(x)

In ERP i dati hanno spesso code lunghissime (pochi articoli fanno volumi enormi)
quindi l'applicazione del log diventa fondamentale per migliorare i modelli

TRASFORMAZIONE POLINOMIALE
La trasformazione polinoniale crea nuove feature elenando le feature esistenti a una
potenza.
Serve quando la relazione tra le variabili non è lineare, ma una curca. I modelli
lineari, come la regressione linceare, possono imparare solo relazioni del tipo
retta. Le trasformazioni polinomiale, permette di usare lo stesso modello lineare
per rappresentare curve.
Sebbene sia una tecnica di FE, è formalmente una trasformazione della feature stessa.
Il suo scopo è permettere ai modelli lineari di catturare relazioni non lineari tra
input e output.
Tuttavia, si deve fare attenzione all'eccessiva complessità e al rischio di overfitting,
che aumenta almeno di ordine quadratico.

RADICE QUADRATA
E' una tecncia di trasformazione dei dati simile alla trasforamzione logaritmica,
ma meno agressiva. Serve principalmente a ridurre l'assimetria della distribuzione positive
e a comprimere i valori grandi, ma senza schiaccialrli troppo.
Si prende il valore originale e si calcola la radice quadrata.
Esempio 1,4,9,16,25,100 dopo la trasformazione 1,2,3,4,5,10
I valori grandi si riducono, ma molto meno rispetto al logaritmo
Come per il logartimo si modifica la percezione della distanza del modello

FUNZIONE RECIPROCA
La formula è sempicissima y=1/x, si prende il valore originale e lo si sostituisce 
con il suo inverso
Una curca iperbolica, non lineare, puoi trasformarla in una relazione lineare usando 
il suo reciproco.
Il suo vero valore è linearizzare relazioni iperboliche
La trasformazione reciprova comprime moltissimo i valori grandi e amplifica invece
quelli piccoli 

Viene applicata quando la relazione tra le feature è il target è di tipo inverso.
Può essere utile per modellare tassi o proporzioni
Ha l'effetto di correggere l'assimetrica quando i dati sono concentrati su valori 
piccoli
Richiede cautela se i dati contengono valori prossimi o uguali a zero (divisione impossibile)


TRASFORMAZIONI DI STRUTTURA

Le trasformazioni di struttura non cambiano i valori delle variabili (come fa il log ecc)
Cambiano la struttura delle variabili nel dataset.
In altre parole modificano come sono organizzati i dati o come sono rappresentate le
variabili.
Sono operazioni di feature engineering.
Servono per rendere i dati utilizzabili dai modelli di ML.

Esistono alcune trasformazioni di struttura:
    * La DISCRETIZZAZIONE (o BINDING) converte le feature continue in categoriche
      discrete o intervalli range. L'intervallo di valori viene diviso in un numero 
      finito detto BIN. Esempio i dati di età possono essere convertite in range di età
      Il beneficio principale è la semplificazione delle relazioni che il modello
      deve apprendere. Rende il modello meno sensibile ai valori di input precisi e, 
      di conseguenza, agli outlier.
      E' una tecnica comune per gli algoritmi che lavorano meglio con dati categorici,
      come i Decision Tree
    * La BINARIZZAZIONE è una forma più semplice di discretizzazione. Converte una 
      feature in un valore binario (0 o 1), in base ad una soglia (threshold). E' 
      essenzialmente la creazione di un indicatore di presenza o assenza di una certa
      condizione.
      Viene spesso utilizzata per trasformare le feature di conteggio in attributi
      booleani.
    * La GENERAZIONE DELLA GERARCHIA DI CONCETTI organizza i dati in livelli di 
      astrazione. Questo processo fornisce una visione di livello superiore e facilita
      l'analisi. Esempio una feature CAP può essere astratta a 'Provincia' o 'Regione'
      E' utile per modelli che beneficiano di feature meno dettagliate.

TRASFORMAZIONI DI SCALA

Lo Scaling (trasformazioni di scala) è una trasformazione cruciale che agisce 
sulle feature numeriche per uniformare i valori.
E' essenziale per impedire che le variabili con un range più ampi dominino il 
processo di apprendimento.
Questa uniformità garantisce l'imparzialità per gli algoritmi che calcolano la distanza
o che utilizzano la discesa del gradiente.
Le trasformazioni di scala, a differenza rispetto alla trasformazioni viste fin ora,
non cambiano la forma della distribuzione di una singola colonna, servono a mettere
tutte le variabili (tutte le colonna) sulla stessa scale numerica.
Esempio prezzo: 10-200 quantita: 1-10 sconto: 0-0.2
In questo caso se usi algoritmi basati sulla distanza (KMeans, KNN,PCA) la variabile
prezzo domina completamente il modello perchè ha numeri molto più grandi rispetto
alle altrue due variabili (quantità e sconto). Le trasformazioni di scala servono
proprio ad evitare questo problema.
Le tecniche princopali sono:
    * Normalizzazione (Min-Max Scaling) che trasforma i valori in intervalli (0-1), 
      utile per KNN e reti neurali.
    * Standarizzazione (Z-Score) che centra i dati sulla media e scala secondo la
      deviazione standard, utile per regressioni lineari, funzionano principalmente
      settando la media a zero e la varianza a 1.

Applicare correttamente le trasformazioni di scala, significa assicurarsi che tutte
le feature dei dataset, contribuiscano in modo equilibrato al processo di apprendimento.
In molti algoritmi di ml, come quelli basati su distanza o gradienti, l'ampiezza 
numerica di una feature può influenzare in modo sproporzionato il risultato finale.
Scalare i dati consente di ripristinare le assunzioni matematiche degli algoritmi
di ml, che spesso presuppongono che tutte le variabili siano espresse su scale
comparabili o che abbiano distribuzioni simili.

Una variabile con valori tra 0 e 10_000 può 'dominare' una variabile che varia
solo tra 0 e 1, anche se quest'ultima ha un peso concettualmente più importante.
In questo caso diventa importante scalare i dati, prima di essere passati ai modelli.

Quando lo scaling viene trascurato, le conseguenze possono essere significative.
i confini decisionali dei modelli lineari o delle rete neurali, possono risultare 
distorti, rendendo difficile distinguere correttamente le classi o stimare il valore
di output.
Inoltre, la discesa del gradiente (processo di ottimizzazione) può diventare
estremamente lento o instabile, perchè l'algoritmo 'fatica' a muoversi in spazi
in cui le dimensioni hanno scale diverse. 
L'applicazione corretta dello scaling, è dunque un prerequisito per ottenere
modelli stabili, coerenti e accurati.
La trasformazione in scale è pertanto una vera e propria condizione necessaria per
permettere all'algoritmo di apprendere in modo equilibrato.
* Lo scaling (normalizzazione/standarizzazione) si occupa solo di aggiustare l'intervallo
  o la varianza dei valori
* L'encoding (codifica) si occupa di convertire le stringe categoriche in numeri.

Lo scaling riguarda esclusivamente i valori numerici: serve a regolare l'intervallo o
la varianza dei dati, mettendoli su scale comparabili.
E' un'operazione che agisce sull'aspetto quantitativo dei dati, ma non ne cambia
il significato.
Ad esempio, un reddito espresso in euro o migliaia di euro, rappresenta la stessa
informazione, ma su scale diverse: lo scaling serve a uniformare queste differenze 
per evitare che l'algoritmo venga influenzato dalla grandezza dei numeri.

L'encoding invece si occupa delle variabili categoriche, cioè trasforma le stringhe
o le etichette testuali in rappresentazioni numeriche in modo che l'algoritmo che 
lavora esclusivamente con numeri, possa 'comprenderle'.
Senza encoding, un modello non sarebbe in grado in interpretare valori categorici ( es.
rosso, blu, ecc) perchè sarebbero solo parole prive di significato matematico.

Queste trasformazioni sono quindi complementari: lo scaling garantisce uniformità
tra i numeri, mentre l'encoding permette di tradurre informazioni simboliche in 
forma numerica.
Insieme assicurano che l'algoritmo riceva in input dati coerenti, interpretabili e 
bilanciati.
In pratica, senza questa fase, anche un modello sofisticato, rischia di fallire, 
non per mancanza di potenza o complessità di calcoloma solo perchè non 'capisce' 
i dati.
E' come fornire istruzini in una lingua che l'algoritmo non parla, anche se 
intelligente non potrà mai eseguire il suo compito in modo corretto.



"""
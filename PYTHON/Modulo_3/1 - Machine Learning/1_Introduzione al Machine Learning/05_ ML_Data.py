"""
MACHINE LEARNING PROCESS: DATA, MODEL, LOSS

Ogni progetto di Data Science si base sull'interazione di tre elementi fondamentali:
1) Dati: rappresentano la base dell'indagine, sono il punto di partenza, la loro qualità e quantià 
    determina l'efficacia del modello.
2) Modello: sono gli strumenti matematici-statistici ed informatici che apprendono gli schemi e le 
    relazioni e pattern sottostanti i dati.
3) Funzioni di perdita (loss functions): misurano quanto le previsioni e generalizzazioni del modello
    si discostano dai valori reali.

Tra i 3 componenti (dati, modello, loss functions) è necessario un equilibrio, dati di qualità, modelli 
adeguati e funzioni di perdita appropriete portano risultati affidabili.
L'ottimizzazione di una sola delle componenti influisce anche sulle altre, creando un processo 
iterativo di miglioramento.
Se si migliora la qualità dei dati, anche il modello troverà relazioni più dettagliate e di conseguenza
ci saranno meno perdite.
L'obiettivo di questo ciclo iterativo è trovare un trade-off che minimizzi le perdite del modello (migliori
l'accuratezza delle previsioni del modello), sia ottimizzi le prestazioni del modello 
(sulla base di dati nuovi, quelle su previsioni che dovrà ancora fare)

DATI & DATASET
Per molti problei dovremmo focalizzare il nostro mindset non solo a migliorare il codice ma anche a 
migliorare la qualità dei dati.
Con 'dati' si intende una collezione di data points.
Con data points si intendono oggetti, registrazioni, casi, campioni, entità o istanze.
Il valore di un data point può essere: una persona, un'immagine, un segnale, ecc
In generale i data points portano delle informazioni:
    * Le features ('qualità'): proprietà ogettive di un data point (oggetto) spesso facili da 
        misurare e/o calcolare. Ad un data scientis interessano relativamento poco in se.
        basso livello di interesse
    * Le labels ('etichette'): difficili da misurare e/o determinare, alto livello di interesse.
        Sono il vero interesse di un data scientisc, sono proprio quelle che devono essere apprese
        da un algoritmo di ml
Nella pratica, distinguere questi due tipi di informazione a volta può risultare confusionario

Le FEATURES sono informazioni rilevati di un oggetto per distinguere un data point da un altro.
Possono essere valori numerici, categorici o testuali.
Molto spesso, per semplicità e comodità, vengono convertiti in valori numerici.
La scelta e la qualità delle feature influenzano fortemente le prestazioni di un modello.
Feature Engineering è il processo di trasformare, selezionare, o aggiungere features più utili al fine
della ricerca.
Una combinazione di feature viene descritta tramite una feature vector.

Le LABESL anche chiamate output variable, target, o response variable.
Sono frutto di una scelta di progettazione dei data scientist. Definire la label significa definire l'intero
tipo di problema. Se un data point ha pià di una label si affronta un problema multi-label per un multi-task
learning.
Possono essere: 
    - NUMERICHE: si affronta un task di REGRESSIONE 
    - CATEGORICHE: si affronta un task di CLASSIFICAZIONE
        - con due categorie: binary classification (es. getto o cane)
        - con tre o più categorie: multi-class classification

NUMERO DI FEATURES
Anche il numero delle feature di ogni data point influenza la qualità dei dati e, di conseguenza, tutta la
triade di componenti ML.
Non è consigliabile selezionare troppe feature, ma nemmeno poche: entrambe le scelte compromettono le prestazioni.
Usare feature importanti ma mancanti può determinare una scarsa accuratezza del modello.
Stesso effetto si ha utilizzando feature poco rilevanti, con il rischio aggiuntivo di incontrare 
nell'overfitting
Il numero corretto di feature va deciso considerando il compromesso tra complessità ed interpretabilità:
    - troppe poche feature rischiano di far perdere informazioni cruciali e peggiorare le perfomance del modello
    - troppe feature
        - richiedono più tempo e risorse per il calcolo
        - possono portare alla curse of dimensionality (fenomeno per il quale tanti più dati, tanto più
        difficile trovare dei pattern)
"""
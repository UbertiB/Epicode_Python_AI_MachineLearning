"""
Numpy è una libreria open source per colmare una lacuna di python:
la gestione efficiente dei dati numerici. Oggi diventato lo standard
in elaborazione scientifica dei dati, ed è alla base di Pandas,
Scipy, TensorFlow, e Scikit-learn.
Si appoggiano tutti a numpy per gestire i calcoli numerici.
Le liste sono ottime per piccoli dataset, non sono adatte per calcoli
su larga scala. 
Numpy sfrttando il linguaggio C su cui è basato, applica la velocità
delle operazioni vettoriali, in più numpy riduce la quantità di 
codice che si deve scrivere.
L'ggetto principale di numpy è l'array, simile alla vista, 
ma tutti gli elementi devono avere lo stesso tipo di dato, e questa 
caratteristica è ciò che arrende gli array molto veloci rispetto
alle liste
Gli array possono avere più dimensioni, non c'è limite al numero di dimensioni
gli array occupano molto meno spazio rispetto alle liste, i dati sono
memorizzati in blocchi contigui.
Quando ho l'array posso eseguire operazioni matematiche
+-*/ elemento per elemento es. a+b viene eseguita su tutto l'array
Per gli array multidimensionali supporta array 2d (matrici)
funzione reshape() per cambiare forma
funzione dot() per moltiplicare matrici
Tutto ciò è la base per il calcolo lineare ed il machine learning
NP ha funzionalità avanzate come random, calcolo medie, varianze,
deviazioni standard. Tutti indispensabili per il lavoro scientifico
dei dati (UFUNC).
Vantaggi:
veloce, efficiente, semplice, ci permete di lavorare con dataset
di grandi dimensioni.

"""
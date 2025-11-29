"""
Strumenti e flusso tipico di un progetto di data science.
La data science è un processo completo che unisce diverse discipline 
(statistica, informatica, conoscenza del contesto in cui si lavora
flusso standard:
1) Raccolta dati
2) Pulizia e preparazione
3) Analis esplorativa
4) Modellazione
5) Valutazione
6) Comunicazione risultati
Ognuna di queste fasi ha degli strumenti specifici che ci aiutano a lavorare.

1) Raccolta dati: diverse fonti csv, sql, nosql, json, api per dati da servizi esterni, web scrmbling direttamente dalle pagine web
Pandas ci mette a disposizione diverse funzioni per raccogliere i dati
, oppure riquest per recuerare dati da internete
, sqlarchemid per collegarci al database

2) Pulizia e preparazione: senza dati di qualità nessun progetto può partire. 
I dati devono essere affidabili. I dati reali sono quasi sempre "sporchi": 
mancanza dati, errori di battitura, formati sbagliati.
Quindi rimuovo o riempio i valori mancanti, poi converto i tipi di dati,
normalizzo e standarizzo i valori
Gli strumenti per far questo sono 1) Pandas 2) Numpy

3) Analisi esplorativa: Con i dati puliti si passa all'analisi esplorativa (ETA) l'obbiettivo
qui è di capire i dati, prima di costruire un modello. Si creano delle statistiche
descrittive, si raccolgono medie, deviazioni standard, ecc
Visualizziamo i dati con grafici
Gli strumenti sono 1) matplotlib 2) pandas per generare report esplorativi automatici.
Mi devo fare un'idea di come sono distribuiti i dati e ci guida le scelte delle 
fasi di modellazione

4) Modellazione: Dopo aver capito i dati arriva la modellazione, applico gli algortimi
di machine learning ed a secondo del tipo di problema da risolvere si decide l'algoritmo
distinguire tra spam è no spam, uso algoritmi di classificazione
se volgio prevedere un valore numerico (prezzo di una casa) entrano in gioco algoritmi di regressione
se voglio raggruppare dati simili tra di loro, utilizzo tecniche di clustering
skitlean (per ml classico) tensofor e pytorc per il deaplearning
Trasformo i dati in predizione e modelli utili

5) Valutazione: Devo capire quanto funziona un modello, dividendo il dataset da 
traning set e testset. Cosi' capisco se il modello è capace di generalizzare su dati nuovi
Se il modello funziona devo metterlo in produzione

6) Comunicazione risultati: rappresentazione dei risultati a chi deve prendere
delle decisioni. Gli strumenti sono tanti, notebook jumpyter, matplotlib, seaborn
ma anche Power BI o Tablau
La chiave è adattare il messaggio al pubblico.


"""
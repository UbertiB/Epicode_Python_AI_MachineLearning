"""
HEATMAP

La Heatmap è una tecnica di visualizzazione.
Una Heatmap è una matrice di valori rappresentata con colori. Ogni cella ha un valore numerico, e il colore 
rappresenta l'intensità del valore.
I numeri vengono trasformati in colori, per rendere le informazioni più immediatamente visibili.
Invece che leggere tabelle piene di numeri, i colori permettono di individuare rapidamento patterns, 
relazioni e anomalie.
Sono molto diffuse perchè semplificano l'interpretazione dei dati senza necessità di calcoli aggiutivi.
In un singolo grafico possiamo capire quali aree attirano l'attenzione e quali invece sono irrilevanti.
Per questo motivo sono uno strumento essenziale in analisi esplorativa e machine learning più in generale.

Possono essere utilizzate per:
    1) Analisi correlazioni, Correlation Matrix: ogni cella è una correlazione tra due variabili
    2) Confusion Matrix, Confusion Matrix
    3) Clustering, Cross Validation

Le heatmap sono usatissime nella analisi statistiche e nella ricerca scientifica.
In machine learning servono per visualizzare correlazioni, confusion matrix, e parametri più performanti.
In biologia vengono usate per confrontare l'espressione genica.
In economia evidenziano variazione delle performance tra aree e periodi.
Sono uno strumento versatile in tutti i contesti in cui i dati sono organizzati in forma matriciale.

Le heatmap visualizzano matrici: strutture con righe e colonne che si incrociano.
Ogni incrocio contiene un numero che viene colorato secondo una scala graduale.
Più intenso è il colore, maggiore è il valore oppure più forte è la relazione tra due variabili.
Il tipo di palette scelta influenza enormemente la comprensione del dato.
Una buona heatmap deve comunicare informazioni senza ambiguità

righe= entità (esempio art A, art B, art C, ecc)
colonne= variabili o dimensini (esempio quantità totale annua, n. ordini, quantita media ordine, 
        varianza quantità, massimo ordine, minimo ordine)
celle= valori, numeri
colore= funzione dei numeri.
La heatmap trasforma i numeri in colori

Una heatmap efficace è composta da una MATRICE chiara, una LEGENDA colori leggibile e VALORI ben allineati.
La scelta del RANGE CROMATICO deve essere coerente con il significato dei dati.
Gli assi devono essere etichettati chiaramente affinchè l'interpretazione sia immediata.
Spesso di aggiungono annotazioni numeriche per una maggiorE precisione.
Ogni elemento grafico serve a ridurre l'incertezza e facilita il confronto.

Le heatmap devono essere utilizzate quando i dati possono essere strutturati in forma tabellare con 
relazioni tra righe e colonne.
Sono ideali nella fase di Exploratory Data Analysis (EDA) che avviene prima della modellazione.
Trovano spazio anche dopo, nei processi di valutazione e tuning.
Sono utili per confrontare elementi e trovare pattern nascosti e si applicano in molti contesti di 
decision-making basati sui dati.
Se i dati hanno molte varibili, la heatmap può diventare troppo affollata e difficile da leggere.
La heatmap va sempre affiancata da analisi numeriche e statistiche più precise.

Le heatmap aiutano a comunicare i risultati anche a chi non ha un background tecnico.
Possono essere incluse in report e presentazioni per migliorare la trasparenza del modello.
Facilitano la comprensione delle decisioni prese dall'algoritmo.
In contesti professionali rafforzano la fiducia nella scelte tecniche presentate.
Sono quindi uno strumento potente per la parte interpretativa del machine learning.

Applicazioni delle Heatmap:

1) CORRELATION MATRIX (matrice di correlazione)

Una delle applicazioni più importanti delle Heatmap è la visualizzazione della matrice di correlazione.
Una matrice di correlazione indica quanto due variabili si muovono insieme.
Non è causa-effetto, è solo "si muovono insieme oppure no"
 - Valori posivici vicini a +1: indicano che le variabili crescono insieme in modo positivo
 - Valori negativi vicini a -1: indicano che una cresce quando l'altra diminuisce.
I colori rendono immediato individuare gruppi di variabili correlate.
E' un primo passo essenziale prima di costruire modelli predittivi, soprattutto nel caso della feature 
selection.

Parto da una tabella con più colonne (esempio ogni riga rappresenta un articolo le colonne rappresentano:
- vendite - prezzo - margine)
La matrice di correlazione confronta ogni colonna con tutte le altre.
La diagonale della matrice è sempre 1 (una variabile confrontata con sè stessa), la matrice è simmetrica,
quello che sta sotto la diagonale è identico a quello che sta sopra la diagonale (confronto vendite con 
prezzo e prezzo con vendite), si guarda sempre le coppie di variabili (es. vendite e prezzo, vendite e margine,ecc)
Da ricordare che la matrice non esprime la causa ma una relazione tra due variabili.
Esempio: le vendite dei gelati aumentano con l'aumento della tempoerature, ma non è la temperatura che
'causa' le vendite, è solo una relazione. Quindi non prendere decisioni basate solo da correlazioni.

Variabili molto correlate tra loro (che si influenzano reciprocamente) possono ridondare e peggiorare 
le performance del modello.
Una heatmap mostra subito quali colonne del dataset meritano di essere rimosse o trasformate.
Permettono anche di scoprire relazioni inattese che possono guidare nuove ipotesi.
E' quindi una tecnica sia analitica sia esplorativa.

La matrice di correlazione può anche essere usata per 'scoprire' variabili tra loro correlate. Se la matrice
da due variabili è vicino a 1, sono tra loro correlate e stai duplicanto la stessa informazione.

In pratica la matrice di correlazione serve per capire il dataset non per fare modelli direttamente.

Una volta generata le heatmap, bisogna concentrarsi sulle aree più intense.
Se sono presenti gruppi di varibili molto correlate tra loro, è consigliabile valutare di eliminarne
alcune.
Le variabili che non mostrano correlazioni significative potrebbero risultare poco utili al modello.
Anche valori estremi o sospetti possono indicare dati da revisionare
Ogni scelta nel modello dovrebbe avere una giustificazione basata sul grafico.

Una correlazione è una misura statisticha che quantifica la forza della relazione tra due variabili.
Esistono diversi modi per calcolare la correlazione, uno dei quali è la covarianza, che però dipende dalle
unità di misura delle variabili.
Per confrontare variabili diverse con covarianza, queste devono avere la stessa unità o essere normalizzate.
Il coefficiente di Pearson risolve il problema della normalizzazione, consentendo di rilevare correlazioni
lineari senza preoccuparsi delle scale delle variabili.
Tuttavia Perarson cattura solo relazioni lineari e può non identificare pattern più complessi.

Non tutte le relazioni tra variabili sono lineari e quindi Pearson può fallire nel rilevare correlazioni 
(es. relazione non lineare che si trova spesso è quella quadratica)
In questi casi entra in gioco la correlazione di Spearman, che utilizza i ranghi delle variabili invece dei 
valori grezzi.
Questo altro approccio consente di misurare relazioni monotone crescenti o decrescenti, anche non lineari.
Il coefficiente di Spearman assume valori:
    - -1 se è monotona decrescente
    - 0 se non esiste correlazione monotona
    - +1 quando la relazione è monotona crescente.
E' uno strumento prezioso per rilevare pattern nascosti da Peaerson non può cogliere, specialmente in 
dataset complessi o con comportamenti non lineari.

2) CONFUSION MATRIX

Un'altra applicazione della heatmap è la visualizzazione della matrice di confusione
Parti da un modello che deve classificare, esempio sano/non sano, cliente compra/cliente non compra.
Il modello fa previsioni, ma non ti basta sapere quante sono giuste, devi capire come sbaglia.
La confusion matrix è una tabella 2X2
righe=realtà
colonne=previsini
La confusion matrix divide:
Reale POS: 
    TP (true positive): reale positivo, predetto pos
    FN (false negative): reale positivo, predetto negativo
Reale NEG:
    FP (false positive): reale negativo, predetto positivo
    TN (true negative): reale negativo, predetto negativo

I colori evidenziano dove il modello effettua più errori e dove invece predice correttamente.
I valori sulla diagonale (TP, TN) rappresentano le predizioni corrette, mentre gli off-diagonal 
mostrano errori (FP, FN).
Con una heatmap si riconoscono subito le classi più problematiche.
E' uno strumento fondamentale nella valutazione della qualità del modello.

3) CROSS VALIDATION

Un'altra applicazione delle hatmap è nella cross validation, in particolare la GridSearch
Durante la Grid Search, le prestazioni dei modelli cambiano in base ai iperparametri testati.
Una heatmap può mostrare quali combinazioni offrono performance migliori.
La cross validation serve a valutare il modello.
La heatmap serve a visualizzare i risultati.
Le zone più "calde" indicano le scelte ottimali.
Questo permette di interpretare il processo di tuning con maggiore trasparenza.
Più i dati del tuning sono complessi, più la heatmap diventa utile per orientarci.

In Python è possibile costruire una heatmap in pochi passaggi usando le librerie Pandas e Seaborn
Prima di calcola la matrice di correlazione di tutte le varibili numeriche del DataFrame
    - corr=df.corr(numeric_only=True)
Poi si passa a Seaborn per la visualizzazione:
    - sns.heatmap(corr,annot=True)
        - genera giù un grafico chiaro e utile
        - annot=True aiuta a leggere i valori esatti senza sacrificare la visione d'insieme.
Questo semplice strumento è indispensabile nella fasi iniziali di analisi

Vantaggi:
le heatmap sono immediatamente ed estremamente intuitive.
Rendono visbili relazioni che nei numeri non si notano facilmente.
Possono riassumere una grande quantità di informazioni in un'unica figura.
Sono personalizzabili in base all'obiettivo delle studio
Risultano fondamentali nel collegare analisi tecnica e comunicazione visiva ed esplorazione dei dati.

Considerazioni
Una buona interpretazione inizia dalla legenda: indica come i colori rappresentano i dati.
Bisogna osservare la scala cromatica per capire se il grafico enfatizza le differenze.
E' importante controllare l'ordine delle variabili, perchè un diverso ordinamento può cambiare la perecezione
dei pattern.
Si devono interpretare i colori con logista statistica, non solo estetica.
La heatmap è utile se ci guida a decisioni basate su dati.

Prima di creare una heatmap, pulire e normalizzare i dati, questo perà va a migliorare la leggibilità della matrice
E' utile riordinare righe e colonne per evidenziare gruppi di valori simili.
Inserire annotazioni numeriche aiuta a evitare interpretazione errate.
Una heatmap deve sempre avere legenda e titolo chiari.
Ogni elemento grafico deve servire allo scopo, non alla decorazione.

Le heatmap sono strumenti essenziali per chi lavora con i dati e modelli predittivi.
Permettono di comprendere rapidamente correlazioni, errori, e risultati del tuning dei parametri.
Devono essere usate come supporto alla decisione, non come  unico criterio di valutazione.
La loro efficacia dipende dal modo in cui i colori e le informazioni vengono presentate.
Usate correttamente, rappresentano uno dei modi più potenti per trasformare dati grezzi in conoscenza.
"""
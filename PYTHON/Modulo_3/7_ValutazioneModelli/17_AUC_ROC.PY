"""
PERFORMANCE METRICS: AUC e ROC

E' un altra metrica delle performance
AUC-ROC misura quanto bene il modello riesce a distingue le classi.

ROC

Ho un modello che produce probabilità, devo decidere sopra di probabilità quale soglia considero 
'positivo'.
ROC è un grafico che mostra cosa succede cambiando soglia.
Come produco le probabilità del positivo?:
Le probabilità le produce il modello facendo model.predict_proba(X)
Il predict_proba restituisce, per ogni riga, una coppia di valori, la prima colonna è la probabilità 
classe 0 (negativo), la seconda colonna è la probabilità classe 1 (positivo)
Esempio
    predict_proba restituisce: [0.2,0.8] [0.7,0.3] [0.1,0.9]
    di questa coppie di valori, prendo solo la seconda colonna (probabilità classe 1)
    y_prod=model.predict(X_test)[:,1]
    Quindi nell'esempio precedente prendo 0.8, 0.3 ,0.9
    Queste sono le probabilità che usa ROC
    Quind il modello mi da le probabilità dei positivi, devo decidere sopra quale valore considerare
    positivo. Defaul 0.5 è quasi sempre sbagliato
    La soglia dipende dal contesto

Roc mi restituisce:
    - FPR (falsi positivi)
    - TPR (veri positivi)
    - Thresholds (le soglie)
Sull'asse X metto FPR (falsi positivi) e sull'asse y metto TPR (veri positivi)
Il punto ideal è FPR=0 TPR=1, falsi positivi=0 veri positivi=1
Il caso peggiore è l'opposto FPR=1 TPR=0, falsi positivi=1 veri positivi=0
La soglia ottimale che oscilla tra questi due valori, non è fissa ma dipende dal compromesso tra
falsi positivi e falsi negativi, dipende sempre dal contesto

AUC

Auc deriva da ROC e corrisponde all'area sotto la curva ROC
Viene disegnata  una diagonale (0,0)(1,1) e si osserva la parte di curva che sta sotto questa diagonale
La diagonale significa:
- al crescere dei falsi positivi (FPR),  asse x
- crescono allo stesso modo i veri positivi (TPR), asse y
Se il modello segue questa diagonae, sta 'indovinando a caso'
Quella retta corrisponde a TPR=FPR
Ogni volta che aumenti la soglia prendi più positivi, ma anche più negativi nello stesso modo
Sopra la diagonale il modello è buono, prende più veri positivi che falsi positivi
Sulla diagonale il modello è inutile, come lanciare una moneta
Sott la diagonale il modello sbaglia, classifica peggio del caso, modello inutile

Esempio
    1) dataset
    riga1: valore reale (y)=1 probabilità=0.9
    riga2: valore reale (y)=0 probabilità=0.8
    riga3: valore reale (y)=1 probabilità=0.7
    riga4: valore reale (y)=0 probabilità=0.2
    2 positivi, 2 negativi
    2) ordiniamo per probabilità
    0.9 (pos), 0.8 (neg), 0.7 (pos), 0.2 (neg)
    Ogni probabilità unica rilevata (np.unique(y_prob)) può diventare una soglia (questo perchè il 
    comportameto cambia solo quando 'superi' una probabilità presente nei dati)

ROC = tanti punti (FRP,TPR) (errori sui negativi, positivi corretti)
AUC = quanto è grande la curva sopra la diagonale
Curva buona TPR alto FPR basso
AUC misura quanto la curva sta 'in alto a sinistra'
AUC misura quanto il modello riesce a separare positivi e negativi
Il modello è pereftto quando AUC=1, cioè la curva sale subito in alto
Il modello è casuale quando AUC=0.5
Il modello è pessimo quanto AUC<0.5 ciao la curva sta sotto la diagonale

Il modello calcola le probabilità per ogni riga, e AUC usa queste probabilità
per valutare globalmente il modello

Praticamente il modello per ogni singolo caso, non si limita a dare 0 o 1
ma da la probabilità che il singolo caso sia positivo.
Risponde alla domanda: il modello distingue bene tra positivi e negativi?
E' un grqafico con i seguenti assi:
- X: False Positive Rage (FPR), quanti positivi veri riesco a predire
- Y: True Positive Rate (TPR), quanti negativi sbaglio classificandoli positivi

Ogni modello di classificazione predice delle etichette in base ai dati di input.
Valutare quanto siano corrette queste predizioni è fondamentale per capire se il modello funzione bene.
Alcune metriche come accuracy, precision e recall misura la performance a una soglia fissa di decisione.
Spesso però serve un''indicazione più completa che consideri tutte le possibili soglie.
AUC e ROC forniscono proprio questo: sono strumenti per capire come cambia la performance del modello 
al variare di questa soglia

In molti scenare il problema principale non è solo "quanto è preciso il modello"
Un classificatore può sembrare buone se guardiamo solo l'accuracy, ma fallire in modo critico su alcuni
casi importanti.
ROC permette di visualizzare il compromesso tra falsi positivi e veri positivi su tutte le soglie.
Questo è particolarmente utile quando le classi sono sbilanciate o alcuni errori sono più costi di altri.
ROC aiuta quindi a scegliere il miglior compromesso tra sensibilità e specificità in maniera informata.

"""
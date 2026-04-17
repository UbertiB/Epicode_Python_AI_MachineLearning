"""
PERFORMANCE METRICS: PRECISION

E' un'altra metrica per la valutazione dei modelli.
Rappresenta la proporzione di predizioni positive corrette (TP) sul totale delle predizioni positive 
effettuate (TP+FP).
Precisione= TP/(TP+FP)
Indica quanto sono affidabili i positivi che il modello segnala/predice.
In altre parole misura l'affidabilità delle predizioni positive, ma penalizza i falsi allarmi
In altre parole: tra quelli che il modello ha detto essere positivi, quanti sono davvero positivi?
Il valore migliore è 1, il valore peggiore è 0
1= tutti i positivi predetti sono positivi, alta affidabilità nelle predizioni positive
0= tuutti i positivi predetti sono negativi, il modello genera molti falsi positivi
La precision non si interessa della capacità del modello di trovare tutti i positivi.
Per questa ragione un modello può avere una precision alta ma ignorare molti casi realmente positivi (FP)
deve pertanto essere interpretata nel giusto contesto applicativo.
E' particolarmente utile quando è importante ridurre i falsi positivi
Un modello con alta precision identifica correttamente le istanze positive senza classificare 
erroneamente le negative come positive.
precision alta = pochi falsi positivi
penalizza i FP False Positive (cioè quelli che il modello ha predetto come falsi ma in realtà sono 
positivi)
E' possibile avere una precision alta, pochi errori ma perdo i casi cioè i FP
Scegli precision quando il costo del falso positivo è alto, esempio: bloccare clienti buoni, segnalare
frodi inesistenti, identificare una persona malata quando non lo è
In applicazioni come il rilevamento di malattie rare, la precision indica quante delle persone 
classificate come malate lo sono realmente.

La precision è complementare alla RECALL, che invece misura la capacità di identificare tutti gli
esempi positivi

In Python si implementa tramite precision_score del modulo metrics di scikit-learn
Richiede due vettori: - etichette reali - predizioni del modello
Altri parametri sono:
    - pos_label: definisce quale classe è quella "positiva" di cui calcolare la precizione
    - average: in problemi multiclasse si usa per scegliere come aggregare la precision per tutte
      le classi (default="binary")

Average = MICRO
Somma tutti i TP e FP globali, poi calcola la precision una sola volta 
    (TP_classeA+TP_classeB+TP_classeC)/(TP+FP)_classeA+(TP+FP)_classeB+(TP+FP)_classeC
Tratto tutto il dataset come un unico problema

Average = MACRO
Calcola precision per ogni classe, poi fa la media semplice (precisionA+precisionB+precisionC)/3
tutte le classi contano uguale

Average = WEIGHTED
Media pesata per numero di esempi
Al numeratore la precisione di ogni classe è moltiplicata per il numero di esempi poi di questo si
fa la somma
Le classi più grandi pesano di più

Average=None
Non fa la media, restituisce precisioni per ogni classe
output=[precision_A, precision_B, precision_C]

Micro e Macro sono più realistici su dati sbilanciati

Esempi Classificazione Binaria
    considerando un dataset di 20 esmpi
        - 12 appartengono alla classe A
        - 8 appartengono alla classe B
    ipotizzando che le predizioni del modello siano:
        TP=10, TN=6, FP=2, FN=2
    Precision=TP/(TP+FP)=10/(10+2)=10/12=83.33%
    Il modello, quando predice la classe A, predisce correttamente per 83.33% delle volte, 
    sbaglia circa 16.7% delle volte

Esempi Classificazione Multiclasse
    considerando il dataset di 9 rilevazioni
    y_true=(A,A,A,B,B,B,C,C,C)
    y_pred=(A.B.A.B.B.C.C.B.C)
    Classe A: TP=2 FP=1 Precision=2/(2+1)=2/3=66.67%
    Classe B: TP=2 FP=1 Precision=2/(2+1)=2/3=66.67%
    Classe C: TP=2 FP=1 Precision=2/(2+1)=2/3=66.67%
    La precision è la media delle precision di ogni classe= 66.67%

Vantaggi
E' molto utile quando il costo di un falso positivo è alto, come in diagnostico medico o frodo bancarie
Non tiene conto dei falsi negativi, quindi da sola può essere ingannevole se molti esempi positivi
vengono persi.
E' complementare alla recall e spesso si usa il F1_score per bilanciare precision e recall
Svantaggi
La precision ignora completamente i falsi negativi e può dare una visione incompleta del modello.
Un modello può ottenere altra precision non trovando quasi nessun positivo reale
Interpretare questo valore da solo può condurre a decisioni errate
E' necessario affincare recall o F1_score
La valutazione deve essere sempre basata sul contesto applicativo

Considerazioni
La precision fornisce una misura chiara dell'affidabilità delle predizioni positive.
Va sempre interpretata insieme ad altre metriche come recall e F1_score
In problemi multiclasse, può essere calcolata per ciascuna classe o usando micro/macro/ averaging
Aiuta a prendere decisioni informate sul bilanciamento tra falsi positivi e falsi negativi.

L'analisi completa dei modelli richiede di considerare precision, recall, accuracy e F1_score insieme


"""

from sklearn.metrics import precision_score

y_true=["A"]*12+["B"]*8
y_pred=["A"]*10+["B"]*8+["A"]*2

precision_A=precision_score(y_true,y_pred,pos_label="A")
precision_B=precision_score(y_true,y_pred,pos_label="B")

print(f"Precion A: {precision_A*100:.2f}")
print(f"Precion B: {precision_B*100:.2f}")

y_true=["A","A","A","B","B","B","C","C","C"]
y_pred=["A","B","A","B","B","C","C","B","C"]

precision_micro=precision_score(y_true,y_pred,average="micro")
precision_macro=precision_score(y_true,y_pred,average="macro")
precision_weighted=precision_score(y_true,y_pred,average="weighted")

print (f"Precisoni micro: {precision_micro*100:.2f}%")
print (f"Precisoni macro: {precision_macro*100:.2f}%")
print (f"Precisoni weighted: {precision_weighted*100:.2f}%")
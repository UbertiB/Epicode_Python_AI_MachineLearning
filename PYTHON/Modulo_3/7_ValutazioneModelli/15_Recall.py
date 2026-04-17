"""
PERFORMANCE METRICS: RACALL

E' un'altra metrica per la valutazione dei modelli.
Rappresenta la proporzione di predizioni positive corrette (TP) sul totale delle rilevazioni positive 
(TP+FN) (tutti i positivi reali).
recalle= TP/(TP+FN)
TP=true positive (un positivo predetto positivo)
FN=false negative (un positivo predetto negativo)
Indica quanti veri positivi riesci a trovare
Recall alto= perdi pochi casi positivi (casi importanti), il modello non si lascia scappare i positivi
Ciò che penalizza il modello sono i FN (False Negative), cioè i casi importanti (positivi) ma predetti
negativi.
recall= quanto sono affidabili i positivi
Recall= quanti positivi trovi sul totale dei positivi
Il valore migliore è 1 e il valore peggiore è 0

Scegli Recall quando il costo del FN è alto, fondamentale quando non puoi permetterti di perdere
eventi importanti.
E' particolarmente utile quando è importante ridurre i falsi negativi

Un modello con alto recall indivisua la maggior parte delle istanza positive senza trascurare esempi reali
In applicazioni come il rilevamento di malattie rare, la recall indica quante delle persone effettivamente
malate vengono correttamente diagnosticate.
La recall è complementare alla recall, che invece misura la correttezza delle predizioni positive
effettuate.

Un valore di recall vicino a 1 identifica che il modello identifica quasi tutti gli esempi di positivi
reali.
Un valore basso indica che il modello perde molti positivi, generando falsi negativi.
La Recall non si interessa della correttezza delle predizioni positive, ma della copertura dei positivi
reali.
Per questa ragione un modello può avere un recall elevato ma includere anche molti falsi positivi.
La recall, come la precision deve sempre essere interpretata nel guisto contesto applicativo, 
tenendo conto dei costi dei falsi negativi.

Considerando un sistema che segnala mail come spam:
    - Un elevato recall significa che quasi tutte le email realmente spam vengono identificate correttamente
    - Un basso recall implica che molte mail spam passano inosservate nella casella principale.
In un test diagnostico, un falso negativo può comportare la mancata individuazione di una malattia,
con rischi grazi per il paziente.
    - il recall aiuta a capire quando il modello cattura tutti i casi positivi reali
    - Un modello diagnostico con recall elevato riduce il rischio di predere esempi critici che 
      necessitano attenzione immediata

In Python si implementa tramite recall_score del modulo metrics di scikit-learn
Richiede due vettori: - etichette reali - predizioni del modello
Altri parametri sono:
    - pos_label: definisce quale classe è quella "positiva" di cui calcolare la precizione
    - average: in problemi multiclasse si usa per scegliere come aggregare la i recall per tutte
      le classi (default="binary")

Average = MICRO
Somma tutti i TP e FN globali, poi calcola la recall una sola volta 
    (TP_classeA+TP_classeB+TP_classeC)/(TP+FN)_classeA+(TP+FN)_classeB+(TP+FN)_classeC
Tratto tutto il dataset come un unico problema

Average = MACRO
Calcola recall per ogni classe, poi fa la media semplice (recallA+recallB+recallC)/3
tutte le classi contano uguale

Average = WEIGHTED
Media pesata per numero di esempi
Al numeratore il recall di ogni classe è moltiplicata per il numero di esempi poi di questo si
fa la somma
Le classi più grandi pesano di più 

Average=None
Non fa la media, restituisce recall per ogni classe
output=[reacall_A, reacall_B, recall_C]

Micro e Macro sono più realistici su dati sbilanciati

Esempi Classificazione Binaria
    considerando un dataset di 20 esempi
        - 12 appartengono alla classe A
        - 8 appartengono alla classe B
    ipotizzando che le predizioni del modello siano:
        TP=10, TN=6, FP=2, FN=2
    Recall=TP/(TP+FP)=10/(10+2)=10/12=83.33%
    Il modello, quando predice la classe A, predisce correttamente per 83.33% delle volte, 
    Il modello non riesce ad identificare circa 16.7% dei casi reali della classe A

Esempi Classificazione Multiclasse
    considerando il dataset di 9 rilevazioni
    y_true=(A,A,A,B,B,B,C,C,C)
    y_pred=(A,B,A,B,B,C,C,B,C)
    Classe A: TP=2 FN=1 Recall=2/(2+1)=2/3=66.67%
    Classe B: TP=2 FN=1 Recall=2/(2+1)=2/3=66.67%
    Classe C: TP=2 FN=1 Recall=2/(2+1)=2/3=66.67%
    La Recall è la media delle recall di ogni classe= 66.67%

Vantaggi
Indica quandi positivi reali sono stati individuati dal modello
Riduce il rischio di falsi negativi anche in contesti critici
Permette di valutare l'efficacia del modello anche in dataset sbilanciati
Si combina con Precision e F1-Score per ottenere una valutazione completa
Svantaggi
Non tiene conto dei falsi positivi, quindi un Recall alto può nascondere predizioni errate frequenti
Da solo non da indicazioni sulla qualità complessiva delle predizioni
Serve confrontarli con altre metriche per avere una visoine completa delle performance del modello

Recall è fondamentale quando 'perdere' un positivo ha costi elevati
Serve sempre affiancarlo a Precision e F1-Score per valutare l'equilibrio tra copertura e accuratezza.
La scelta di dare priorità al Recall dipende dal contesto applicativo e dai costi relativi di falsi
positivi e falsi negativi.
Recall è uno strumento chiave per selezionare modelli sensibili ai positivi reali
L'interpreatzione corretta di Recall permette decisioni informate nella valutazione delle performance
del modello.
"""


from sklearn.metrics import recall_score

y_true=["A"]*12+["B"]*8
y_pred=["A"]*10+["B"]*8+["A"]*2

recall_A=recall_score(y_true,y_pred,pos_label="A")
recall_B=recall_score(y_true,y_pred,pos_label="B")

print(f"Recall A: {recall_A*100:.2f}")
print(f"Recall B: {recall_B*100:.2f}")

y_true=["A","A","A","B","B","B","C","C","C"]
y_pred=["A","B","A","B","B","C","C","B","C"]

recall_micro=recall_score(y_true,y_pred,average="micro")
recall_macro=recall_score(y_true,y_pred,average="macro")
recall_weighted=recall_score(y_true,y_pred,average="weighted")

print (f"Recall micro: {recall_micro*100:.2f}%")
print (f"Recall macro: {recall_macro*100:.2f}%")
print (f"Recall weighted: {recall_weighted*100:.2f}%")
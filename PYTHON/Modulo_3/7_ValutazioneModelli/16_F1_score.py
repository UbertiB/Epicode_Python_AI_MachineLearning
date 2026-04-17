"""
PERFORMANCE METRICS: F1 SCORE

F1-score=equilibrio tra precision e F1_score

F1=2*(Precision*F1_score)(Precision+F1_score)
Quanto il modello è bravo sia a non sbagliare (precision), sia a non perdere casi importanti (F1_score)
Solo precision o solo F1_score possono ingannare

La F1-score rappresenta la media armonica tra pecision e F1_score, fornendo una misura unica dell 
equilibrio tra accuratezza delle predizioni positive e copertura dei positivi reali.
E' particolarmente utile quando è necessario bilanciare il rischio di falsi positivi e falsi negativi.
Un modello con alta F1-score indica che riesce a identificare correttamente le istanze positive sia
a minimizzare gli errori sulle predizioni positive.
La F1-score è complementare a precision e F1_score, sintetizzando in un solo valore la loro performance
combinata

Il valore migliore è 1
Il valore peggiore è 0

Questa formula evidenzia l'equilibrio tra correttezza delle predizioni positive e copertura dei positivi
reali.
Un modello con molti falsi positivi o falsi negativi avrà rapidamente un F1-score basso, mostrando
quanto il modello sia inefficace nel bilanciare precision e F1_score

Un valore di F1-score vicino a 1 indica che il modello mantiene un buon equilibrio tra precision e F1_score
Un valore basso indica che il modello fallisce nel bilanciare correttezza delle predizioni positive
e copertura dei positivi reali.
La F1-score considera sia i falsi positivi sia i falsi negativi, sintetizzando la performance complessiva.
Per questa ragione un modello può avere precision o F1_score elevati separatamente, ma un F1-score
basso se non bilancia entrambi.
La F1-score deve sempre essere interpretata nel giusto contesto applicativo, tenendo conto dei costi
dei falsi positivi e dei falsi negativi.

Considerando un sistema che segnala email come spam:
    - Un elevato F1-score indica che il modello riesce sia a identificare correttamente le mail spam
      sia a minimizzare gli errori sulle predizioni positive.
    - Un basso F1-score segnala che il modello o perde molte email spam, o genera troppi falsi allarmi
In un test diagnostico, un basso F1-score può indicare che il modello non bilancia correttamente falsi
positivi e falsi negativi, aumentando il rischio per il paziente.
    - La F1-score aiuta a capire quanto il modello equilibra la copertura dei positivi reali e
      l'affidabilità delle predizioni
    - Um modello con F1-score elevato riduce sia il rischio di falsi allarmi, sia quello di mancati
      rilevamenti critici

Esempio
    modello A
    precision=100% (tutto quello che predice positivo lo è realmente)
    F1_score=10% (tra tutti ipositivi solo il 10% è predetto)
    Il modello A è perfetto quando segnala un positivo ma trova pochissimi casi (10%)
    modello B
    precision=50% (dei positivi che predice solo il 50% lo è realmente)
    F1_score=90% (di tutti i positivi ne trova correttamente il 90%)
    Trova quasi tutti i positivi (90%) ma sbaglia spesso (50%) dei positivi che predice tanti in realtà
    sono negativi

Per dire quale dei due modelli è il migliore, entra in gioco F1
    modello A
    F1=18%
    modello B
    F1=64%

In Python si implementa tramite f1_score del modulo metrics di scikit-learn
Richiede due vettori: - etichette reali - predizioni del modello
Altri parametri sono:
    - pos_label: definisce quale classe è quella "positiva" 
    - average: in problemi multiclasse si usa per scegliere come aggregare F1-score per tutte
      le classi (default="binary")
    - labels: lista dellel classi quando average è non binary

Esempi Classificazione Binaria
    considerando un dataset di 20 esempi
        - 12 appartengono alla classe A
        - 8 appartengono alla classe B
    ipotizzando che le predizioni del modello siano:
        TP=10, TN=6, FP=2, FN=2
    F1_score=2*(Precision*f1_score)/(Precision + f1_score)=83.33%
    Il modello bilancia precision e f1_score catturando correttamente circa 83.33% dei positivi reali
    e commettendo relativamente pochi falsi positivi.

Esempi Classificazione Multiclasse
    considerando il dataset di 9 rilevazioni
    y_true=(A,A,A,B,B,B,C,C,C)
    y_pred=(A,B,A,B,B,C,C,B,C)
    Classe A: TP=2 FN=1 F1_score=66.67%
    Classe B: TP=2 FN=1 F1_score=66.67%
    Classe C: TP=2 FN=1 F1_score=66.67%
    La F1_score è la media delle F1_score di ogni classe= 66.67%    

Vantaggi
F1-score bilancia precision e recall in un unico valore, utile quando entrambi sono importanti
E' particolarmente indicata in problemi di classi sbilanciate, dove l'accuracy può risultare fuorviante.
Aiuta a identificare rapidamente se un modello commette troppi falsi positivi o falsi negativi.
Consente confronti rapidi tra modelli diversi valutando complessivamente la loro efficacia sulla classi
critiche.
Sintetizza la performance complessiva senza concentrarsi solo su TP o FP
Svantaggi
Non distingue tra falsi positivi e falsi negativi: due modellli con errori diversi possono avere la 
stessa F1-score.
Non tiene conto della distribuzione delle classi: un modello con poche istanze può dominare il punteggio
medio.
Può essere meno intuitiva rispetto a precision o recall singolarmente per comunicare risultati concreti.
In problemi multilabel o multiclasse, è necessario scegliere average, che può cambiare il valore in 
modo significativo.
Non fornisce informazioni sulla performance assoluta per ogni singola classe senza un'analisi aggiuntiva.

La F1-score sintetizza in un unico valore la capacità del modello di essere sia preciso sia completo
nel riconoscere gli esempi positivi.
E' particolarmente utile quando è necessario bilanciare il rischio di falsi positivi e falsi negativi, 
come in ambito medico o rilevamento frodi, o altri come rilevamenti intruzione in cyber security.
Valori elevati indicano un buon equilibrio tra precision e recall, mentre valori bassi evidenziano 
criticità nella classificazione.
Va sempre integrata insieme ad altre metriche, come precision, recall, accuracy, per avere una visione
completa delle prestazioni del modello, per avere un quadro completo della classificazione.
In contesti multilabel o multiclasse, scegliere correttamente il tipo di aggregazione è fondamentale
per rappresentare fedelmente la performace del modello
"""


from sklearn.metrics import f1_score

y_true=["A"]*12+["B"]*8
y_pred=["A"]*10+["B"]*8+["A"]*2

f1_score_A=f1_score(y_true,y_pred,pos_label="A")
f1_score_B=f1_score(y_true,y_pred,pos_label="B")

print(f"f1_score A: {f1_score_A*100:.2f}")
print(f"f1_score B: {f1_score_B*100:.2f}")

y_true=["A","A","A","B","B","B","C","C","C"]
y_pred=["A","B","A","B","B","C","C","B","C"]

f1_score_micro=f1_score(y_true,y_pred,average="micro")
f1_score_macro=f1_score(y_true,y_pred,average="macro")
f1_score_weighted=f1_score(y_true,y_pred,average="weighted")

print (f"f1_score micro: {f1_score_micro*100:.2f}%")
print (f"f1_score macro: {f1_score_macro*100:.2f}%")
print (f"f1_score weighted: {f1_score_weighted*100:.2f}%")
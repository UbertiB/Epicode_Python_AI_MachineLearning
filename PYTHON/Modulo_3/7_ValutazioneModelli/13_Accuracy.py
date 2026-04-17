"""
PERFORMANCE METRICS: ACCURACY

l'Accuracy è un'altra metrica di performance.
Rappresenta la proporzione di osservazioni correttamente classificate rispetto al totale.
E' una misura intuitiva che indica quanto il modello predice correttamete in generale.
Non distingue tra classi positive e negative, ma considera tutte le predizione corrette.
E' utilizzata come indicatore preliminare della bontà del modello.
Permette un confronto rapito tra modelli simili senza addentrarsi nei dettagli dei singoli errori.

L'accuracy si calcola come il rapporto tra predizioni corrette (positive e negativo) e 
toale delle osservazioni.
In un contesto binario, è espressa come:
Accuracy=(TP+TN)/(TP+TN+FP+FN)
Mostra in modo chiaro la percentuale di esempi classificati correttamente.
E' semplice da interpretare e comunicare anche a non esperti.

Non riflette, però, la distribuzione delle classi e può essere fuorviante con dataset sbilanciati.

In python si utilizza il modulo metrick di scikit-learn.
Esistono due tipi di metriche:
    1) ACCURACY_SCORE: restituisce la proporzione complessiva di predizioni corrette sul totale. 
       Non tiene conto dello sbilanciamento tra classi.
       Può sovratimare le prestazioni se una classe domina
    2) BALANCE_ACCURACY_SCORE: calcola l'accuracy normalizzata per ogni classe e poi effettua la media
       di tutte le accuracy, questo fornisce una visione più realistica della capacità del modello 
       di identificare correttamente tutte le classi ed è utile soprattuto in caso di dataset sbilanciati
Entrambi gli oggetti richiedono due vettori: - etichette reali - predizioni del modello, in modo da
calcolare la confuzion-matrix e vedere i casi di TP,TN,FP,FN

La matrice può essere visualizzata con seaborn.heatmap per evidenziare gli errori.

L'uso combinato delle metriche e della matrice, consente di avere una panoramica completa delle 
prestazioni del modello, aiutando a prendere decisioni più informate durante il tuning dei parametri 
o la selezione dei modelli

Classificazione binaria:
    considerando un dataset di 20 esempi in cui:
    - 12 appartengono alla classe A
    - 8 appartengono alla classe B
    ipotizando che le predizioni del modello siano:
        TP=10, TN=6, FP=2, FN=2
    Accuracy=(10+6)/(10+6+2+2)=16/20=80%
    Il modello classifica correttamente l'80% degli esempi totali

Classificazione Multiclasse:
    considrando un dataset di 9 esempi così composto:
        1: valore effettivo A; valore predetto A -> Classe A=TP Classe B=FP Classe C=FP
        2: valore effettivo A; valore predetto B -> Classe A=TN Classe B=FN Classe C=FN
        3: valore effettivo A; valore predetto A -> Classe A=TP Classe B=FN Classe C=FN
        4: valore effettivo B; valore predetto B -> Classe A=FP Classe B=TP Classe C=FP
        5: valore effettivo B; valore predetto B -> Classe A=FP Classe B=TP Classe C=FP
        6: valore effettivo B; valore predetto C -> Classe A=FN Classe B=TN Classe C=FN
        7: valore effettivo C; valore predetto C -> Classe A=FP Classe B=FP Classe C=TP
        8: valore effettivo C; valore predetto B -> Classe A=FN Classe B=FN Classe C=TN
        9: valore effettivo C; valore predetto C -> Classe A=FP Classe B=FP Classe C=TP
    Classe A: TP=2
    Classe B: TP=2
    Classe C: TP=2
    Accuracy=(2+2+2)/9=6/9=66.66%
    Il modello classifica correttamente questo dataset quasi al 70%

Vantaggi
E' intuitiva e facile da interpretare 
Fornisce una misura globale di correttezza del modello
Permete un confronto rapito tra modelli simili
Può essere calcolata facilmente a mano o in Python
E' utile come indicatore preliminare delle prestazioni
Svantaggi
Non riflette la distribuzione delle classi in caso di dataset sbilanciati.
Può dare risultati fuorvianti se una classe è dominante
Non evidenzia quali errori hanno maggior impatto nel contesto applicativo
Non distingue tra falsi positivi e falsi negativi
Non sempre è sufficiente per decidere quale modello scegliere

Considerazioni: Dataset Sbilanciato
Considerando un dataset di 10.000 esempi:
  - 100 appartenenti alla classe A
  - 9.900 appartenenti alla classe B
Un modello che predice sempre la classe B ha un accuracy del 99%
Tuttavia, nessun esempio della classe minoritario (classe A) viene rilevato correttamente
Questo evidenzia come l'accuracy possa essere ingannevole se non si considera l'importanza relativa
delle classi.
In contesti sensibili (es. diagnosi medica) misclassificare esempi di una classe rara può avere
conseguenze gravi.
E' quindi necessario valutre metriche alternative quando la rilevanza delle classi è diversa.

L'accuracy fornisce una visione generale delle prestazioni del modello.
E' particolarmente utile in contesti con classi bilanciate
Serve come primo passo prima di considerare metriche più specifiche
Permette di confrontare modelli diversi senza analizzare ogni singolo errore.
E' un indicatore essenziale ma deve essere sempre interpretato nel contesto dei dati.

"""

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, balanced_accuracy_score

y_true=["A"]*12+["B"]*8
y_pred=["A"]*10+["B"]*8+["A"]*2

accuracy=accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")

y_true=["A","A","A","B","B","B","C","C","C"]
y_pred=["A","B","A","B","B","C","C","B","C"]

#in questo è multiclasse pertanto utilizzo balance_accuracy
accuracy=accuracy_score(y_true, y_pred)
balanced_accuracy=balanced_accuracy_score(y_true, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")
print(f"Balance Accuracy: {balanced_accuracy*100:.2f}%")
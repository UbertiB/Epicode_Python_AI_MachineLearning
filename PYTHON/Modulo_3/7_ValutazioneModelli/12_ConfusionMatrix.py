"""
PERFORMANCE METRICS: CONFUSION MATRIX

Quando si valuta un modello di machine learning, bisogna distinguere tra loss e metriche
Le LOSS sono pensate per la macchina: servono a minimizzare l'Empirical Risk Minimization (ERM) e a 
ottimizzare i parametri del modello.
Le METRICHE, invece, sono pensate per gli esseri umani: permettono di capire la qualità del modello
e guidano la scelta degli iperparametri.
In pratica, le loss guidano l'apprendimento, le metriche guidano la valutazione e la selezione del
modello.
E' importante tenere questa distinzione chiara prima di entrare nelle metriche di classificazione.

Per valutare un modello supervisionato si considerano più punti di vista:
    - Efficienza: riguarda i tempi esecuzione, per es. quanto tempo serve per costruire il modello 
      e per fare previsioni
    - Scalabilità: indica se il modello regge con dataset grandi o con molte variabili (più dimensioni)
    - Robustezza: considera la sensibilità a rumore, dati mancanti o outlier
    - Interpretabilità: valuta quando sia chiaro il comportamento del modello e quando si a compatto.
 Un'altra dimensione fondamentale è la qualitù della predizione, per problemi di:
    - Regressione: si possono usare metriche come il Mean Squared Error (MSE) o il Mean Absolute Error 
      (MAE)
    - Classificazione: invece si usano altre metriche specifiche, che misurano quanto il modello 
      distingue correttamente le classi
Questa qualità indica se il modello è utile in contesti reali, oltre che performante matematicamente.
Capire la qualità della predizione è il passo successivo alla valutazione di efficienza e robustezza.

Per la classificazione si considerano metriche che misurano la correttezza delle predizioni:
    - Confusion Matrix: che mostra come il modello classifica ogni esempio
    - Accuracy: percentuale di predizioni corrette sul totale
    - Precision, Recall, F-measure: sia per classe singola sia mediate su tutte le classi
    - ROC Curves: per analizzare il compromesso tra veri positivi e falsi positivi.
Queste metriche permettono di confrontare diversi modelli e scegliere quello più adatto.


CONFUSION MATRIX

La Confusion Matrix è una tabella che mostra il numero di esempi classificati correttamente e quelli
classificati erroneamente.
Si usa per valutare un modello di classificazione (valori discreti/categorie), quando l'output del
modello è una categorie

Esempio:
valuto 0/1, valuto si/no,valuto difettoso/non difettoso.
Se, invece , ho un problema di regressione (output numero continuo) è un problema di regressione e
non uso confuzion Matrix per la valutazione, ho altri velutatori che vediamo dopo.
Una regressione può essere traformata in una classificazione, esempio vendite >1000 alto <1000 basso, 
in questo caso va bene anche confusion matrix per la valutazione

Se devo prevedere una categoria, siamo sempre nel campo della classificazione (non regressione), 
in questo caso devo mettere una classe contro tutte.
Esempio se deve prevedere il tipo di fiore (setosa, versicolor, virginica) posso prendere il valore
di classe "setosa" e dire che sotosa è positiva mentre le altre negative.
Poi mi sposto sulla classe "versilore" e dire che versicolor è positiva le altre negative, e così via.

Consente di distinguere tra 4 diversi casi di classificazione
Fornisce una panoramica dettagliata delle prestazioni di un classificatore.
Permette di identificare quali classi vengono predette correttamente e quali vengono confuse.
Costituisce la base per il calcolo delle principali metriche di valutazione.

Se ho una 

La matrice, di dimensioni 2X2, include 4 parametri:
    - TN: True Negative
    - FP: False Positive
    - FN: False Negative
    - TP: True Positive
Ogni cella, di questa matrice, rappresenta il conteggio dei casi corrispondenti
La diagonae principale (in alto a sinistra a in basso a destra) mostra le predizioni corrette
Tutte le altre celle, al di fuori di questa diagonale mostrano errori del modello
La matrice consente un'analisi dettagliata e completa delle prestazioni

Parametri TN
True Negative (TN) indicano casi negativi identificati correttamente del modello.
Permettono di valutare la capacità del modello di evitare flasi allarmi.
Un numero elevato di TN evidenzia una buona selettività nelle predizioni negative.
Aiutano a comprendere quanto il modello mantiene sotto controllo gli errori di tipo falso positivo.
contribuiscono a una valutazione equilibrata delle prestazioni complessive.
Parametri FP
False Positive (FP) si verifica quando un caso negativo viene classificato erroneamente come positivo.
Questo tipo di errore può avere conseguenze significative in contensti sensibili.
Un numero elevato di FP indica che il modello tende a segnalare falsi allarmi.
Aiuta a individuare limiti nella capacità del modello di distinguere correttamente le classi.
Permette di valutare il rischio di sovrastimare eventi positivi.
Parametri FN
False Negative (FN) si verificano quando un caso positivo non viene identificato correttamente.
Rappresentano casi incui eventi importanti sfuggono al modello.
Un numero eleavato di FN indica rischi nella mancata rilevazione dei positivi.
Permette di analizzare quanto il modello è sensibile alla classe positiva.
Fornisce informazioni critiche per comprendere punti deboli del modello.
Parametri TP
True Positive (TP) rappresentano i casi positivi correttamente identificati dal modello.
Permettono di capire quanto il modello riesce a catturare la classe positiva.
Un elevato numero di TP indica un buon livello di rilevazione della classe positiva.
Sono la base per comprendere la capacità del modello di individuare esempi rilevanti.
Contribuiscono a fornire una visione dettagliata della correttezza delle predizioni.

Problema Multiclasse
Quando ci sno più classi la matrice non è più "X" (come nel caso binario) ma diventa nXn (dove n
è il numero dei valori che può assumere la label)
Ogni riga rappresenta la classe reale, ogni colonnna la classe predetta.
La diagonale principale (da in alto a sx a in basso a dx) mostra le corrette predizioni, tutt le 
altre celle gli errori.
E' possibile identificare quali classi vengono frequentemente confuse.
Fornisce una panoramica dettagliata della distribuzione degli errori.

In scikit-learn la Confuzion Matrix può essere calcolata facilmente utilizzando confusion_matrix
del modulo metrics
La funzione richiede due valori:
- etichette reali
- predizioni del modello.
La matrice risultante restituisce i conteggi di TP, TN, FP, FN organizzati in tabella.
I valori della matrice possono essere stampati direttamente a schermo o visualizzati con una 
heatmap usanto la libreria seaborn
Per problemi di classificazione multiclasse utilizzare il metodo multiclass_confusion_matrix

La confusione matrix rappresenta la base per tutte le analisi di classificazione
Permette di osservare in dettaglio i comportamenti del modello su ogni classe.
Fornisce informazioni essenziali per interpretare gli errore e le predizioni corrette.
Consente una comprensione approfondita dei punti di forza e delle limitazioni.
Rimane uno strumento fondamentale per valutare la qualità dei classificatori.

"""

#esempi di confusione matrix

import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, multilabel_confusion_matrix

y_true_bin=[0,1,0,1,0,1,1]
y_pred_bin=[0,1,0,0,0,1,1]

y_true_multi=[0,1,2,1,0,2,1]
y_pred_multi=[0,2,2,1,0,0,1]

#classificazione binaria
cm_bin=confusion_matrix(y_true_bin,y_pred_bin)
print(cm_bin)

#classificazione multiclasse
cm_multi=multilabel_confusion_matrix(y_true_multi, y_pred_multi)
print(cm_multi)

#plottiamo la confusion matrix binaria
classes_bin=sorted(set(y_true_bin))

plt.figure(figsize=(8,6))
sns.heatmap(cm_bin,annot=True,fmt="d",cmap="Blues",xticklabels=classes_bin,yticklabels=classes_bin)
plt.title("Confuzione matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()

#plottiamo la confusion matrix multiclasse

#faccio una confusion matrix sui valori della "multilabel confusion matrix"
cm_multi = confusion_matrix(y_true_multi, y_pred_multi) 

classes_multi = sorted(set(y_true_multi))

plt.figure(figsize=(8, 6))
sns.heatmap(cm_multi, annot=True, fmt="d", cmap="Blues", xticklabels=classes_multi, yticklabels=classes_multi)
plt.title("Multilabel Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.show()



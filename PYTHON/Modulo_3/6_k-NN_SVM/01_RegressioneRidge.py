"""
REGRESSIONE RIDGE

La regressione Ridge è una delle varianti della regressione lineare che include una penalizzazione
sui coefficienti.
Serve a ridurre l'overfitting e migliorare la generalizzazione del modello.
Cioè evitare che il modello di adatti troppo al modello generalizzando male su nuovi dati.
Particolarmente utile quando le variabili indipendenti sono fortemente correlate e se ho pochi dati.
L'idea principale è introdurre un termine di regolarizzazione nella funzione costo.
Questo termine impedisce ai coefficienti di assumere valori troppo grandi.
SE hai:
- pochi dati - molte feature - feature correlate: la regressione lineare esegera
Risultato:
- coefficienti grandi - modello instabile  - generalizzazione pessima.

L'idea è quella di introdurre 'rumore' sulle label (y) aggiungendo una penalizzazione, in questo
modo minimizzo l'errore e la grandezza dei coefficienti.

Ridege serve:
1) Multicollinearità: feature correlate tra loro, esempio peso, volume, dimensione
2) Tante feature: con tante colonne la regressione lineare impazzisce, mentre Ridge funziona meglio
3) Modelli rumorosi: dati sporchi, ride evita coefficiente estremi.

La regressione lineare tradizionale può adattarsi troppo ai dati ditrainig.
Questo porta a modelli che performano male sui dati nuovi, cioè al fenomento dell'overfitting.
y=x0 + (w1 * x1)+(w2 * x2) + ... + (wn * xn)
Obiettivo trovare i coefficienti di w che minimizzano l'errore

Con la Ridge Regression si introduce un controllo sulla complessità del modelli, aggiungendo una 
penalità sui coefficienti.
y= x0 + (w1 * x1 + coefficiente1) + (w2 * x2 + coefficiente2)
Il controllo si ottiene penalizzando la somma dei quadrati dei coefficienti.
In questo modo si ottiene un comportamento tra errore di bias e varianza.
Si preferisce un modello leggermente meno preciso ma più stabile.
Quando il coefficiente è basso o nullo abbiamo una situazione simile alla regressione lineare 
con rischio di overfitting, quando il coefficiente è alto si ha il rischio opposto di underfitting.

La funzione di costo di Ridge combina l'errore quadratico medio e un termine di penalità L2
Il termine di penalità è proporzionale alla somma dei quadrati dei coefficienti.
Il parametri alfpha controlla l'intensità della regolarizzazione: tanto più è grande, tanto 
più i coefficienti vengono verso zero.
Quando alpha=0, Ridge diventa una regressione lineare classica.
Con valori più alti di alpha, i coefficienti vengono progressivamente ridimensionati.
La regolarizzazione riduce la varianza ma può aumentare il bias.
L'obiettivo è trovare un bilanciamento ottimale tra questi due effetti
Questo equilibrio si traduce in una maggiore stabilità del modello

La Ridge Regression affronta il problema della multicollinearità.
Quando due o più feature sono fortemente correlate tra loro (una feature si può ricavare da altre), 
i coefficienti possono diventare instabili.
L'aggiunta del termine di penalità stabilizza la stima dei parametri.
Il modello riesce così a gestire meglio feature ridondanti
Questo la rende una scelta naturale in dataset con molte varibili correlate.

Il parametro alpha è fondamentale per determinare la forza della penalizzazione.
Valori bassi lasciano il modello quasi invariato (quando è 0 corrisponde alla regressione lineare)
rispetto alla regressione lineare.
Valori alti riducono drasticamente i coefficienti e semplificano il modello.
La scelta ottimale di alpha si ottine tramite valisazoine incrociata 
Scikit-lear fornisce metodi automatici per ottimizzare questo parametro.

Ridge vs Linear Regression
Se hai dati semplici, preferire il modello lineare
Se hai dati reali più complessi, preferire rigde
In azienda usa Ridge come default, non la lineare pura.

Ridge vs Lasso
Ridge riduce i coefficienti, mantiene tutte le variabili
Lasso azzera i coefficienti, fa feature selection
Se hai 20 variabili ma solo 5 utili, ridge usa tutte e 20, Lasso ti lascia le 5 più imporatnti

Se non scali, Ridge lavora male

Importante scegliere lamda in modo corretto.
Si può utilzzare la cross validation

from sklearn.linear_model import RidgeCV
model = RidgeCV(alphas=[0.1,1,10,100])
model.fit(X, y)

Vantaggi
Riduce overfitting migliorando la capacità predittiva.
Stabilizza le stime in presenza di multicollinearità.
E' semplice da implementare e interpretare.
Può essere estare a modelli non lineari tramite feature polinomiali.
Richiede un solo iperparametro principale da ottimizzare
Svantaggi
Ridge non effettua selezione di feature, quindi tutte rimangono nel modello.
In presenza di molte varibili irrilevanti può risultare inefficiente.
La scelta di alpha influenza fortemente le prestazini
Non è adatta se si desidera un modello sparso o facilmente interpretabile
Può penalizzare troppo le feature più informative se alhpha è troppo elevato

Non effettua feature selection, quidni molto spesso è combinata con tecniche 
di riduzione dimensionale come PCA.
Può essere adattata a modelli non lineari tramite kernel Ridge
E' spesso usata come base per metodo più avanzati come Elastic Net, 
questo modello combina Ridge e Lasso per sfruttare
entramnbi gli approcci a guadagnare vantaggi da entrambi i modelli.

Ridge rappresenta una soluzione elegante al problema del overfitting.
Introducendo la regolarizzazione L2, controlla la complessità del modello.
Offre stabilità, robustezza e buona accuratezza predittiva.
Non effettua selezione delle feature ma le gestisce in modo equilibrato.
E' una tecnica fondamentale da tenere nella toolbox del machine learning moderno.

"""
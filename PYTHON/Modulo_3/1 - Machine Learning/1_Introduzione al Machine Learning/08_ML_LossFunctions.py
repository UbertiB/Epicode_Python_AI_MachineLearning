"""
LOSS FUNCTIONS E EMPIRICAL RISK MINIMIZATION

Loss: funzione che valuta la qualità della predizione del modello per ogni singolo datapoint.
L'obiettivo dell'apprendimento è imparare a predire una label y di un data a partire dalle suo feature x
La loss misura quando le predizioni si discostasno dai valori reali.
Per valutare la qualità del modello è necessario un concetto rigoroso di 'errore medio' sui dati.

in ML i dasti (x,y) vengono trattati come se fossero estratti da un processo casuale.
Una variabile aleatoria è una grandezza che dipende dal caso (esempio lancio del dado)
I dati non sono fissi, ma sono campioni di un fenomeno casuale sottostante.
In ML si assume che i dati siano:
- indipendenti: ogni punto è estratto senza influenzare gli altri (come ogni numero che esce ad ogni lancio 
    di un dato)
- identicamente distribuiti: tutti gli oggetti seguono la stessa distribuzione (ogni faccia del dado ha la
    stessa probabiltà)

In statistica una variabile aleatoria con queste caratteristiche si chiama iid (indipendente e identicamente
distribuita)

I dati (x,y) sono realizzazioni di una variabile aleatoria iid con distrubuzioe p(x,y)
Si definisce la perdita subita per ogni punti come la perdita prevista, cioè in media la perdita sui punti
della distribuzione.
Viene chiamata Expexted Risk o Bayes Risk
Per calcolare questa perdita attesa, è necessario conoscere la distribuzione di probabilità p(x,y)
Nella pratica questa distribuzione non si conosce mai a priori.
Poiche non è nota, si approssima la perdita attesa con le media aritmetica della perdita sui dati osservati.
Con un campione dei dati sufficientemente grande si possono approssimare la media di perdite e expeted risk.
Questa quantita prende il nome di empirical risk (perchè parte proprio da dati empirici)

L'idea centrale dell' ERM (empirical risk minimization) è trovare una impotesi h che vada a minimizzare, 
tra tutti gli h presenti nello spazio delle ipotesi (H) quella che minimizza l'empirical loss quando 
si effettua una predizoine delle label y a partire dalle feature x.
L'empirical risk minimization è il principio su cui si basano la maggior parte degli algoritmi di ML
supervisionato.

ERM nella regressione:
Nella regressione l'obiettivo è prevedere una laber numerica continua y partendo da un vettore di feature x.
Il modello tipico di regressione è lineare o polinomiale.
La funzione di perdita più comune è lo Squared Error Loss, non robusto aglio outlier.,
L'ERM cerca i parametri del modello che minimizzano la perdita media sui dati di apprendimento.

ERM nella regressione lineare.
I dati sono rappresentati da feature numeriche e label numeriche.
Il modlelo è in uno spazio di ipotesi lineari.
La funzione di perdita si misura con lo Squared Error Loss.
L'ERM in questo caso consiste nel minimizzare il parametro w

ERM nella regressione polinomiale
Il modello è in uno spazio di ipotesi lineari.
Per ridurre la complessità del problema si può affettuare una trasformazione delle feature in modo da
renderle lineari nello spazio trasformato.
In questo modo ci si riconduce al problema di regressione lineare, rendendo il processo computazionalmente 
efficiente.

La Loss Function la sua scelta è solo una decisione progettuale.
 - Lo squared error loss: sensibile agli outlier, trascura errori piccoli e penalizza errori grandi
 - Absolute error loss: robusto agli outlier
 - Huner Loss: beneficia di entrambi i vantaggi
La scelta della funzione influenza la forma ottimale della soluzione e la robustezza del modello.

ERM nella Classificazione
Nella regressione le feature sono vettori a valori numerici, le label sono numeriche e le loss si basano
su distanze numeriche.
Nella classificazione invece le feature sono sempre vettori numerici, ma le label sono categoriche.
    - binarie: la label assumo due valori
    - multi-class: la label assume più di due valori.
In entrambi i casi le loss function si basano su misure di confidenza.
 
ERM nella regressione logistica
I dati sono numerici, il modello è nello spazion lineare, ma la predizione avviene tramite il segno e valore
di h
La confidenza si misura con il valore assoluto dell'ipotesi h: tanto è più grande, tanto più la previsione 
della label è 'forte', tanto più il modello è sicuro nel predire una certa label

La funzione di perdita è misurato con la logistic loss
Misura la penalità per previsioni errate in problemi di classificazione binaria.
E' basata su una funzione logaritmica che cresce rapidamente quando la previsione è sbagliata.




"""
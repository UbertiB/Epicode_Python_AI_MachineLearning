"""
REGRESSIONE LINEARE

Serve a prevedere un numero a partire da altre variabili
E' uno dei metodi e diffusi per analizzare relazioni tra variabili
Viene utilizzzata quando la variabile da prevedere è continua, come prezzo, temperatura, peso.
L'obiettivo è stimare una relazione lineare tra uno ao più variabili indipendenti e una dipendente.
Questa relazione è rappresentata da una retta o da un pinao in spazi di dimensione maggiore.
Il modello risultante consente sia di comprendere la relazione che di effettuare previsioni.

y = w1*x1 + w2*x2 + ... b
y = valore da prevedere
x = dati di input (feature)
w = peso (quanto conta ogni variabile)
b = offset

L'idea alla base della regressione lineare è quella di trovare una liena che meglio approssima i dati osserveti.
La linea di regressione minimizza la distanza complessiva tra i punti osserveti e quelli stimati.
Ogni punto contribuisce con il proprio errore, chiamato residuo, alla qualità complessiva del modello.
Il processo consiste nel trovare i coefficienti della retta che rendono questi residui il più
piccoli possibile.
Il risultato è una linea che rappresenta la tendenza media dei dati.

In caso di più variabili esplicative si parla di regressione lineare multipla.
La struttura lineare rimane la stessa ma lo spazio  dei parametri di amplia

L'obiettivo dell'algoritmo è trovare i valori dei parametri che minimizzano l'errore complessivo.
La misura dell'errore è spesso la somma dei quadrati delle differenze tra valori osservati e stimati.
Minimizzando questo errore si ottiene la "migliore" linea possibile in senso dei minimi quadrati.
Questo metodo è noto come Ordinary Least Squares (OLS).
L'algoritmo fornisce una soluzione analitica efficiente e interpretabile, sia a livello di dati che a 
livello di graico.

Il primo passo di questo algoritmo è calcolare la media e la varianza delle variabili coinvolte.
Successivamente si stimano i coefficienti della retta ottimale usando formule derivate dal calcolo
matriciale.
Si calcola la retta di regressione e si confrontano i valori previsti con quelli reali.
Si analizzano poi i residui per verificare la bontà dell'adattamento
Infine si valutano le metriche di performance per validare il modello.

Il modello ho pochi parametri ma ognuno di esse influisce sull'apprendimento
    -fit_intercept: controlla se stimare o meno l'intercetta del modello
    - normalize (nelle vecchie versioni) normalizzava le feature prima del fitting.
Alcune librerie permettono di aggiungere regolarizzazione, ma nella fomra base non è inclusa.
La semplicità dei parametri è uno dei motivi della grande diffuzione della regressione lineare.

La regressione lineare non richiede necessariamente la standarizzazione dei dati.
Tuttavia, la normalizzazione può migliorare la stabilità numerica quando le scale sono molto diverse.
Gli outlier devono essere gestiti perchè possono influenzare fortemente la linea di regressione.
E' utile verificare la linearità delle relazioni tra le variabili prima di applicare il modello.
Il preprocessing corretto aumenta la robustezza e l'affidabilità delle previsioni.

Per implementare la regressione lineare si utilizza l'oggetto
sklearn.linear_model.LinearRegression
Dopo aver importato le librerie si suddividono i dati in set di training e test
Si istanzia il modello specificando eventuali parametri come fit_intercept=True
Si esegue il fitting con il metodo .fit(X_train,Y_train)
Una volta addestrato il modello, si ottengono le previsioni tramite .predict(X_test)

Dopo l'addestramento si possono ispezionare i coefficienti con coef_ e intercetta con intercept_
Questi valori indicano l'influenza di ogni variabile indipendente sulla variabili target.
Un grafico a dispersione (scatterplot) con la retta di regressione aiuta a visualizzare l'adattamento
La qualità del modello si valuta confrontando i valori reali e quelli previsti.
Piccole differenze indicano che il modello rappresenta bene il fenomeno.

Le metriche più comuni per valutare l'adattamento di questo modello sono Mean Squared Error (MSE), 
Root Squared Error (RMSE) e R2
    * MSE: misura la media dei quadrati degli errori, penalizzando fortemente le previsioni errate
    * RMSE: è la radice quadrata del MSE e restituisce un valore interpretabile della stessa scala di y
    * R2: coefficiente di determinazione, indica la proporzione della varianza spiegata dal modello, 
          valori vicini a 1 indicano  un buon adattamento del modello ai dati.
    * Una metrica semplificata può essere definita come la media delle differenze relative tra i valori
          previsti e i valori reali. Questa misura da un'idea intuitiva della precisione media del modello
          Non ha lo stesso rigore statistico delle metriche ufficiali, ma aiuta a interpretare il risultato
          E' particolarmente utile in contesti didattici o esplorativi.
    * I residui mostrano quando i valori previsti di discostano da quelli osservati. Un grafico dei 
          residui distribuiti casualmente attorno allo zero indica u buon modello.
          Pattern evidenti nei residui suggeriscono che la relazione non è completamente lineare.
          Gli outlier possono essere facilmente identificati tramite l'analisi dei redisui.
          Questa fase è essenziale per comprendere i limiti del modello.

Vantaggi
E' un modello semplice, veloce ed altamente interpretabile. Richiede poche risorse computazionale
I risultati sono facili da spiegare, visualizzare, interprestare.
Funziona bene come baseline per modelli complessi.
Può essere estesa facilmente con termini polinomiali o ragolarizzazioni
Svantaggi
Assume che la relazione tra le variabili sia lineare, il che spesso non è realistico. E' sensibile alla
presenza di outlier che possono distorcere la linea di regressione. Le prestazioni diminuiscono quando
le feature sono altamente correlate tra loro. Non riesce  a modellare relazioni complesse o interazioni
non lienari senza trasformazioni aggiuntive.
Il rispetto della assunzioni statistiche è fondamentale per l'affidabilità del modello.

Considerazioni
Quando il modello non si adatta bene, si possono aggiungere veriabili esplicative o trasformazioni non 
lineari.
La regressione polinomiale permette di curvare la retta adattandola meglio ai dati.
Tecniche come Ridge e Lasso introducono penalizzazioni per ridurre l'overtiffing.
La selezione delle variabili rilevanti migliora l'interpretazione e la stabilità del modello.
Una buona diagnostica è spesso più utile dell'aggiuta di complessità inutile.

La direzione e l'intensità delle relazioni possono essere analizzate in modo trasparente.
Questo rende la regressione lineare particolarmente utile in ambiti scientifici e regolamentati.
La chiarezza dei risultati favorisce la comunicazione con decisori e stakeholder

E' utilzzata in economia per prevedere costi o consumi, in sanità per stimare rischi e in ingegneria
per modellare processi fisici
In marketing serve per stimare la rispostas dei clienti a una campagna
In finanza aiuta a prevedere l'andamento dei prezzi o delle vendite.
La sua versatilità la rende uno strumento universale nell'analisi dei dati.
Anche modelli complessi spesso incorporano componenti lineari per garantire interpretabilità

La regressione lineare è un modello semplice ma potente che introduce ai fenomeni della predizione 
quantitativa.
La sua interpretabilità la rende un punto di partenza ideale per comprendere i meccaniscmi dei modelli
statistici
Pur con i suoi limiti, costituisce un riferimento per confrontare modelli più sofisticati.
Il suo ruolo didattico è fondamentale per introdurre concetti come errore, fitting, e generalizzazione.
Comprendere la regressione lineare significa acquisire le basi di ogni forma di modellazione predittiva.

"""
#codice base: 
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X, y)

y_pred = model.predict(X)

"""
il modello impara:
    * model.coef_ : dice quanto pesa ogni variabile
    * intercept_ : dice il valore base

Esempio:
coef=[2.5,0,3]
significa che feature 1 mesa molto, feature 2 pesa poco
    
"""


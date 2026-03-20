"""
NORMALIZATION - FEATURE SCALING

FEATURE SCALING
Il feature scaling è l'insieme delle tecniche per aggiustare le differenze tra gli attributi
in termini di media, varianza e range.
L'obiettivo è garantire che nessuna feature domini il modello a causa della sua scala numerica
maggiore.
E' una fase cruciale per la stabilità e la velocità dei processi di ottimizzazione
Le due tecniche principali sono: 1) Normalization 2) Standarization

Alcune trasformazioni alterna la distribuzione del dato utilizzando funzioni matematiche
semplici, usate per correggere l'assimetria (skewness) o per linearizzare le relazioni.
Tali trasformazioni sono spesso eseguite prima del vero e prorpio scaling
Una trasformazione di attributo è una funzione che mappa l'intero set di valori di una feature
su un nuovo set di valori di sostituzione
La regola fondamentale è che ogni vecchio valore possa essere identificato con uno dei nuovi
valori.
Questa operazione permette di alterare la distribuzione o la scala delle variabili.
Lo scaling è un tipo specifico di trasformazione di attributo

Il feature Scaling si riferisce specificatamente alle tecniche usate per garantire le differenze
tra gli attributi.
L'obiettivo è impedire che feature con range di valori molto ampi (es. reddito in migliaia) 
abbiano un peso sproporzionato rispetto a feature con range piccoli (es. eta in decine).
Questo è vitale per gli algoritmi basati su metriche di distanza, come K-Means o SVM
Se le scale sono diverse, il calcolo della distanza è distorto.

1) NORMALIZATION

La Normalization è una tecnica di ridimensionalmente che spesso viene chiamata Min-Max Scaling
(o rescaling, unity-based normalization).
Il suo obiettivo è portare tutti i valori delle feature nell'intervallo fisso e predefinito di [0,1]
Si base sull'uso del valore minimo e massimo osservato nella feature.
La formula della Normalization sottrae il valore minimo e divide per l'intervallo totale 
(max-min)
Questo assicura che il valore minimo originale diventi 0 e il valora massimo originale diventi 1
Nonostante la compressione, questa trasformazione mantiene la forma della distribuzione
originale dei dati.
E' un approccio molto intuitivo ed interpretabile sia da comprendere che implementare.
x-x(min)/(x(max)-x(min))

Vantaggi
Garantisce che la scala dei dati sia limitata e prevedibile entro un range noto.
E' utile per gli algoritmo che richiedono input positivi o limitati, come alcune funzioni di 
attivazione delle Reti Neurali.
L'output è facile da interpretare perchè è su scala percentuale da 0 a 1
Svantaggi
Estrema sensibilità agli outlier (la formula dipende dai valori min e max, un singolo outlier 
elevato (sia min sia massimo) può comprimere tutti gli altri valori in un range molto stretto)
Riduzione dell'efficacia del modello
Non consigliata in presenza di dati rumorosi.

2) STANDARIZATION

La Standarization (o Z-Score Normalization) è una tecnica di ridimensionamento alternativa
che non è vincolata a un intervallo fisso (come nel caso della normalization).
Il suo scopo è trasformare i dati affinchè abbiano media 0 e deviazione standard unitaria 1
Ciò si ottiene sottranendo la media e dividendo per la deviazione standard.
E' il metodo più robusto per molto algoritmi statistici.
Il vantaggio principale è la sua robustezza agli outlier.
Poichè la Standarization dipende dalla media e dalla variazione standard, i valori estermi non
influenzano la trasformazione tanto quanto influenzerebbero min e max.
Questo la rende preferibile quando i dati sono rumorosi o non si conosce il range esatto.
E' la tecnica raccomandata per PCA, SVM e Regressione.
La differenza fondamentale è che la Standarization non è limitata a un certo range.
I valori risultanti possono essere inferiori a -1 o superiori a 1
Sebbene i valori estermi rimangono, il loro peso relativo è mitigato dalla standarizzazione.
La Standarization è la scelta migliore quando la distribuzione dei dati è approssimativamente
normale o contiene molti outlier.
E' obbligatoria per tutti i modelli che assumono una distribuzione gaussiana dei dati.
Funziona molto bene con gli algoritmi che si basano sulla misura della deviazione standard.
Normalization è per il range la Standarization è per la distribuzione

3)CATEGORIZATION

La Categorization (o Discretizzazione) è la trasformazione di un attributo continuo in uno
discreto o categorico.
E' una forma di semplificazione controllata dei dati, in cui valori numerici molto dettagliati
vengono raggruppati in fasce (bin) o intervalli rappresentativi.
Esempio trasformare l'altezza esatta in fasce come basso, medio, alto.
E' utile per ridurre la sensibilità del modello alle piccole fluttuazioni.
Questa operazione può sembrare una perdita d'informazione, ma in realtà ha scopi molto pratici:
- Semplifica le relazioni che il modello deve apprendere, riducendo il rumore nei dati e 
  migliorando la leggibilità dei pattern
- Riduce la sensibilità del modello a piccole fluttuazioni o misurazioni imprecise: due persone
  con altezza 1.71 e 1.72 vengono considerate uguali dal modello, il che spesso è desiderabile.
- E' particolarmente utile quando il dataset contiene rumore strumentale o quando le feature
  hanno un significato qualitativo più che quantitativo.
Questa fase avviene prima dell'Encoding:
- Prima si decide come raggruppare i valori (es eta 0-18=giovane)
- Dopo si applica l'Encoding (es. one-hot encoding) alla nuova variabile categorica.
Questa distinzione è cruciale nel flusso del preprocessing, perchè determina quando i dati
cambiano significato e quando vengono resi numericamente leggibili dall'algoritmo.
Inoltre, categorizzare in modo coerente permette di preservare il senso semantico dei dati:
è meglio fornire a un modello categorie interpretabili che valori numerici poco significativi.
Inoltre la categorization è anche una forma di controllo sul bias del modello: decidendo noi
i confini delle categorie possiamo bilanciare il peso che certi intervalli assumono nell'
apprendimento.
In sostanza, la Categorization non è solo una trasformazione tecnica, ma anche una decisione
concettuale, che influenza il modo in cui il modello percepirà la realtà

Considerazioni:
- Lo scaling (Normalization/Standarization) è la fase finale di allineamento dei dati numerici
- Garantisce che i processi di ottimizzazione non siano distorti dalle differenze arbitrarie 
  nelle unità di misura
- Un corretto scaling è spesso la differenza tra un modello che converge rapidamente e uno che
  fatica a imparare
- Lo scaling delle feature non solo migliora l'accuratezza, ma accelera drasticamente il processo
  di convergenza degli algoritmi basati sul gradiente.
- Un gradiente efficace richiede che le feature contribuiscono equamente.

Feature scaling è la scelta obbligata in presenza di outlier e quando si utilizzano algoritmi
come PCA e SVM.
Le trasformazioni di scala sono la fase finale di preparazione dei dati ad un'analisi statistica:
- Normalization: preferibile quando si ha bisogno di range limitati o fissi o quando la 
  distribuzione dei dati è uniforme e non contiene outlier troppo significativi.
- Standarization: raccomandata per la maggior parte dei modelli ML, mitiga l'impatto 
  degli outlier e centra la distribuzione
- Categorization: è la trasformazione del tipo di variabile
Senza scaling, il processo di ottimizzazione può oscillare e richiedere molto più tempo
per convergere, rallentando l'intero training.



"""

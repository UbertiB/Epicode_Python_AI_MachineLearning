"""
FEATURE SELECTION & FEATURE ENGINEERING

FEATURE MANAGEMENT

La qualità dei dati di imput è l elemento che influenza le prestazioni di un modello ML
L'efficacia di un algoritmo dipende molto dalla qualità delle feature che dalla
sua complessità intrinseca.
Il feature management è il processo di ottimizzazione di queste variabili, è un
processo che si divide in due approcci:
    1) Feature Engineering: crare nuove feature
    2) Feature Selection: selezionare alcune feature del dataset
L'obbiettivo finale è trasformare il set di dati grezzi nella migliore rappresentazione
possibile per l apprendimento

Un numero eccessivo di feature porta alla CURSE OF DIMENSIONALITY dove lo spazio
dei dati appaiono tutti lontani tra loro
In questi spazi, le distanze tra i punti perdono significato, e gli algoritmi basati
su distanza o similarità perdono efficacia.
Ridurre le feature irrilevanti e ridondanti non solo velocizza il modello, ma
migliora anche la sua capacità di generalizzare a nuovi dati.

1) FEATURE ENGINEERING (FE)

Il Feature Engineering è l'arte e la scienza di creare nuove feature più informative
a partire da quelle esistenti.
E' considerata la fase più creativa in quanto richiede una profonda conoscenza del 
dominio (business e domain expertise del problema)
Una feataure ben ingegnerizzata può risolvere il problema prima ancora di utilizzare
l'algoritmo
Spesso è la tecnica che fornisce il maggior incremento di accuratezza al modello

Lo scopo del FE è trasformare l'informazione implicita in una forma che il modello 
può utilizzare facilmente.
Se la relazione tra due feature è un rapporto o una differenza, calcolarla direttamente
rende il modello più efficace.
Una feature di alto valore mostra una forte correlazione con la variabile target
e può migliorare la capacità predittiva anche senza l'uso algoritmi complessi.
In pratica il FE 'parla la lingua del modello' facilitando l'apprendimento.

Esempi:
si creano feature combinando due o più variabili già esistenti nel dataset attraverso
funzioni e operazioni matematiche, questo riduce, spesso, la complessità del modello finale.
Esempio calcolare l'indice di massa corporea (tra peso ed altezza) è più predittivo
rispetto ai singoli due valori di peso ed altezza.
Inoltre si possono calcolare le differenze o tassi di variazioni tra due misurazioni 
nel tempo. 
Un altro esempio è quello delle colonne di data e ora, fonti incredibilmente ricche
di informazioni. Da una singola data si possono estrarrer giorno della settimana, mese,
anno, giorno festivo/lavorativo, ecc
L'estrazione di feature come la stagione o l'ora permette al modello di catturare 
effetti ciclici e/o stagionali.
Queste nuove feature possono avere un potenziale predittivo elevatissimo

Tecniche

La DISCRETIZZAZIONE (o BINDING) trasforma una variabile continua in intervalli o
fasce discrete (categorie), esempio suddividere i redditi in fasce.
Si usa per semplificare le relazioni e per rendere il modello meno sensibile ai 
valori anomali.
Questo processo crea una variabile ordinale che cattura meglio interazioni non lineari.

Le feature con distribuzioni molto assimeetriche (skewed) possono violare le assunzioni
dei modelli lineari.
Le Trasformazioni Logaritmiche (LOG(x)) vengono applicate per appiattire queste distribuzioni
L'obbiettivo è ottenere una distribuzione che si avvicina alla normalità, migliorando
la performance e la stabilità dei modelli di regressione.
Questa tecnica attenua l'effetto dei valori estremi sul modello.

Le nuove feature create tramite il FE (es. giorno della settimana) sono spesso
variabili categoriche in formato testuale. 
Quest non possono essere inserite direttamente nel modello di ML perchè non interpretabili.
Richiedono l'uso, quindi, dei motodi di codifica.
Questo passaggio di ENCODING (codifica) è un obbligo dopo il FE.
Il FE, se ben documentato, può rendere il modello più trasparente, facilitando
la comunicazione dei risultati.

2) FEATURE SELECIONT

La feature selection è il processo di scegliere un sottoinsieme ottimale dalle 
feature originali.
Lo scopo è eliminare feature che sono non irrilevanti per l'output o ridondanti.
Rimuovere il rumore e la ridondanza migliora la stabilità del modello.
Un modello con meno feature è intrinsecamente più leggero, veloce da addestrare
e più facile da interpretare.

La FE rimuove feature che sono irrilevanti o ridondanti, ovvero che non aggiungono
nessun valore predittivo.
Riduce anche la possibilità di over fitting, migliorando la stabilità del modello
su nuovi dati.
Selezionare un sottoinsieme di feature, permette anche di mantenere l'interpretabilità.
A differenza della Dimensionality Reduction (es. PCA), che combina feature in nuove
variabili statistiche, difficili da interpretare, la FE mantiene le feature originali,
comprensibili e direttamente leggibili.

La FS sceglie un sottoinsieme delle feature originale, mantenendo interpretabilit
LA Dimensionality reduction (es PCA) crea, invece, nuove feature che sono combinazioni
matematico-statistico delle vecchie feature.
La PCA massimizza l'informazione compressa, ma le nuove feature sono meno intuitive
da interpretare all'uomo.
La FS è quindi preferibile quando l'interpretabilità è la priorità.

Il primo vantaggio della FS è eliminare le feature irrilevanti o ridondanti che non
apportano valore predittivo.
Ogni feature inutile è come 'rumore' che confonde il modello.
Con la loro rimozione, il modello si puo concentrare solo sugli input veramente informativi,
riducendo la possibilità di errori e migliorando la stabilità delle predizioni.

Un altro vantaggio della FS è la riduzione di dati, in scenari reali, dove i dataset
possono avere centianio di colonne, ridurre anche solo il 10% di feature irrilevanti,
può ridurre drasticamente il tempo di adddestramento.

La FS rende il modelle più interpretabile, se un modello utilizza meno feature,
è pià facile da capire come il modello prende decisioni.
Questo per spiegare le predizioni agli stakeholder.

Esistono diversi modi per selezionare le feature:
    * Filter: si valutano le feature basandosi su metriche stastiche (come correlazione
      o varianza) indipendentemente dal modello.
    * Wrapper: testano combinazioni di feature utilizzando il modello stesso e 
      selezionando quelle che migliorano le performance
    * Embedded: la selezione avviene durante l'addestramento del modello, come accade
      con gli alberi decisionali che calcono l'importanza ciascun feature.
La scelta di uno di questi approcci dipende dalle risorse computazionali e dalla complessità
del dataset.


Il feature management non è una singola attività ma un ciclo continuo di migiloramento
Generalmente di parte con il feature engineering per creare valore nel dataset
Successivamente, si utilizza la Selection per eliminare quelle feature create o 
originali che non hanno molto impatto
Si ripetono i cicli fino a quando le prestazioni del modello raggiungono un livello
accettabile: FE aggiunge informaioni al dataset, FS pulisce informazioni dal dataset.
Entrambi sono cruciali per costruire modelli robusti, generalizzabili e che siano
sostenibili nel tempo.

Spesso il FE può fare la differenza tra un modello che fallisce e uno che ottiene 
un'accuratezza elevata, anche senza algoritmi complessi. Esempio calcolare il rapporto
o un indicatore derivato (da due altre feature) può rendere più evidente una correlazione
nascosta tra variabili, senza cambiare il modello
La FS, oltre a migliorare le perfomance, aiuta anche nella manutenzione del modello:
feature inutili eliminano rumore e rendono il modello più semplice da aggiornare.
In pratica, quando si aggiungono nuovi dati (righe), un modello con meno feature (colonne)
è più stabile e richiede meno interventi manuali.

Combinando la FE e la FS in cicli iterativi, si ottengono dati puliti, informativi
e compoatto, ideale per modelli robusti e generalizzabili.
Questo ciclo è simile a un processo di raffinazione: prima si aggiunge valore creando
feature, poi si pulisce eliminando ciò che non serve, fino ad ottenere la combinazione
ottimale di feature.

Moltri strumenti di ML moderni, offrono metriche automatiche per la selezione delle
feature, ma il dominio e la conoscenza del pronlema restano cruciali per scegliere
le feature più significative.
Un indicatore che sembra irrilevante da solo, può diventare molto predittivo se 
combinato con altre variabili note dal dominio.
In sintesi, la FM è un investimento sul dataset non solo sull'algoritmo.
Spesso passare ore a migliorare le feature porta più benefici che cambiare
l'algoritmo, la qualità dei dati è proprio la vera chiave per raffinare il modello.






"""
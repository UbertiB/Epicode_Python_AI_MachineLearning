"""
DATA SPLITTING

In questa sezione, esploreremo diverse tecniche di data splitting per valutare le prestazioni dei
modelli di machine learning. Il data splitting è un passaggio cruciale per garantire che i modelli siano
valutati in modo accurato e generalizzabile.
Quando si costruisce un modello di machine learning, è fondamentare capire non solo quanto bene
riesca ad apprendere dai dati disponibili, ma soprattutto quanto bene si comporterà su nuovi dati mai visti.
Valutare un modello solo sul training set produce un'illusione di prestazioni elevate che spesso 
scompare appena il modello incontra dati reali.
Il data splitting nasce per simulare questo ambiente reale, costruendo una 'area di test' controllata
in cui il modello non ha mai potuto allenarsi.
Separare i dati riduce il rischio che il modello impari a memoria il dataset invece di comprendere
davvero le relazioni tra variabili.
E' una pratica indispensabile per capire se il modello è pronto a essere utilizzato in un contesto
di produzione.

Nei progetti reali, il data splitting fa parte di una pipeline più ampia che può includere pulizia
del dataset, feature engineering, e pre-processing condizionato.
Spesso i dati arrivano in più batch nel tempo (blocchi), e lo split deve rispettare la cronologia 
per evitare di usare informazioni future nel training, fenomeno chiamato data leakage.
In ambito industriale la separazione dei dati è una pratica formale, spesso anche obbligatoria per 
garantire affidabilità e tracciabilità del modello.
Anche nei modelli più avanzati, come le reti neurali o gli ensemble, il principio di mantenere un 
test set separato rimane invariato.
La disciplina nel mantenere un corretto splitting permette di costuire modelli robusti e affidabili,
capaci di resistere anche a condizioni operative diverse da quelle del training.

Il train set rappresenta il materiale da cui il modello impara, e contiene la maggior parte dei dati
disponibili perchè serve a catturare pattern, tendenze e strutture nascoste.
Durante il training, il modello ottimizzza i parametri o pesi attraverso algoritmi specifici, 
cercando di minimizzare l'errore sul training set.
Imparare troppo bene dai dati di training può essere controproducente: modella anche il rumore e le
anomalie presenti.
Il training set deve essere ampio e rappresentativo della realtà, includendo casi semplici, intermedi
e anche i più rari.
E' la base su cui si costruisce un modello stabile, affidabile e capace di generalizzare correttamente
su nuovi dati.

Il test set è usato al termine del processo e rimane 'invisibile' al modello fino all'ultimo momento.
Fornisce una misura imparziale della qualità finale del modello, simulando la situazione in cui
il modello viene messo davanti a dati nuovi nel mondo reale.
Utilizzare impropriamente il test set durante lo sviluppo porterebbe a ottimizzazioni guidate 
dai dati di test, invalidando completamente la valutazione finale.
Deve essere abbastanza grande da dare una stima affidabile delle prestazioni, ma non da sottrarre 
troppi dati all'allenamento.
Il risultato ottenuto sul test set rappresenta la vera misura della capacità predittiva del modello.

Spesso non basta una semplice divisione tra train e test, soprattutto quando si vuole ottimizzare
gli iperparametri del modello in modo controllato.
Perciò si introduce un validation test, che permette di testare diverse configurazioni senza 'toccare'
il test set finale.
Questo processo evita il problema del leakage (l'influenza indesiderata dei dati di test nelle decisioni
di progettazione del modello).
Consente di confrontare modelli diversi e scegliere quello con il compromesso migliore tra complessità
e performace).
Quando il dataset è troppo picocolo, si preferisce utilizzare metodi più sofisticati come la 
cross-validation per non sprecare dati preziosi.

Senza un test separato è quasi impossibile capire se il modello sta semplicemente imparando a memoria
i dati invece di coglierne le relazioni sottostanti.
L'overfitting produce prestazioni eccellenti sul training set ma drasticamente peggiori su qualsiasi
dataset.
In data splitting diventa quindi una difesa fondamentale contro questo fenomeno, perchè obbliga il 
modello a confrontarsi con dati che non ha mai visto.
Valutare l'errore sul test set permette di capire quanto la complessità del modello sia realmente 
giustificata dati dati, e se è necessario semplicare di più per ottenere risultati migliori.
Quando la distanza tra errore di training ed errore di test aumenta, è un segnale chiaro che il 
modello non sta generalizzando correttamente.
Anche l'underfitting può essere identificato grazie al data_splitting, perchè il modello mostra
prestazioni molto basse sia sul traing sia sul test.
Questo accade quando il modello è troppo semplice rispetto alla complessità dei dati, e non riesce
a catturare le strutture essenziali.
Un modello underfi,
Questo accade quando troppo semplice rispetto alla complessità dei dati e non reisce a catturare
le strutture essenziali.
Un modello underfitted mostra prestazioni molto basse sia sul training che sul test, indicando
che non ha appreso abbastanza dai dati.
Anche l'underfitting è un problema, perchè il modello non riesce a catturare le relazioni tra le 
variabili, e non è in grado di fare previsioni accurate neanche sui dati di training.
Un modello undefittato spesso presenta un errore simile nei due insiemi, ma sempre molto alto, su train
e test permette di indivisuare se il problema 
Anche l'underfitting  può essere identificato grazie al data splitting, perchè il modello
mostra prestazioni molto basse sia sul training sia sul test.
Questo accade quando il modello è troppo semplice rispetto alla complessità dei dati e non  
riesce a catturare le strutture essenziali. Un modello underfitting spesso presenta un errore simile
nei due insiemi, ma sempre molto alto, indicando che non ha appreso abbastanza dai dati.
Questo accade quando il modello è troppo semplice rispetto alla complessità dei dati e non riesce
a catturare le strutture essenziali. Un modello underfitting.
Analizzare il comportamento underfittato spesso presenta un errore simile nei due insiemi, ma sempre
e molto alto, indice di scarsa capacità predittive

In molti casi la soluzione consiste nell'aggiungere feature, usare modelli più flessibili o aumentare
la dimensione del dataset.

La suddivisione più diffusa nella pratica quotidiana è 80% training e 20% test, un buon equilibrio
per molti dataset moderni ad oggi utilizzato.
In contesti con dataset molto grandi si arriva spesso a 90/10 perchè anche 10% contiene comunque
un numero molto elevato di esempi.
Quando invece i dati sono pochi, alcuni preferiscono usare 70/30 per avere un test più affidabile,
anche se ciò riduce le informazioni disponibili per l'addestramento.
Le percentuali non devono essere scelte a caso, ma sulla base delle dimensioni, della variabilità
e dell'equilibrio del dataset.
Una divisione sbagliata può portare a valutazioni falsamente ottimistiche o ingiustamente
pessimistiche, influenzando l'intero progetto ML

Prima di dividere il dataset, è spesso necessario rimescolare gli esempi per evitare che eventuali
ordinamenti naturali influenzino la qualità dello split.
Un dataset può infatti contenere blocchi ordinati temporalmente, per classe o per tipologia, e senza
shuffle (rimescolamento) si rischierebbe di avere insiemi molto disomogenei.
Il parametro random_state garantisce che la procedura sia ripetibile, permettendo di ottenere
sempre lo stesso split indipendentemente da quando si esegue il codice.
La riproducibilità è fondamentale per il confronto di modelli e per la validazione scientifica dei 
risultati.
Una divisione non casuale può introdurre bias nascosti che il modello non e in grado di compensare.

DIVISIONE
Nei problemi di classificazione, una divisione casuale può creare subset in cui alcune classi
diventano molto più frequenti o molto più rare rispetto al dataset originale.
Questo sbilanciamento altera la qualità dell'addestramento e soprattutto della valutazione finale, 
rendendo i risultati poco affidabili.
La stratificazione serve proprio a mantenere le stesse proporzioni di classe nel train e nel test, 
simulando più fedelmente la distribuzione reale.
Scikit-learn permette di applicare la stratificazione in modo semplice usante il parametro stratify=y
Senza stratificazione si rischia di costruire modelli apparentemente accurati ma totalmente 
inaffidabili quando incontrano classi meno rappresentate.

DATA LEAKAGE
Il data leakage accade quando informazioni provenienti dai test finiscono, anche indirettamente, nel
processo di training, compromettendo la valutazione complessiva.
Questo può avvenire non solo attraverso errori evidenti ma anche tramite preprocessing ingenuo, 
come normalizzare l'intero dastaset prima dello split.
Il leakage porta a risultati falsamente ottimistici, perchè il modello sta 'vedendo' inconsapevolmente
informazioni che non dovrebbe conoscere.
Prevenire il leakage significa applicare qualunque trasformazione solo sul train e poi applicare di 
nuovo gli stessi parametri al test.
E' uno dei problemi più insidiosi per chi inizia, ed è fondamentale riconoscerlo subito per
costruire modelli solidi.

DATA SPLITTING
In scikit-learn, la funzione standard per divider un dataset è train_test_split, disponibile nel
modulo model_selection.
Questa funzione permette di controllare la dimensione del test set, la presenza di shuffle, e la 
riproducibilità attraverso il random_state.
Per problemi di classificazione è buona norma aggiungere la stratificazione per mantenere la 
proporzione tra le classi.
Un singolo comando è in grado di produrre quattro insiemi diversi, pronti per essere usati nel modello.
* X_train e X_test
* y_train e y_test
L'obiettivo di questa divisione è costruire una pipeline chiare e pulita, in cui ogni fase opera
sugli insiemi corretti.

Il codice più semplice prevede una chiamata come train_test_split(X, y, test_size=0.2, random_state=42) per ottenere un 80% di dati per il training
che produce  uno split 80/20 replicabile.
Nei problemi di classificazione è consigliabile aggiungere stratify=y per evitare divisioni sbilanciate.
Il risulto dello split può essere usato direttamente nei modelli scikit-learn come input per .fit()
e .predict().
Questa procedura rappresenta il primo passo nella costruzione di una pipeline ML robusta, ordinata e 
semplice da mantenere.
Comprendere bene questo meccanismo aiuta a evitare errori concettuali che si ripercuotono su tutte
le fasi successive della modellazione.

Uno degli errori più comuni e frequenti è applicare trasformazioni come scaling o encoding prima della 
divisione, contaminando il test set con informazioni del training.
Un altro errore comune è non verificare l'equilibrio della classi nei problemi di classificazione, 
producendo test set sbilanciati e poco rappresentativi.
Spesso si dimentica di fissare il random_state, rendendo impossibile replicare un esperimento
o confrontare due modelli in modo corretto.
Anche l'uso inconsapevole dello shuffle può essere dannoso in dataset temporali o sequenziali,
in cui l'ordine dei dati contiene informazioni importante.
Una corretta gestione dello split richiede quindi attenzione non solo alle percentuali ma anche al
contessto e alla natura dei dati.

CONSIDERAZIONI
Il data splitting ricorda un principio fondamentale della teoria di apprendimento statistico: un
modello valido è quello che generalizza oltre i dati di addestramento.
Il test set rappresenta un insieme di campioni estratti dalla stessa distribuzione del training set,
che permette di stimare l'errore di generalizzazione complessiva.
Questo errore non può mai essere calcolato esatto, ma il test set offre una stima sufficientemente 
accurata per giudare le scelte del modello.
La qualità di questa stima dipende da quanto il test set è rappresentativo, bilanciato e indipendente
dal training.
Un processo di splitting corretto è essenziale per garantire che la stima dell'errore sia il più
affidabile possibile.

Quando il dataset è molto grande, il data splitting è semplice da gestire perchè anche una piccola
porzione dedicata al test risulta statisticamente significative.
Al contrario, con dataset ridotti la suddivisione deve essere più attenta, perchè ogni esempio sottratto
al training riduce la capacità del modello di imparare.
In questo casi tecniche come la cross-validation diventano indispensabili per aumentare la qualità
della stima dell'errore.
Le dimensioni influenzano anche la definizione del validation set, che potrebbe essere troppo piccolo
per una scelta degli iperparametri affidabile.
La strategia di splitting deve essere calibrata in funzione della quantità di dati realmente disponibili

"""
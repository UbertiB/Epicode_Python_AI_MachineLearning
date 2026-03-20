"""
DATA SCIENCE PROCESS

il processo della datascience non è lineare ma ciclico e iterativo, ogni fase è collegate alle altre, 
creando un flusso continuo di apprendimento.
L'obiettivo non è solo analizzare i dati, ma trasformali in conoscenza utile e azionabile.
Non esiste un singolo modello di processo valido per tutti i progetti, ogni caso ha le sue esigenze
E' la data science ad adattarsi al problema e non il contrario, per cui la data science deve essere 
flessibile.

Il processo sembra lineare:
- Data collection   - Data pre-processing and Cleaning  - Model (Planning & Building)   - Deploying & Communicating Results
per poi tornare il punto di partenza.

A cosa serve avere un processo se ogni problema ha le sue necessità ed esigenze?
Il processo fornisce una linea guida dalla stato grezzo dei dati all'interpretazione finale.
Senza una metodologia chiara, il rischio è perdersi nella complessità dei dati e delle tecniche.
Nella Data Science (e non solo), seguire un framework permette di:
    - mantenere qualità, coerenza e ripetibilità,
    - facilitare la comunicazione tra i vari team coinvolti, definendo le mansioni di ciascun ruolo,
    - ridurre errori, evitare sprechi di tempo e rendere più trasparente sul lavoro svolto.

Il processo di Data Science può essere realizzato tramite vari framework, ne vedremo 2

1) CRISP-DM (Cross Industry Standard Process for Data Mining): E' una metodologia ampliamente utilizzata che 
    guida i progetti di data mining.
    Facilita una gestione efficace dei progetti e risultati di successo in diversi settori industriali
    (per questo motivo chiamato crosso indutry), fornendo un approccio strutturato e composto da sei fasi.
    1) Business Understanding: comprensione degli obiettivi e dei requisiti del progetto dal punto di vista aziendale
    2) Data Understanding: raccolta e analisi delle proprietà e pertinenze dei dati per lo scopo
    3) Data Preparation: preprocessing e feature selection
    4) Modelling: applicazione dei metodi statistici e algoritmi di ML per allenare i modelli
    5) Evaluation: valutazione delle performance del modello usando metriche e tecniche per 
        migliorare le performance
    6) Deployment: implementazione del modello in produzione ossia disponibile a livello pratico
        per effettuare previsioni, automatizzare decisioni o fornire approfondimenti.
2) OSEMN
    1) Obtain: raccolta dei dati necessari dalle varie fonti. I dati science devono garantire che i dati
        raccolti siano di buona qualità (pertinenti, consistenti, pertinenti, coerenti, ecc)
    2) Scrub: consiste nel preparare i dati per l'analisi, include la gestione dei valori mancanti, 
        la rimozione dei valori anomali, la correzione degli errori e la standarizzazione dei formati dei dati
    3) Explore: i data scientist analizzano i dati per individuare modelli, tendenze e relazioni. Vengono
        utilizzate varie tecniche come la visualizzazine, l'analisi statistica e le statistiche riassuntive
        per esplorare i dati e generare ipotesi.
    4) Model: creazione di modelli predittivi o descrittivi utilizzando algoritmi di statistica e ML. 
        Il fine è cogliere con precisione i pattern sottostanti nei dati e di effettuare previsioni o classificazioni
    5) Interpret: valutazione delle prestazioni del modello, l'interpretazione dei risultati e la 
        comunicazione dei risultati, alle parti interessate per decision making.

Entrambi i framework esplicano le stesse funzioni anche più o meno, nello stesso ordine. La scelta tra i 
due dipende dalla complessità del progetto, dalle esigenze dell'organizzazione e dalle preferenze del team.
Esempio per creare un sistema di manutenzione predittiva di un impianto industriale CRISP-DM garantisce
una comprensione completa delle peculiarità dei macchinari e la loro integrazione nel flusso di lavoro 
già esistente.
OSEMN invece è più appropriato quandi si tratta di iniziative su piccola scala o quandi si eseguono esercizi
preliminari di esplorazione dei dati.
Quando si perfezionano le caratteristiche del prodotto analizzando il feedback dei clienti, OSEMN consente 
di estrarre rapidamente informazioni chiave, supportando cosi un rapido processo decisionale e processi
di miglioramento iterativi.
Non esiste un framework migliore, dipende sempre dal contesto.
Molto spesso di adottano approcci misti per trarre benefici e vantaggi di entrambi.

Librerie Python:
    - Pandas: analisi e manipolazione dei dati
    - Numpy: calcolo scientifici
    - Matplotlib e Seaborn: per visualizzazione e grafici
    - Scikit-lear: per machine learning
    - PyTorch (sviluppato da Meta) e TensorFlow & Keras: per deep learning
  
"""
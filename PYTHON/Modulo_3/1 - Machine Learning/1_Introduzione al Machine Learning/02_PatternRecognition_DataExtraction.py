"""
PATTERN RECOGNITION E DATA EXTRACTION

DATA EXTRACTION
    - DESCRIZIONE: 
        E' un processo durante il quale si estraggono informazioni utili da date grezzi, spesso 
        non strutturati o difficili da analizzare direttamente.
        E' uno step fondamentale poichè i dati disponibili raramente sono pronti per essere utilizzati
        per un'analisi.
        L'obbiettivo è raccogliere i dati da diverse fonti e in diversi formati, per poi renderli disponibili
        e utilizzabili in progetti di Data SCience 
        Nelle aziende viene adottato un modello ETL (Extract, Transform, Load), nella fase di estrazione
        sono presenti varie fonti, vengono raccolti, trasformati in un formato uniforme e caricati in un
        altro database, pronti all'uso per un'analisi statistica
    - Fonti dati:
        Esistono diverse fonti da dove provengono i dati:
            - Registrazioni passive: dati tipicamente già strutturati esempio transazioni bancarie, 
                registrazioni acquisti, documenti archiviati. Vengono solo raccolti e normalmente non serve
                alcne trasformazione.
            - Generazione attiva: dati semi-strutturati o destrutturati, esempio social media.
            - Produzione automatica: dati mobili e sensori a posizione e contesto, esempio dispositivi
                connessi a OiT, uma macchina, un firewall
    - Acquisizione: La fase di acquisizione consiste nel raccoglire e trasferire i dati dalla loro fonte
        verso infrastrutture dedicate, che possono essere sistemi, applicazioni e più in generale servizi.
        Una volta raccolti, i dati devono essere trasmessi attraverso collegamenti ad alta capacità fino ai
        data center.
        Successivamente vengono integrati, puliti, e privati delle ridondanze per garantire consistenza
        e qualità (preprocessing) per l'analisi.
        Esistono due approcci per la collezione dei dati:
         1) PULL: esempio web crawler (scannarizza pagine web), API REST (si espone un servizio e dei 
            sistemi vanno a richiedere i dati necessari), pyton pandas
         2) PUSH: chi ha bisogno di acquisire questi dati non ha la necessità di tirarli, ma vengono 
            automaticamente acquisiti; esempio videosorveglianza, notifiche log dai server
    - Archiviazione: la memorizzazione dei dati richiede infrastutture scalabili e resilienti.
        Si possono utilizzare diverse tecnologie di storage: HDD o SSD a seconda delle performance richieste.
        In generale queste tecnologie si possono adoperare in diversi modi che vanno ad influenzare 
        l'accessibilità dei dati:
            1) DAS (Direct Attached Storage):
            2) NAS (Network Attached Storage): i sistemi di archiviazione sono 'interno ad un network ed 
                acessibili da tutti gli altri host che ne fanno parte
            3) SAN (Storage Area Network):collegamento tra server e sistemi di archiviazione
        In generale la gestione dei dati passa sempre attraverso file system distribuiti come 
        Hadoop Distributed FS o Ceph, database a colonne come Cassandra, o documentali come MongoDB (JSON-like)
    - Preprocessing: I dati reali sono spesso sporchi e la loro qualità influenza anche il prodotto finale 
        dall'analisi. Molto professonisti della datascience dedicano più tempo e cura a questa fase che 
        nelle restanti.
        Il preprocessing server a pulire i dati:
            - riducendo il rumore
            - risolvendo le incoerenze, incosistenze, informazioni vuote
            - eliminando outlier
    - Machine learning, Data Mining e statistica    
        Quano i dati sono puliti, è possibile applicare motodo di machine learning, data mining, e statistica,
        per estrarre informazioni utili dai dati disponibili.
        L'informazione estratte deve essere implicita, non ovvia all'umano e spesso sconosciuta a priori e 
        possibilmente utile.
        Il risultato è rappresentato tramite modelli astratti chiamati pattern, sono delle regole che non sono
        visibili all'occhio umano ma riconoscibili da un algoritmo.
        I pattern sono la base per costruire previsioni, classificazioni e decisioni data-driven.
    - SFIDE PRINCIPALI:
        - Qualità dei dati: può compromettere l'intera pipeline di analisi
        - Varieta delle fonti: introduce complessità, poichè ogni formato richiede un metodo di estrazione
            diverso
        - Scalabiiltà: gestire grandi volumi di dati richiede architetture distribuite e risorse elevate.
        - Attendibiità: i dati cambiano nel tempo ed è necessario aggiornare la loro veridicità, legato alla
            qualità dei dati.
        - Legalità: la raccolta e l'elaborazione deve rispettare la data privacy e copyright, secondo
            le normative e regolamenti vigenti (es. GDPR per l'Europa, CCPA per la California, ecc)

PATTERN RECOGNITION
    - DESCRIZIONE: Il pattern recognition è il processo che permette di identificare automaticamente schemi, 
        strutture o regolarità all'interno dei dati.
        L'obiettivo è estrarre informazioni utili e comprensibli da dati puliti e pre-processati.
        E' estremamente legata alla Data Extraction: prima si raccolgono i dati puliti ed ordinati, 
        poi si cercnao i pattern  significativi.
        E' alla base di molte applicazioni moderne: riconoscimento facciale, anomaly detection, ecc
        In generale permette di identificare schemi e regolarità all'interno dei dati. Mira a classificare 
        dati in categorie note o raggrupparli in cluster.
        Consente di individuare anomalie e comportamenti fuori dal normale.
        Supporta decisoini basate sui dati in settori diversi come finanza, marketing, cybersecurity, e tante altre
        Facilita la predizioni, l'automazione dei processi e ottimizzazione delle operazioni.
    - PROCESSO:
        Il processo parte dai dati grezzi, già estratti e preprocesati duranti la fase di Data Extraction.
        E' lo step successivo alla Feature Extraction che seleziona le caratteristiche più rilevanti dai dati,
        dati che sono già stati puliti, preprocessati ed ordinati.
        Ad identificare schemi e pattern nei dati sono algoritmi di Machine Learning o Pattern Mining.
        Le informazioni ottenute sono rappresentate da classificazioni, cluster, o anomalie individuate in 
        moto automatico.
    - TECNICHE: Si utilizzano tecniche statistiche, per analizzare correlazioni, medie e varianze per scoprire
        pattern nei dati.
        Il Deep Learning consente di riconoscere pattern complessi: CNN (Convolutional Neural Networks) per
        immagini e RNN (Recurrent Neural Networks) per le sequenze.
        Text Mining e NPL (Natural Language Processing) permettono di estrarre schemi dai testi scritti e documenti.
        Il Graph Mining identifica pattern nelle relazioni tra nodi e elementi di rete.
    - SFIDE: Le sfide che si sono incontrate nella Pattern Recognition sono molto legate a quelle della data
        Extraction ma hanno delle leggere sfumature:
        - Qualità dei dati: anche qui, la qualità dei dati è fondamentale, dati sporchi, incompleti o incoerenti
            producono pattern errati.
        - Scalabilità: volumi di dati molto grandi richiedono elevate capacità e risorse computazionali
        - Interpretabilità: alcuni modelli complessi chiamati 'black box', ossia si sa cosa sono gli 
            input e gli output ma non cosa avviene all'interno
        - Generalizzazione: alcuni pattern possono non valere o essere applicati in contesti diversi
        - Legalità: rispetto di privacy, copyright, normative e regolamentazioni
"""
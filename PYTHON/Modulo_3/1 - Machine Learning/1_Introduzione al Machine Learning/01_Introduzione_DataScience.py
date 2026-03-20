"""
INTRODUZIONE ALLA DATA SCIENCE E KNOWLEDGE DISCOVERY

BIG DATA
- Cosa sono: 
    I big data sono dati la cui  scalabilità, diversità, complessità, richiede nuove archietture, tecniche,
    algoritmi e metodi di analisi per gestirli ed estrarre valore e informazioni nascoste da essi.
    I big data sono generata da utenti, esempio on-line tramite piattaforme social, ecc, generano flussi di
    dati. Possono essere sistemi informatici legati alla sanitià, scienza, log di sistemi informatici, iot,
    gestionale. I dati arrivano da diverse fonti eterogenee.
- Caratteristiche:
    5 V (Volume, Velocità, Varietà, Veridicità, Valore)
    Volume: quantità di dati. Che è cresciuto e continua a crescere in modo esponenziale nel tempo.
    Valocità: ossia la loro velocità di generazione. In sistemi ed applicazione, parallelamente alla valocità
        di generazione è richiesta la velocità di elaborazione.
    Varietà: diversi formati di rappresentazione che i dati possono assumere (numeri, alfabetici, audio,
        video, immagini, ecc). Riassunta in 3 macrocategorie: 1) strutturata: i dati rispettano una struggura
        e regole definite (esempio excel csv) 2) destrutturata: non viene rispettata nessuna forma (audio, foto
        video) 3) semi-strutturata: i dati rappresentati rispettando una forma, mantenendo una certa flessibilità
        (esempio log dei server)
    Veridicità: i dati disponibili possono risultare talvolta disordinati, incoerenti, rendendo la loro 
        qualità e accuratezza difficili da controllare. 
        La qualità dei dati è compromessa da diversi fattori tra i quali: distorsione, informazioni vuote (
        prive di signitifato), outlier, bug dei software, errore umano.
    Valore: il valore è la caratteristica più importante dei big-data. I dati privi di valore non sono utili
        ad un'azienda e/o istituzione o privati, e meno che non si trovi un'utilità. Altrimenti sarebbero
        dei bit conservati in memoria, che occupano spazio inuttilmente.
        Di per se, i dati non hanno utilità, ma possono essere convertiti in qualcosa di prezioso per 
        estrarre informazioni utili. Per questo motivo è la 'V' più importante.
        Trovare valore dai dati permette di: - carpire vantaggi - supportare processi decisionali.
        Alcuni esempi: comportamento dei clienti per prevedere le preferenze future, andamento del mercato
        avendo a disposizione lo storico di un'azione si può prevedere l'andamento futuro
        , prestazioni aziendali, ecc
- Sfide:
    Le principali sfide incontrare sono:
    1) Archiviazione: un'enorme quantità di dati richiede un'infrastruttura di archiviazione avanzata, che 
        può essere costosa e complessa da mantenere. 
        Una soluzione è l'archiviazione in Cloud permette l'adozione di soluzioni scalabili come Amazon S3, Google Cloud
        Storage o Microsoft Azure, possono aiutare a gestire grandi volumi di dati.
    2) Analisi: applicare algoritmi di analisi dei big-data per estrarre informazioni preziose può essere
        complesso e laborioso. Strumenti di analisi avanzata come Apache Spark e Apache Hadoop riduce la 
        complessità di elaborazione

La crescita esponenziale dei dati ha reso necessario sviluppare nuove tecnologia per la loro archiviazione,
gestione ed analisi efficiente. 
Queste sfide hanno stimolato la nascita della Data Science, focalizzata sull'analisi e l'alaborazione dei
Big-Data per estrarre conoscenza ed informazioni utili.

DATA SCIENCE
- Descrizione: La data science si pone come centro dei BigData, integrando discipline come Data Mining, 
    Artificial Intelligence, Machine Learning, Pattern Recognition, Statistical Learning e Deep Learning
    La Data Science significa estrarre  informazioni di significato da grandi quantità di dati (D.J. Patil)
    Nata per sopperire ai limiti dei metodi tradizionali (matematico/statistici, database classici) è la 
    disciplina che combina statistica, informatica e dominio applicativo, per estrarre conoscenda dai dati.
    E' quindi un processo interdisciplinare, che trasforma dati grezzi in informazioni utili e decisioni,
    integrando tecniche di statistica, machine learning e analisi computazionale.
    - Parte da un fenomeno, evento di caso reale, da cui si osserva e si raccolgono dati (raw data) 
    - A questi dati vengono applicate delle tecniche per portarle ad uno stato di pulizia e ordine
     (data cleaning o data pre-processing)
    - Con i dati puliti si possono applicare uno o più metodo statistici o di machine learning, con 
        il fine di creare un MODELLO, un ente informatico statistico, in gradi di capire quali sono
        le relazioni che intercorrono tra questi dati
    - Il modello è in gradi di generalizzare, o estrarre, costruire altri dati, 
    - Questa conoscenza astratta ritorna ad interagire con il caso reale da cui siamo partiti per migliorare
        il processo decisionale, creando un flusso continuo di auto-apprendimento
- Ricetta: sono le conoscenze e competenze necessarie per avviare un progetto di analisi di data science:
    - Data Espertise: conoscere e gestire strutture dati e tecniche di elaborazione
    - Data Analysis: applicare algoritmi di ml
    - Visualizatione Expertise: rappresentare i dati in modo chiaro e intuitivo
    - Domain Expertise: interpretare le informazioni del dominio e campo di applicazione per l'interpretazione
    - Business Expertise: trasformare gli insight dell'analisi in decisioni strategiche di business
    Oltre a tutte queste competenze è necessario porsi delle domande: capire lo scopo dell'analisi, da cosa
    si parte, quali dati saranno utilizzati, quali sono le tecniche che verranno utilizzate, come si 
    valutano i risultati, risorse necessario e quelle disponibili.
- Processo: il processo di data science è composto da 4 step fondamentali:
    1) Data Selection: selezionare e raccogliere i dati da fonti rilevanti, come database aziendali, sensori
        log, ecc. E' il momento in cui si decide cosa vale la pena analizzare
    2) Data Preprocessing: Raccolti i dati vengono puliti e preparat: si eliminano errori, duplicati o valori
        mancanti e si trasformano in un formato uniforme. Questa fase è cruciale perchè la qualità dei dati
        determina direttamente la qualità delle analisi e dei modelli.
    3) Modeling & Analisi: Qui entrano in gioco algoritmi e tecniche statistiche per individuare pattern, 
        fare previoini e scoprire relazioni nascoste. E' la parte 'più intelligente' del processo, 
        dove la Data Science diventa uno strumento per trasformare i dati in conoscenza
    4) Interpretazione: I risultati devono poi essere interpretati e comunicati in modo chiaro, tramite
        visualizzazioni, dashboard o report comprensibili. Questa fase serve a trasformare numeri e modelli
        complessi in decisioni concrete e strategiche.
"""
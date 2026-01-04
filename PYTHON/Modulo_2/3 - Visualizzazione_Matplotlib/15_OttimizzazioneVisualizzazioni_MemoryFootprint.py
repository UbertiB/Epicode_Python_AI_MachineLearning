"""
La capacità di ottimizzare la visualizzazione e gestire in modo efficiente la momoria diventa importante
quando i dati diventano tanti. Non basta saper creare grafici accattivanti ma devono essere anche semplici e veloci
Il memory footprint è lo spazio di memoria occupato da un programma durante l'esecuzione. 
Ridurlo è una priorità, dove ogni mb risparmiato può tradursi in maggiore scalabilità e stabilità

Tecniche per ottimizzare i grafici, afforntare dataset di grandi dimensioni, riduerre il consumo di memoria,
valutare compromessi tra qualità e prestazioni e adottare strumenti workflow avanzati per miglioarare 
efficiente a produttività

Un grafico ben progettato non deve essere solo esticamente carino ma anche rapido da generare e facile da interpretare.
L'ottimizzazione parte dalla riduzione degli elementi superflui, quando una sintesi o un campionamento può trasmettere
lo stesso messaggio in modo più leggero.
Acluni formati randset possono risultare pesanti con tanti dati, mentre grafici vettoriali possono 
risultare più veloci.
Anche piccoli argomenti, come ridurre lo spessore delle linee, ridurre i colori, alleggerire le griglie, 
possono migliorare le prestazioni.
Quando si affrontano dataset molto grandi, il caricamente completo in memoria diventa non fattibile, in questi casi 
è necessario ricorrere a strategia alternative.
Una tecnica diffusa è il chunk, dividere il dataset in dataset più piccoli da lavorare sequenzialmente.
E' importante adottare formati di archiviazione più efficienti del classico csv (esempio parquet o feder)
La gestione di dataset di grandi dimensioni, richiede una mentalità scalalbile, non chiedersi solo come
analizzare tutti subito ma come suddividere filtrare, ridurre i dati, manenendo intatta l'informazione rilevante.
La scelta del tipo di dato aiuta a ridurre le dimensioni con downcasting.
Np offre anche array estremamente compatti rispetto alle struttura native di python (come le liste) 
quindi preferire array np per grandi volumi di dati, questo migliora le prestazioni e riduce l'uso della memoria.
Ogni processo di ottimizzazione implica un compromesso tra qualità e prestazioni.
non sempre è utile generare grafici estremamente dettagliati.
Il principio guida deve essere la chiarezza, un grafico con milioni di punti diventa illegibile rispetto 
ad un grafico con meno dettagli.
Bisoga valutare il contesto, per una pubblicazione scientifica può essere accettabile sacrificare le prestazioni 
in favore della precisione, mentre per una dashboard iterativa preferibile la velocità. 
La scelta ottimale non è assoluta ma dipende dall'obbiettivo comunicativo e dal pubblico

Esistono degli strumenti dedicati per distruibuire elaborazioni di dati su più core o più cluster consentendo
di gestire dataset che superano la memoria disponibile.

L'ottimizzazione non è un processo isolato deve essere parte integrante di un workflow ideale
- pianificazione preventiva, scegliere i formati di archiviazione e strutture dati ottimizzate
- riduzione dei dati, lavorare solo sulle informazioni necessarie evitando di caricare colonne o righe non utili 
- ottimizzazione interativa, testando diverse strategie di visualizzazione e confrontando l'impatto in termini di memoria
- automatizzazione integrando chunck, conversioni di tipo e formati di output
Questo permette di migliorare le prestazioni, ridurre errori, aumentari la produttività

"""


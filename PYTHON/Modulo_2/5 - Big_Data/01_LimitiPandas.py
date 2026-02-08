"""
LIMITI DI PANDAS CON DATASET DI GRANDI DIMENSIONI

Pandas è una delle librerie più diffuse e potenti per la manipolazione ed analisi dei dati con Python.
Grazie alla sua flessibilità ed alla sua faciltà d'uso, è lo strumento preferito per operazioni 
di data cleaning, trasformazioni e analisi epslorativa.
Con dataset molto grandi, pandas mostra limiti strutturali che possono compromettere le prestazioni.
Questi limiti arrivano dalla sua architettura.
Pandas è pensato per analisi in memoria e non per gestire quantità di dati che 
eccedono la dimensione della ram.
Conoscere questi limiti è essenzionale per affrontare scenari di big-data.
Analizziamo le principali criticità di pandas con dataset di grandi dimensioni e le possibili soluzioni 
interne ed esterne a Pandas.
Il primo ed evidente limite di Pandas è la sua dipendenza della memori ram, perchè ogni df viene caricato
interamente in memoria, questa vuol dire che le dimensioni dei dati non possono superare la quantità di 
memoria, questo porta che alcuni dataset grandi possono saturare la memoria.
Inoltre le operazioni di copia implicita dei df, che pandas esegue in molte trasformazioni, amplifica il 
consumo di memoria.
Per mitigare questo limite è utile:
- caricare solo il subset necessario
- utilizzare tipi di dato più leggeri
- leggere i files in streaming
Ma l'approccio è limitato con dataset molto elevati.

Pandas è pensato per operazioni vettoriali molto efficienti, ma NON SFRUTTA IL PARALLELISMO DEL PROCESSORE.
Molte operazioni vengono eseguite su un singolo core, il che limita la scalabilità su macchine multi-core.
In scenari complessi, Panda può risultare più lento rispetto a framework distribuiti, anche se 
sfrutta librerie ottimizzate come numpuy. 
la mancanza di parallelismo rimane un collo di bottiglia.
Un'altra limitazione è la GESTIONE SEQUENZIALE DEI TASK, la maggior parte delle operazioni NON può essere
suddivisa automaticamente in blocchi indipendenti ad essere eseguiti in modo parallelo.
La gestione dei TIPI DI DATO in pandas influisce notevolmente sull'uso di memoria e sulle prestazioni.
Per impostazione predefinita molti campi sono caricati come object anche quando potrebbero essere 
rappresentati con tipi più compatti.
Questa scelta, se non corretta manualmente, comporta un aumento drastico del consumo di memoria 
e rallentamenti.
Inoltre la conversione automatica dei tipi puo introdurre errori o perdita di precisione nei dati numerici
un uso consapevole dei tipi di dati, definendoli esplicitamente, è una delle tecniche pià efficaci per
migliorare le prestazioni di pandas riducendo il consumo di memoria.
Pandas è ottimizzato per analisi su scala medio piccola, quando la dimensione del dataset cresce le sue 
prestazioni non scalano in modo lineare, operazioni possono richiedere  minuti o ore su molti dati.
La mancanza della gestiona nativa della memoria virtuale e la difficoltà di lavorare in chunk rendono pandas
inadatto a dataset che non possono essere caricati interamente in ram.

Per gestire dataset oltre le capacità di Pandas, è necessario ricorrere a tecniche di campionamento
elaborazioni distribuite, o strumenti per gestire flussi di dati progressivi.
Nonostrante i suoi limiti Pandas offre alcune soluzioni
Una delle strategiè più comuni è la LETTURA DEI DATI IN CHUNK, permette di elaborare i dati 
progressivamente senza caricali interamente in memoria.
Un altra soluzione consiste nella compressione e nella conversione in FORMATI PIu'' EFICIENTI 
compe parquet o feather che riducono il peso del file grazie al loro formato binario.
Anche la scelta dei TIPI DI DATO può migliorare significativamente le prestazioni.
Inoltre l' integrazione di pandas con numpy pyerrow e librerie di calcolo vettoriale consente di ottimizzare
alcune operazioni anche se il guadagno riamane limitato rispetto ad approcci distribuiti.

Quando i dataset diventano troppo grandi, è opportuno ricorrere a strumenti alternativi:
* DASK: estende Pandas ma dive i dati in blocchi distribuiti permettendo l'elaborazione parallela 
        su più core/cluster
* POLARS: Basato su Rust, molto veloce e multi-thread, rappresentando un'alternativa moderna e performante
* VAEX: Lazy evaluation, gestione dataset enormi senza caricarli in ram
* DUCKDB: Query SQL su file giganti, ideali per analisi veloci, permette analisi su disco
* PYSPARK: Big data distribuiti su cluster, permette analisi su disco
"""

#Generiamo un file molto grande

import pandas as pd
import numpy as np

n=1_000_000
np.random.seed(42)

if False:
    df=pd.DataFrame({
        "id":np.arange(1,n+1),
        "categoria": np.random.choice(["A","B","C","D"],n),
        "valore": np.random.uniform(10,1000,n),
        "data":pd.date_range("2020-01-01",periods=n,freq="H"),
    })
    df.to_csv("dati_grandi.csv",index=False)

#lettura in chunck
chunks=pd.read_csv("dati_grandi.csv",chunksize=100_000)
for chunk in chunks:
    media=chunk["valore"].mean()
    print(media)

#conversione di tipi di dati per ridurre la memoria
df=pd.read_csv("dati_grandi.csv")
df["categoria"]=df["categoria"].astype("category")
df["id"]=df["id"].astype("int32")
print(df.info(memory_usage="deep"))
#prima di convertire in int32 assicurati che non ci siano valori notanumber,se ci sono devi prima gestireli
#esempio riempirli o usare int32pandasnullabledtipye
#è possibile anche leggere con dtype specificati direttamente in read_csv

#utilizzo di DASK come alternativa a pandas

import dask.dataframe as dd

df=dd.read_csv("dati_grandi.csv")
media=df["valore"].mean().compute() #.compute usa le partizioni cpu 
print(media)
#compute esegure il calcolo parallelamente usando tutte le partizioni cpu disponibili e restituisce  
#direttamente il risultato finale


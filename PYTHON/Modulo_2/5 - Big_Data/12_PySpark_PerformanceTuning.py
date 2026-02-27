"""
PYSPARK PERFORMANCE TUNING: PARTITIONING, CACHING, E SHUFFLES

Quandi si lavora con dataset di grandi dimensioni su cluster distribuiti, il semplice utlizzo di 
pyspark non garantisce, automaticamente, alte performance.
Ogni operazioni (dalle aggregazioni ai join complessi) comporta un costo in termini di tempo e risorse 
computazionali, soprattutto quando si tratta di dataset molto grandi.
Comprendere come spark gestisce i dati in memoria, come divide le partizioni e come trasferisce i dati
tra i nodi è fondamentale per ottimizzare i job.
Il Tuning delle performance consiste nell'applicare strategie mirate per migliorare la velocità di 
esecuzione, ridurre l'uso di memoria e prevenire colli di bottiglia.
Tra gli sturmenti principali troviamo partitioning, caching, e shuffle optimization, elementi che 
influenzano direttamente le performance di Spark.

PARTITIONING
Il partitioning è il modo in cui Spak divide i dati elaborabili in parallelo.
Ogni partizione può essere processata da un core o da un nodo del cluster consentendo parallelismo e
scalabilità.
La scelta di un buon schema di partizionamento è fondamentale, partizioni troppo grandi possono 
creare colli di bottiglia, mentre troppe partizioni piccole generano overhead nella gestione dei task.
Partizionare correttamente i dati, migliora l'efficienza di join ed aggregazioni, perchè riduce
il numero di dati che devono essere trasferiti tra nodi, minimizzando i costi di shuffle.

Shuffle è il processo di ridistribuzione dei dati tra le partizioni durante operazioni come join 
e groupby, è una delle operazioni più costose in termini di tempo e risorse computazionali, 
perchè comporta la scrittura e lettura dei dati su disco e il trasferimento dei dati tra i nodi 
del cluster (trasferimento di rete). Questo succede con le operazioni che richiedono dati da altre
partizioni, come join, orderby e groupby. Durante lo shuffle Spark crea file intermedi (spesso su disco)
e li redistribuisce tra i nodi.
Filter e select non hanno bisogno di spostare i dati (shuffle) perchè lavorano localmente su ciascuna 
partizione, mentre join e groupby richiedono uno shuffle
Conoscere il funzionamento interno di spark e come il partitionig influsce sul dag dei job è il 
primo passo per ottenere performance ottimali.
Minimizzare gli shuffle è essenziale per migliorare le performance, soprattutto quando si lavora con
dataset di grandi dimensioni, perchè gli shuffle possono diventare un collo di bottiglia significativo,
rallentando drasticamente i tempi di esecuzione e aumentando l'uso di risorse computazionali.
Identificare quali operazioni generano shuffle permettono di miglioare i job
Una corretta distribuzione dei dati, tramite partitioning, 
Un altra tecnico è il broadcast join, che consente di inviare una piccola tabella a tutti i nodi 
del cluster, evitando lo shuffle durante i join con tabelle più grandi.

Possiamo controllare il numero di partizioni con metodi come REPARTITION() e COALESCE(), e scegliere
il tipo di partizionamento più adatto al nostro caso d'uso.
* df.repartition(n): ridistribuisce uniformemente i dati creando n partizioni, spesso generando  uno
  shuffle completo;
* df.coalesce(n): riduce il numero di partizioni n senza eseguire uno shuffle completo. Risultanto
  più efficiente quando si lavora con dataset già ridistribuiti correttamente.
Utile quando le partizioni originali sono sbilanciate o il carico sui nodi non è uniforme.

La scelta del numero di partizioni dipende dal numero di core disponibili, dalla dimensione dei dati
e dal tipo di operazioni da eseguire, importante trovare un equilibrio tra parallelismo e overhaed.
Una regola empirica suggerisce di avere 2 o 4 partizioni per ogni core fisico.

PARTITIONING PER KEY (DATA SKEW)
Il data skew si verifica quando una chiave specifica ha un numero sproporzionato di record, causando
partizioni sbilanciate e conseguenti colli di bottiglia.
Alcune chiavi hanno una quantità enorme di righe rispetto ad altre, causando partizioni molto
grandi e partizioni molto piccole, questo squilibrio può portare a rallentamenti significativi, 
perchè alcune partizioni richiedono molto più tempo per essere processate rispetto ad altre, causando
inefficienze e tempi di esecuzione più lunghi.
Per gestire il data skew, si utilizzano tecniche come il salting, che consiste nell'aggiungere un 
valore casuale alla chiave per distribuire i meglio dati in modo più uniforme tra le partizioni 
o il custom partition dove si definisce una funzione di partizionamento basata sulla frequenza 
delle chiavi.
Ridurre lo skew è essenziale in join ed aggregazioni, perchè partizioni sbilanciate possono causare
rallentamenti significativi, con alcune partizioni che richiedono molto più tempo per essere
processate rispetto ad altre, causando inefficienze e tempi di esecuzione più lunghi.

CHASING E PERSISTING
Il chaching è una tecnica fondamentale che consente di memorizzare i dati in memoria per velocizzare
le operazioni successive.
df.cache() Spark mantiene i dati in memoria, evidando di dover ricalcolare i dati in operazioni 
successive.
In alternativa df.persist(StorageLevel.MEMORY_AND_DISK) permette di definire il livello di 
memorizzazione desiderato, se la memoria è insufficiente, i dati vengono scritti su disco, 
garantendo che siano sempre disponibili per operazioni successive, anche se a costo di prestazioni 
inferiori rispetto al caching in memoria.
Spark offre diverse opzioni di caching, come MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, che permettono 
di scegliere come gestire i dati in memoria e su disco in caso di mancanza di memoria.
Il caching è particolarmente utile quando si eseguono più operazioni su un dataset, come join o 
aggregazioni, perchè evita di dover ricalcolare i dati ogni volta, migliorando significativamente 
le performance.
Il persisting è simile al caching, ma offre più opzioni di memorizzazione, 
come MEMORY_ONLY_SER, MEMORY_AND_DISK_SER, che consentono di memorizzare i dati in formato 
serializzato per risparmiare memoria, a costo di un maggiore tempo di CPU per la serializzazione 
e deserializzazione.
Scegliere tra caching e persisting dipende dalle esigenze specifiche del job, dalla dimensione 
dei dati e dalle risorse disponibili, è importante monitorare l'utilizzo della memoria e le 
performance per ottimizzare l'uso di queste tecniche.
df.cache(): spark memorizza i dati in memoria, se la memoria è insufficiente, i dati non vengono
memorizzati e devono essere ricalcolati quando necessario. 
Questo evita di ricalcolare datafreme complessi in operazioni successive.
df.persist(StorageLevel.MEMORY_AND_DISK): permette di definire il livello di memorizzazione desiderato
se la memoria è insufficiente, i dati vengono scritti su disco, garantendo che siano sempre 
disponibili per operazioni successive, anche se a costo di prestazioni inferiori rispetto al 
caching in memoria.

Utilizzare correttamente queste tecniche può ridurre drasticamente i tempi di esecuzione, quando si 
lavora con dataset di grandi dimensioni, evitando ricalcoli inutili e migliorando l'efficienza 
complessiva del job.

COME RIDURRE GLI SHUFFLE 
Lo shuffle è il processo con cui Spark ridistribuisce i dati tra le partizioni durante operazioni come
join, groupby e aggregazioni, è una delle operazioni più costose in termini di tempo e risorse
computazionali, perchè comporta la scrittura e lettura dei dati su disco e il trasferimento dei dati
tra i nodi del cluster (trasferimento di rete).
Per ridurre gli shuffle, è importante progettare le query in modo da minimizzare la necessità di 
ridistribuire i dati, ad esempio evitando join non necessari, filtrando i dati il prima possibile e
sfruttando le funzionalità di caching e persistenza di Spark SQL.
Utilizzare partizioni basate su chiavi comuni per join e aggregazioni può ridurre significativamente
i costi di shuffle, perchè i dati che devono essere uniti o aggregati si trovano già nella stessa
partizione, evitando la necessità di trasferire grandi quantità di dati tra i nodi del cluster.
Ottimizzzare le query per ridurre gli shuffle è essenziale per migliorare le performance, soprattutto
quando si lavora con dataset di grandi dimensioni, perchè gli shuffle possono diventare un collo di
bottiglia significativo, rallentando drasticamente i tempi di esecuzione e aumentando l'uso di risorse
computazionali.
Comprendere come funzionano gli shuffle è fondamentale per progettare query efficienti e ottimizzare
le performance di Spark SQL, sopratutto in ambito aziendale, dove la velocità di esecuzine è spesso
un fattore critico per il successo dei progetti di analisi dei dati.
In sintesi, il tuning delle perfomance di Spark SQL richiede una comprensione approfondita di come
Spark gestisce i dati in memoria, come dividere le partizioni e come ridurre i costi di shuffle, 
attraverso tecniche come il partitioning, il caching e la progettazione di query efficienti, è 
possibile miglioare significativamente le perfomance di job complessi.

BROADCAST
Broadcast significa "questa tabella è piccola, la copio su tutti gli executor, così evito lo
shuffle della join".
Il broadcast join è una tecnica che consente di inviare una piccola tabella a tutti i nodi del cluster,
evitando lo shuffle durante i join con tabelle più grandi, è particolarmente utile quando si
lavora con dataset di grandi dimensioni, perchè riduce significativamente i costi di shuffle, 
migliorando la performance complessiva dei job Spark SQL.

Per ottimizzare le performance è importante monitorare i jon e diagnosticare i colli di bottiglia,
utilizzando strumenti come SPARK UI, che fornisce informazioni dettagliate sui job, le fasi di esecuzione
e le operazioni di shuffle, permettendo di identificare le arre che richiedono ottimizzazione e di 
applicare le tecniche appropriate per miglioare le perfomance complessiva dei job Spark SQL.
EVENT LOG e le METRICHE DI CPU e MEMORIA aiutano ad individuare partizioni squilibrate o dataset
troppo grandi per alcune operazioni.
Analizzare i dag e le dipendenze tra le operazioni è fondamentale per identificare i punti critici e 
ottimizzare il piano di esecuzione, riducendo i tempi di esecuzione e migliorando l'efficienza 
complessiva dei job Spark SQL.

1) PARTITIONING: scegliere un buon schema di partizionamento, evitare partizioni troppo grandi o  
   troppo piccole, utilizzare tecniche come il salting per gestire il data skew, e utilizzare il 
   broadcast join per evitare shuffle durante i join con tabelle più grandi.
2) CACHING E PERSISTING: utilizzare il caching per memorizzare i dati in memoria e velocizzare le 
   operazioni successive, e utilizzare il persisting per definire il livello di memorizzazione 
   desiderato, scegliendo tra diverse opzioni di caching in base alle esigenze specifiche del job.
3) RIDURRE GLI SHUFFLE: progettare le query in modo da minimizzare
   la necessità di ridistribuire i dati, evitando join non necessari, filtrando i dati il prima possibile e sfruttando le funzionalità di caching e persistenza di Spark SQL, e utilizzare partizioni basate su chiavi comuni per join e aggregazioni per ridurre significativamente i costi di shuffle.
   Il tuning delle performance di Spark SQL richiede una comprensione approfondita di come Spark gestisce i dati in memoria, come dividere le partizioni e come ridurre i costi di shuffle, attraverso tecniche come il partitioning, il caching e la progettazione di query efficienti, è possibile migliorare significativamente le performance di job complessi, soprattutto in ambito aziendale, dove la velocità di esecuzione è spesso un fattore critico per il successo dei progetti di analisi dei dati.

"""

from pyspark.sql import SparkSession
import time
import os
from pathlib import Path
from pyspark.sql.functions import broadcast

HADOOP_HOME = r"C:\hadoop"


# set env
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")

# pyspark python
os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

spark=SparkSession.builder.appName("Partition example").getOrCreate()

data=[(I,I%3) for I in range(1_000_000)]
df=spark.createDataFrame(data,["valore","categoria"])
print(f"N. di partizoini iniziali: {df.rdd.getNumPartitions()}")

#repartition per bilanciare il carico, riorganizzo i dati in 10 partizini basando sul valore
#della colonna categoria
df_repart=df.repartition(10,"categoria")
print(f"N. di partizoini dopo repartition: {df_repart.rdd.getNumPartitions()}")

#caching dei dati
df_chached=df_repart.cache()
#eseguo un'azione per forzare l'esecuzione del caching
df_chached.count() #lasy evaluetione, con count forse l'esecuzione
#viene eseguita solo per contare le righe, ma i dati vengono memorizzati in memoria per operazioni successive
totale_per_categoria=df_chached.groupBy("categoria").sum("valore").show()

#broadcast (join con tabella più piccolare) per ridurre lo shuffle
#il broadcast join per evitare lo shuffle durante il join, inviando la tabella più piccola a tutti 
#i nodi del cluster, migliorando le performance complessive del job Spark SQL.
small_df=spark.createDataFrame([(0,"A"),(1,"B"),(2,"C")],["categoria","descrizione"])
df_join=df_repart.join(broadcast(small_df), on="categoria",how="inner")
df_join.show()

spark.stop()

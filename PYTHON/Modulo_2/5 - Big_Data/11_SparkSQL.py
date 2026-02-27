"""
SPARK SQL: QUERY DISTRIBUITE E INTEGRAZIONE AZIENDALE
Spark SQL è un modulo di Apache Spark che consente di eseguire query SQL su dati distribuiti.
Spark SQL fornisce un'interfaccia per lavorare con dati strutturati e semistrutturati, 
consentendo agli utenti di eseguire query SQL su DataFrame e Dataset.
Spark SQL supporta anche l'integrazione con sistemi di archiviazione esterni, 
come HDFS, S3, Hive e JDBC, consentendo agli utenti di accedere e analizzare dati da diverse fonti.
Spark SQL utilizza un motore di esecuzione ottimizzato per eseguire query in modo efficiente 
su grandi volumi di dati, sfruttando la potenza di calcolo distribuito di Spark.
Spark SQL supporta anche l'ottimizzazione delle query, che consente di migliorare le prestazioni 
delle query attraverso tecniche come il pushdown dei filtri, la gestione intelligente delle 
partizioni e l'ottimizzazione del piano di esecuzione.
Spark SQL è ampiamente utilizzato in ambito aziendale per l'analisi dei dati, la creazione di report 
e la costruzione di pipeline di dati complesse, grazie alla sua capacità di gestire grandi volumi 
di dati in modo efficiente e scalabile.
Permette agli utenti di sfruttare tutta la potenza di Spark mantentendo la sintassi famigliare di 
query SQL.
La forza di spark SQL sta nella capacita di combinare query distribuite con l'elaborazione di grandi
dataset in paralello, consentendo analisi veloci e scalabili. Questo approccio rende spark sql
uno strumento ideale per progetti aziendali (performance ed affidabilità sono fondamentali)
Spark SQL si base su un architettura modulare ottimizzata.
Il cuore di Spark SQL è il CATALYST OPTIMIZER, un motore di ottimizzazione delle query che analizza 
e trasforma le query SQL in piani di esecuzione efficienti. 
Catalyst utilizza tecniche avanzate di ottimizzazione, come la riscrittura delle query, l'ottimizzazione 
del piano di esecuzione e la gestione intelligente delle partizioni, per migliorare le prestazioni 
delle query su grandi volumi di dati.
Ogni query passa attraverso diverse fasi di ottimizzazione, semplificazione delle espressioni, 
eliminazione delle ridondanze, pianificazione del join ed ottimizzazione degli shuffle, 
per garantire che le query vengano eseguite nel modo più efficiente possibile.

Spark SQL supporta anche il DATAFRAME API, che consente agli utenti di lavorare con dati strutturati 
in modo più intuitivo e flessibile rispetto alle query SQL tradizionali. 
Il DataFrame API offre un'interfaccia di programmazione ad alto livello per manipolare i dati, 
consentendo agli utenti di eseguire operazioni come filtraggio, aggregazione, ordinamento e 
join in modo semplice e efficiente.
Spark SQL è progettato per essere altamente scalabile e può gestire grandi volumi di dati in modo 
efficiente, sfruttando la potenza di calcolo distribuito di Spark. 
Grazie alla sua architettura modulare e al motore di ottimizzazione Catalyst, Spark SQL è in grado 
di eseguire query complesse su grandi dataset in modo rapido e affidabile, rendendolo uno strumento 
ideale per l'analisi dei dati in ambito aziendale.

In Spark SQL ogni query viene automaticamente distribuita tra i nodi del cluster.
Operazione vengono suddivise in task paralleli che vengono eseguiti sui nodi del cluster, sfruttando la potenza di calcolo distribuito di Spark.
Spark SQL gestisce automaticamente la distribuzione dei dati e l'esecuzione delle query, consentendo agli utenti di concentrarsi sull'analisi dei dati senza doversi preoccupare della complessità dell'elaborazione distribuita.
Spark SQL utilizza un motore di esecuzione ottimizzato per eseguire query in modo efficiente su grandi volumi di dati, sfruttando la potenza di calcolo distribuito di Spark.
Spark SQL supporta anche l'ottimizzazione delle query, che consente di migliorare
le prestazioni delle query attraverso tecniche come il pushdown dei filtri, la gestione intelligente delle partizioni e l'ottimizzazione del piano di esecuzione.
Spark SQL è ampiamente utilizzato in ambito aziendale per l'analisi dei dati, la creazione di report e la costruzione di pipeline di dati complesse, grazie alla sua capacità di gestire grandi volumi di dati in modo efficiente e scalabile.
Spark SQL è uno strumento potente per l'analisi dei dati in ambito aziendale, grazie alla sua capacità di eseguire query distribuite su grandi volumi di dati in modo efficiente e scalabile.
Spark SQL consente agli utenti di sfruttare tutta la potenza di Spark mantenendo la sintassi famigliare di query SQL, rendendolo uno strumento ideale per progetti aziendali in cui le prestazioni e l'affidabilità sono fondamentali.

le query distribuite riducono drasticamente i tempi di esecuzione, anche su dsataset complessi e 
voluminosi.
Spark SQL si integra facilmente con diverse fonti dati aziendali, come database relazionali, 
data warehouse e sistemi di archiviazione cloud, consentendo agli utenti di accedere e analizzare 
dati da diverse fonti in modo efficiente.
Spark SQL supporta anche l'integrazione con strumenti di business intelligence (BI) e dashboard, 
consentendo agli utenti di creare report e visualizzazioni basati sui dati analizzati con Spark SQL.
Spark SQL è uno strumento potente per l'analisi dei dati in ambito aziendale, grazie alla sua 
capacità di eseguire query distribuite su grandi volumi di dati in modo efficiente e scalabile, 
rendendolo una scelta ideale per progetti aziendali in cui le prestazioni e l'affidabilità sono 
fondamentali. 

Questa flessibilità consente di centralizzare l'elaborazione dei dati in un unico framework.

L'adozione di spark sql porta numerosi vantaggi, permformance, scalabiltà, integrazione con fonti
dati aziendali, supporto per strumenti di BI e dashboard, facilità d'uso e una comunità attiva che
contribuisce allo sviluppo e al miglioramento continuo del framework.

Ottimizzare query evitando join non necessari, filtrando i dati il prima possibile, utilizzando partizioni
e sfruttando le funzionalità di caching e persistenza di Spark SQL, sono tutte strategie efficaci 
per migliorare le prestazioni delle query su grandi volumi di dati.

"""
import os
os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("SparkSQL")
    .config("spark.sql.adaptive.enabled", True)
    .getOrCreate()
)

# 1) dati in memoria
dati=[("A",10),("B",20),("C",30),("D",40),("A",50),("B",60),("C",70),("D",80)]
df=spark.createDataFrame(dati,["categoria","valore"])
df.createOrReplaceTempView("tabella_dati")

spark.sql("SELECT * FROM tabella_dati WHERE valore > 30").show()
spark.sql("SELECT categoria, AVG(valore) AS media_valore FROM tabella_dati GROUP BY categoria").show()

# 2) lettura CSV
df_csv = spark.read.csv(r"C:\EPICODE\5 - Big_Data\dati_grandi.csv", header=True, inferSchema=True)
df_csv.createOrReplaceTempView("tabella_csv")

spark.sql("SELECT * FROM tabella_csv WHERE valore > 100").show()
spark.sql("SELECT categoria, COUNT(valore) AS conteggio FROM tabella_csv GROUP BY categoria").show()

# 3) JDBC MySQL (vedi note sotto)
# df_db = spark.read.format("jdbc")...
# df_db.createOrReplaceTempView("tabella_db")
# spark.sql("SELECT ...").show()

spark.stop()


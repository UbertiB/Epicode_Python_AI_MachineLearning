"""
DIFFERENZE TRA SPARK DATAFRAME E PANDAS DATAFRAME

Con l'aumentare delle dimensione dei dati, i DataFrame di Pandas possono diventare
inefficienti e causare problemi di memoria. Spark DataFrame, invece, è progettato
per gestire grandi volumi di dati distribuiti su cluster, offrendo scalalbilità e prestazioni
migliori. Ecco alcune differenze chiave tra i due:
1. Scalabilità: Spark DataFrame è progettato per gestire grandi volumi di dati distribuiti
   su cluster, mentre Pandas DataFrame è più adatto per dati che possono essere gestiti in
   memoria.
2. Prestazioni: Spark DataFrame utilizza l'elaborazione distribuita, che può migliorare 
   le prestazioni su grandi dataset, mentre Pandas DataFrame può diventare lento o causare
   problemi di memoria con dataset di grandi dimensioni.
3. API: Spark DataFrame offre un'API simile a SQL e supporta operazioni di trasformazione
   complesse, mentre Pandas DataFrame è più orientato a operazioni di manipolazione dei dati
   in memoria.
4. Integrazione: Spark DataFrame si integra bene con altri componenti sull'ecosistema
   Spark, come Spark SQL e Spark MLLib, mentre Pandas DataFrame è più adatto per l'analisi
   dei dati in memoria e l'integrazione con libreria Pyton come NumPy e Matplotlib.
5. Gestione dei dati mancanti: Spark DataFrame gestisce i dati mancanti in modo più
   efficiente, mentre Pandas DataFrame può diventare lento o causare problemi di memoria.
6. Supporto per i tipi di dati: Spark DataFrame supporta una vasta gamma di tipi di dati,
   inclusi tipi complessi come array e struct, mentre Pandas DataFrame è più limitato nei
   tipi di dati supportati.
7. Operazioni di join: Spark DataFrame è ottimizzato per eseguire operazioni di join su
   grandi dataset, mentre Pandas DataFrame può diventare lento o causare problemi di memoria
   con operazioni di join su grandi dataset.
8. Operazioni di aggregazione: Spark DataFrame è ottimizzato per eseguire operazioni di 
   aggregazione su grandi dataset, mentre Pandas DataFrame può diventare lento o causare
   problemi di memoria con operazioni di aggregazione su grandi dataset.
9. Supporto per il machine learning: Spark DataFrame si integra bene con Spark MLLib, 
   una libreria di machine learning distribuita, mentre Pandas DataFrame è più adatto per
   l'analisi dei dati in memoria e l'integrazione con libreria Pyton come scikit-learn.
10. Supporto per il streaming: Spark DataFrame supporta l'elaborazione dei dati in streaming,
    mentre Pandas DataFrame è più adatto per l'analisi dei dati in memoria e non supporta
    l'elaborazione dei dati in streaming.
11. Supporto per il cloud: Spark DataFrame è progettato per essere eseguito su cluster
    distribuiti, inclusi cluster in cloud come AWS EMR, Google Cloud Dataproc e Azure HDInsight,
    mentre Pandas DataFrame è più adatto per l'analisi dei dati in memoria e non è progettato
    per essere eseguito su cluster distribuiti.
12. Supporto per il parallelismo: Spark DataFrame utilizza l'elaborazione distribuita e il
    parallelismo per migliorare le prestazioni su grandi dataset, mentre Pandas DataFrame è 
    più adatto per l'analisi dei dati in memoria e non supporta il parallelismo.
13. Supporto per il caching: Spark DataFrame supporta il caching dei dati in memoria per
    migliorare le prestazioni su operazioni ripeture, mentre Pandas DataFrame è più adatto
    per l'analisi dei dati in memoria e non supporta il caching dei dati.
14. Supporto per il fault tolerance: Spark DataFrame è progettato per essere fault tolerant,
    con meccanismi di recupero automatico in caso di guasti, mentre Pandas DataFrame è più
    adatto per l'analisi dei dati in memoria e non è progettato per essere fault toleranti.
15. Supporto per il linguaggio: Spark DataFrame supporta più linguaggi di programmazione,
    tra cui Python, Scala, Jave e R, mentre Pandas DataFrane è specifico per Python e non 
    supporta altri linguaggi di programmazione.
16. Supporto per il formato dei dati: Spark DataFrame supporta una vasta gamma di formati
    di dati, tra cui CSV, JSON, Parquet, Avro e ORC, mentre Pandas DataFrame è più adatto
    per l'analisi dei dati in memoria e supporta principalmente formati dei dati come CSV e
    Excel.
17. Supporto per il tipo di dati distribuiti: Spark DataFrame è progettato per gestire dati
    distribuiti su cluster, mentre Pandas DataFrame è più adatto per l'analisi dei dati in
    memoria e non è progettato per gestire dati distribuiti su cluster.
18. Supporto per il tipo di dati strutturati: Spark DataFrame è progettato per gestire 
    dati strutturati, come tabelle relazionali, mentre Pandas DataFrame è più adatto 
    per l'analisi dei dati in memoria e non è progettato per gestire dati strutturati.
19. Supporto per il tipo di dati non strutturati: Spark DataFrame è progettato per gestire 
    dati non strutturati, come testo e immagini, mentre Pandas DataFrame è più adatto 
    per l'analisi dei dati in memoria e non è progettato per gestire dati non strutturati.
20. Supporto per il tipo di dati semi-strutturati: Spark DataFrame è progettato per gestire 
    dati semi-strutturati, come JSON e XML, mentre Pandas DataFrame è più adatto per 
    l'analisi dei dati in memoria e non è progettato per gestire dati semi-strutturati.
21. Supporto per il tipo di dati geospaziali: Spark DataFrame supporta l'elaborazione di 
    dati geospaziali, mentre Pandas DataFrame è più adatto per l'analisi dei dati in memoria 
    e non è progettato per gestire dati geospaziali.
22. Supporto per il tipo di dati temporali: Spark DataFrame supporta l'elaborazione di dati 
    temporali, mentre Pandas DataFrame è più adatto per l'analisi dei dati in memoria e non 
    è progettato per gestire dati temporali.    

"""


import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg
import os
import pandas as pd

#percorso per il worker
os.environ["PYSPARK_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"
#percorso per il driver
os.environ["PYSPARK_DRIVER_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"

if False:
    spark=SparkSession.builder.appName("Spark vs Pandas").getOrCreate()

    data=[("Alice", 34, "Roma"), ("Bob", 45, "Milano"), ("Charlie", 29, "Milano"), ("David", 40, "Torino"), ("Eve", 25, "Firenze")]
    colonne=["Nome", "Età", "Città"]
    df_spark=spark.createDataFrame(data, colonne)

    roma_df=df_spark.filter(col("Città")=="Roma")
    milano_df=df_spark.filter(col("Città")=="Milano")
    media_eta=df_spark.groupBy("Città").agg(avg("Età").alias("Media Età"))

    print("Dati di Roma:")
    roma_df.show()
    print("Dati di Milano:")
    milano_df.show()
    print("Media età:", media_eta)

    spark.stop()

if False:
    spark=SparkSession.builder.appName("Spark vs Pandas IO").getOrCreate()
    df_spark=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
    df_spark=df_spark.groupBy("categoria").sum("valore").show(5)
    spark.stop()
    df_pandas=pd.read_csv("dati_grandi.csv")
    df_pandas=df_pandas.groupby("categoria")["valore"].sum()
    print(df_pandas.head())

if True:
    spark=SparkSession.builder.appName("Conversione Pandas Spark").getOrCreate()
    df_pandas=pd.DataFrame({"Nome": ["Alice", "Bob", "Charlie", "David", "Eve"],
                            "Età": [34, 45, 29, 40, 25],
                            "Città": ["Roma", "Milano", "Milano", "Torino", "Firenze"]})
    #dal df pandas converto in df spark
    df_spark=spark.createDataFrame(df_pandas)
    df_spark.groupBy("Città").agg(avg("Età").alias("Media Età")).show()
    spark.stop()
    #dal df spark converto in df pandas
    df_pandas_back=df_spark.toPandas()
    print(df_pandas_back.head())



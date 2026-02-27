"""
ESERCIZIO 1
* Crea un dataframe di spark da un file csv e calcola il numero medio di vendite per regione
ESERCIZIO 2
* Confronta i tempi di esecuzione della stessa aggregazione tra pandas e spark su
un file di grandi dimensioni
ESERCIZIO 3
* Convertire un dataframe pandas in spark, applicare una trasformazione e riconvertirlo
in pandas verificando che i risultati coincidano
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg
import os
import pandas as pd
import time

#percorso per il worker
os.environ["PYSPARK_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"
#percorso per il driver
os.environ["PYSPARK_DRIVER_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"


"""
ESERCIZIO 1
* Crea un dataframe di spark da un file csv e calcola il numero medio di vendite per regione
"""
if True:
    spark=SparkSession.builder.appName("Spark vs Pandas IO").getOrCreate()
    df_spark=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
    df_spark=df_spark.groupBy("categoria").avg("valore").show()
    spark.stop()

"""
ESERCIZIO 2
* Confronta i tempi di esecuzione della stessa aggregazione tra pandas e spark su
un file di grandi dimensioni
"""
if False:
    t1=time.time()
    df_pandas=pd.read_csv("dati_grandi.csv")
    df_pandas=df_pandas.groupby("categoria")["valore"].mean()
    t2=time.time()
    print("Tempo esecuzione Pandas:", t2-t1, "secondi")
    t3=time.time()
    spark=SparkSession.builder.appName("Spark vs Pandas IO").getOrCreate()
    df_spark=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
    df_spark=df_spark.groupBy("categoria").avg("valore").show(5)
    spark.stop()
    t4=time.time()
    print("Tempo esecuzione PySpark:", t4-t3, "secondi")

"""
ESERCIZIO 3
* Convertire un dataframe pandas in spark, applicare una trasformazione e riconvertirlo
in pandas verificando che i risultati coincidano
"""    
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

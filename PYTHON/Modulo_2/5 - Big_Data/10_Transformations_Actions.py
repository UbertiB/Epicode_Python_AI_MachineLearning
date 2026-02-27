"""
OPERAZIONI PRINCIPALI SU SPARK DATAFRAME: TRANSFORMATIONS E ACTIONS

Apache Spark è uno dei framework più popolari per l'elaborazione distribuita dei dati. Spark DataFrame
è una delle principali API di Spark per la manipolazione dei dati strutturati. Le operazioni su Spark
Data Frame sono suddivise in due categorie principali: transformations e actions. 
Ogni operazione su un DataFrame è gestita in modo efficiente grazie al motore spark sql.
Le transformations sono operazioni che trasformano un DataFrame in un altro DataFrame, 
mentre le actions sono operazioni che restituiscono un risultato al driver o scrivono i dati 
su un sistema di archiviazione esterno.
Ogni operazione sul df non produce subito  un risultato, spark costruisce un piano logico, una sequenza
di operazioni da eseguire, questo approcio prende il nome di lazy evaluation, l'esecuzione avviene solo
quando viene chiamata un'azione, a quel punto spark ottimizza il piano di esecuzione e lo esegue in 
modo distribuito sui nodi del cluster.
Spark rimanda l'esecuzione fino a quando non è necessario per ottimizzare le prestazionio ed evitare
passaggi innutili.

1. Transformations: Le transformations sono operazioni che trasformano un DataFrame in un altro DataFrame. 
   Queste operazioni sono "lazy", il che significa che non vengono eseguite immediatamente, 
   ma vengono registrate come parte di un piano di esecuzione. 
   Esempi di transformations includono:
    - filter(): Filtra le righe in base a una condizione specifica.
    - select(): Seleziona specifiche colonne da un DataFrame.
    - groupBy(): Raggruppa i dati in base a una o più colonne.
    - agg(): Esegue operazioni di aggregazione sui dati raggruppati.
    - withColumn(): Aggiunge una nuova colonna o modifica una colonna esistente.
    - join(): Unisce due DataFrame in base a una condizione di join.
    Alcune operazioni lavorano localmente su ciascuna partizione, mentre altre richiedono una shuffling
    dei dati tra le partizioni, come ad esempio groupBy() e join(), queste operazioni sono più costose
    in termini di prestazioni rispetto alle operazioni che lavorano localmente, come filter() e select().

2. Actions: Le actions sono operazioni che restituiscono un risultato al driver o scrivono i dati su un sistema di archiviazione esterno. Queste operazioni forzano l'esecuzione del piano di esecuzione registrato dalle transformations. Esempi di actions includono:
    - show(): Mostra le prime righe di un DataFrame.
    - collect(): Restituisce tutte le righe di un DataFrame al driver come una lista.
    - count(): Restituisce il numero di righe in un DataFrame.
    - take(): Restituisce un numero specifico di righe da un DataFrame.
    - write(): Scrive i dati di un DataFrame su un sistema di archiviazione esterno, come HDFS o S3.
    - saveAsTable(): Salva un DataFrame come una tabella in un catalogo di metadati, come Hive.
    - foreach(): Esegue una funzione su ogni riga di un DataFrame, senza restituire un risultato al driver.
    - reduce(): Esegue una funzione di riduzione su un DataFrame, restituendo un singolo valore al driver.
    - countByKey(): Conta il numero di occorrenze di ogni chiave in un DataFrame raggruppato per chiave.
    - first(): Restituisce la prima riga di un DataFrame.
    - head(): Restituisce la prima riga di un DataFrame, simile a first(), ma con un comportamento leggermente diverso in caso di DataFrame vuoti.
    - max(): Restituisce il valore massimo di una colonna specifica in un DataFrame.
    - min(): Restituisce il valore minimo di una colonna specifica in un DataFrame.
    - mean(): Restituisce la media di una colonna specifica in un DataFrame.
    - sum(): Restituisce la somma di una colonna specifica in un DataFrame.
    - avg(): Restituisce la media di una colonna specifica in un DataFrame, simile a mean(), ma con un comportamento leggermente diverso in caso di valori nulli.
    - stddev(): Restituisce la deviazione standard di una colonna specifica in un DataFrame.
    - variance(): Restituisce la varianza di una colonna specifica in un DataFrame.
    - describe(): Restituisce statistiche descrittive per una o più colonne in un DataFrame.
    - summary(): Restituisce statistiche descrittive per una o più colonne in un DataFrame, simile a describe(), ma con un comportamento leggermente diverso in caso di valori nulli.
    - distinct(): Restituisce un DataFrame con righe distinte, eliminando i duplicati.
    - dropDuplicates(): Restituisce un DataFrame con righe distinte, eliminando i duplicati, simile a distinct(), ma con un comportamento leggermente diverso in caso di valori nulli.

Fino al momento dell'action spark non esegue nulla, riducendo la quantità di dati scambiati
tra i nodi del cluster e migliorando le prestazioni complessive dell'elaborazione dei dati.

"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg, count
import os
import pandas as pd

#percorso per il worker
os.environ["PYSPARK_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"
#percorso per il driver
os.environ["PYSPARK_DRIVER_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"

if False:
    spark=SparkSession.builder.appName("Transformations Actions").getOrCreate()

    dati=[("A",10),("B",20),("C",30),("D",40),("A",50),("B",60),("C",70),("D",80)]
    df=spark.createDataFrame(dati,["categoria","valore"])
    #applico una transformation per filtrare i dati
    df_filtrato=df.filter(col("valore")>30)
    #applico un'azione per contare il numero di righe nel dataframe filtrato
    conteggio=df_filtrato.count()
    print("Numero di righe con valore maggiore di 30:", conteggio)
    #applico una transformation per raggruppare i dati per categoria e calcolare la media dei valori
    df_aggregato=df.groupBy("categoria").agg(avg("valore").alias("media_valore"))
    #applico un'azione per mostrare i risultati dell'aggregazione
    df_aggregato.show()
    spark.stop()


if False:
    spark=SparkSession.builder.appName("Transformations Actions").getOrCreate()
    df=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
    #applico una transformation per filtrare i dati
    df_2=df.filter(col("valore")>100)
    df_3=df_2.select("categoria", "valore")
    df_4=df_3.groupBy("categoria").agg(count("valore").alias("conteggio"))
    #applico un'azione per mostrare i risultati dell'aggregazione
    df_4.show()
    spark.stop()

if False:
    spark=SparkSession.builder.appName("NarrowWide").getOrCreate()
    dati=[("A",10),("B",20),("C",30),("D",40),("A",50),("B",60),("C",70),("D",80)]
    df=spark.createDataFrame(dati,["categoria","valore"])
    df_mappato=df.withColumn("valore_doppio", col("valore")*2)
    df_aggregato=df_mappato.groupBy("categoria").agg(avg("valore_doppio").alias("media_valore_doppio"))
    df_aggregato.show()
    spark.stop()

    



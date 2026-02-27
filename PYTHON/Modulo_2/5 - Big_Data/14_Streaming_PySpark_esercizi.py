"""
ESERCIZIO 1
* Crea uno straming DataFrame leggendo dati da una cartella in tempo reale
applica un filtro su un campo numerico, stampalo su console
ESERCIZIO 2
* Implementa un'aggregazione su finestre temporali di 30 secondi e visualizza il 
conteggio dei record per categoria
ESERCIZIO 3
* Simula un join tra unno straem di vendite e un datasset batch di prodotti, stampando
il flusso arricchito
ESERCIZIO 4
* Testa il watermarketing definendo un ritardo mnassivo di 2 minuti e oserva come 
spark gestisce gli eventi tardivi
"""


from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg,max,min, count,window
import os
from pathlib import Path
from pyspark.sql import functions as F

HADOOP_HOME = r"C:\hadoop"
# set env
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")
# pyspark python
os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"


"""
ESERCIZIO 1
* Crea uno straming DataFrame leggendo dati da una cartella in tempo reale
applica un filtro su un campo numerico, stampalo su console
"""

if False:
    spark=SparkSession.builder.appName("ESERCIZIO 1").getOrCreate()

    #lettura cartella
    #(dataframe dinamico che si aggiorna ogni volta che un csv è inserito nella cartella
    stream_df=(spark.readStream.format("csv")
        .option("header","true") #prima riga con nomi delle colonne
        .option("maxFilesPerTrigger", 1)  # legge 1 file per micro-batch 
        .schema("id INT,categoria STRING,valore DOUBLE,data TIMESTAMP") #tipi alle colonne assegnati manualmente
        .load(r"C:\EPICODE\5 - Big_Data\dati") #percorso
    )
    #filtro i valori 
    filter_df=stream_df.filter(col("valore")>350)

    #output in console con la query
    query=(filter_df.writeStream.outputMode("append") #scrivo solo i nuovi record che arrivano nello streaming
        .format("console") #stampo i dati in console
        .option("truncate",False) #stampo le colonne intere senza troncamenti
        .start() #avvio lo straming
    )

    query.awaitTermination() #blocca il programma fino a quando lo stream è attivo
    spark.stop()


"""
ESERCIZIO 2
* Implementa un'aggregazione su finestre temporali di 30 secondi e visualizza il 
conteggio dei record per categoria
"""    

if False:
    spark=(SparkSession.builder
           .appName("ESERCIZIO 2")
           .config("spark.ui.showConsoleProgress", "false")
           .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR") #mostra solo errori, taglia le info innutili

    #lettura cartella
    #(dataframe dinamico che si aggiorna ogni volta che un csv è inserito nella cartella
    stream_df=(spark.readStream.format("csv")
        .option("header","true") #prima riga con nomi delle colonne
        .option("maxFilesPerTrigger", 1)  # legge 1 file per micro-batch 
        .schema("id INT,categoria STRING,valore DOUBLE,data TIMESTAMP") #tipi alle colonne assegnati manualmente
        .load(r"C:\EPICODE\5 - Big_Data\dati") #percorso
    )
    #group by, finestra temporale di 30 secondi
    window_agg=(stream_df
                .withWatermark("data","30 seconds") #ritardo accettato dei dati
                .groupBy(window(col("data"),"30 seconds"),col("categoria"))
                .agg(
                    avg("valore").alias("media"),
                    count("*").alias("n_righe")
                )
    )

    query=(window_agg.writeStream
           .outputMode("update") #scrivo solo i nuovi record che arrivano nello streaming
            .format("console") #stampo i dati in console
            .option("truncate",False) #stampo le colonne intere senza troncamenti
            #salvo lo stato della query (deve ricordarsi cosa ha già letto e cosa no)
            .option("checkpointLocation",r"C:\EPICODE\5 - Big_Data\_chk_es3") 
            .start() #avvio lo straming
    )

    query.awaitTermination() #blocca il programma fino a quando lo stream è attivo
    spark.stop()


"""
ESERCIZIO 3
* Simula un join tra unno straem di vendite e un dataset batch di prodotti, stampando
il flusso arricchito
"""
if True:
    spark=(SparkSession.builder
           .appName("ESERCIZIO 3")
           .config("spark.ui.showConsoleProgress", "false")
           .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR") #mostra solo errori, taglia le info innutili
    #lettura cartella in streaming
    df_vendite=(spark.readStream.format("csv")
        .option("header","true") #prima riga con nomi delle colonne
        .option("maxFilesPerTrigger", 1)  # legge 1 file per micro-batch 
        .schema("id INT,categoria STRING,valore DOUBLE,data TIMESTAMP") #tipi alle colonne assegnati manualmente
        .load(r"C:\EPICODE\5 - Big_Data\dati") #percorso
    )
    #leggo file in batch
    df_categorie = (spark.read.format("csv")
        .option("header", "true")  #se faccio leggere lo schema dal file excel
        #meglio scriverlo per essere più sicuri dei tipi
        #.option("inferSchema", "true") #evito schema manuale
        .schema("id INT,categoria STRING,valore DOUBLE") #tipi alle colonne assegnati manualmente
        .load(r"C:\EPICODE\5 - Big_Data\dati_CATEGORIE.csv")
        #rinomino subito le colonne che hanno lo stesso nome dell'altro df (poi darò join())
        .withColumnRenamed("id", "id_categoria")
        .withColumnRenamed("valore", "costo_categoria")        
    )

    #rinomino le colonne con lo stesso nome
    #df_categorie2=df_categorie.withColumnRenamed("valore","costo_categoria")
    #join
    df_join = (df_vendite
        .join(df_categorie,
            on="categoria",
            how="left")
        .select(
            "id",
            "categoria",
            F.col("valore").alias("valore_vendita"),
            "costo_categoria",
            "data"
        )
    )
    query=(df_join.writeStream
           .outputMode("append")
           .format("console")
           .option("truncate",False)
           .option("checkpointLocation", r"C:\EPICODE\5 - Big_Data\_chk_es5")
           .start()
           )
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("Interruzione manuale...")
        query.stop()
        spark.stop()

"""
ESERCIZIO 4
* Testa il watermarketing definendo un ritardo mnassivo di 2 minuti e oserva come 
spark gestisce gli eventi tardivi
"""    




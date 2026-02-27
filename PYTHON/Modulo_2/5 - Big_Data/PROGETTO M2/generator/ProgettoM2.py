"""
ESAME PRATICO: DATA ENGINEERING PIPELINE
Scenario: Sei un Data Engineer presso "MegaShop". L'azienda ha storici di vendita enormi e il
vecchio sistema basato su file Excel/CSV non regge più. Devi migrare l'analisi su tecnologie
Big Data (Spark/Dask) e creare un'architettura dati moderna.
Requisiti: Python, Pandas, Dask, PySpark, Seaborn/Matplotlib.

STEP 0: Setup Iniziale
1. Scarica il file generator.py fornito dal docente ed eseguilo.
2. Ǫuesto script creerà una cartella ./dataset contenente:
    o transazioni_json/: File di log grezzi delle vendite.
    o transazioni_parquet/: Archivio storico vendite ottimizzato.
    o anagrafiche/: Tabelle Prodotti e Clienti.
È possibile configurare al suo interno le dimensioni del dataset in base alle
disponibilità HW della macchina di sviluppo.

ESERCIZIO 1: Ingestion e Limiti di Memoria (Pandas vs Dask)
Obiettivo: Leggere file multipli tendendo in conto l'ottimizzazione della RAM
1.  Il blocco di Pandas: Prova a leggere tutti i file contenuti nella cartella
    dataset/transazioni_json/ usando Pandas. Noterai che è lento o complesso unire tanti
    file.
    o Task: Scrivi uno script che legge i file JSON uno alla volta (ciclo for), calcola la
            somma della colonna amount per ogni file e stampa il totale generale alla fine.
2.  La soluzione Dask: Utilizza la libreria dask.dataframe.
    o Task: Leggi tutti i file JSON in un colpo solo usando il carattere jolly (*.json).
    o Task: Raggruppa le vendite per payment_type e calcola la media degli importi.
    Esegui il calcolo con .compute() e stampa il risultato.

ESERCIZIO 2: Pipeline ETL con PySpark
Obiettivo: Unire fonti dati diverse (Data Warehousing).
1. Inizializza una SparkSession.
2. Extract: Carica le tre tabelle principali dalla cartella parquet/:
    • Transazioni (transactions_batch_*.parquet)
    • Prodotti (products.parquet)
    • Regioni (regions.parquet)
3. Transform:
    • Unisci (JOIN) le Transazioni con i Prodotti (su product_id) per avere la categoria.
    • Unisci(JOIN) con le Regioni(su region_id) per avere il nome della regione
    (region_name).
    • Crea un DataFrame finale pulito con: transaction_id, region_name, category, amount,
    year.
4. Load: Salva il risultato in data_local/processed_sales in formato Parquet, partizionato per
    year.

ESERCIZIO 3: Data Visualization (Reporting)
Obiettivo: Creare insight visivi per il management.
1. Partendo dal DataFrame Spark pulito (creato nell'Esercizio 2):
    o Calcola il Fatturato Totale per Categoria (category).
    o Esegui l'azione .toPandas() per portare questo risultato aggregato (che sarà
    piccolo, poche righe) in memoria locale.
2. Utilizza Seaborn o Matplotlib per generare un Grafico a Barre (Bar Chart) che mostri il
    fatturato per ogni categoria.
3. Salva il grafico come immagine fatturato_per_categoria.png o mostralo a video.

ESERCIZIO 4 (Bonus): Real-Time Streaming
Obiettivo: Monitoraggio live.
1. Crea uno script che ascolta la cartella data_local/json/.
2. Ogni volta che viene aggiunto un file, lo script deve calcolare in tempo reale il numero
    totale di transazioni per ogni region.
3. Stampa l'aggiornamento a video (Console Sink).


"""

import pandas as pd
import numpy as np
import time
from glob import glob

"""
ESERCIZIO 1: Ingestion e Limiti di Memoria (Pandas vs Dask)
Obiettivo: Leggere file multipli tendendo in conto l'ottimizzazione della RAM
"""
print("---------------------------")
print("-------ESERCIZIO 1---------")
print("---------------------------")
#
#Utility
#
def calcola_tempo(t0:float,t1:float, testo:str) ->str:
    t = t1 - t0  #differenza in secondi
    minuti = int(t // 60) #calcolo minuti
    secondi = int(t % 60) #calcolo secondi
    millisecondi = int((t - int(t)) * 1000) #calcolo millisecondi
    return print(f"Tempo impiegao lettura {testo}: {minuti:02d}:{secondi:02d}:{millisecondi:03d}")

#
#configurazione
#
cartella = r"data_local/json/transactions_part_*.jsonl"
files = sorted(glob(cartella))

if not files:
    raise FileNotFoundError(f"Nessun file trovato nella cartella: {cartella}")



"""
1.  Il blocco di Pandas: Prova a leggere tutti i file contenuti nella cartella
    dataset/transazioni_json/ usando Pandas. Noterai che è lento o complesso unire tanti
    file.
    o Task: Scrivi uno script che legge i file JSON uno alla volta (ciclo for), calcola la
            somma della colonna amount per ogni file e stampa il totale generale alla fine.
"""

t0=time.time()

totale_generale=0.0
#lettura ogni singolo file
for f in files:
    try:
        df_pandas=pd.read_json(f,lines=True)
        if df_pandas.empty:
            print(f"File {f} vuoto.")
            continue
        df_pandas["amount"]=pd.to_numeric(df_pandas["amount"],errors="coerce")
        totale=df_pandas["amount"].sum() #totale per file
        totale_generale+=totale  #totale generale
        #print(f"File: {f}, TOTALE: {totale}")
    except ValueError as e: 
        print(f"{f} ERRORE")
t1=time.time()
print(f"Totale amount: {totale_generale}")

t = t1 - t0  #differenza in secondi
calcola_tempo(t0,t1,"Pandas")
"""
2.  La soluzione Dask: Utilizza la libreria dask.dataframe.
    o Task: Leggi tutti i file JSON in un colpo solo usando il carattere jolly (*.json).
    o Task: Raggruppa le vendite per payment_type e calcola la media degli importi.
    Esegui il calcolo con .compute() e stampa il risultato.
"""
import dask.dataframe as dd
import dask.array as da

t0=time.time()

df_dask = dd.read_json(cartella, lines=True)

df_dask["amount"]=dd.to_numeric(df_dask["amount"],errors="coerce")
#cambio il nome della colonna payment_type con region_id perchè non trovo il campo nei files transactions_part_*.jsonl
if "payment_type" not in df_dask.columns:
    df_dask_groupby = df_dask.groupby("region_id")["amount"].mean().compute()
else:
    df_dask_groupby = df_dask.groupby("payment_type")["amount"].mean().compute()

print(f"Media amount: \n{df_dask_groupby}")

t1=time.time()
calcola_tempo(t0,t1,"Dask")

"""
ESERCIZIO 2: Pipeline ETL con PySpark
Obiettivo: Unire fonti dati diverse (Data Warehousing).
"""
import os
from pathlib import Path

#essendo che Spark andava in errore leggendo i files delle transazioni, perchè presente 
#la colonna timestamp in formato 'nanosecondi' (Illegal Parquet type: INT64 (TIMESTAMP(NANOS,false)))
#ho convertito i files (con aiuto di ai)
#cambiare "if False" in "if True" se necessario
if False:

    src_dir = r"data_local/parquet"
    dst_dir = r"data_local/parquet_spark_compat"
    os.makedirs(dst_dir, exist_ok=True)

    files = sorted(glob(os.path.join(src_dir, "transactions_batch_*.parquet")))
    print("File transazioni da convertire:", len(files))
    if not files:
        raise FileNotFoundError("Non trovo transactions_batch_*.parquet in data_local/parquet")

    for src in files:
        df = pd.read_parquet(src, engine="pyarrow")

        dt_cols = list(df.select_dtypes(include=["datetime64[ns]"]).columns)
        if dt_cols:
            print("Datetime ns in", os.path.basename(src), ":", dt_cols)
            for col in dt_cols:
                df[col] = df[col].astype("datetime64[us]")

        dst = os.path.join(dst_dir, os.path.basename(src))
        df.to_parquet(dst, index=False, engine="pyarrow")
        print("Convertito:", dst)        

HADOOP_HOME = r"C:\hadoop"

# set env
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")

# pyspark python
os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

from pyspark.sql import SparkSession

print("---------------------------")
print("-------ESERCIZIO 2---------")
print("---------------------------")

"""
1. Inizializza una SparkSession.
"""
spark = (
    SparkSession.builder
    .appName("Spark")
    .master("local[*]")
    .config("spark.ui.showConsoleProgress", "false") #tolgo messaggi superflui
    .config("spark.sql.adaptive.enabled", "true")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("ERROR")
"""
2. Extract: Carica le tre tabelle principali dalla cartella parquet/:
    • Transazioni (transactions_batch_*.parquet)
    • Prodotti (products.parquet)
    • Regioni (regions.parquet)
"""
from glob import glob
import os

cartella_parquet = r"data_local/parquet_spark_compat"  
cartella= r"data_local/parquet"  
pattern = os.path.join(cartella_parquet, "transactions_batch_*.parquet")

paths_trans = sorted(glob(pattern))
if not paths_trans:
    raise FileNotFoundError(f"Nessun file trovato con pattern: {pattern}")

df_transazioni = spark.read.parquet(*paths_trans)
df_prodotti = spark.read.parquet(os.path.join(cartella, "products.parquet"))
df_regioni  = spark.read.parquet(os.path.join(cartella, "regions.parquet"))
#df_transazioni.show(10)

#verifica nomi colonne
#if False:
    #print(f"Transazioni: {df_transazioni.columns}")
    #print(f"Prodotti: {df_prodotti.columns}")
    #print(f"Regioni: {df_regioni.columns}")

"""
3. Transform:
    • Unisci (JOIN) le Transazioni con i Prodotti (su product_id) per avere la categoria.
    • Unisci(JOIN) con le Regioni(su region_id) per avere il nome della regione
    (region_name).
    • Crea un DataFrame finale pulito con: transaction_id, region_name, category, amount,
    year.
"""
from pyspark.sql.functions import col, year

#join con prodotti e regioni
df_totale = (
    df_transazioni
    .join(df_prodotti.select("product_id", "category"), on="product_id", how="left")
    .join(df_regioni.select("region_id", "region_name"), on="region_id", how="left")
)


#verifica nomi colonne
#if False:
#    print(f"Transazioni completo: {df_totale.columns}")

#DataFrame finale pulito con le colonne richieste
df_finale = df_totale.select(
    "transaction_id",
    "region_name",
    "category",
    "amount",
    "year"
)

df_finale.show(10, truncate=False)
df_finale.printSchema()
"""
4. Load: Salva il risultato in data_local/processed_sales in formato Parquet, partizionato per
    year.
"""
cartella_output = r"data_local/processed_sales"
#pulizia colonna anno
df_output=(df_finale
           .withColumn("year",col("year").cast("int"))
           .filter(col("year").isNotNull())
)
#scrittura file.parquet per anno
(df_output
 .write.mode("overwrite")
 .partitionBy("year")
 .parquet(cartella_output)
)
print("Scritto in:", os.path.abspath(cartella_output))

"""
ESERCIZIO 3: Data Visualization (Reporting)
Obiettivo: Creare insight visivi per il management.
1. Partendo dal DataFrame Spark pulito (creato nell'Esercizio 2):
    o Calcola il Fatturato Totale per Categoria (category).
    o Esegui l'azione .toPandas() per portare questo risultato aggregato (che sarà
    piccolo, poche righe) in memoria locale.
2. Utilizza Seaborn o Matplotlib per generare un Grafico a Barre (Bar Chart) che mostri il
    fatturato per ogni categoria.
3. Salva il grafico come immagine fatturato_per_categoria.png o mostralo a video.
"""
print("---------------------------")
print("-------ESERCIZIO 3---------")
print("---------------------------")

"""
1. Partendo dal DataFrame Spark pulito (creato nell'Esercizio 2):
    o Calcola il Fatturato Totale per Categoria (category).
    o Esegui l'azione .toPandas() per portare questo risultato aggregato (che sarà
    piccolo, poche righe) in memoria locale.
"""
from pyspark.sql import functions as F
df_fatturato_categoria = (
    df_finale
    .groupBy("category")
    .agg(F.sum("amount").alias("totale"))
    .orderBy(F.desc("totale"))
)
#df_fatturato_categoria.show(truncate=False)

pdf=df_fatturato_categoria.toPandas()
print(pdf)

"""
2. Utilizza Seaborn o Matplotlib per generare un Grafico a Barre (Bar Chart) che mostri il
    fatturato per ogni categoria.
"""
import matplotlib.pyplot as plt
import seaborn as sns

#ordine decrescente per fatturato
pdf_plot = pdf.sort_values("totale", ascending=False)
#costruisco il grafico
plt.figure(figsize=(10, 5))
sns.barplot(data=pdf_plot, x="category",y="totale",hue="category")
plt.xlabel("Categoria")
plt.ylabel("Totale")
plt.title("Totale transazioni per categoria")
plt.xticks(rotation=45, ha="right") #ruoto
plt.tight_layout()
"""
3. Salva il grafico come immagine fatturato_per_categoria.png o mostralo a video.
"""
plt.savefig("fatturato_per_categoria.png")  #salvataggio
plt.show() #visualizzo


"""
ESERCIZIO 4 (Bonus): Real-Time Streaming
Obiettivo: Monitoraggio live.
1. Crea uno script che ascolta la cartella data_local/json/.
2. Ogni volta che viene aggiunto un file, lo script deve calcolare in tempo reale il numero
    totale di transazioni per ogni region.
3. Stampa l'aggiornamento a video (Console Sink).
"""

print("---------------------------")
print("-------ESERCIZIO 4---------")
print("---------------------------")

from pyspark.sql.types import (StructType, StructField,StringType, LongType, DoubleType, IntegerType, TimestampType)

cartella =  r"data_local/json"   #cartella da ascoltare

#definisco lo schema
schema = StructType([
    StructField("transaction_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("region_id", LongType(), True),  
    StructField("quantity", LongType(), True),
    StructField("amount", DoubleType(), True),
    StructField("ts", TimestampType(), True),
    StructField("year", IntegerType(), True),
    StructField("month", IntegerType(), True),
])
df_streaming=(
    spark.readStream
    .format("json")
    .option("header","true") #prima riga con nomi delle colonne
    .option("multiLine", "false")
    .schema(schema)
    .load(cartella) #percorso
)
#aggregazione
agg_df=(
    df_streaming
    .groupBy("region_id")
    .agg(F.count("*").alias("tot_transazioni"))
    .orderBy(F.col("region_id"))
    )
#output in console con la query
query=(
    agg_df.writeStream
    .outputMode("complete") #complete=mostro tutto append= scrivo solo i nuovi record che arrivano nello streaming
    .format("console") #stampo i dati in console
    .option("truncate",False) #stampo le colonne intere senza troncamenti
    .trigger(processingTime="5 seconds")  #ogni 5 secondi controlla nuovi file
    .start() #avvio lo straming
)

query.awaitTermination() #blocca il programma fino a quando lo stream è attivo

spark.stop()




"""
DATA LAKES e DELTA LAKES: GESTIONE DATI TRANSAZIONALE
Con l'aumentare della quantità dei dati generati dalla aziende, le gestione dei dati diventa fondamentale
I data lake sono archivi centralizzati progettati per conservare grandi volumi di dati, sia strutturati
che semi strutturati e non strutturati, senza la necessità di uno schema rigido. 
Permettendo di avere dati che arrivano da diverse fonti, db relazionali, json, avro, log di applicazioni,
o dati di senzori iot, parquet, ecc.
Spark e datalake offrono strumenti potenti per leggere, scrivere e consesrvare questi dati in modo 
distribuito

DATA LAKE
Un DataLak è una zona di storage dove metti dati grezzi, senza schema rigido, 
in grande quantità.
Tipicamente: file CSV, JSON, Parquet, Log, dump ERP
Caratteristiche: storage economico (filesystem, S3, ADLS), schema on-read (decidi lo schema quando 
leggi), dati spesso append-only, poco controllo di qualità.
La cartella dove salvo i file csv, jon e parquet degli esempi degli esercizi, è un micro data lake
on filesystem
I problemi dei data lake sono:
- file duplicati
- schema che cambia
- nessuna transazione
- niente controllo di concorrenza
- nessuna gestione elegante di update/delete
Non accettano scritture concorrenti, non testa scritture parziali, compromettendo la qualità dei dati

DELTA LAKES
Delta lakes è un layer sopra il data lake che aggiunge:
- ACID transactions (come un database): 
    A=Atomicity, Atomicità (tutto o niente) Una transazione o va tutta a buon fine oppure non va tutta, nessuno stato intermedio sporco
    C=Consistency, Consistenza (rispetto schema) Il databse deve restare coerente rispetto alle regole, ci sono vincoli di integrità
    I=Isolation, Isolamento (no interferenze parallele) Due utenti che lavorano contemporaneamente non devono corrompersi i dati, il DB gestisce
    conflitti, lock, e versioni
    D=Durability, Durabilità (persistente anche dopo errore) Il dato una volta scritto è scritto
- Schema enforcement: il sistema ti obbliga a rispettare lo schema
- Schema evolution: lo schema può cambiare nel tempo in modo controllato, senza buttare via tutto
  e senza corrompere i dati. Oggi hai una tabella, domani aggiunti una colonna nuova e il sistema
  ti permette di scriverla, mantenendo compatibilità con i dati vecchi.
- Time travel: è tenuto un log delle versioni dei vari oggetti (tipi file log di SQL) si chiama transaction log. Ogni 
  scrittura crea una nuova 'versione' della tabella. Puoi leggere una tabella com'era a una versione
  passata o a un timestamp passato, senza sovrascrivere nulla
- Versioning: un oggetto (tabella, file, modello, codice, ecc) non esiste in una sola copia 'attuale'
  ma in una sequenza di versioni numerate o datate. Ogni modifica crea una nuova versione, e le vecchie
  restano recuperabili (finchè non le elimini con policy)
- Merge (upsert): aggiorna i record ed inserisce quelli nuovi in un'unica operazione. Se la chiave 
  primaria esiste già, aggiorno i campi (update) se non esiste, aggiunto una nuova riga (insert), queste
  due operazioni fatte in una sola istruzione
- Gestione robusta dello streaming
Il delta lakes è visto come un vero e prorpio database distribuito.
Lo stesso codice spark può leggere dati in arrivo in tempo reale o dati storici già salvati
Questo semplifica il codice evitando la duplicazione di codice.
Operazione critiche come aggiornamenti, cancellazione e merge senza rischiare incosistenze.
L'architettura di basa su un insieme di file Parquet combinati con un log transazionale, ogni modifica
nei dati genera un nuovo comit nel log, mantenendo la cronologia completa.
Spark utilizza questo log per garantire la consistenza dei dati e permetter il time travel, cioè
la possibilità di leggere i dati ad uno stato precedente. 
spark.read.format("delta").option("versionAsOf",5).load("/data/events").
Permette rollback, audit, replay di versioni passate.
Necessario per audit, debugging, o ripristino di dati cancellati, senza dover ricorrere a backup esterni.
Lo stesso codice Spark può leggere dati in arrivo in tempo relae, o dati storici già presenti, trattandoli
come un unico dataframe, semplificando codice.
I dati che non rispettano lo schema definito vengono automaticamente respinto, supporta lo schema evolution
permettendo modifica di schema, i dastaset possono evolvere nel tempo rimanengo coerenti e integrabili

"""
import os
from pathlib import Path

import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable
from pyspark.sql.functions import expr


# --- ENV (Windows) ---
HADOOP_HOME = r"C:\hadoop"
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")

os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

# Path Delta (cartella che conterrà parquet + _delta_log)
delta_path = r"C:\EPICODE\5 - Big_Data\dati\delta\prodotti"

# Temp più “stabile” su Windows (riduce rogne di delete in %TEMP%)
spark_tmp = r"C:\spark_tmp"
os.makedirs(spark_tmp, exist_ok=True)


def build_spark():
    builder = (
        SparkSession.builder
        .appName("Esempio Delta Lake - completo")
        .master("local[*]")
        .config("spark.local.dir", spark_tmp)
        # Delta extensions/catalog
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        # meno rumore
        .config("spark.ui.showConsoleProgress", "false")
    )
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    return spark


if __name__ == "__main__":
    spark = None
    try:
        spark = build_spark()

        # --- 1) CREA DATI ---
        df_pandas = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "categoria": ["A", "B", "C", "A", "B"],
            "quantita": [10, 20, 15, 5, 25]
        })
        df = spark.createDataFrame(df_pandas)

        # --- 2) SCRIVI DELTA (versione 0) ---
        # overwrite solo QUI va bene: stai “inizializzando” la tabella
        df.write.format("delta").mode("overwrite").save(delta_path)

        print("\n=== VERSIONE CORRENTE (dopo prima scrittura) ===")
        spark.read.format("delta").load(delta_path).orderBy("id").show()

        # --- 3) UPDATE VERO (NO overwrite) ---
        # aumenta quantita di 5 dove id=3
        dt = DeltaTable.forPath(spark, delta_path)
        dt.update(
            condition=expr("id = 3"),
            set={"quantita": expr("quantita + 5")}
        )

        print("\n=== VERSIONE CORRENTE (dopo update id=3) ===")
        spark.read.format("delta").load(delta_path).orderBy("id").show()

        # --- 4) TIME TRAVEL ---
        print("\n=== TIME TRAVEL: versionAsOf = 0 (prima dell'update) ===")
        spark.read.format("delta").option("versionAsOf", 0).load(delta_path).orderBy("id").show()

        print("\n=== TIME TRAVEL: versionAsOf = 1 (dopo l'update) ===")
        spark.read.format("delta").option("versionAsOf", 1).load(delta_path).orderBy("id").show()

        # --- 5) ESEMPIO AGGREGAZIONE ---
        print("\n=== SOMMA QUANTITA PER CATEGORIA (versione corrente) ===")
        (spark.read.format("delta").load(delta_path)
             .groupBy("categoria")
             .sum("quantita")
             .orderBy("categoria")
             .show()
        )

    except KeyboardInterrupt:
        print("\nInterruzione manuale (CTRL+C).")
    finally:
        if spark is not None:
            try:
                spark.stop()
            except Exception:
                pass

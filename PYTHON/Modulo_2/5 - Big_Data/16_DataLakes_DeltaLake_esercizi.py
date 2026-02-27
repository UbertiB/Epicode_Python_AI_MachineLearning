"""
ESERCIZIO 1
* Crea un dataframe Delta Lake con dati di vendita e calcola la somma per categoria
ESERCIZIO 2
* Modifica alcuni record e leggi lo stato storico dei dati  usanto time travel
ESERCIZIO 3
* Implementa una pipeline steaming che aggiunge nuovi ordini di Delta Lake
e verifica la consistenza dei dati in presenza di più scritture concorrenti

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
delta_path = r"C:\EPICODE\5 - Big_Data\dati\delta\prodotti2"

# Temp più “stabile” su Windows (riduce rogne di delete in %TEMP%)
spark_tmp = r"C:\spark_tmp"
os.makedirs(spark_tmp, exist_ok=True)


def build_spark():
    builder = (
        SparkSession.builder
        .appName("Esempio Delta Lake - completo")
        .master("local[*]") # master definisce il claster manager, local[*]=esegue tutto in locale *=usa tutti i core cpu disponibili
        .config("spark.local.dir", spark_tmp)
        # Delta extensions/catalog
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        # meno rumore
        .config("spark.ui.showConsoleProgress", "false")
    )
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    #riduco il rumore
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def latest_version(dt: DeltaTable) -> int:
    # history(1) = ultimo commit, ordine decrescente (ultimo prima)
    return dt.history(1).select("version").collect()[0][0]


if __name__ == "__main__":
    spark = None
    try:
        spark = build_spark()
        """
        ESERCIZIO 1
        * Crea un dataframe Delta Lake con dati di vendita e calcola la somma per categoria
        """
        # --- 1) CREA DATI ---
        df_pandas = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "categoria": ["A", "B", "C", "A", "B"],
            "vendite": [10, 20, 15, 5, 25]
        })
        df = spark.createDataFrame(df_pandas)

        # SCRIVI DELTA (versione 0) ---
        # overwrite solo QUI va bene: stai “inizializzando” la tabella
        df.write.format("delta").mode("overwrite").save(delta_path) 

        dt = DeltaTable.forPath(spark, delta_path)

        v_before = latest_version(dt)
        print(f"\n=== TIME TRAVEL versionAsOf = {v_before} ===")
        (spark.read.format("delta")
                .option("versionAsOf", v_before)
                .load(delta_path)
                .orderBy("id")
                .show()
        )

        # AGGREGAZIONE ---
        print("\n=== SOMMA VENDITE PER CATEGORIA (versione corrente) ===")
        (spark.read.format("delta").load(delta_path)
             .groupBy("categoria")
             .sum("vendite")
             .orderBy("categoria")
             .show()
        )    

        """
        ESERCIZIO 2
        * Modifica alcuni record e leggi lo stato storico dei dati  usanto time travel
        """

        #primo update
        dt.update(
            condition=expr("id = 1"),
            set={"vendite": expr("5")}
        )
        v_before = latest_version(dt)
        print(f"\n=== TIME TRAVEL versionAsOf = {v_before} ===")
        (spark.read.format("delta")
                .option("versionAsOf", v_before)
                .load(delta_path)
                .orderBy("id")
                .show()
        )

        #secondo update
        dt.update(
            condition=expr("id = 2"),
            set={"vendite": expr("vendite + 5")}
        )  
        v_before = latest_version(dt)
        print(f"\n=== TIME TRAVEL versionAsOf = {v_before} ===")
        (spark.read.format("delta")
                .option("versionAsOf", v_before)
                .load(delta_path)
                .orderBy("id")
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

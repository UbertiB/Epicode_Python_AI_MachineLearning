"""
ESERCIZIO 1
* Caricare un dataset csv in spark sql, creare una tabella temporanea
e scrivere query per calcolare aggregazioni per categoria e regione
ESERCIZIO 2
* Integrare dati da un database PostgreSQL, e da file Parquet locali,
generando un report unificato con spark sql
ESERCIZIO 3
* Testare performance di query complesse usando formati diversi (csv vs parquet)
e confrontare i tempi di esecuzione su cluster locale
"""

import os
from pathlib import Path

HADOOP_HOME = r"C:\hadoop"

print("CWD:", os.getcwd())
print("HADOOP_HOME pre:", os.environ.get("HADOOP_HOME"))
print("hadoop.home.dir pre:", os.environ.get("hadoop.home.dir"))

# set env
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")

# hard checks
print("Check winutils:", Path(HADOOP_HOME, "bin", "winutils.exe"))
print("Exists:", Path(HADOOP_HOME, "bin", "winutils.exe").exists())
print("Check hadoop.dll:", Path(HADOOP_HOME, "bin", "hadoop.dll"))
print("Exists:", Path(HADOOP_HOME, "bin", "hadoop.dll").exists())


# pyspark python
os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

from pyspark.sql import SparkSession
import time
import os

#percorso per il worker
os.environ["PYSPARK_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"
#percorso per il driver
os.environ["PYSPARK_DRIVER_PYTHON"] = r"c:\users\uberti\.conda\envs\spark311\python.exe"


spark = (
    SparkSession.builder
    .appName("SparkSQL")
    .config("spark.sql.adaptive.enabled", True)
    .getOrCreate()
)

"""
ESERCIZIO 1
* Caricare un dataset csv in spark sql, creare una tabella temporanea
e scrivere query per calcolare aggregazioni per categoria 
"""

df_csv = spark.read.csv(r"C:\EPICODE\5 - Big_Data\dati_grandi.csv", header=True, inferSchema=True)
df_csv.createOrReplaceTempView("tabella_csv")

spark.sql("SELECT * FROM tabella_csv WHERE valore > 30").show()
spark.sql("SELECT categoria, AVG(valore) AS media_valore FROM tabella_csv GROUP BY categoria").show()

"""
ESERCIZIO 2
* Integrare dati da un database PostgreSQL, e da file Parquet locali,
generando un report unificato con spark sql
"""
# df_db = spark.read.format("jdbc")...
# df_db.createOrReplaceTempView("tabella_db")   
# spark.sql("SELECT ...").show()

""" 
ESERCIZIO 3
* Testare performance di query complesse usando formati diversi (csv vs parquet)
e confrontare i tempi di esecuzione su cluster locale
"""
df_parquet = spark.read.parquet("dati_grandi.parquet")
df_parquet.createOrReplaceTempView("tabella_parquet")
start_time = time.time()
spark.sql("SELECT categoria, AVG(valore) AS media_valore FROM tabella_parquet GROUP BY categoria").show()
end_time = time.time()
print(f"Tempo di esecuzione su Parquet: {end_time - start_time} secondi")
start_time = time.time()
spark.sql("SELECT categoria, AVG(valore) AS media_valore FROM tabella_csv GROUP BY categoria").show()
end_time = time.time()
print(f"Tempo di esecuzione su CSV: {end_time - start_time} secondi")

spark.stop()



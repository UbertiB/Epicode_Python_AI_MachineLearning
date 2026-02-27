"""
ESERCIZIO 1
* Crea un dataframe spark di grandi dimensioni e testa repartition() e coalesce(),
osservando tempi e numero di partizoni
ESERCIZIO 2
* Applica caching su un dataframe usato in più aggregazioni e confronta
i tempi di esecuzione con e senza cache.
ESERCIZIO 3
* Prova a fare join tra DataFrame grandi e piccoli usando broadcast, misurando
la differenza di performance rispetto a un join standard
ESERCIZIO 4
* Analizza lo skew dei dati su chiavi specifiche e sperimenta il salting
per sbilanciare le partizioni
"""


from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg, count
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

"""
ESERCIZIO 1
* Crea un dataframe spark di grandi dimensioni e testa repartition() e coalesce(),
osservando tempi e numero di partizoni
"""

data=[(I,I%3) for I in range(1_000_000)]
df=spark.createDataFrame(data,["valore","categoria"])
print(f"N. di partizoini iniziali: {df.rdd.getNumPartitions()}")

#REPARTITION per bilanciare il carico, riorganizzo i dati in 10 partizini basando sul valore
#della colonna categoria
df_repart=df.repartition(10,"categoria")
print(f"N. di partizoini dopo repartition: {df_repart.rdd.getNumPartitions()}")
#COALESCE per ridurre il numero di partizioni, senza riorganizzare i dati
df_coal=df_repart.coalesce(5)
print(f"N. di partizoini dopo coalesce: {df_coal.rdd.getNumPartitions()}")

"""
ESERCIZIO 2
* Applica caching su un dataframe usato in più aggregazioni e confronta
i tempi di esecuzione con e senza cache.
"""
#creo un dataframe di esempio
#data=[(I,I%3) for I in range(1_000_000)]
#df=spark.createDataFrame(data,["valore","categoria"])

#applico una transformation per filtrare i dati
df_filtrato=df.filter(col("valore")>500_000)
#applico un'azione per contare il numero di righe nel dataframe filtrato    
conteggio=df_filtrato.count()
print("Numero di righe con valore maggiore di 500_000:", conteggio)

start_time = time.time()
#applico una transformation per raggruppare i dati per categoria e calcolare la media dei valori
df_aggregato=df_filtrato.groupBy("categoria").agg(avg("valore").alias("media_valore"))
#applico un'azione per mostrare i risultati dell'aggregazione
df_aggregato.show()
end_time = time.time()
print(f"Tempo di esecuzione senza cache: {end_time - start_time} secondi")

#applico il caching al dataframe filtrato
df_filtrato.cache()
#applico nuovamente le stesse operazioni per osservare i tempi di esecuzione con il caching
start_time = time.time()
conteggio=df_filtrato.count()
print("Numero di righe con valore maggiore di 500_000 (con cache):", conteggio)
df_aggregato=df_filtrato.groupBy("categoria").agg(avg("valore").alias("media_valore"))
df_aggregato.show()
end_time = time.time()
print(f"Tempo di esecuzione con cache: {end_time - start_time} secondi")

"""
ESERCIZIO 3
* Prova a fare join tra DataFrame grandi e piccoli usando broadcast, misurando
la differenza di performance rispetto a un join standard
"""
#creo un dataframe grande e uno piccolo
df_grande=spark.createDataFrame([(I,I%3) for I in range(1_000_000)],["valore","categoria"])
df_piccolo=spark.createDataFrame([(0,"A"),(1,"B"),(2,"C")],["categoria","descrizione"])
#join standard
start_time = time.time()
df_join=df_grande.join(df_piccolo, "categoria")
df_join.show()
end_time = time.time()
print(f"Tempo di esecuzione join standard: {end_time - start_time} secondi")
#join con broadcast
start_time = time.time()
df_join_broadcast=df_grande.join(broadcast(df_piccolo), "categoria")
df_join_broadcast.show()
end_time = time.time()
print(f"Tempo di esecuzione join con broadcast: {end_time - start_time} secondi")

"""
ESERCIZIO 4
* Analizza lo skew dei dati su chiavi specifiche e sperimenta il salting
per sbilanciare le partizioni
"""
dati_skew=[(I%10, I) for I in range(1_000_000)]
df_skew=spark.createDataFrame(dati_skew,["chiave","valore"])
print(f"N. di partizoini iniziali: {df_skew.rdd.getNumPartitions()}")
#analizzo lo skew dei dati contando il numero di righe per chiave
df_skew.groupBy("chiave").count().show()
#applico il salting aggiungendo una colonna con un numero casuale tra 0 e 9
from pyspark.sql.functions import rand
df_salted=df_skew.withColumn("salt", (rand()*10).cast("int"))
#riorganizzo i dati in partizioni basate sulla chiave e sul salt
df_salted_repart=df_salted.repartition(10, "chiave", "salt")
print(f"N. di partizoini dopo salting e repartition: {df_salted_repart.rdd.getNumPartitions()}")

spark.stop()

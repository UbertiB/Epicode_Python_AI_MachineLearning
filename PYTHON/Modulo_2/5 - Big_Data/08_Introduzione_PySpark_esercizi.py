"""
ESERCIZI 1
* Crea un datafram di spark a partire da una lista di tuple e applica i filtri 
e ordinamento su una colonna numerica
ESERCIZI 2
* Leggere un file csv con pyspark e calcola il totale delle vendite per categoria, cofrontando i tempi
di esecuzione con Pandas
ESERCIZI 3
* Visualizza il DAG generato da un'operazione pyspark e descrivi come viene suddiviso il job, stages e tasks
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
import sys
import time
import pandas as pd

"""
ESERCIZI 1
* Crea un datafram di spark a partire da una lista di tuple e applica i filtri 
e ordinamento su una colonna numerica
"""
if False: 
    #sessione spark
   spark = SparkSession.builder.appName("Esempio PySpark").getOrCreate()
   #lista di tuple, dati che poi converto in dataframe spark
   dati=[("Mario",28),("Luca",35),("Anna",23)]
   #creo il dataframe di spark (converto la lista)
   df=spark.createDataFrame(dati,["nome","eta"])
   #applico un filtro per eta maggiore di 25 e ordino per eta
   df=df.filter(col("eta")>25).orderBy(col("eta").desc())
   #mostro i dati del dataframe in console con il metodo show()
   df.show()
   #termino la sessione spark
   spark.stop()

"""
ESERCIZI 2
* Leggere un file csv con pyspark e calcola il totale delle vendite per categoria, cofrontando i tempi
di esecuzione con Pandas
"""
if False:
   t1=time.time()
   #leggo il file csv con pandas 
   df_pandas=pd.read_csv("dati_grandi.csv")
   #calcolo il totale delle vendite per categoria con pandas
   totale_pandas=df_pandas.groupby("categoria")["valore"].sum()
   t2=time.time()
   print("Tempo esecuzione Pandas:", t2-t1, "secondi")
   t3=time.time()
   #sessione spark
   spark =  SparkSession.builder.appName("Esempio PySpark").getOrCreate()
   df_csv=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
   totale=df_csv.groupBy("categoria").sum("valore")
   totale.show()     
   t4=time.time()
   print("Tempo esecuzione PySpark:", t4-t3, "secondi")  

"""
ESERCIZI 3
* Visualizza il DAG generato da un'operazione pyspark e descrivi come viene suddiviso il 
job, stages e tasks
"""  
if True:
   #sessione spark
   spark =  SparkSession.builder.appName("Esempio PySpark").getOrCreate()
   df_csv=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
   totale=df_csv.groupBy("categoria").sum("valore")
   totale.show()     
   #visualizzo il DAG con il metodo explain()
   print(f"\nDAG generato da PySpark:")
   totale.explain()
   #termino la sessione spark
   spark.stop()
"""
BIG DATA E PYSPARK: ARCHITETTURA E CONCETTI CHIAVE

Gli strumenti tradizionali come Pandas e Numpy non sono più sufficiente per dataset enormi distribuiti su più nodi 
di calcolo. Apache Spark nasce come risposta a questa esigenza, offrendo una soluzione per elaborazione parallela
e distribuita di grandi volumi di dati.
PySpark è l'interfaccia Python di apache Spark e consente di utlizzare tutta la potenza del framework direttamente
in Python, con un API intuitiva e adatta sia all'analisi sia al ml.
Il suo scopo è permettere gli analisti di scalare il proprio codice da un singolo computer ad interi cluster
senza cambiare la logica dei programmi.
Apache Spark è un motore open source per l'elaborazione distribuita dei dati, progettato per essere veloce, scalabile
e general purpose.
Permette di mantenere i dati in memoria durante le operazioni riducendo drasticamente i tempi di elaborazione.
Spark supporta vari tipi di carichi di lavoro: batch processing, straming in tempo reale, ml e query SQL.
La sua flessibilità lo rende un framework unificato per analizzare dati di qualsiasi dimensione e formato, sia
su cluster locali che su infrattutture cloud come aws, gcp o azure.
PySpark è il modulo che collega Apache Spark al linguaggio Python, offrendo un api compatibile con la sintassi
e le librerie più diffuse nel mondo della data science, consente di creare, manipolare ed analizzare grandi dataset
distribuiti sfruttando la stessa logica che si utilizzerebbe con Pandas ma su scala molto più ampia.
Ditro le quinte Pyspark prende le operazioni e le distribuisce tra i nodi del cluster, questo meccaniscmo permette
di scrivere codice python che gira in parallelo su centinaia di macchine, mantenendo al tempo stesso la semplicita 
e la leggibilità del linguaggio.
L'architettura di Spark è composta da tre elementi principali:
1) Driver: è il processo principale che controlla l'esecuzione del programma, creando il piano logico delle operazioni
   invianto i task ai nodi del cluster. Coordina l'applicazione Spark e suddivide il lavoro in task
2) Cluster Manager: Gestisce le risorse e distribuisce i carichi di lavoro (esempi Yarn, Kubernetes, Spark Standalone)
3) Executor: sono i processi che eseguono fisicamente i task assegnati, operando sui dati in parallelo. 
   Esegue le operazioni sui nodi dei cluster, ogni executor ha processi e memoria dedicati

Garantisce tolleranza ai gusti, ottimizzazione delle memoria e scalabilità dinamica.

Il cuore di spark è rappresentato dagli RDD (Resilient Distributed Dataset), un RDD è una collezione distribuita di
dati immutabile e tollerante ai guasti, divisa i partizioni che vengono elaborate in parallelo.
Ogni trasformazione (es. map, filter, ecc) genera un nuovo RDD senza modificare l'originale. 
La gestione degli RDD può risultare molto complessa, per questo motivo spark ha introdotto astrazioni di livello
superiore come i dataframe ed i dataset, più semplici ed ottimizzate per la maggior parte delle operazioni analitiche
Idf in spark sono simili a pandas ma distribuiti su più cluster, consentono di lavorare su dati tabellari con colonne
tipizzate e di applicare operazionoi sql lite come select group by o join.
Dietro le quinte Spark ottimizza automaticamente le query, riducendo il tempo di elaborazione.

Uno dei concetti più importanti di Spark è la Leasy evaluation, le operazioni non vengono eseguite immediatamente
ma vengono registrate in un grafo DAG (Directed Acyclic Graph). Questo grafo descrive le trasformazioni da applicare
ai dati e le loro dipendenze. Solo quando si esegue un'azione come count(),  collect(), o show(), l'esecuzione avviene.
Vantaggi di ottimizzazione automatica del piano di esecuzione e riduzione delle letture/scritture inutili.
Spark ottimizza il piano e distribuisce le operazioni.

Quando  si esegue un programma PySpark il codice python viene analizzato dal driver che crea il DAG delle operazioni
e le invia cluster manager, quest'ultimo assegna i task agli executors che elaborano i task in parallelo sulle varie
partizioni dei dati, i risultati vengono raccolti e combinati dal driver che restituisce l'output finale.
Ogni jon è suddiviso in stage e task, spark gestisce la loro schedulazione e il recupero in caso di errore.

"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os
import sys

import subprocess

if False:
   #sessione spark
   spark = SparkSession.builder.appName("Esempio PySpark").getOrCreate()
   #lista di tuple, dati che poi converto in dataframe spark
   dati=[("Mario",28),("Luca",35),("Anna",23)]
   #creo il dataframe di spark (converto la lista)
   df=spark.createDataFrame(dati,["nome","eta"])
   #mostro i dati del dataframe in console con il metodo show()
   df.show()
   #termino la sessione spark
   spark.stop()

if False:
   #sessione spark
   spark =  SparkSession.builder.appName("Esempio PySpark").getOrCreate()
   #nuovo dataframe filtrato
   dati=[("Mario",28),("Luca",35),("Anna",23)] #lista di dati
   df=spark.createDataFrame(dati,["nome","eta"])   #dataframe di spark
   df=df.filter(col("eta")>25) #filtro per eta maggiore di 25 
   #il fliltro è leasy, pertanto l'operazione non è ancora eseguita, viene registrata nel DAG

   df.show() #solo ora viene eseguito il DAG e viene mostrato il risultato

if False:
   #sessione spark
   spark =  SparkSession.builder.appName("Esempio PySpark").getOrCreate()
   #nuovo dataframe filtrato
   dati=[("Mario",28),("Luca",35),("Anna",23)] #lista di dati
   df=spark.createDataFrame(dati,["nome","eta"])   #dataframe di spark
   df=df.filter(col("eta")>25) #filtro per eta maggiore di 25 
   #il fliltro è leasy, pertanto l'operazione non è ancora eseguita, viene registrata nel DAG

   print(df.count()) #solo ora viene eseguito il DAG e viene mostrato il risultato

if True:
   spark =  SparkSession.builder.appName("Esempio PySpark").getOrCreate()
   df_csv=spark.read.csv("dati_grandi.csv", header=True, inferSchema=True)
   totale=df_csv.groupBy("categoria").count()
   totale.show()  


"""
ESERCIZIO 1
* Crea una mini-pipeline ETL con Spark che legga dati da CSV, li pulisca e li salvi in formato Parquet
ESERCIZIO 2
* Configurare un DAG Airflow che automatizzi le tre fasi di un processo ETL (extract, transform, load)
ESERCIZIO 3
* Simulare un flusso streaming Kafka con Spark Structured Steaming e visualizzare i dati in tempo reale su console
"""
from pyspark.sql import SparkSession

from pathlib import Path
from pyspark.sql import SparkSession

import os
from prefect import flow, task
import pandas as pd

"""
ESERCIZIO 1
* Crea una mini-pipeline ETL con Spark che legga dati da CSV, li pulisca e li salvi in formato Parquet
"""

if True:
    #ETL distribuito con Spark
    spark=SparkSession.builder.appName("ETL_Scalabile").getOrCreate()
    df=spark.read.csv("dataanalistici.csv",header=True,inferSchema=True) #lettura file
    df_clean=df.dropna().withColumnRenamed("categoria","famiglia") #cambio nome colonne
    #queste operazioni non eseguono subito il calcolo, costruiscono il piano di esecuzione DAG
    df_clean.write.mode("overwrite").parquet("dataanalistici.csv") #qui viene eseguito tutto
"""

ESERCIZIO 2
* Configurare un DAG Airflow che automatizzi le tre fasi di un processo ETL (extract, transform, load)
"""

if True:
    @task
    def estrai_dati(file_csv="vendite_1.csv"):
        print(f"Estrazione dei dati da: {file_csv}")
        df=pd.read_csv(file_csv)
        print(f"Estratti {len(df)} record")
        return df
    @task
    def trasforma_dati(df):
        print("Estrazione dati...")
        df=df.dropna(subset=["categoria"])
        df["categoria"]=df["categoria"].str.upper()
        print(f"Trasformazione completata, record rimanenti: len{df}")
        return df
    @task
    def carica_dati(df,file_output="vendite_pulito.csv"):
        print(f"Caricamento dati su: {file_output}")
        df.to_csv(file_output,index=False)
        print(f"Dati salvati: {file_output}")
        return file_output
    
    #flow principale (DAG grafo di dipendenza lineare)
    @flow(name="Pipeline unica")
    def pipeline_completa(file_csv="dati_grandi.csv", file_output="vendite_pulite.csv"):
        print(f"Pipeline completa")
        df_estratto=estrai_dati(file_csv)
        df_trasformato=trasforma_dati(df_estratto)
        output=carica_dati(df_trasformato,file_output)
        return output
    
    #eseguo il flow
    if __name__=="__main__":
        print("Inizio")
        pipeline_completa("dati_analistici.csv", "dati_analistici.csv")    


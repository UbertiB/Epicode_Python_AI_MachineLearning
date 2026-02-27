"""
PRINCIPI DI ETL SCALABILE E PIPELINE DISTRIBUITE

ETL (Extract, Transform, Load): estrai i dati da uno o più fonti, li trasformi (pulizia, normalizzazione,
arricchhimento), poi li carichi in una destinazione pronta per analisi o operatività.
Una pipeline distribuita è la stessa idea, ma eseguita in parallelo su piu core o pià macchine, perchè 
i dati o i tempi, non stanno più comodi su un singolo pc.
ETL non è più batch notturno, oggi ETL batch, micro-batch e streaming (per dati in continuo).

Nel mondo della data analytic moderna l'ETL rappresenta il cuore pulsante di ogni processo analitico.
Con l'aumento del volume dei dati, i sistemi ETL tradizionali non sono più sufficienti. Serve una nuova pipeline
scalabile, in grado di prendere i dati da fonti eterogenee garandendo affidabilità, prestazioni e coerenza.
Un sistema etl scalabile, non li limita a spostare dati ma trasforma i dati in modo efficiente e resiliente 
mantenendo la possibilità di espandersi con la crescita del business.

- Estrai i dati da diverse sorgenti
- Trasforma i dati in un formato coerente
- Carica i dati in un sistema di destinazione, solitamente un databse analitico o un data warehouse

La fase di estrazione può coinvolgere file, api, flussi in tempo reale, database relazionali
La trasformazione, invece, è il punto in cui i dati vengono puliti, aggregati, validati ed arricchiti
Mentre il caricamento è il passo finale verso la persistenza o l'analisi
In un contesto big dasta questi 3 passaggi non vengono più in modo sequenziale ma spesso vengono in modo
distribuito e parallelo, l'obbiettivo è ridurre i colli di bottiglia, migliorare la latenza e consentire 
l'aggiornamento incrementali senza dover rielaborare l'intero dataset.

Affinche un processo ETL sia realmente scalabile, deve poter crescere in modo orrizontale, invece di 
potenziare un singolo server, l'architettura deve consentire di aggiungere più nodi di elaborazione 
che lavorano in parallelo.
Questo principio è alla base del distribution computer, permette di gestire carichi di lavoro sempre più grandi
mantenendo tempi di esecuzione accettabili.
La scalabilità richiede anche elasticità, capacità del sistema di adeguarsi automaticamente alle variazioni 
di carico, in ambienti cloud questo avviene tramite autoscaling, mentre in contesti on primise richiede un 
design accurato della distribuzione dei job e la gestione delle code di elaborazione.

Una architettura ETL scalabile è composta da più livelli che cooperano tra di loro:
- Ingestione: consiste nell'acquisire grandi flussi di dati in tempo reale, gestendo la persistenza temporanea
  tramite log distribuiti
- Trasformazione: i dati vengono processati in batch o streaming
- Storage: caricamento finale distribuito come in amazon, google, che supportano la paralelizzazione nativa
- Orchestration
Disaccopiamento tra le fasi, ogni componente deve poter scalare indipendentemente, migliorando la resilienza
e la manutenzione.

La scalabilità dell'ETL passa inevitabilmente attraverso il parallelismo esistono due strategie principali
1) Data parallelism: il dataset diviso in partizioni elaborati da nodi diversi
2) Task parallelism: dove più operazioni eseguite simultaneamente su flussi differenti
Combinando questi approcci è possibile ottenere una pipeline molto performante.

L'uso di framework distribuiti come Spark consente di estrarre il parallelissmo a livello logicom, l'utente
definisce le trasformazioni, mentre il motore di esecuzione si occupa della distribuzione dei task.
Questa separazione permette di scrivere codice opeartive che rimane efficiente anche su cluster di centinaia
di nodi.

Un buon sistema ETL distribuito deve essere non solo veloce ma anche affidabile e tracciabile.
Ogni job dovrebbe essere idempotente, ovvero riprodurre lo stesso risultato anche eseguito più volte, 
evitando duplicazioni.
E' importante gestire i check point in modo centralizzato, per poter riprendere l'elaborazione in caso 
di errore.

Separazione tra codice di trasformazione e configurazione operative, consente di mantenere le pipeline
flessibili e facilmente estensibili.

Negli ultimi anni si è affermato ELT (extract - load - trasform), in questo modello i dati vengono prima
caricati nel sistema di destinazione (data lake) e poi vengono trasformati in loco (Spark SQL, dbt)
L'avvento dei nuovo modelli di motore SQL distribuiti ha reso questa strategia più efficiente, riducendo
la complessita delle pipeline tradizionali.

Data lakehouse: unisce vantaggi di data lake, flessibilità e basso costo con quelli di data warehouse, 
coerenza e prestazioni

"""
from pyspark.sql import SparkSession

from pathlib import Path
from pyspark.sql import SparkSession

import os
from prefect import flow, task
import pandas as pd


if False:
    #ETL distribuito con Spark
    spark=SparkSession.builder.appName("ETL_Scalabile").getOrCreate()
    df=spark.read.csv("dataanalistici.csv",header=True,inferSchema=True) #lettura file
    df_clean=df.dropna().withColumnRenamed("categoria","famiglia") #cambio nome colonne
    #queste operazioni non eseguono subito il calcolo, costruiscono il piano di esecuzione DAG
    df_clean.write.mode("overwrite").parquet("dataanalistici.csv") #qui viene eseguito tutto

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
    def pipeline_completa(file_csv="dati_grandi.csv", file_output="vendite_pulite"):
        print(f"Pipeline completa")
        df_estratto=estrai_dati(file_csv)
        df_trasformato=trasforma_dati(df_estratto)
        output=carica_dati(df_trasformato,file_output)
        return output
    
    #eseguo il flow
    if __name__=="__main__":
        print("Inizio")
        pipeline_completa("dati_grandi.csv", "vendite_pulite")


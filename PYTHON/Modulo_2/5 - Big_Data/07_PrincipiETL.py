"""
PRINCIPI DI ETL SCALABILE E PIPELINE DISTRIBUITE

ETL (Extract, Transform, Load): estrai i dati da uno o più fonti, li trasformi (pulizia, normalizzazione,
arricchhimento), poi li carichi in una destinazione pronta per analisi o operatività.
Una pipeline distribuiita è la stessa idea, ma eseguita in parallelo su piu core o pià macchine, perchè 
i dati o i tempi, non stanno più comodi su un singolo pc.
ETL non è più batch notturno, oggi ETL batch, micro-batch e streaming (per dati in continuo).

Nel mondo della data analytic moderna l'ETL rappresenta il cuore pulsante di ogni processo analitico.
Con l'aumento del volume dei dati, i sistemi ETL tradizionali non sono più sufficienti. Serve una nuova pipeline
scalabile, in grado di prendere i dati da fonti eterogenee garandendo affidabilità, prestazioni e coerenza.
Un sistema etl scalabile trasforma i dati in modo efficiente e resiliente mantenendo la possibilità di 
espandersi con la crescita del business.

- Estrai i dati da diverse sorgenti
- Trasforma i dati in un formato coerente
- Carica i dati in un sistema di destinazione, solitamente un databse analitico o data warehouse

La fase di estrazione può coinvolgere file, api, flussi in tempo reale, database relazionali
La trasformazione è il punto in cui i dati vengono puliti, validati ed arricchiti
Mentre il caricamento è il passo finale verso la persistenza o l'analisi
In un contesto big dasta questi 3 passaggi non vengono più in modo sequenziale ma spesso vengono in modo
distribuito e parallelo, l'obbiettivo è ridurre i colli di bottiglia e consentire l'aggiornamento in tempo
reale senza dover rielaborare l'intero dataset.


Affinche un processo ETL sia scalabile, deve poter crescere in modo orrizontale, invece di aggiungere
più server, l'architettura deve consentire di aggiungere più nodi che lavorano in parallelo.
Questo principio è alla base del distribution computer, permette di gestire cariche di lavoro sempre più grandi
mantenendo tempi di esecuzione accettabili.
La scalabilità richiede elasticità, capacità del sistema di adeguarsi automaticamente alla dimensioni di 
carico, in ambienti cloud questo avviene tramite autoscaling.

Una architettura ETL scalabile è composta da più livelli che cooperano tra di loro:
- Ingestione: consiste nell'acquisire grandi flussi di dati
- Trasformazione: i dati vengono processati batch o streaming
- Storage, caricamento distribuito in amazon, google, che supportano la paralelizzazione nativa
- Orchestration
Disaccopiamento tra le fasi, ogni componente deve poter scalare indipendentemente

Il parallelismo è fondamentale
- Data parallelism
- Task parallelism

Un buon sistema ETL distribuito deve essere non solo veloce ma anche affidabile e tracciabile.
ogni job deve essere idempotente, ovvero riprodurre lo stesso risultato anche eseguito più volte, evitando
duplicazioni.
E' importante gestire i check point per poter riprendere l'elaborazione in caso di errore.

Separazione tra codice di trasformazione e configurazione operative, consente di mantenere le pipeline
facilmente estensibili.

Negli ultimi anni si è affermato ELT (extract - load - trasform), in questo modello i dati vengono prima
caricati nel sistema di destinazione (data lake) e poi vengono trasformati in loco (Spark SQL, dbt)
L'avvento dei nuovo modelli di motere SQL distribuiti ha reso questa strategia più efficiente, riducendo
la complessita delle pipeline tradizionali.

Data lakehouse: uniche data lake e data warehouse

"""
from pyspark.sql import SparkSession

#ETL distribuito con Spark
from pathlib import Path
from pyspark.sql import SparkSession

import os

os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jdk-17.0.18.8-hotspot"
os.environ["PATH"] = os.environ["JAVA_HOME"] + r"\bin;" + os.environ.get("PATH", "")


base = Path(__file__).resolve().parent
csv_path = base / "dati_gradi2.csv"

spark = SparkSession.builder.master("local[*]").appName("ETL_Scalabile").getOrCreate()

df = spark.read.csv(str(csv_path), header=True, inferSchema=True)
df_clean = df.dropna().withColumnRenamed("categoria", "famiglia")

out_dir = base / "dati_grandi2_parquet"
df_clean.write.mode("overwrite").parquet(str(out_dir))

spark.stop()
print("OK:", out_dir)


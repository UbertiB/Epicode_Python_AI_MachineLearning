"""
STREAMING CON PYSPARK: STRUCTURED STREAMING

Streaming con PySpark è Spark che finge che un flusso infinito di dati sia una tabella che cresce
nel tempo.
Scrivi query 'da batch' su un DataFrame e Spark la esegue a micro-batch continui
Framework di straming continuo e scalabile basato su spark sql, permette di trattare i dati in tempo
reale come se fossero batch, con semplicità

Batch: hai una tabella 'finita' di righe. Fai una query e fine
Streaming: hai una tabella 'infinita', dove arrivano continuamente nuove righe. Tu scrivi la query 
   una volta sola e Spark la riesegue continuamente sui nuovi dati.
   
I dati in arrivo vengono suddivisi in piccoli batch elaborati sequenzialmente da spark
questo permette di ottenere coerenza e tolleranza agli errori grazie ai checkpoint ed alla gestione
automatica dei commit.
Il framework separa chiaramente tra
- Gestione
- Trasformazone
- Output
permettendo una gestione flessibile dei flussi, ogni operazione viene tradotta in un grafico di
esecuzione che Spark pianifica e distribuisce tra i vari nodi del clusetr in modo efficiente.

Uno streaming dataframe si crea con un approcio simile a quello dei dataframe batch, è possibile
collegarsi ad una fonte dati come filesystem, kafka o socket, definire le trasformazioni desiderate 
ed ottenere un flusso continuo di risultati.
Si possono utilizzare le stesse operazioni sul df sia su dati storici che su quelli in tempo reale,
senza cambiare la logica di elaborazione.
Il vantaggio principale è la trasparenza tra batch e streaming, ossia la possibilità di riutilizzare
le stesse operazioni sql sui dataframe sia sui dati storici che su quelli in tempo reale, senza cambiare
la logica di elaborazioe.

Structured Streaming permette di applicare operazioni complesse come aggregazioni, join e calcoli di
finestre temporali in maniera distribuita e scalalbile.

Si possono anche utilizzare modelli di  ml addestrati su batch precedenti, per fare inferenze in 
tempo reale, integrando ml e streaming.
Le trasformazoni sono deterministiche, garantendo la stessa coerenza dei dati anche in caso di riavvio
dell'applicazione, questo tramite il meccanismo del checkpoint e gestione dello stato interno.

Lo structured straming supporta diverse modalità di output:
- append: scrive solo nuovi record dal flusso
- complete: riscrive l'intera tabella aggregata ogni volta
- update: scrive solo i record aggioranti/modificati dall'ultimo batch

Pyspark e structured straming può leggere dati da fonti eterogenee come Kafka, socket, file system, 
hdfs, tpc, e scrivere su destinazione file system, kafka o db esterni.
Questa flessibilità lo rende ideale in integrazioni aziendali complessi, permettendo di orchestrare
flussi eterogenei con facilità.

Il chepoint è fondamentale per garantire la tolleranza degli errori. Pypark salva lo stato dell'elaborazione
e i processi dei micro batch su storage affidabile, in caso di crash sturctured streaming può partire 
dal punto corretto senza la perdita dei dati.

Le aggregazioni su finestre temporali permettono di calcolare metriche su intervalli di tempo
definiti. Ad esempio conteggi delle transazione a minuto
E' possibile eseguire join tra stream ed altri stream o tra stream e batch, consentendo di correlare
dati in arrivo con dati storici creare allert in tempo reale.
I join sono ottimizzati per ridurre la latenza.

Strumenti di monitoraggio integrati, metriche come latenza, dimensione dello stato, tempo di esecuzione
per indivisuare colli di bottiglia, rendendo il sistemo più robuto e prevedibile.

- Leggi un flusso con spark.readstream (invece di spark.read)
- Trasformazioni: fai le stesso cose del batch (select, filtre, groupby, ecc)
- Output: scrivi con writeStream verso un sink (console, file, kafka, memory,foreachbatch...) 
  definisci un checkpoint per la tolleranza ai guasti

Spark di solito, usa micro-batch:
- ogni N secondi (o appena arrivano dati) prende i nuovi dati
- li processa cone un mini-batch
- aggiorna output
Quindi non si scrive un loop, ma come fosse batch

Esistono 3 elementi fondamentali:
1) Source: da dove arrivano i dati (file, kafka, socket, ecc)
2) Query: trasformazioni (select, filtre, join, groupby)
3) Sink: dove scrivi i risultati
Se manca uno dei 3 non è streaming

Se fai solo filtri e colonne calcolate, Spark può lavorare senza "memoria lunga"
Se fai aggregazioni (groupby), finestre temporali (window), join tra strem, Spark deve ricordarsi
cose tra un micro-batch e il successivo. Questo 'ricordo' è lo stato.
Esempio: vuoi contare quanti eventi per cliente negli ultimi 10 minuti, Spark deve conservere conteggi
intermedi, questo è lo state o chekpoint
Senza il chekpoint se si ferma e riparte, rischi duplicati o perdi progressi.

Output modes: append, update, complete
- Append: scrive solo le righe 'nuove' definitive (tipico per stream senza aggregazioni o con finestre
  temporali concluse)
- Update: scrivi solo righe cambiate dall'ultimo micro-batch (tipico per aggregazioni)
- Complete: riscrive tutta la tabella aggregata ogni volta
La scelta dipende dal tipo di query
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col,avg,max,min,window
import os
from pathlib import Path

HADOOP_HOME = r"C:\hadoop"
# set env
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["hadoop.home.dir"] = HADOOP_HOME
os.environ["PATH"] = str(Path(HADOOP_HOME, "bin")) + ";" + os.environ.get("PATH", "")
# pyspark python
os.environ["PYSPARK_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"C:\Users\uberti\.conda\envs\spark311\python.exe"

spark=SparkSession.builder.appName("SteamingExample").getOrCreate()

#
#LETTURA IN STREAMING DI PIU' CSV
#

if False:
    #lettura cartella
    #(dataframe dinamico che si aggiorna ogni volta che un csv è inserito nella cartella
    stream_df=(spark.readStream.format("csv")
        .option("header","true") #prima riga con nomi delle colonne
        .option("maxFilesPerTrigger", 1)  # legge 1 file per micro-batch 
        .schema("id INT,categoria STRING,valore DOUBLE,data TIMESTAMP") #tipi alle colonne assegnati manualmente
        .load(r"C:\EPICODE\5 - Big_Data\dati") #percorso
    )
    #filtro i valori 
    filter_df=stream_df.filter(col("valore")>350)

    #output in console con la query
    query=(filter_df.writeStream.outputMode("append") #scrivo solo i nuovi record che arrivano nello streaming
        .format("console") #stampo i dati in console
        .option("truncate",False) #stampo le colonne intere senza troncamenti
        .start() #avvio lo straming
    )

    query.awaitTermination() #blocca il programma fino a quando lo stream è attivo
  
#
#AGGREGAZIONE SU FINESTRE TEMPORALI
#
if False:
    #lettura file
    stream_df=(spark.readStream.format("csv")
        .option("header","true") 
        .option("maxFilesPerTrigger", 1)  # legge 1 file per micro-batch 
        .schema("id INT,categoria STRING,valore DOUBLE,data TIMESTAMP") 
        .load(r"C:\EPICODE\5 - Big_Data\dati")
    )
    #filtro
    filter_df=stream_df.filter(col("valore")>350)
    #group by, finestra temporale di 1 minuto
    window_agg=filter_df.groupBy(window("data","1 minute"),"categoria").agg(avg("valore").alias("media_valore"),max("valore").alias("max_valore"),min("valore").alias("min_valore"))
    #con query definisco l'output in console in update a console
    query=(window_agg.writeStream.outputMode("update").format("console").option("truncate",False).start())    

    query.awaitTermination() #blocca il programma fino a quando lo stream è attivo

#
#lettura dataset batch
#
if True:
    stream_df=(spark.readStream.format("csv")
        .option("header","true") 
        .option("maxFilesPerTrigger", 1)  # legge 1 file per micro-batch 
        .schema("id INT,categoria STRING,valore DOUBLE,data TIMESTAMP") 
        .load(r"C:\EPICODE\5 - Big_Data\dati")
    )
    filter_df=stream_df.filter(col("valore")>350)

    #leggo il file con batch senza streaming
    batch_df = (spark.read.format("csv")
    .option("header", "true")  # se il tuo file ha header
    .schema("id INT,categoria STRING,valore DOUBLE,data TIMESTAMP")
    .load(r"C:\EPICODE\5 - Big_Data\output.csv")
    )

    # alias per evitare ambiguità
    s = filter_df.alias("s")
    b = batch_df.alias("b")

    # join stream (s) con batch (b)
    enriched_stream=filter_df.join(batch_df,filter_df.id==batch_df.id, "left").select(filter_df.id,"categoria","valore","data").withColumnRenames("valore","quantita")

    query=enriched_stream.writeSteam.outputMode("append").format("console").option("truncate",False).strat()
    query.awaitTermination()
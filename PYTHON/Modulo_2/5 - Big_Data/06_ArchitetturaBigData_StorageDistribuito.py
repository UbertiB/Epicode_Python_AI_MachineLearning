"""
ARCHITETTURA BIG DATA: STORAGE DISTRIBUITO E FORMATI (PARQUET, ORC)

Nel mondo dei big-data la quantità di informazioni memorizzate ogni giorno, supera di gran lunga la 
capacità di memorizzarle in modo efficiente.
Non si tratta solo di archiviazione di grandi volumi di dati, ma di farlo in modo da garantire accesso rapido, 
scalabilità e affidabilità.
Le architetture big-data nascono proprio per risolvere questo problema, distribuire DATI e CALCOLI su più 
nodi, riducendo i colli di bottiglia e migliorando la risposta complessiva del sistema.
L'obbiettivo non è oiù gestire un singolo database su un server centrale, ma creare un ecosistema distribuito
dove ogni nodo contribuisce allo sotrage o all'elaborazione.
Questo consente di analizzare enormi quantita di informazioni provenienti da fonti eterogenee, mantenendo
prestazioni elevate.
Nella big data i DATI SUDDIVISI IN BLOCCHI e REPLICATI su diversi nodi di un cluster.
Questo modello garantisce scalabilità orizzontale, cioè di aumentare la capacità semplicemente aggiungendo
nuovi nodi senza modificare l'architettura già esistente.
Un altro principio fondamentale è la tolleranza ai guasti, la ridondanza dei dati permette di continuare
le operazioni anche se un nodo si guasta, l'elaborazione dei dati è affidata a framework come Hadoop, 
Dask e Spark che distribuiscono i compiti su vari nodi e ne coordinano l'esecuzione. I dati non si muovono
è il codice a spostarsi verso i nodi che i dati li contengono.
Lo storage distribuito è il cuore dell'architettura big-data, i file vengono divisi in blocchi ed archiviati
su più macchine, ciascuna con una copia parziale dei dati, il sistema mantiene automaticamente le repliche
per garantire la disponibilità ed integrità. 
Esempi sono: 
1) HDFS: memorizza i dati in blocchi da 64 o 128 MB replicando su nodi multipli (default 3 copie) 
   garantendo alta disponibilità e fault tolerance. Adatto per la lettura/scrittura di grandi volumi di dati
   rendendoli ideali per analisi e ml, tuttavia richiede anche formati di archiviazione ottimizzati per lavorare
   con blocchi distribuiti
2) S3, GCS, Azure Blob: Object storage cloud compatibile con Hadoop/Spark, garantisce scalabilità automatica
   e costi basati sull'uso

Dask, di base, è un motore di calcolo distribuito. Lo storage distribuito non è obbligatorio per usare Dask.
Puoi usare Dask benissimo anche su un singolo PC con file locali. 
Dask spezza il calcolo in 'pezzi di lavoro' e costruisce un grafo di dipendenze (DAG). Spesso Dask spezza 
anceh i dati, ma spezzare i dati in dask non significa automaticamente 'metterli su storage distribuito'.
Sono due livelli diversi.
Appena i dati crescono, emergono
due mondi diversi:
1) Calcolo distribuito (Dask):
   - Dask spezza il lavoro in task (un grafo di task).
   - Scheduler decide l'ordine e manda i task ai worker (processi o macchine). 
   - Il grosso vantaggio è parallelizzare e gestire dataset più grandi della RAM con
   chunk/partizioni
2) Storage (dove stanno i dati):
   - Locale: file su disco del tuo PC
   - Network share: cartella su server
   - HDFS/Object storage: dati distribuiti davvero.

Il collo di bottiglia spesso non è il calcolo ma l'I/O. Se leggi CSV enorme da un disco lento, puoi avere
64 core ma comunque aspettare.

Riassumento, 1) Dask spezza i calcoli 2) Dask spezza i dati (a livello logico), ma dipende da come 
li crei/leggi, Dask Array: chunk, Dask DataFrame: partizioni (blocchi di righe).
Dask non spezza i dati anche su HDFS/Object storage, Dask legge e scrive su storage che è già organizzato
in file/oggetti.

Quidi oltre al calcolo che viene distribuito, anche i dati vengono distribuiti e
replicati su diversi nodi di un cluster, questo modello garantisce scalabilità
orizzontale, cioè la possibilità di aumentare la capacità semplicemente aggiungendo
nuovi nodi, senza modificare l'architettura già esistente.
Un altro principio fondamentale è la tolleranza ai guasti. La ridondanza dei dati
permette di continuare le operazioni anche se un nodo si guasta.
L'elaborazione dei dati è affidata a framework come Hadoop e Spark che distribuiscono
i compiti su vari nodi e ne coordinano l'esecuzione.
Il modelli di calcolo si base sull'idea che i dati non si muovono, è il codice che 
si sposta dove i dati sono presenti, riducendo i costi di trasferimento.
Lo storage distribuito è il cuore dell'architettura Big-Data, i file vengono divisi
in blocchi e archiviati su più macchine ciascuna con una copia parziale dei dati.

Anche i formati di archiviazione sono importanti per lavorare con blocchi distribuiti.
- CSV (testuale): è un formato testuale, lento da leggere, non compresso. Non adatto
  ai big-data, formato row based non adatto per analisi, per leggere una colonna è necessario caricare
  l'intero file, un altro limiti è l'assenza da metadati strutturati che rende difficile ottimizzare query
  o compressione, in scenari distribuiti questo significa caricare e processare enormi quantita di dati
  non necessari, con un impatto diretto sulle prestazioni e sui costi.
- JSON (semi-strutturato): ridondanza elevata. Non adatto ai big-data. Per leggere una
  singola colonna, bisogna comunque caricare l'intero db.
- AVRO (binario row-based): Ottimo per streaming, meno per le analisi. 

Da qui nasce la necessità di formati binari colonnari come Parquet o ORC. Memorizzano i dati per colonne 
e non righe. Pensati per la lettura veloce e l'analisi distribuita

L'achiviazione dei dati può avvenire per riga o per colonna, prendiamo come esempio una tabella di 4 colonne
(cliente, data, articolo, valore):
1) row based: salva i record  uno dopo l'altro, riga per riga. La prima riga completa, la seconda completa, ecc
   L'unita 'naturale' di lettura/scrittura è la riga, cioè l'intero record. Questo è perfetto quando devi 
   leggere/scrivere record completi (inserimento/modifiche dati) oppure quando devi fare lookup di una singola
   riga o pochie righe (esempio dammi tutti i dati del cliente x)
2) column based: momorizza, sul disco, blocchi di colonna, quindi tutta la prima colonna (clienti) poi
   tutta la seconda colonna (data), ecc
   Questo è perfetto per le analytics, perchè 'normalmente' leggi tante righe e poche colonne, fai aggregazioni
   su colonne esplicite prendendo tutte le righe (esempio zone di tutti i clienti). Le righe coinvole in analisi
   spesso sono tutte, potenzialmente milioni, mentre le colonne necessarie sono poche (esempio data, cliente,
   importo).
   Esempi sono Parquet o ORC

PARQUET: è un formato colonnare generico. Colonnare significa che i valori della stessa colonna 'stanno vicini'
         così puoi leggere solo le colonne che ti servono. La struttura interna sono blocchi di righe, 
         ma dentro sono organizzati per colonne. 
         Vantaggi: 
         - Letture veloci quando fai analytics: tante righe, poche colonne
         - Buona compressione perchè per colonna i valori sono 'simili' e comprimibili
         - Grandissima compatibilità: è diventato lo standard del data lake moderno (Spark, Trino/Presto,
           DuckDB, Arrow, ecc)
         Attenzione che se scrivi con row group 'sbagliati' (troppo piccoli o grandi) o con troppi file piccoli,
         le prestazioni crollano

ORC (Apache ORC): è, come parquet, colonnare ma nasce dentro l'ecosistema Hive/Hadoop, con un'enfasi forte
                  su statistiche e indici interni per saltare dati inutili. Questo permette di 'scartare'
                  porzioni di file durante la lettura quando i filtri lo consentono         

La scelta tra Parquet o ORC dipende spesso dall'ecosistema, Parquet domina nei contesti multipiattaforma
ORC eccede nei cluster Hadoop puri       

Data lake è un posto dove confluiscono fiumi di dati da diverse fonti. I dati arrivano in modo diverso, 
si dice che arrivano a fiume (lake) i formati sono i più svariati e dipendono dalle fonti, esempi possono 
essere: csv, json, parquet, log, eventi, estratti da erp, se questi dati non vengono 'gestiti' 
diventa presto una palude (data swamp)
"""
import pandas as pd
import numpy as np
import time
import pyarrow.orc as orc
import pyarrow as pa

#
#LETTURA/SCRITTURA FORMATO PARQUET
#
df=pd.DataFrame({
    "id":np.arange(1,1001),
    "categoria": np.random.choice(["A","B","C"],1000),
    "valore": np.random.uniform(10,1000,1000)
})

df.to_parquet("dati_analistici.parquet",compression="snappy")
df.to_csv("dati_analistici.csv")
#le dimensioni (fisiche) di un file csv o parquet cambiano, parquet sicuramente più
#piccolo perchè salvando i dati per colonna 'funziona' meglio la compressione (i dati
#per colonna sono spesso simili)
df_letto=pd.read_parquet("dati_analistici.parquet")
#quando vado a leggere un file parquet, poi diventa un df 'standard' è solo l'archiviazione
#che è colonnare.
#quindi con parquet è spesso utile utilzzare usecols=["nome_colonna"] per estrarre solo
#le colonne interessate (mentre la stessa cosa non è possibile con csv)

print(df_letto.head())

#
#CONFRONTO PRESTAZIONE PARQUET E CSV
#
df=pd.read_csv("dati_grandi.csv")
t1=time.time()
df.to_csv("output.csv", index=False)
t2=time.time()

t3=time.time()
df.to_parquet("output.paquet", compression="snappy")
t4=time.time()

print(f"Scrittura CSV {t2-t1:.3f}s | Scrittura Parquet {t4-t3:.3f}s")

#scrivere in parquet spesso è più veloce anche perchè occupa meno spazio e più 
#veloce da leggere per analisi che richedono poche colonna (da specificare con usecols)


#
#UTILIZZO FORMATO ORC
#
df=pd.DataFrame({
    "prodotto":["X","Y","Z"]*4,
    "prezzo":[100,150,200]*4,
    "vendite": [10,20,15]*4
})
table=pa.Table.from_pandas(df)
with open("vendite.orc","wb") as f:
    orc.write_table(table,f)

"""
INTRODUZIONE A DASK: PARALELIZZAZIONE E CONCETTI BASE
77
Con aumentare della dimensione dei dataset, gli struenti tradizionali come np e pd iniziano
a mostrare limiti evidenti in termini di consumo di memoria

DASK nasce proprio per risolvere questo problema
E' una libreria python progettata per l'elaborazione parallela e distribuita
Mantiene un api simile a pd e np
Consente agli analisti di scalare il proprio codice senza doverli riscrivere da zero, passando dal lavoro
su un singolo laptop all'esecuzione su un cluster di calcolo.
Dask si distingue per la sua capacità di gestier dataset più grandi della memoria fisica, e di sfruttare 
proceddori multi core.
Quando pandas inizia a rallentare o generare errori di memoria, dask permette di suddividere i dati in
partizoini (chunk) che vengono elaborate in parallelo. Evitando il caricamente completo del dataset in ram
E' compatibili con l'ecosistema scientifico di python si integra con np, pd e scikitleanr, consentendo di 
distribuire i calcoli senza modificare la logica del codice.
Inoltre esegue piani di calcolo intelligente grazie a un grafo di dipendenze
L'architettura è basata su due componenti principali
1) COLLEZIONI
   Come dask dataframe, dask array rappresentano strutture di dati distribuite che imitano pd e np, ma che ì
   operano su frammenti di dati gestiti in parallelo. Ogni operazine non è eseguita immediatamente, bensi
   tradotta in un grafico di calcolo per gestire le dipendenze tra i vari passaggi dell'elaborazione
2) MOTORE DI ESECUZIONE
   il motore di esecuzione analizza il grafo di calcolo e decide come distribuire i compiti tra i core ed
   i nodi, gestendo memoria, priorità, e la comunicazione tra i processi.
   Questo approccio consente di eseguire lavori complessi in modo efficiente, ottimizzando l'utilizzo delle
   risorse disponibili 
I concetti fondamentali si riassumono:
- Lasy Evaluation: le operazioni non vengono eseguite subito ma solo quando si chiede esplicitamente un risultato
 con metodo compute. questo permette di pianificare ed organizzare l'esecuzione
- task graph: è la rappresentazione delle operazioni da svolgeer, ogni nodo è un'operazione e gli archi
  definiscono le dipendenze
- collezioni distribuite: sono le strutture principali con cui si lavora in dask. Dask array per operazioni
  numeriche su matrici di grandi dimensioni
  dask datafram per analisi tabellari
  dask bag per dati semistrutturati o iterabili complessi

La vera forza di dask risiede nella paralelizzazione automatica dei calcoli
Ciascuna partizione del dataset viene elaborata in parallelo da un core o da un nodo del dataset
questo significa che le operazioni possono essere eseguite contemporaneamente su più porzioni dei dati
Dask supporta diversi tipi di dati schedul
  - singol machine schedul: per esecuzione parallela su singolo computer multicore
  - distributed schedul: per calcolo su cluster con interfaccia di monitoraggio web
La gestiona automatica del parallelismo consente di ottenere scalabiltà orrizontale e verticale
senza modifcare il codice sorgente
Dask è la scelta ideale quando i dataset diventano troppo grandi per essere gestiti con pandas
ma non al punto da richiedere infrastrutture complesse come spark
Non è sempre necessario dask per dataset piccoli o medi pandas rimane più semplice ed immediata.
Dask mostra il suo valore quando la memoria è limitata o è importante sfruttare tutti i core disonibili
per velocizzare i calcoli.
In molti casi sono possibili anche soluzioni ibride: pandas per esplorazione e dask per esecuzione finale.

"""
import dask.dataframe as dd
import pandas as pd
import numpy as np

#modo lasy
pdf=pd.DataFrame({
    "valore":np.random.randint(1,100,2_000_000),
    "categoria":np.random.choice(["A","B","C"],2_000_000)
})
df=dd.from_pandas(pdf,npartitions=8) #i dati suddivisi in 8 blocchi indipendneti permettendo calcoli paralleli
media_per_categoria= df.groupby("categoria")["valore"].mean() #costruiamo un grafo di calcolo per calcolare la media
#qui non succede ancora nessun calcolo per dask è lazy
print(media_per_categoria.compute()) #qui esegue i calcoli, aggrengando le 8 partizioni in parallelo

#lettura parallela di files multipli in parallelo
df=dd.read_csv("dati/vendite_*.csv")
totali=df.groupby("categoria")["valore"].sum().compute()
print(totali)

#parallelizzazione con dask array

import dask.array as da
import time

x=np.random.random((10_000,10_000))
dx=da.from_array(x,chunks=(1000,1000))
t1=time.time()
risultato=(dx+dx.T-dx.mean(axis=0)).mean().compute()
t2=time.time()
print(risultato)
print(f"tempo di esecuzione: {t2-t1:.3f} s")
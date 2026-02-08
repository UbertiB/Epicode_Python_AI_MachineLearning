""""
TECNICHE DI OTTIMIZZAZIONE IN PANDAS PER BIG DATA

Tecniche di ottimizzazione in pandas per big-data
Lavorare con dataseet di grandi dimensioni rappresenta una delle sfide principali in data science
Sebbene pandas sia uno strumento potente, la sua architettura è bassato su memoria ram, questo può
generare rellentamenti su dati di grandi dimensioni.
Big data infondono quindi un cambio di mentalità
non basta scrivre codice che funziona, ma che funziona in modo efficiente. ottimizzare significa ridurre
l'uso di memoria, miglioarare la velocità di esecuzione.
Vedremo che idnetificare i limiti principarli di pandase con dataset di grandi dimensioni e quali tecniche
adottare per miglioare le prestazioni

CONTROLLARE I TIPI DI DATO
Controllare i tipi di dato è una dlele operazioni fondamentali.
Pandas assegna tipi di defaul che occupano molta memoria rispetto al necessario.
Convertire i numeri in float32 o int 32
e quelle categoriali in category
riduce drasticamente l'uso di memoria, migliorando sia la memoria utilizzata che la velocità 
di tutte le operazini.
Applicare conversioni mirate prima di qualsiasi ananlisi pesante è fondamentale per ridurre il tempo impiegato.

CARICAMENTO DEL DATASET
Pandas fornisce diverse soluzione per ottimizzare la lettura dei dati.
E possibile specificare il tipo di dato (in fase di caricamento) tramite il parametro dtype, 
evitando conversioni successive
Inoltre con usecols consente di importare solo le colonne necessarie.
Caricare i dati a CHUNCK in questo modo pandas elabora un numero limitato di righe per volta
Questa stategia è ideale per processi di analsii incrementale o la costruzine di pipline automatizzate.

Uno degli aspetti più potenti di pandas è la possiblità di eseguire operazioni in modo VETTORIALE senza
dover ricorrere a cicli espliciti come for
Le operazioni vettoriale sono programmate in C risultando molto veloci.
L'uso di funzioni come apply o for devono essere valutate molto attentamente e sono invece da preferire
le operazioni vettoriali
Un'ulteriore livello  di ottimizzazione si ottiene con la lazy evaluation, ovvero ritardando l'esecuzione
delle operazioni fino a quando non è strettamente necessario.
Sebbene Pandas non la implementi nativamente, può essere simulata combinando generato con dask che gestisce
i calcoli in maniera differita e parallela.

Molti problema di prestazioni in Pandas derivano dalla creazoine involontaria di 
copie dei dati (copie implicite)
Esempio la selezione o un filtro Pandas può generare una copia del df. (utilizzare inplace per evitare)
- Evitare copie inutili: usare inplace=True dove possibile
- Rilasciare oggetti non più necessari con del e gc.collect() (in questo modo libero la memoria)
- Usare copy (deep=False) per copie leggere
- Controllare le dimensioni con memory_usate()

Quando le ottimizzazioni interne a Pandas non sono pù sufficenti è possibile integrarlo con strumenti
esterni per ottenere prestazoini di livello superiore.
* Dask DataFrame: parallelismo su più core/cluster. Tratta dataset più grandi della memori del computer
  suddividendoli in blocchi gestisti dinamicamente
* Modin: backend distribuito (Ray o Dask) per accellelare le operazioni pandas 
  senza modificare il codice esistente
* Polars: alternativa moderna in Rust
* PyArrow: formato colonnare veloce per I/O
Permettono di scalare Pandas su Big-Data reali.

"""

import pandas as pd
import numpy as np
import gc

df=pd.DataFrame({
    "id":np.arange(3_000_000),
    "citta":np.random.choice(["Roma","Milano","Napoli","Crema","Torino"],3_000_000),
    "vendite": np.random.uniform(10,500,3_000_000),
    "sconto":np.random.uniform(0,0.3,3_000_000)
})
print(f"Uso di memoria iniziale: {df.memory_usage(deep=True).sum()/1e6}")
#cambio dei tipi
df["citta"]=df["citta"].astype("category")
df["vendite"]=df["vendite"].astype("float32")
df["sconto"]=df["sconto"].astype("float32")
print(f"Uso di memoria dopo conversione tipo: {df.memory_usage(deep=True).sum()/1e6}")

#salviamo i dati in parquet e compresso
df.to_parquet("vendite_ottimizzato.parquest",compression="snappy")

#gestione delle copie implicite
df=pd.DataFrame({
    "cliente":np.random.randint(10_000,20_000,2_000_000),
    "spesa":np.random.uniform(5,200,2_000_000),
    "sconto":np.random.uniform(0,0.3,2_000_000),
})
print(f"Uso di memoria iniziale: {df.memory_usage(deep=True).sum()/1e6}")
df["spesa_netto"]=df["spesa"]*(1-df["sconto"])
df.drop(columns="sconto",inplace=True)
del gc.garbage[:]  #libero memoria inutilizzata
gc.collect()
print(f"Uso di memoria : {df.memory_usage(deep=True).sum()/1e6}")
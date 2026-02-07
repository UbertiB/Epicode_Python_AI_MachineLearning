"""
OTTIMIZZAZIONE DELLE VISUALIZZAZIONI E GESTIONI DEL MEMORY FOOTPRINT

La capacità di ottimizzare la visualizzazione e gestire in modo efficiente la momoria diventa importante
quando i dati diventano tanti. Non basta saper creare grafici accattivanti ma devono essere anche semplici e veloci
Il memory footprint è lo spazio di memoria occupato da un programma durante l'esecuzione. 
Ridurlo è una priorità, dove ogni mb risparmiato può tradursi in maggiore scalabilità e stabilità

Tecniche per ottimizzare i grafici, affrontare dataset di grandi dimensioni, ridurre il consumo di memoria con np,
valutare compromessi tra qualità e prestazioni e adottare strumenti workflow avanzati per miglioarare 
efficiente a produttività

Un grafico ben progettato non deve essere solo esticamente carino ma anche rapido da generare e facile da interpretare.
L'ottimizzazione parte quindi dalla riduzione degli elementi superflui, quando una sintesi o un campionamento 
può trasmettere lo stesso messaggio in modo più chiaro e leggero.
Acluni formati, grafici Raster (come png) possono risultare pesanti in alta risoluzione, 
mentre grafici vettoriali (come svg o pdf) possono risultare più veloci.
Anche piccoli argomenti, come ridurre lo spessore delle linee, limitare il numero di colori, 
alleggerire le griglie, possono migliorare le prestazioni senza compromettere la qualità visiva.

Quando si affrontano dataset molto grandi, il caricamente completo in memoria diventa non fattibile, in questi casi 
è necessario ricorrere a strategia alternative.
Una tecnica diffusa è il CHUNK, dividere il dataset in blocchi più piccoli da lavorare sequenzialmente.

E' importante adottare FORMATI DI ARCHIVIAZIONE più efficienti del classico csv.
Formati come Parquet o Feather sono compressi, binari e ottimizzati per la lettura parziale dei dati, riducendo
il tempo di caricamento.

La gestione di dataset di grandi dimensioni, richiede una mentalità scalalbile, non chiedersi solo come
analizzare tutti subito ma come suddividere, filtrare, ridurre i dati, manenendo intatta l'informazione rilevante.

NUMPY è il cuore delle operazioni numeriche in Python ed uno degli strumenti più potenti per ridurre il consumo 
di memoria.
La scelta del TIPO DI DATO è un aspetto cruciale, molto spesso si utilizzano float64 al posto di float32/16
o int 64 anche quando può essere memorizzato in int32/16.
Np offre anche ARRAY ESTREMAMENTE COMPATTI rispetto alle struttura native di python (come le liste) 
quindi preferire array np per grandi volumi di dati, questo migliora le prestazioni e riduce l'uso della memoria.

Ogni processo di ottimizzazione implica un COMPROMESSO TRA QUALITà E PRESTAZIONI.
non sempre è utile generare grafici estremamente dettagliati.
Il principio guida deve essere la chiarezza, un grafico con milioni di punti può sembrare accurato ma 
diventa illegibile rispetto ad un grafico con meno dettagli.

Bisoga VALUTARE IL CONTESTO, per una pubblicazione scientifica può essere accettabile sacrificare le prestazioni 
in favore della precisione, mentre per una dashboard iterativa è preferibile un rendering rapido e leggero. 
LA SCELTA OTTIMALE NON è ASSOLUTA ma dipende dall'obbiettivo comunicativo e dal pubblico di destinazione.

Esistono degli strumenti dedicati per distruibuire elaborazioni di dati su più core o più cluster (con Dask) 
consentendo di gestire dataset che superano la memoria disponibile.

L'ottimizzazione non è un processo isolato deve essere parte integrante di un workflow quotidiano.
Un approccio ideale prevede:
- pianificazione preventiva, scegliere i formati di archiviazione e strutture dati ottimizzate
- riduzione dei dati, lavorare solo sulle informazioni necessarie evitando di caricare colonne o righe non utili 
- ottimizzazione interativa, testando diverse strategie di visualizzazione e confrontando l'impatto in termini di memoria
- automatizzazione integrando chunck, conversioni di tipo e formati di output
Questo permette di migliorare le prestazioni, ridurre errori, aumentari la produttività e garantire che i progetti
rimangono scalabili nel tempo.

"""
import matplotlib.pyplot as plt
import numpy as np
import dask.dataframe as dd  #pip install "dask[dataframe]"
import pandas as pd
import seaborn as sns

x=np.random.rand(10_000_000).astype(np.float32)
y=np.random.rand(10_000_000).astype(np.float32)

#prendo solo 50_000 punti su 10_000_000 casuali
idx=np.random.choice(len(x),size=50_000,replace=False)
x_sample=x[idx]
y_sample=y[idx]

plt.figure(figsize=(10,6))
plt.scatter(x_sample,y_sample,s=3,alpha=0.4)   
plt.title("Analisi di un dataset enorme con ottimizzazione memoria e campionamento")       
plt.xlabel("Variabile X")
plt.ylabel("Variabile Y")
plt.show()

np.random.seed(42)
tickers=[f"Titolo_{i}" for i in range(100)]
dates=pd.date_range(start="2018-01-01",end="2023-12-31")
data=np.random.rand(len(dates),len(tickers)).astype(np.float32)*100
df=pd.DataFrame(data,index=dates,columns=tickers)
#print(df)
#calcolo rendimenti giornalieri solo su un campione di titoli
sample_tickers=np.random.choice(tickers,size=10,replace=False)
df_sample=df[sample_tickers].pct_change().dropna()
corr_matrix=df_sample.corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr_matrix,cmap="coolwarm",center=0,annot=True,fmt=".2f")
plt.title("Correlazione campione titoli")
plt.show()

# Visualizzazione frontiera efficiente semplificata
mean_returns = df_sample.mean()
cov_matrix = df_sample.cov()
num_portfolios = 5000
results = np.zeros((3, num_portfolios))

for i in range(num_portfolios):
    weights = np.random.random(len(sample_tickers))
    weights /= np.sum(weights)
    port_return = np.sum(weights * mean_returns)
    port_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    results[0,i] = port_std
    results[1,i] = port_return
    results[2,i] = port_return / port_std  # Sharpe ratio

plt.figure(figsize=(10,6))
plt.scatter(results[0,:], results[1,:], c=results[2,:], cmap='viridis', alpha=0.5)
plt.xlabel("Rischio (Deviazione Std)")
plt.ylabel("Rendimento Atteso")
plt.title("Frontiera efficiente: campione titoli")
plt.colorbar(label="Sharpe Ratio")
plt.show()

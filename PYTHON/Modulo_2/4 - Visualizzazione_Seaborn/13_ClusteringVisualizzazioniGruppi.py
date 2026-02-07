"""
CLUSTERING E VISUALIZZAZIONI DI GRUPPI CON SEABORN

L'obbiettivo del clustering è raggruppare osservazioni simili tra di loro, in base alle
loro caratteristiche senza l'uso delle etichette predefinite. In altre parole si tratta 
di  una forma di apprendimento non supervisionato che permette di scoprire strutture
nascoste nei dati, come sottogruppi naturali o comportamenti ricorrenti.

Mentre tecniche come PCA riducono il numero di variabili, tecniche di clustering raggruppano
gli elementi per caratteristiche simili. PCA comprime le colonne (feature space), clustering
comprime le righe in categorie (entity space) 

Nella data scienze, la combinazione di algoritmi di clustering, con strumenti di visualizzazione
come Seaborn è particolarmente potente, perchè consente di interpretare i risultati in modo
immediato. Le rappresentazioni grafiche rendono evidente la distribuzione dei cluster, la
distanza tra i gruppi, e la coerenza interna di ciascun inseme di punti.
Bisogna preparare i dati, applicare algoritmi di clustering, e visualizzare i risultati per
essere valutati.
Tra i metodi di clustering più diffusi ci sono:
- K-MEANS: partiziona i dati in k gruppi, minimizzando la distanza intra-cluster (valutazione
  silhoutte). E' l'algoritmo più conosciuto. Rapido e funziona bene su dati numerici 
  normalizzati, ma richiede di specificare a priori il numero di cluster.
- DBSCAN: raggruppa punti in base alla densità, utile per cluster irregolari. Non richiede di
  specificare il numero di cluster. E' l'ideale per dati rumorosi o forme non lineari, ma fatica 
  con dataset a densità molto variabile
- AGGLOMERATIVE CLUSTERING: costruisce gerarchie di cluser (dendogrammi). Parte considerando
  ogni punto come cluster e li unisce, progressivamente in gruppi più grandi, genera una struttura
  ad albero, dendogramma, utile per capire le relazioni tra gruppi

Ogni algoritmo ha vantaggi e limiti diversi.

Questi algoritmi generano etichette che possono essere visualizzate con Seaborn

Le variabili (colonne) devono essere pulite, prive di valori mancanti e scalate in modo 
coerente perchè molti algoritmi di clustering sono sensibili a questi dati.
E' anche utile selezionare solo le varibili più significative, rimuovendo quelle innutili
o ridondanti per non introdurre 'rumore' nei risultati.
Inoltre, visualizzare i dati prima del cluster evidenzia se ci sono pattern evidenti o
anomalie da correggere. Un analisi preliminare con scatterplot o pairplot può fornire 
informazioni utili sulla struttura interna del dataset.

Dopo aver eseguito un algorimo di clustering, la prima forma di visualizzazione da utilizzare
è uno SCATTERPLOT che mostra i punti colorati in base al cluster.
Consentendo di verificare se i gruppi sono ben separati o presentano sovrapposizioni, 
l'uso del parametro hue è perfetto per evidenziare il cluster. 
Mentre parametri come size e style possono aggiungere ulteriori informazioni, ad esempio rappresentando 
variabili quantitative o categoriali aggiuntive.
Un'ulteriore pratica è aggiungere la posizione dei centroidi come punti evidenziati per visualizzare
il centro di ciascun gruppo

Quando le variabili sono più di 2, lo scatterplot non è più sufficiente per interpretare la
struttura dei cluster, in questi casi si utilizza il PAIRPLOT andando a colorare i punti 
in base al cluster di appartenenza (hue=cluster). Il pairplot permette di evidenziare come
i cluster di distribuiscono rispetto a ciascuna coppia di variabili e di individuare le dimensioni
che discriminano meglio i gruppi. 
spesso alcune coppie mostrano separazioni nette, mentre altre sovrapposizioni, questo aiuta a comprende
quali variabili sono più informative per il modello.

Le HEATMAP sono strumenti efficaci per rappresentare grafica mente le relazioni tra cluster e variabili.
Una heatmap piò visualizzare, per esempio, la media di ogni feature per ciascun cluster
mostrando quali caratteristiche distinguono i gruppi tra di loro. E' possibile creare una
heatmap a partire da un df che contiene le medie o le distanze tra centroide, i colori 
delle celle consentono di evidenziare pattern.
Analizzando i valori medi di ogni cluster posso comprende la separazione geometrica ma anche
il significato semantico dei gruppi, individuando variabili che definiscono ciascun cluster

La riduzione dimensionale è uno step essenziale per visualizzare i clusetr in modo comprensible
tecniche come PCA o TSNE riducono le dimensioni a 2/3, preservando la struttura dei cluster.
Dopo la riduzione dimensionale si possono rappresentare i punti con uno scatterplot
bidimensionale con i colori che indicano il cluster, questo permette di capire la qualità 
del clustering.
Gruppi compatti e bene separati suggeriscono un buon risultato, mentre sovapposizioni
ulteriori controlli.

Seaborn non fa clusering 'di suo' (non calcola KMeans, DBSCAN, ecc). Seaborn serve a visualizzare
bene i gruppi, e a volte a mostrare struttura 'tipo cluster' via heatmap + clustering
gerarchico (clustermap). Il clustering vero lo si fa con scikit-learn, poi passi etichette 
e centroidi a Seaborn per il plot e la visualizzazione.

Gli algoritmi di clustering consentono di scoprire strutture nascoste, e di identificare
gruppi omogenei ma solo attraverso la visualizzazione è possibile intrpretare correttamente
i risultati, combinando scatterplot, pairplot ed heatmap possiamo confrontare la coerenza
iterna dei cluster, comprendere le ralazioni tra variabili, e valutare la qualità del 
raggruppamento. Strumenti per pcs e tsne rendono possibile rappresentare in modo intuitivo
anche dastaset complessi, traducendo in variabili bidimensionali

ESEMPIO 1: CLUSTER GIA' NOTO, scatter con colori
"""
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("iris")  # dataset demo
sns.scatterplot(data=df, x="sepal_length", y="sepal_width", hue="species")
plt.title("Gruppi (classi) visualizzati con hue")
plt.show()

"""
qui 'species' non è un cluster calcolato da Seaborn o altre tecniche, 
è un cluster noto e con hue colora i gruppi.
Deduci che se i colori sono ben separati, le variabili separano i gruppi. Se i colori sono
mescoalti la separazione è nulla o scarsa.
"""

"""
Esempio 2: CLUSTERING VERO (KMeans) + Seaborn per visualizzare
Qui fai clustering e poi visualizzi i gruppi trovati
"""
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = sns.load_dataset("iris").copy()
X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]

# Standardizza: se non lo fai, KMeans viene falsato dalle scale diverse
X_scaled = StandardScaler().fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
df["cluster"] = kmeans.fit_predict(X_scaled)

sns.scatterplot(data=df, x="petal_length", y="petal_width", hue="cluster", palette="tab10")
plt.title("KMeans: cluster calcolati e visualizzati")
plt.show()

"""
STANDARIZZA sempre prima di calcolare i gruppi con tecniche di clustering (k-means o altro).
Se non standarizzi, falsi il risultato.
KMEANS: 
N_CLUSTERS ha bisogno di sapere quanti gruppi creare, non scopre da solo quanti
cluster esistono, il numero devi passarglielo.
Per questo motivo è necessario provare diversi valori di n_clusters e si valuta poi il migliore.
random_state=42 serve per rendere riproducibile il risultato (perchè k-means parte da valori
scelti in modo casuale)
N_INIT="auto", k-means, di suo, non fa un solo tentativo per clusterizzare, ne fa n e poi 
sceglie il migliore, con 'auto' lasci a scikit-learn decidere quanti tentativi fare
SILHOUETTE, la 'silhouette score' serve a valutare se il clusering ha senso
e spesso per scegliere il n_cluster in KMeans. Per calcolare la silhouette si calcola 
la distanzia media dei vari punti (clienti, articoli, ecc) dagli altri punto dello stesso
cluster e si fa la differenza con la distanza media del punto dal cluster più vicino 
(e non suo). Ottengo valori tra -1 e +1
- +1 o vicino: punto ben assegnato (sta vicino al suo cluster e non agli altri)
- 0 o vicino: punto sul confine di due cluster
- <0: probabilmente assegnato a cluster sbagliato.
La silhouette score è la media di tutti i punti, più è alto meglio è. Non esistono soglie
universali, ma  una lettura in tal senso può aver senso:
- 0.5: cluster abbastanza netti
- 0.25-0.50: cluster deboli, ma magari utili
- <0.25: stai forzando gruppi che in realtà non esistono, o hai kpi, scale sbagliate
- <0: clustering molto sospetto.

Esempio: provo diversi n_cluster per poi sceglire il migliore
"""
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

scores = {}
for k in range(2, 11):
    labels = KMeans(n_clusters=k, random_state=42, n_init="auto").fit_predict(X)
    scores[k] = silhouette_score(X, labels)

print(scores)  # scegli k con score più alto (ma controlla anche il senso business)
"""
risultato: {2: np.float64(0.6810461692117465), 3: np.float64(0.5511916046195927), 4: np.float64(0.49764331793219296), 5: np.float64(0.4930804067193529), 6: np.float64(0.36784649847122536), 7: np.float64(0.3542978877198859), 8: np.float64(0.34467972180562056), 9: np.float64(0.31558878533897866), 10: np.float64(0.3014143745325154)}
sembrerebbe corretto prendere k=2 (perchè ha lo score più alto) ma in questo modo crei due gruppi
che maggiormente rappresentano i dati, se vuoi una rappresentazione più fine, potrebbe anche
aver senso considerre k=3
"""

"""
Esempio 3: VISUALIZZARE CLUSTER IN PIù DIMENSIONI CON PAIRPLOT
Quando hai 4-10 variabili (tipico ERP), lo scatter 2D è riduttivo, Pairplot ti fa vedere
tutte le coppie
"""
import seaborn as sns
import matplotlib.pyplot as plt

cols = ["sepal_length", "sepal_width", "petal_length", "petal_width", "cluster"]
sns.pairplot(df[cols], hue="cluster", corner=True, plot_kws={"alpha": 0.7, "s": 25})
plt.show()
"""
Cosa guardi: se i cluster sono separati in molte coppie di variabili, oppure se sono 
separati solo in una coppia, in questo caso quella metrica è sufficiente e non serve
un clustering più complesso con più variabili
"""

"""
Esempio 4: HEATMAP CON CLUSTERING GERARCHICO (Seaborn clustermap)
"""
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

df = sns.load_dataset("iris").copy()
X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
X_scaled = StandardScaler().fit_transform(X)

sns.clustermap(X_scaled,metric="euclidean",method="ward",cmap="vlag",yticklabels=False)
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

np.random.seed(0)
df=pd.DataFrame({
    "x":np.random.normal(0,1,200),
    "y":np.random.normal(0,1,200),
})
scaler=StandardScaler()
df_scaled=scaler.fit_transform(df) #necessario scalere per k-means
kmeans=KMeans(n_clusters=3,random_state=0)
df["cluster"]=kmeans.fit_predict(df_scaled)
sns.scatterplot(data=df,x="x",y="y",hue="cluster",palette="Set2",s=70)
plt.title("Clustering K-Means con Seaborn")
plt.show()

df["z"]=np.random.normal(0,1,200)
sns.pairplot(data=df,hue="cluster",corner=True)
plt.suptitle("Paiplot con cluster")
plt.show()

#heatmap dei centroidi
centroids=pd.DataFrame(kmeans.cluster_centers_,columns=["x","y"])
sns.heatmap(centroids,annot=True, cmap="coolwarm")
plt.title("Heatmap dei centroidi del clustering")
plt.show()





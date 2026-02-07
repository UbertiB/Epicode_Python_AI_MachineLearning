"""
VISUALIZZAZIONI PER ANALISI MULTIVARIATE (correlazioni multiple)

Analisi multivariata significa studiare più variabili insieme, nello stesso momento. Non due sole variabili
ma un sistema (esempio: prezzo, sconto, domanda, leadtime, margine, rotazione, ecc).
In ERP è normale perchè quasi nessun fenomeno è a una causa sola.
L'analisi multivariata è un inseme di metodi per tre obbiettivi diversi:
- Esplorazione: descrivere la struttura e pattern;
- Inferenziale: spiegare e testare ipotesi;
- Predittivo/ML: prevedere e decidere.

Prima di procedere con l'analisi è necessario essere 'sicuri' dei dati con pulizia, null, outlier, duplicati e
definizione KPI coerenti.

KPI COERENTI si intende KPI che abbiano lo stesso significato in tutte le analisi, e che siano calcolati
sempre nello stesso modo
esempio: 
    rotazione=venduto annuo/giacenza media, 
    rotazione=costo venduto/giacenza media, 
    rotazione=prelievi/giacenza attuale, 
la rotazione ha diversi modi di calcolo, ma si deve applicare lo stesso metodo in tutta l'analisi.
Anche il PERIMETRO deve essere lo stesso, esempio includi/escludi note di credito, campionature, movimenti
interni, ecc
COERENZA SCALE NUMERICHE
Mettendo insieme più variabili è necessario prestare attenzione alle scale numeriche diverse: se metti insieme 
euro, giorni, percentuali, ecc, senza standarizzare (scaling), molte tecniche di analisi 'vedono' solo 
la variabili con scala più grande.
Scaling significa standarizzare/normalizzare, serve a rendere confrontabili le scale numeriche.
Esempio
- Prezzo in euro (scala da 0 a 1.000)
- Lead time in giorni (scala da 1 a 60)
- Sconto in percentuale (scala da 0 a 0.3)
Molte tecniche (PCA, KMeans, regressioni) vengono dominate dalla variabile con range più grande o varianza
più alta. Quandi è necessario standarizzare questi importi.
Ci sono diverse tecniche di standarizzazione, esempio:
- Z-SCORE (standarizzazione): così ogni variabile ha media 0 e deviazione 1 e 'pesa' in modo comparabile.
  from sklearn.preprocessing import StandardScaler
  X_scaled = StandardScaler().fit_transform(X)
- MIN-MAX (0-1):
  from sklearn.preprocessing import MinMaxScaler
  X_scaled = MinMaxScaler().fit_transform(X)

Grafici utili per analisi multivariata:
SCATTER MATRIX: si vede come una griglia di scatter. Serve per capire relazioni a due a due tra molte variabili,
   soprattuto a scoprire non linearità e outlier. E' il primo filtro per capire se ha senso parlare di correlazoini
   o regressioni. Limite: con tanti dati diventa nebbia.
HEATMAP DI CORRELAZIONE: serve per una vista sintetiche delle dipendenze lineari. E' utile come 'mappa di
   coerenza' dei KPI. Limite: la correlazione non ti dice la forma e spesso è distorta da mix di popolazioni (
   famiglie diverse, clienti diversi). La heatmap va sempre letta insieme a segmentazione. Una heatmap su tutta
   la popolazione spesso inganna, perchè stai mescolando gruppi diversi. La segmentazione serve a verificare
   se la relazione è stabile o se è un effetto di mix. Per segmentare posso utilizzare metodi diversi. 
   1) Heatmap diverse: per ogni popolazione visualizzare una heatmap diversa 
        num_cols = ["leadtime_giorni","prezzo","sconto","domanda_mese","copertura_giorni","margine_pct","rotazione"]
        for seg, g in df.groupby("segmento"):
            corr = g[num_cols].corr()
            mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
            plt.figure(figsize=(8,6))
            sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", center=0, linewidths=0.3)
            plt.title(f"Correlazioni per segmento = {seg}")
            plt.show()
   2) Differenza tra correlazioni (per vedere dove i segmenti divergono)
            corr_A = df[df["segmento"]=="A"][num_cols].corr()
            corr_C = df[df["segmento"]=="C"][num_cols].corr()
            diff = corr_A - corr_C
            mask = np.triu(np.ones_like(diff, dtype=bool), k=1)
            plt.figure(figsize=(8,6))
            sns.heatmap(diff, mask=mask, annot=True, fmt=".2f", center=0, linewidths=0.3)
            plt.title("Differenza correlazioni: A - C")
            plt.show()
   3) HUE (per capire forma e outlier). Quando vuoi capire se una correlazione nasce da due nuvole separate,
      lo vedi subito con scatter/jointplot con hue
            sns.scatterplot(data=df, x="leadtime_giorni", y="rotazione", hue="segmento", alpha=0.4)
            plt.title("Rotazione vs lead time con segmentazione (hue)")
            plt.show()
PARALLEL COORDINATES: Ogni riga è un profilo multivariato (da approfondire)

PCA (Principal Component Analysis). Concetto base: riduzione dimensionale. Prendi molte variabili e le 
comprimi in poche 'componenti' che catturano la maggior parte della variabilità. E' algebra lineare per trovare
nuovi assi che spiegano più informazione possibile. Limite PCA è lineare e richiede scaling.

CLUSTERING SU PCA. Qui è unsupervised ML: raggruppi profili simili (articoli/clienti/fornitori) usando più
varibili insieme (PCA). Va validato non cruduto ciecamente.

   
In questa analisi variabili numeriche, variabili categoriche e variabili temporali non sono trattate tutte 
allo stesso modo.

L'analisi di correlazioni multiple è un passaggio cruciale per comprendere come più variabili interagiscono
tra di loro in un dataset. 
Spesso non basta osservare coppie isolate di variabili, è necessario avere una visione globale delle 
relazioni, identificando pattern, cluster o associazione statisticamente significative.

Più dimensioni richiedono strumenti di visualizzazione avanzati per essere comprese appieno.
Le visualizzazioni giocano un ruolo chiave in questo contesto, permettono di interpretare strutture complesse
e trend nascoste nei dati.

Seaborn ed altre librerie di Python offrono una varietà di strumenti per creare grafici sofisticati che 
facilitano l'analisi di correlazioni multiple.
Consentendo di combinare matrici di correlazione, scatterplot multipli, netword graph e rappresentazioni
derivate da pca

Partiamo dalla heatmap classiche fino a biplot per ottenere una panoramica completa delle correlazioni
multiple.

MATRICE DI CORRELAZIONE E HEATMAP
La matrice di correlazione rappresenta la prima tappa per analisi di correlazione multiple
Mostra tutti i coefficiente di correlazione tra le variabili numeriche in una griglia, permettendo 
di individuare immediatamente associazioni forti o deboli.
Le heatmap di seaborn consentono di visualizzare queste matrici in modo intuitivo, con codifica a colori che
evidenza l'intensità delle correlazioni, è possibile aggiungere annotazioni numeriche, 
colorare in base alla forza della correlazione e applicare maschere per evidenziare solo 
le parti rilevanti della matrice, personalizzare palette e scale.
P-VALUES
Le heatmap diventano ancora più informative se abbinate a pvalue o simboli di significatività evidenziando
quali correlazioni sono statisticamente affidabili.

PAIRPLOT (SCATTERPLOT MATRIX) E FACETGRID
Il PAIRPLOT o scatterplot matrix è uno strumento prezioso quando si vogliono analizzare tutte le coppie
possibili di variabili, ogni variabile viene rappresentata sia sull'asse x che y in una griglia 
generando un insieme completo di scatterplot bidimensionali.
Oltre ai punti è possibile aggiungere linee di regressione lineari, kde bidimensionali o 
hue per differenziare categorie.
Il pairplot consente di individuare rapidamente pattern generali, cluster o outlier presenti nei dati e di
osservare come le relazioni variano tra le diverse coppie di variabili.
Per dataset numerosi, è utile combinare il pairplot con alpha e palette di colori coerenti per evitare 
sovrapposizioni confuse e migliorare la leggibilità.

Il JOINTPLOT multiplo estende il concetto di joinplot a più coppie di variabili, mostrando scatterplot,
kde o regplot centralmente e distribuzioni marginali lungo gli assi, la possibilità di aggiungere hue
o più tipi di grafici centrali, permette di confrontare relazioni simili tra diversi gruppi o condizioni.

Il pairplot è particolarmente utile per dataset con un numero moderato di variabili,
poiché la griglia può diventare rapidamente ingombrante con l'aumentare delle dimensioni.
Un altro strumento potente per l'analisi di correlazioni multiple è il FacetGrid,
che permette di creare una griglia di grafici separati per ogni combinazione di categorie.
Questo è particolarmente utile quando si vogliono confrontare relazioni tra variabili

Questi strumenti di visualizzazione avanzata con Seaborn facilitano l'analisi di correlazioni multiple,
consentendo di scoprire pattern nascosti e interazioni tra variabili che potrebbero non essere evidenti
con metodi più semplici.

CORRELOGRAMMA E NETWORK GRAPH
Il correlogramma
è una rappresentazione avanzata delle correlazioni multiple
che combina la matrice di correlazione con annotazioni statistiche aggiuntive come p-value o 
simboli di significatività per evidenziare quali relazioni sono statisticamente rilevanti.
Oltre ad evidenziare la forza della correlazione consente di distinguere tra relazioni 
casuali e significative, migliorando l'interpretazione delle correlazioni multiple.
Questi grafici possono essere triangolare o completi, spesso includono una codifica cromatica per evidenziare
le significatività
Network graph delle correlazioni
Un approccio alternativo e intuitivo è rappresentare le correlazioni multiple come un network graph
In questa visualizzazione le variabili diventano nodi e le correlazioni rappresentano archi tra i nodi 
con larghezzza o colore proporzionali alla forza della relazione.
Questo metodo evidenzia immediatamente cluster di variabili strettamente correlate e nodi isolati o
con poche connesioni.
In network graph utili con dataset ad alta dimensionalità e consentono di interpretare la struttura
della correlazioni con una rete complessa, facilitando l'individuazione di gruppi di variabili interconnesse.

BIPLOT E RIDUZIONE DELLA DIMENSIONALITÀ PCA
Quando il numero di variabili è elevato, tecniche di riduzione della dimensionalità come PCA (Principal Component Analysis)
possono essere utilizzate per sintetizzare le informazioni in un numero ridotto di componenti principali.
Queste componenti possono poi essere visualizzate tramite un biplot o scatterplot 3D,
fornendo una rappresentazione visiva delle relazioni tra le variabili originali e le componenti principali.

Questi strumenti avanzati di visualizzazione con Seaborn e altre librerie Python facilitano l'analisi di correlazioni multiple,
consentendo di scoprire pattern nascosti e interazioni tra variabili che potrebbero
non essere evidenti con metodi più semplici.
Il biplot permette di sintetizzare le relazioni multiple in uno spazio ridotto, facilitando l'interpretazione
e l'individuazione di pattern complessi nei dati.
In combinazione con altre visualizzazioni rappresenta uno degli strumenti più potenti per l'analisi esplorativa dei dati

"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Esempio 1
#matrice di correlazione con heatmap
np.random.seed(0)
#df = pd.DataFrame(np.random.randn(100, 5), columns=list("ABCDE"))
#df = pd.DataFrame({"A": np.random.randn(100), 
#                   "B": np.random.randn(100),
#                   "C": np.random.randn(100),
#                   "D": np.random.randn(100),
#                   "E": np.random.randn(100),
#                  "gruppo": np.random.choice(["Gruppo 1", "Gruppo 2"], size=100)})
df = pd.DataFrame(np.random.randn(100, 5)) #matrice 100 x 5 di numeri casuali
columns=list("ABCDE")
print(f"Data set: \n{df.head(10)}")
corr = df.corr(numeric_only=True) #matrice di correlazioni tra colonne

sns.heatmap(corr, annot=True, cmap="coolwarm", center=0)
plt.title("Matrice di correlazione")
plt.show()

#Esempio 2
df["gruppo"] = np.random.choice(["Gruppo 1", "Gruppo 2"], size=len(df))
sns.pairplot(df, hue="gruppo",kind="scatter", diag_kind="kde", plot_kws={"alpha":0.7})
plt.suptitle("Scatterplot Matrix con hue", y=1.02)
plt.show()

#Esempio 3
import networkx as nx

G = nx.Graph() #grafi vuoto (G)
threshold = 0.3 #sogli di correlazione (correlati solo i valori con correlazione > 0.3)
threshold = 0.10 #alzo la soglia per avere connessioni (essendo un dataset casuale 'normalmente' non ha connessioni)
cols=corr.columns #corr contiene solo variabili numeriche
#creo gli archi del grafo
for i, col1 in enumerate(cols): 
    for j, col2 in enumerate(cols):
        if i < j and abs(corr.loc[col1, col2]) > threshold:
            G.add_edge(col1, col2, weight=corr.loc[col1, col2])

pos = nx.spring_layout(G) #calcoliamo la disposizine nei nodi nello spazio in modo che i collegamenti si dispongano automaticamente
edges = G.edges()

print("Numero archi:", G.number_of_edges())
print("Numero nodi:", G.number_of_nodes())
print("Archi con peso:") 
for u, v, d in G.edges(data=True):
    print(u, "-", v, "r =", round(d["weight"], 3))


weights = [abs(G[u][v]['weight'])*5 for u,v in edges] #spessore di ciasun archi in base alla correlazione
nx.draw(G, pos, with_labels=True, width=weights, node_color="skyblue", node_size=800)
plt.title("Network Graph delle correlazioni")
plt.show()

#Esempio 4
#pca e biplot semplicifcato
from sklearn.decomposition import PCA

x=df.select_dtypes(include='number') #solo colonne numeriche
pca = PCA(n_components=2)
components = pca.fit_transform(x) #prendo solo colonne numeriche
plt.figure(figsize=(6,5))
plt.scatter(components[:,0], components[:,1], alpha=0.7)
for i, col in enumerate(x.columns):  #per ogni variabile originale (le colonne) traccio una freccia
    plt.arrow(0,0, pca.components_[0,i]*3, pca.components_[1,i]*3,
              color='r', alpha=0.5)
    plt.text(pca.components_[0,i]*3.2, pca.components_[1,i]*3.2, col, color='r')
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Biplot PCA")
plt.show()

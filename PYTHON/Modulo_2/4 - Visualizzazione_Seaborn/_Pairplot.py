"""
PAIRPLOT
Mostra tutte le relazioni a coppie tra variabili numeriche (scatter) e le distribuzioni
sulla diganoale (istrogramma o KDE). E' uno strumento da EDA utile per farsi un'idea
veloce, 'pericoloso' se lo prendi come 'prova' di qualcosa.
Serve per scovare pattern (lineari, monotoni, cluster, outelri), e per vedere subito
se due variabili hanno relazioni strane 

Quandi si analizzano dataset con molte variabili diventa difficile capire come esse si 
relazioni, ci viene in aiuto parplot che ci permette di vedere le relazioni tra
le variabili numeriche (in una unica mastrice), mostrando sia le distribuzioni 
individuali che le correlazioni bivariate. 
Rappresentazione potente per analisi esplorativa dei dati.
Permette di identificare pattern, correlazioni linerari (o no), outlier e possibili
cluster.
Parametri fondamentali del pairplot permette di colorare punti in base a variabii
categoriali, rappresentare cluster, combinare paiplot con tecniche di riduzione 
dimensionali per dataset con molte feature.
Si possono modificare i tipi di grafici sulla diagonale, impostare le palette di colori,
aggiungere variabile categoriale con hue, impostare dimensioni, trasparenza ed altri parametri
filtrare colonne specifiche, dimensioni, marker, ecc

La funzione pairplot crea una griglia di grafici che mette in relazione ogni coppie
di variabili numeriche.
Ottini una panaramica completa delle correlazioni all'interno del dataset.
Ogni cella rappresenta la relazione tra due variabili
Se i punti formano pattern linerai è probabile esista una relazione positiva o negativa.
Se invece sono dispersi, la relazione potrebbe essere debole o assente.
Le diagonali mostrano la distribuzione delle singole variabili.
Le forme simmetriche indicano una distribuzione normale, mentre code lunghe o picchi
accentuati, possono rilevare outlier o dati errati.
Questo mi permette di decidere se applicare trasformazioni, normalizzazioni o trattamenti
sui dati prima di ulteriori analisi.
Con hue è possibile vedere come i punti si distribuiscono in base a categorie differenti.
Suggerendo relazioni significative tra variabili numeriche e categoriali.
Uno dei vantaggi è la capacità di mostrare tutte le correlazioni in una unica figura.
Consentendo di individusare rapidamente quali sono le coppie fortemente correlate e quali
no, senza dover calcolare la matrice di correlazione manualmente.
Quando alcune relazioni appaiono forti devono essere approfondite in seguito con 
grfici di regresione o analisi statistiche più dettagliati.
Corner true riduce la ridondanza mostrando solo metà matrice.
mentre diaking kinde permette di visualizzare la densità di distribuzione anziche istogrammi

In contesti di clustering non supervisionato, come k-means o dbscan è possibile aggiungere
al dataset una colonna con le etichette dei cluster generati ed utilizzare il pairplot
per visualizzare la loro disposizione nello spazio delle faeture,
questo aiuta a comprendere se i cluster torvati sono coerenti, distinti o parzialmente
sovrapposti.
Allo stesso modo, nel caso si analisi supervisionate, il pairplot consente di osservare
la separabilità delle classi, elemento chiave nella scelta delle variabili più 
predittive.

La visualizzazione dei gruppi facilita sia l'interpretazione che la validazione dei 
modelli di machine learning

Quando il numero di variabili è molto elevato il pariplot diventa difficile da leggere.
In questi casi è utilile applicare una riduzione dimensionale, come pca (principal 
component analisyt) o tsne, per sintetizzare le informazioni principali in due o tre
componenti.
Dopo aver ridotto le dimensioni del dataset possiamo utilizzare il paiplot per visulizzare
le nuove variabili sintetizzate.
Combinare pca con paiplot è una tecnica comune in analisi esplorativa multivariata
Si ottengono grafici compatti, interpretativi ed informativi.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

df=sns.load_dataset("iris")

#
#Pairplot base
#
sns.pairplot(data=df)
plt.show()
#serve ad indivisuare la correlazioni tra variabili

#con hue
sns.pairplot(data=df,hue="species",diag_kind="kde",palette="Set2")
plt.suptitle("Pairplot con distinzione di specie",y=1.02)
plt.show()
#diag_kind="kde" sostituisce gli istogrammi con delle curve di densita

#pairplot dopo riduzione dimensionale
features=df.drop("species",axis=1) #tolge le variabili categoriali
pca=PCA(n_components=3)
components=pca.fit_transform(features) #trasforma le 4 variabili originali in 3 variabili (indicate come n_components)
df_pca=pd.DataFrame(components,columns=["PC1","PC2","PC3"])
df_pca["species"]=df["species"] #riporto la variabile categorica cancellata per eseguire la riduzione dimensionale variabili 
sns.pairplot(data=df_pca,hue="species",diag_kind="kde",palette="coolwarm")
plt.suptitle("Paiplot sulle componenti principali")
plt.show()


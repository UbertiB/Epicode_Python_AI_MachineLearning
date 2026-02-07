"""
DISTRIBUZIONI MULTIVARIATE ED ALTA DIMENSIONALITA'

Distribuzioni multivariate ad alta dimensionalità
Analisi di distrubuzioni multivariate, rappresenta una sfida centrala in data science
soprattutto quando i dati contrngono molte variabli.
in questi contesti le relazioni tra le variabili possono essere complesse e non immediatamente
evidenti, rendendo difficile interpretazione diretta dei dati.
Qui introduciamo concetti per analizzare distribuzioni multivariate e comprendere le
interazioni tra variabili ed identificare pattern nascosti in spazi ad alta dimensionalita
affornteremo modelli matematici che descrivono queste distribuzioni
esploreremo analisi statistica avanzata
tecniche di riduzine dimensionale
e strategie per visualizzare dati complessi

Le distribuzioni multivariate estendono il concetto di distribuzioni unvariata
considerando più variabili simutaneamente
un esempio è la distirbuzione normale multivariata definita da un vettore di medie ed una
matrice di covariante che descrive le relazioni tra le variabili.
Oltre alla normale multivariate esisteno distrubuzioni complesse come le t-multivariate, le
Direchlet e le copule, utili per catturare le dipendenze non lineari e correlazioni 
complesse tra variabili in spazi ad alta dimensionalità.

L'analisi di distribuzioni multivariate richiede strumenti statistici avanzati per calcolare
le coovariante, correlazioni e misure di associazioni tra variabili
pd a np permettono di calcolare matrice di correlazioni e statistiche descrittive multivariate
mentre pacchetti come skypy e  statsmodels offrono test statistici multivariati ed analisi
di cluster
Un'altra tecnica è la stima della densità multivariata (KDE multivariata) che permette
di approsimare la distribuzione dei dati senza assumere una dimensione predefinita

La riduzione dimensionale è uno strumento chiave per analisi multivariate. Tecniche come
PCA, permettono di proiettare i dati in uno spazio di dimensioni inferiore. Oltre a PC
abbiamo TSNE e UMAP sono efficaci per ridurre la dimensionalità. facilitando cos' 
indivisuazione di clustter in pattern nascosti.
Queste tecniche consentono di semplificare dataset complessi.

Visualizzare dati multivariati esistono diverse strategie, pariplot e scatterplot 3d, 
permettono di esplorare relazioni tra un numero limitato di variabili mentre heatmap di correlazione
e matrici di coovarianza, forniscono una panoramica completa delle dipendenze tra tutte
le variabili.
Tecniche di riduzioni dimensionali possono essere integrate con visualizzazioni 2d o 3d
consentendo di rappresentare clustern o pattern nascosti.
Anche uso di colori, forme, o trasparenze per distinguere gruppi o categorie, può migliorare
la leggibilità dei dati

"""
#
#correlazione multivariata CORR()
#

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(0)

df=pd.DataFrame(np.random.rand(200,5),columns=list("ABCDE")) #array 200 x 5
plt.figure(figsize=(6,5))
sns.heatmap(df.corr(),annot=True,cmap="coolwarm")
plt.title("Matrice di correlazione tra variabili")
plt.show()
#ovviamente essendo un df random i valori sono vicini a zero, nessuna relazione reale


#
# RIDUZIONE DIMENSIONALE
#
from sklearn.decomposition import PCA

pca=PCA(n_components=2) #riduco a due dimensioni passando da 5 variabili originali a 2 variabili
components=pca.fit_transform(df) #risultato un array 200 x 2
plt.scatter(components[:,0],components[:,1],cmap="coral",alpha=0.6)
plt.title("Proiezione PCA dei dati multivariati")
plt.xlabel("Componente principale 1 (PC1)")
plt.ylabel("Componente principale 2 (PC2)")
plt.show()
#la pca serve per ridurre la dimensionalità per poi visualizzarli in 2d o 3d ed identificare
#pattern nascosti nelle variabili

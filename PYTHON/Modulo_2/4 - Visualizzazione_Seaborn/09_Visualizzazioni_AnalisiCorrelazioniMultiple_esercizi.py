
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

penguins = sns.load_dataset("penguins").dropna()
num_cols = penguins.select_dtypes(include='number').columns  # almeno 6 variabili

# Esercizio 1
# Creare una matrice di correlazione annotata con Heatmap per un dataset di almeno sei variabili, interpretando le correlazioni più forti.

corr = penguins[num_cols].corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr,annot=True,fmt=".2f",cmap="coolwarm",cbar_kws={"label": "Correlation"})
plt.title("Matrice di correlazione delle variabili numeriche")
plt.show()

# Esercizio 2
# Generare un Pairplot completo con hue per una variabile categoriale, confrontando le relazioni tra tutte le coppie di variabili.

#vars=num_cols (solo variabili numeriche)
sns.pairplot(penguins,vars=num_cols, diag_kind="kde",corner=False)
plt.suptitle("Pairplot delle variabili numeriche (senza hue)", y=1.02)
plt.show()

sns.pairplot(penguins,vars=num_cols,hue="species", palette="Set2",diag_kind="kde",corner=False)
plt.suptitle("Pairplot delle variabili numeriche per specie", y=1.02)
plt.show()

# Esercizio 3
# Costruire un network graph delle correlazioni per evidenziare cluster e connessioni significative, scegliendo un opportuno threshold.

import networkx as nx
import numpy as np

threshold = 0.5  # soglia per connessioni significative
edges = [(i,j,{'weight':corr.loc[i,j]}) 
         for i in num_cols for j in num_cols if i != j and abs(corr.loc[i,j])>threshold]

G = nx.Graph()
G.add_nodes_from(num_cols)
G.add_edges_from(edges)

pos = nx.circular_layout(G)
plt.figure(figsize=(8,8))
nx.draw(
    G, pos, with_labels=True, node_color="skyblue", edge_color="gray",
    width=[abs(d['weight'])*5 for (u,v,d) in G.edges(data=True)],
    node_size=2000, font_size=10
)
plt.title("Network delle correlazioni > 0.5")
plt.show()

# Esercizio 4
# Eseguire una PCA sul dataset, visualizzando il biplot e commentando quali variabili contribuiscono maggiormente alle componenti principali.

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

X = penguins[num_cols]
#scaling delle varibili numeriche per renderle confrontabili
X_scaled = StandardScaler().fit_transform(X) 
#pca per riduzine dimensionale variabili numeriche
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8,6))
plt.scatter(X_pca[:,0], X_pca[:,1], c=pd.Categorical(penguins['species']).codes, cmap="Set2", s=50)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("Biplot PCA delle componenti principali")
#c=pd.Categorical(penguins['species']).codes
#c è simile a hue, hue è di seaborn c è di matplotlib inoltre c funziona anche con variabili numeriche mentre hue e spesso assiciato a variabili categoriche
#pd.Categorical(penguins['species']).codes trasforma ogni categoria in un numero intero, per poi colorarlo con cmap="Set2" che definisce la palette di colori

# Vettori delle variabili
for i, col in enumerate(num_cols):
    plt.arrow(0, 0, pca.components_[0,i]*3, pca.components_[1,i]*3,
              color='r', alpha=0.5, head_width=0.1)
    plt.text(pca.components_[0,i]*3.2, pca.components_[1,i]*3.2, col, color='r')

plt.grid(True)
plt.show()
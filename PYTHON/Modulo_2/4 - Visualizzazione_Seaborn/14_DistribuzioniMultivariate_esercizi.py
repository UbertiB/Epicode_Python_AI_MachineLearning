# Esercizio 1 – Analisi di correlazione multivariata
# Creare un dataset sintetico con almeno 5 variabili numeriche.
# Calcolare la matrice di correlazione tra tutte le variabili.
# Visualizzare la matrice con una heatmap di Seaborn.
# Commentare quali variabili mostrano correlazioni più forti o più deboli.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Dataset sintetico

df = sns.load_dataset("diamonds")
df_numeric = df.select_dtypes(include="number").copy()


# Matrice di correlazione
corr = df_numeric.corr()

# Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title("Matrice di correlazione")
plt.show()


# Esercizio 2 – Riduzione dimensionale con PCA
# Applicare PCA sul dataset creato nel punto 1 e ridurre i dati a 2 componenti principali.
# Creare uno scatterplot delle componenti principali.
# Colorare i punti in base a una variabile a scelta per evidenziare eventuali pattern.

from sklearn.decomposition import PCA

# PCA a 2 componenti
pca = PCA(n_components=2)
components = pca.fit_transform(df_numeric)
df_pca = pd.DataFrame(components, columns=['PC1', 'PC2'])
df_pca['ColorVar'] = df['carat']  # ad esempio Var2 per colorare i punti

# Scatterplot PCA
plt.figure(figsize=(8,6))
sc = plt.scatter(df_pca['PC1'], df_pca['PC2'], c=df_pca['ColorVar'], cmap='viridis', s=80)
plt.title("PCA: 2 componenti principali")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(sc, label='Valore Var2')
plt.show()



# Esercizio 3 – Densità multivariata con KDE
# Selezionare due variabili dal dataset e stimarne la densità con sns.kdeplot.
# Utilizzare gradienti di colore o livelli per evidenziare le zone di maggiore densità.
# Interpretare i pattern rilevati e eventuali zone di concentrazione dei dati.

plt.figure(figsize=(8,6))
sns.kdeplot(
    x=df['Var1'], y=df['Var2'],
    fill=True, thresh=0, levels=20, cmap='mako'
)
plt.scatter(df['Var1'], df['Var2'], c='white', s=20, edgecolor='black', alpha=0.5)
plt.title("Densità bidimensionale Var1 vs Var2")
plt.xlabel("Var1")
plt.ylabel("Var2")
plt.show()
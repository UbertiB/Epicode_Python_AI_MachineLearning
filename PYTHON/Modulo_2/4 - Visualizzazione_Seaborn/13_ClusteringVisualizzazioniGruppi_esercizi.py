# Esercizio 1
# Applicare K-Means su un dataset con almeno tre variabili, 
# standardizzandole prima dell’analisi.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Caricamento dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)

# Standardizzazione
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
labels = kmeans.fit_predict(X_scaled)
df['Cluster'] = labels

print("Centroidi dei cluster (standardizzati):")
print(kmeans.cluster_centers_)


# Esercizio 2
# Visualizzare i cluster in uno scatterplot 2D colorato con Seaborn e aggiungere i centroidi.

# Riduzione dimensionale per scatterplot 2D
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['PCA1'] = X_pca[:,0]
df['PCA2'] = X_pca[:,1]

# Scatterplot con Seaborn
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='PCA1', y='PCA2', hue='Cluster', palette='Set1', s=80)

# Centroidi nello spazio PCA
centroids_pca = pca.transform(kmeans.cluster_centers_)
plt.scatter(centroids_pca[:,0], centroids_pca[:,1], c='black', s=200, marker='X', label='Centroidi')
plt.title("Cluster K-Means su dataset Iris (PCA 2D)")
plt.legend()
plt.show()


# Esercizio 3
# Creare un pairplot per analizzare come le variabili discriminano i cluster.
# Generare una heatmap delle medie di ciascun cluster per confrontarne i profili.
# Utilizzare PCA o t-SNE per ridurre le dimensioni e visualizzare i cluster nello spazio bidimensionale.

# Pairplot
sns.pairplot(df, vars=iris.feature_names, hue='Cluster', palette='Set1', corner=True)
plt.suptitle("Pairplot delle variabili per cluster", y=1.02)
plt.show()

# Heatmap dei profili dei cluster
cluster_means = df.groupby('Cluster')[iris.feature_names].mean()
plt.figure(figsize=(8,6))
sns.heatmap(cluster_means, annot=True, cmap='coolwarm')
plt.title("Heatmap delle medie dei cluster")
plt.show()

# PCA già mostrata nello scatterplot precedente, ma possiamo usare t-SNE
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)

plt.figure(figsize=(8,6))
sns.scatterplot(x=X_tsne[:,0], y=X_tsne[:,1], hue=labels, palette='Set1', s=80)
plt.title("Visualizzazione cluster con t-SNE")
plt.show()
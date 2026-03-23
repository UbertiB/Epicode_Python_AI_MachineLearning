"""
GMM (Gaussian Mixture Mode)

Mixture=miscela
Gaussian=distribuzione normale (a campana)
GMM assume che i dati siano generati da più 'campane' sovrapposte
Ogni punto può appartenere a più cluster con una probabilità, esempio un punto sta tra due 
cluster, 70% cluster A, 30% cluster B

GMM usa algoritmo chiamato EM (Expectation-Maximization)
Step 1 - Inizializzazione: parte con centroidi casuali
Step 2 - Expectation (E): calcola probabilità che ogni punto appartenga a ogni cluster
Step 3 - Maximization (M): aggiorna media e varianza dei cluster
Ripete fino a convergenza.

Differenza GMM con K-Means
K-Means:
    distnaza dal centro (euclidea)
    Cluster 'tondi'
GMM:
    probabilità (statistica)
    cluster ellittici (più flessibili)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture

# 1. Carico il dataset
iris = load_iris()
X = iris.data
y = iris.target
feature_names = iris.feature_names
#print(feature_names)
# il dataset iris contiene 4 feature

# 2. Standardizzo le feature
scaler = StandardScaler()
X_std = scaler.fit_transform(X)
#print(pd.DataFrame(X).head(5))
#print(pd.DataFrame(X_std).head(5))
#standardscaler serve a portare tutte le feature sulla stessa scala. 
#Anche con GMM è buona pratica farlo

# 3. Creo il modello GMM
gmm = GaussianMixture(n_components=2, covariance_type='full', random_state=42)
#chiedo al modello di cercare 2 distribuzioni gaussiane, cioè 2 cluster probabilistici

# 4. Addestro il modello e ottengo i cluster
labels = gmm.fit_predict(X_std)
#con il metodo fit_predict si impara i parametri dal modello e si assegna, a ogni punto, 
#il cluster più probabile

# 5. Ottengo le probabilità di appartenenza
probs = gmm.predict_proba(X_std)
#restituisce, per ogni riga, la probabilità di appartenenza a ciuascun cluster

print("Prime 5 etichette di cluster:")
print(labels[:5])

print("\nPrime 5 probabilità di appartenenza:")
for i in range(5):
    p0,p1=probs[i]*100 #trasformo in %
    print(f"Cluster 0: {p0:.2f}% | Cluster 1: {p1:.2f}%")

print("\n% per cluster di appartenenza:")
max_probs=probs.max(axis=1)
for i in np.argsort(max_probs)[:10]:  #ordina gli indici in base ai valori
    p0,p1=probs[i]*100
    print(f"Riga {i} → {p0:.2f}% | {p1:.2f}%")

# 6. Grafico con incetezza
threshold = 0.6  # sotto questo → incerti 
threshold = 0.9999  # sotto questo → incerti -- aumento la percentuale a 99.99% perchè non o casi

uncertain_mask = max_probs < threshold  # memorizza true se punto incerto, false se punto certo

plt.figure(figsize=(8,6))

# punti normali
plt.scatter(
    X_std[~uncertain_mask,0],  #con la tilde faccio l'opposto, pertanto prendo i punti certi
    X_std[~uncertain_mask,1],
    c=labels[~uncertain_mask],
    cmap="viridis",
    s=50,
    alpha=0.5
)

# punti incerti
plt.scatter(
    X_std[uncertain_mask,0],
    X_std[uncertain_mask,1],
    c="red",
    s=150,
    label="Ambigui"
)

plt.legend()
plt.title("Punti ambigui GMM")

plt.show()

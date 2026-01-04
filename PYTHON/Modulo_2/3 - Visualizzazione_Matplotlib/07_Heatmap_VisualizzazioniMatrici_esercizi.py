"""
ESERCIZIO 1
* Visualizza una matrice 10x10 du vendite mensili per prodotto: aggiunti annotazioni dinamiche
e market automatici>90
ESERCIZIO 2
* Crea una heatmap della correlazione tra 5 variabili casuali: usa testi automatici per mostrare
i valori di correlazione
ESERCIZIO 3
* Genera una heatmap interattiva di dati metereologici (temperature giornaliere per 7 giorni e
7 citta), in cui al passaggio del mouse compaiono dettagli aggiuntivi
ESERCIZIO 4
* Combina annotazioni dinamiche e market automatici per evidenziare simultaneamente valori
critici e valori estermi

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from scipy.spatial.distance import pdist, squareform

# ESERCIZIO 1
#* Visualizza una matrice 10x10 du vendite mensili per prodotto: aggiunti annotazioni dinamiche
#e market automatici>90

#crea matrice casuale
    #Esempio 1

if False:
    # Creo una matrice sintetica
    data = np.random.randint(0, 100, (10,10))
    print(data)
    fig, ax = plt.subplots(figsize=(8,6))
    cax = ax.matshow(data, cmap="viridis")

    # Aggiungo annotazioni dinamiche
    for i in range(data.shape[0]):  #shape[0] restituisce il numero di righe
        for j in range(data.shape[1]): #shape][1] restituisce il numero di colonne
            ax.text(j, i, str(data[i, j]), va='center', ha='center', color='white')
            if data[i,j]>90:
                ax.text(j, i, f"({str(data[i, j])})", va='center', ha='center', color='white')
    plt.colorbar(cax)
    ax.set_title("Heatmap con annotazioni dinamiche")
    plt.show()

if True:

    # Per ripetibilità
    np.random.seed(42)

    # 1) Creo 5 variabili casuali (100 osservazioni)
    n = 10
    df = pd.DataFrame(
        np.random.randn(n, 5),
        columns=["Var1", "Var2", "Var3", "Var4", "Var5"]
    )
    print(df)
    # 2) Matrice di correlazione (Pearson di default)
    corr = df.corr()
    print(corr)

    # 3) Heatmap con matshow
    fig, ax = plt.subplots(figsize=(7, 6))
    cax = ax.matshow(corr.values, cmap="viridis", vmin=-1, vmax=1)

    # Etichette assi
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="left")
    ax.set_yticklabels(corr.index)

    # 4) Testi automatici dentro le celle
    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", va="center", ha="center", color="white")

    plt.colorbar(cax)
    ax.set_title("Heatmap correlazione (5 variabili casuali)")
    plt.show()




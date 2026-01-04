
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns

if True:
    #Esempio 1

    # Creo una matrice sintetica
    data = np.random.randint(0, 100, (6,6))
    print(data)
    fig, ax = plt.subplots(figsize=(8,6))
    cax = ax.matshow(data, cmap="viridis")

    # Aggiungo annotazioni dinamiche
    for i in range(data.shape[0]):  #shape[0] restituisce il numero di righe
        for j in range(data.shape[1]): #shape][1] restituisce il numero di colonne
            ax.text(j, i, str(data[i, j]), va='center', ha='center', color='white')

    plt.colorbar(cax)
    ax.set_title("Heatmap con annotazioni dinamiche")
    plt.show()


if False:
    #Esempio 2
    #from sklearn.metrics import confusion_matrix
    #import seaborn as sns

    y_true = [0, 1, 2, 2, 0, 1, 1, 0]
    y_pred = [0, 2, 1, 2, 0, 1, 1, 0]

    cm = confusion_matrix(y_true, y_pred)
    print(cm)
    fig, ax = plt.subplots(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)

    ax.set_title("Matrice di confusione con testi automatici")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    plt.show()

if False:
    #Esempio 3
    data = np.random.randint(0, 100, (8,8))
    print(data)
    fig, ax = plt.subplots(figsize=(8,6))
    cax = ax.matshow(data, cmap="coolwarm")

    # Marker automatici: evidenzio valori > 80
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j] > 80:
                ax.plot(j, i, marker="o", color="black", markersize=10, fillstyle="none")

    plt.colorbar(cax)
    ax.set_title("Heatmap con marker automatici su valori critici")
    plt.show()


if False:
    #Esempio 4

    data = np.random.randint(0, 100, (5,5))
    print(data)
    fig, ax = plt.subplots(figsize=(6,6))
    cax = ax.matshow(data, cmap="plasma")
    plt.colorbar(cax)

    # Funzione per annotazioni interattive
    annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="yellow", alpha=0.8),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(event):
        if event.inaxes == ax:
            x, y = int(event.xdata + 0.5), int(event.ydata + 0.5)
            if 0 <= x < data.shape[1] and 0 <= y < data.shape[0]:
                annot.xy = (x, y)
                annot.set_text(f"Valore: {data[y,x]}")
                annot.set_visible(True)
                fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", update_annot)
    ax.set_title("Heatmap con annotazioni interattive")
    plt.show()
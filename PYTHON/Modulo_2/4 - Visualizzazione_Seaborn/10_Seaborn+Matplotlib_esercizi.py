# Esercizio 1
# Creare un overlay di istogramma + KDE per un dataset reale, personalizzando bin, colori e trasparenza.

import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")
plt.figure(figsize=(8,5))

sns.histplot(tips["total_bill"],bins=20,kde=True, color="skyblue",alpha=0.5, edgecolor="black")

plt.title("Overlay di istogramma + KDE di total_bill")
plt.xlabel("Total Bill")
plt.ylabel("Frequenza")
plt.show()

# Esercizio 2
# Costruire un plot combinato violin + swarm per confrontare almeno tre gruppi, modificando palette e dimensione dei punti.

plt.figure(figsize=(10,6))

sns.violinplot(
    data=tips,
    x="day",
    y="total_bill",
    palette="Pastel1",
    inner=None
)

sns.swarmplot(
    data=tips,
    x="day",
    y="total_bill",
    color="k",
    size=5,
    alpha=0.7
)

plt.title("Violin + Swarm per Total Bill per giorno")
plt.show()

# Esercizio 3
# Creare una Heatmap con overlay di contour per evidenziare aree di massimo e minimo valore.

import numpy as np

# Dataset sintetico 2D
x = tips["total_bill"]
y = tips["tip"]
heatmap, xedges, yedges = np.histogram2d(x, y, bins=30)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.figure(figsize=(8,6))
plt.imshow(heatmap.T, extent=extent, origin='lower', cmap="YlGnBu", alpha=0.7)
plt.colorbar(label="Count")

# Contour
X, Y = np.meshgrid((xedges[1:]+xedges[:-1])/2, (yedges[1:]+yedges[:-1])/2)
plt.contour(X, Y, heatmap.T, colors='k', linewidths=1)
plt.xlabel("Total Bill")
plt.ylabel("Tip")
plt.title("Heatmap con overlay di contour")
plt.show()

# Esercizio 4
# Creare un JointGrid ibrido con scatterplot e KDE marginale, aggiungendo annotazioni o linee di riferimento.

g = sns.JointGrid(data=tips, x="total_bill", y="tip", height=7)
g.plot(sns.scatterplot, sns.kdeplot)
g.ax_joint.axhline(y=tips["tip"].mean(), color='red', linestyle='--', label='Tip medio')
g.ax_joint.axvline(x=tips["total_bill"].mean(), color='blue', linestyle='--', label='Total bill medio')
g.ax_joint.legend()
plt.suptitle("JointGrid scatter + KDE con linee medie", y=1.02)
plt.show()

# Esercizio 5
# Creare una serie temporale con bande personalizzate che rappresentano intervalli di confidenza o deviazione standard.

import pandas as pd

# Dati sintetici
np.random.seed(0)
dates = pd.date_range("2023-01-01", periods=100)
values = np.cumsum(np.random.randn(100))
std_dev = np.random.rand(100)*2

plt.figure(figsize=(10,5))
plt.plot(dates, values, color="blue", label="Serie principale")
plt.fill_between(dates, values - std_dev, values + std_dev, color="blue", alpha=0.2, label="± deviazione standard")
plt.xlabel("Data")
plt.ylabel("Valore")
plt.title("Serie temporale con bande di deviazione standard")
plt.legend()
plt.show()
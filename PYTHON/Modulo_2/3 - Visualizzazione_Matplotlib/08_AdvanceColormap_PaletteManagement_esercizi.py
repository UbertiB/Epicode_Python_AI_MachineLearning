"""
ESERCIZIO 1
Visualizza una matrice 10*10 di vendite mensili per prodotto: aggiunti annotazioni dinamiche 
e market automatici per valori >90
ESERCIZIO 2
Crea una headmap della correlazione tra 5 variabili casuali: usa testi automatici per mostrare
i valori di correlazone
ESERCIZIO 3
Genare una headmap interattiva di dati metereologici (temperatura giornaliere per 7
giorni e 7 citta), in cui al passaggio del mouse compaiono dettagli aggiuntivi
ESERCIZIO 4
Combina annotazioni dinamiche e market automatici per evidenziare simultaneamente valori critici 
e valori estermi
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns


#
#ESERCIZIO 3
#

import plotly.express as px

# 7 giorni
giorni = pd.date_range("2025-12-24", periods=7, freq="D").strftime("%a %d/%m")

# 7 città
citta = ["Milano", "Roma", "Torino", "Napoli", "Bologna", "Firenze", "Venezia"]

# Temperature giornaliere (°C) - esempio coerente, non random
temp = [
    [3,  4,  2,  1,  3,  4,  2],   # Milano
    [10, 11, 9,  8,  10, 12, 9],   # Roma
    [1,  2,  0, -1,  1,  2,  0],   # Torino
    [12, 13, 11, 10, 12, 14, 11],  # Napoli
    [6,  7,  5,  4,  6,  8,  5],   # Bologna
    [7,  8,  6,  5,  7,  9,  6],   # Firenze
    [5,  6,  4,  3,  5,  7,  4],   # Venezia
]

df = pd.DataFrame(temp, index=citta, columns=giorni)

# Heatmap interattiva
fig = px.imshow(
    df,
    labels=dict(x="Giorno", y="Città", color="Temperatura (°C)"),
    aspect="auto"
)

# Dettagli al passaggio mouse
fig.update_traces(
    hovertemplate="Città: %{y}<br>Giorno: %{x}<br>Temp: %{z} °C<extra></extra>"
)

fig.update_layout(title="Heatmap interattiva temperature (7 giorni x 7 città)")
fig.show()

"""

#
#ESERCIZIO 1
#

articoli = ["Art 01", "Art 02", "Art 03", "Art 04", "Art 05", "Art 06", "Art 07", "Art 08", "Art 09", "Art 10"]
mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott"]
# Matrice 10x10 inizializzata a 0
df = pd.DataFrame(0, index=articoli, columns=mesi)
#random su quantita (ora a 0)
df.loc[:,:]=np.random.randint(low=0, high=300, size=df.shape)
#alcuni articoli vendono poco 
df.loc["Art 08":"Art 10", :] = np.random.randint(0, 50, size=(3, 10))
#stagionalità
df[["Giu", "Lug", "Ago"]] = np.random.randint(150, 300, size=(10, 3))

print(df)

fig, ax = plt.subplots(figsize=(8, 4))

#valore minimo/massimo per la scala
vmin=0
vmax=300

img = ax.imshow(df, cmap="viridis", vmin=vmin, vmax=vmax)

# Assi
ax.set_xticks(range(len(mesi)))
ax.set_xticklabels(mesi)
ax.set_yticks(range(len(articoli)))
ax.set_yticklabels(articoli)

ax.set_title("Quantita venduta per articolo/mese")

# Colorbar
cbar = fig.colorbar(img, ax=ax)
cbar.set_label("Qta venduta")

# Valori nelle celle (per pochi articoli)
for i in range(len(articoli)):
    for j in range(len(mesi)):
        ax.text(j, i, df.iloc[i, j], ha="center", va="center", fontsize=9)

plt.tight_layout()
plt.show()


#
#ESERCIZIO 2
#


#supponiamo di avere 50 articoli di cui ho 5 kpi
np.random.seed(0)  # riproducibilità
n_articoli=50
df = pd.DataFrame({
    "Vendite_annue": np.random.randint(50, 1000, n_articoli),
    "Giacenza_media": np.random.randint(10, 500, n_articoli),
    "Rotazione": np.random.uniform(0.5, 12, n_articoli),
    "Copertura_giorni": np.random.randint(5, 180, n_articoli),
    "Movimenti_magazzino": np.random.randint(20, 800, n_articoli)
})
#creo la matrice di correlazione
#quando una variabili cresce, l'altra tende a crescere, scendere, o non c'entra nulla?
corr=df.corr()
print(corr)

fig, ax = plt.subplots(figsize=(7, 5))

img = ax.imshow(corr, cmap="RdBu", vmin=-1, vmax=1)

# Assi
ax.set_xticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha="right")
ax.set_yticks(range(len(corr.index)))
ax.set_yticklabels(corr.index)

# Testi automatici nelle celle
for i in range(corr.shape[0]):
    for j in range(corr.shape[1]):
        ax.text(
            j,
            i,
            f"{corr.iloc[i, j]:.2f}",
            ha="center",
            va="center",
            fontsize=9
        )

# Colorbar
cbar = fig.colorbar(img, ax=ax)
cbar.set_label("Coefficiente di correlazione (Pearson)")

ax.set_title("Heatmap di correlazione tra KPI articoli")

plt.tight_layout()
plt.show()


"""
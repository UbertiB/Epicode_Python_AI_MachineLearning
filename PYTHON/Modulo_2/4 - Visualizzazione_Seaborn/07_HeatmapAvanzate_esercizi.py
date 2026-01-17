"""
ESERCIZIO 1
* Crea una Heatmap tringolare delle correlazioni di un dataset a scelta,
aggiungendo le annotazioni dei p-value

ESERCIZIO 2
* Genera una Clustered Heatmap che mostri i gruppi di variabili simili, modificando la
matrice di distanza e il metodo di collegamento

ESERCIZIO 3
* Costruire una Heatmap di medie e deviazioni standard per un dataset categoriale,
aggiungendo una legenda coerente

ESERCIZIO 4
* Applicare una correzione per i confronti multipli e colorare le celle significative

"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import pearsonr



penguins = sns.load_dataset("penguins").dropna()
num_cols = penguins.select_dtypes(include='number').columns

# Esercizio 1
# Creare una Heatmap triangolare delle correlazioni di un dataset a scelta, aggiungendo le annotazioni dei p-value.

# Calcolo correlazioni e p-value
corr = penguins[num_cols].corr()
pvals = pd.DataFrame(np.zeros((len(num_cols), len(num_cols))), columns=num_cols, index=num_cols)

for i in num_cols:
    for j in num_cols:
        _, p = pearsonr(penguins[i], penguins[j])
        pvals.loc[i,j] = p
        print(p)

# Maschera triangolare superiore
mask = np.triu(np.ones_like(corr, dtype=bool))

plt.figure(figsize=(8,6))
sns.heatmap(
    corr,
    mask=mask,
    annot=pvals.applymap(lambda x: f"{x:.2g}"),
    cmap="coolwarm",
    fmt="",
    cbar_kws={"label": "Correlation"}
)
plt.title("Heatmap triangolare delle correlazioni con p-value")
plt.show()

# Esercizio 2
# Generare una Clustered Heatmap che mostri i gruppi di variabili simili, modificando la metrica di distanza e il metodo di collegamento.

sns.clustermap(
    penguins[num_cols],
    metric="euclidean",   # metrica distanza
    method="ward",        # metodo linkage
    cmap="vlag",
    standard_scale=1,     # normalizza le colonne
    figsize=(8,8)
)
plt.suptitle("Clustered Heatmap delle variabili numeriche", y=1.02)
plt.show()

# Esercizio 3
# Costruire una Heatmap di medie e deviazioni standard per un dataset categoriale, aggiungendo una legenda coerente.

# Creazione pivot table: media e deviazione standard di "bill" per giorno e fascia
tips = sns.load_dataset("tips")
agg_mean = tips.pivot_table(index="day", columns="time", values="total_bill", aggfunc="mean")
agg_std  = tips.pivot_table(index="day", columns="time", values="total_bill", aggfunc="std")

# Combiniamo media e deviazione standard in stringa
annot = agg_mean.round(1).astype(str) + " ± " + agg_std.round(1).astype(str)

plt.figure(figsize=(8,6))
sns.heatmap(
    agg_mean,
    annot=annot,
    fmt="",
    cmap="YlGnBu",
    cbar_kws={"label": "Media totale conto"}
)
plt.title("Heatmap di media e deviazione standard dei total_bill")
plt.show()

# Esercizio 4
# Applicare una correzione per confronti multipli e colorare le celle significative.

from statsmodels.stats.multitest import multipletests

# Usiamo pvals calcolati prima e applichiamo Bonferroni
pvals_flat = pvals.values.flatten()
reject, pvals_corrected, _, _ = multipletests(pvals_flat, method='bonferroni')
reject_matrix = reject.reshape(pvals.shape)

plt.figure(figsize=(8,6))
sns.heatmap(
    corr,
    mask=mask,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    cbar_kws={"label": "Correlation"},
    linewidths=0.5,
    linecolor='gray'
)

# Evidenzia celle significative con bordo spesso
for i in range(len(num_cols)):
    for j in range(i+1, len(num_cols)):
        if reject_matrix[i,j]:
            plt.gca().add_patch(plt.Rectangle((j,i),1,1,fill=False, edgecolor='black', lw=3))

plt.title("Heatmap con correzione Bonferroni e evidenziazione celle significative")
plt.show()
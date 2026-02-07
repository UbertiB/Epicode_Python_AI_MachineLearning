"""
STRIPPPLOT
E' uno scatterplot dove un asse è categoriale (esempio famiglia, fornitore, ecc) e l'altro è numerico
(prezzo, leadtime, ecc). Serve a vedere tutti i punti e non solo un riassunto statistico. 

Lo Stripplot utile per dataset piccoli o medi dove ongi punto ha un significato
I punti potrebbero essere sovrapposti se troppi, in questo caso viene in aiuto  un po di 'jitter' 
(spostamento casuale) lungo l'asse delle categorie per ridurre la sovrapposizione dei punti.
Grafico scatter monodimensionale che dispone i punti lungo un asse, mostra ogni singolo dato evidenziando
valori replicati e variabilità all interno delle categorie.

Stripplot semplice e leggero da visualizzare

Visualizza:
- dispersione, outlier, cluster, differenze tra categorie
- non visualizza densità reale quando hai tantissimi punti sovrapposti (si crea una macchia). In questo caso
  meglio affincare un box/violiplot 
"""

import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

df = pd.DataFrame({
    "fornitore": ["F001","F001","F002","F002","F003","F003","F003","F004"],
    "magazzino": ["MAG1","MAG2","MAG1","MAG2","MAG1","MAG1","MAG2","MAG2"],
    "lead_time_g": [5, 7, 12, 10, 6, 8, 15, 9],
    "giacenza": [120, 80, 40, 55, 200, 180, 20, 60]
})


sns.stripplot(data=df, x="fornitore", y="lead_time_g", jitter=0.25)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# AGGIUNGO HUE

sns.stripplot(data=df, x="fornitore", y="lead_time_g",
              hue="magazzino", dodge=True, jitter=0.25, alpha=0.6)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

#SOVRAPPOSTO A BOXPLOT PER LEGGERE SIA DISTIBUZIONE CHE OUTLIER

sns.boxplot(data=df, x="fornitore", y="lead_time_g", showfliers=False)
sns.stripplot(data=df, x="fornitore", y="lead_time_g",
              color="black", alpha=0.4, jitter=0.25, size=3)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

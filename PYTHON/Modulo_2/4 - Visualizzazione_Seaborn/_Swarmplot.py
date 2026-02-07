"""
SWARMPLOT
E' molto simile a Stripplot ma dispone i punti in modo più intelligente
E' uno scatter 'categoriale' dove i punti vengono spostati lungo l'asse della categoria in modo da 
NON  sovrapporsi. E' il classico effetto 'sciame d'api', visualizza tutti i valori dove si addensano, senza che 
i punti si coprano a vicenda.
Mentro lo striplot mette i punti nella categoria e, se attivi jitter, li 'sparpaglia' in modo casuale
Lo swarmplot sposta i punti con una regola per evitare sovrapposizoini, in questo modo leggi meglio la densità
"""

import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

df = pd.DataFrame({
    "fornitore": ["F001","F001","F002","F002","F003","F003","F003","F004","F004","F004"],
    "magazzino": ["MAG1","MAG2","MAG1","MAG2","MAG1","MAG1","MAG2","MAG1","MAG2","MAG2"],
    "lead_time_g": [5, 7, 12, 10, 6, 8, 15, 9, 11, 14],
    "giacenza": [120, 80, 40, 55, 200, 180, 20, 60, 90, 30]
})


sns.swarmplot(data=df, x="fornitore", y="lead_time_g", size=4)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

#combinato al boxplot 

import seaborn as sns
import matplotlib.pyplot as plt

sns.boxplot(data=df, x="fornitore", y="lead_time_g", showfliers=False)
sns.swarmplot(data=df, x="fornitore", y="lead_time_g", size=3, alpha=0.6)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

#sottocategorie con hue

sns.swarmplot(data=df, x="fornitore", y="lead_time_g", hue="magazzino", dodge=True, size=3)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


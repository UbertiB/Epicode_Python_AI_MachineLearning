"""
VIOLINPLOT
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)

giorni=["lun","mar","mer","gio","ven"]
fasce=["Mattina","Pomeriggio","Sera"]
data={
    "giorno":np.random.choice(giorni,300),
    "fascia":np.random.choice(fasce,300),
    "soddisfazione":np.concatenate([
        np.random.normal(7,1,100),
        np.random.normal(5,1.5,100),
        np.random.normal(6,0.8,100)
    ])
}
df=pd.DataFrame(data)

sns.set_theme(style="whitegrid", palette="tab10")

#
# 1) VIOLINPLOT semplice
#
sns.violinplot(y="soddisfazione", data=df, inner="quartile")
plt.title("Violin: distribuzione complessiva (VIOLIN base)")
plt.show()

#
# 2) VIOLINPLOT per una categoria (giorno)
#
sns.violinplot(x="giorno", y="soddisfazione", data=df, inner="quartile")
plt.title("Violin: soddisfazione per giorno")
plt.show()

#
# 3) VIOLINPLOT per una categoria con ordine controllato (giorno)
#

ordine_giorni = ["lun", "mar", "mer", "gio", "ven"]

sns.violinplot( x="giorno", y="soddisfazione",data=df, order=ordine_giorni, inner="quartile")
plt.title("Violin per giorno (ordine corretto)")
plt.show()

#
# 4) VIOLINPLOT per una categoria (fascia)
#
sns.violinplot( x="fascia", y="soddisfazione",data=df,inner="quartile")
plt.title("Violin: soddisfazione per fascia")
plt.show()

#
# 5) VIOLINPLOT doppia categoria (con HUE)
#
ordine_giorni = ["lun", "mar", "mer", "gio", "ven"]
sns.violinplot(x="giorno", y="soddisfazione",hue="fascia",data=df,inner="quartile",order=ordine_giorni)
plt.title("Violin: giorno e fascia (inner=quartile)")
plt.show()

#
# 6) VIOLINPLOT SPLIT (se hue ha 2 livelli)
#

#
# 7) VIOLINPLOT leggibile con riduzione rumore
#
sns.violinplot( x="fascia", y="soddisfazione", data=df,inner="quartile",cut=0)
plt.title("Violin per fascia (cut=0: niente estensioni oltre i dati)")
plt.show()

#
# 8) VIOLINPLOT DECISIONALE (con confronto tra giorni dentro fascia)
#
sns.violinplot(x="fascia", y="soddisfazione",hue="giorno",data=df,inner="quartile",cut=0)
plt.title("Violin: fascia con dettaglio per giorno")
plt.show()




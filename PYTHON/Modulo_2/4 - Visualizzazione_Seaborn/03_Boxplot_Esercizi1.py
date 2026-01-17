"""
il BOXPLOT non mostra medie, mostra distribuzioni.
E' il grafico giusto se:
- confronta tra gruppi
- KPI operativi
- smascherare decisioni basate solo sulla media
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(42)

giorni = ["lun", "mar", "mer", "gio", "ven"]
fasce = ["Mattina", "Pomeriggio", "Sera"]

data = {
    "giorno": np.random.choice(giorni, 300),
    "fascia": np.random.choice(fasce, 300),
    "soddisfazione": np.concatenate([
        np.random.normal(7, 1, 100),
        np.random.normal(5, 1.5, 100),
        np.random.normal(6, 0.8, 100)
    ])
}

df = pd.DataFrame(data)

sns.set_theme(style="whitegrid", palette="tab10")

#
# 1) BOXPLOT semplice
#
sns.boxplot(y="soddisfazione", data=df)
plt.title("Distribuzione complessiva della soddisfazione (BOXPLOT semplice)")
plt.show()

#
# 2) BOXPLOT per una categoria
#
sns.boxplot(x="giorno", y="soddisfazione", data=df)
plt.title("Soddisfazione per giorno (BOXPLOT per categoria)")
plt.show()

#
# 3) BOXPLOT con ordine controllato
#
ordine_giorni = ["lun", "mar", "mer", "gio", "ven"]

sns.boxplot(x="giorno",y="soddisfazione",data=df,order=ordine_giorni)
plt.title("Soddisfazione per giorno (BOXPLOT oridne controllato)")
plt.show()

#
# 4) BOXPLOT con un'altra categoria
#
sns.boxplot(x="fascia", y="soddisfazione", data=df)
plt.title("Soddisfazione per fascia oraria (BOXPLOT per categoria)")
plt.show()

#
# 5) BOXPLOT con doppia categorizzazione (con hue)
#
sns.boxplot(x="giorno",y="soddisfazione",hue="fascia",data=df)
plt.title("Soddisfazione per giorno e fascia (BOXPLOT con HUE)")
plt.show()

#
# 6) BOXPLOT leggibile (best practice)
#
sns.boxplot(x="giorno",y="soddisfazione",hue="fascia",data=df,showfliers=False)
plt.title("Soddisfazione per giorno e fascia (senza outlier)")
plt.legend(title="Fascia")
plt.show()

#
# 7) BOXPLOT orientato al confronto decisionale
#
sns.boxplot(x="fascia",y="soddisfazione",hue="giorno",data=df)
plt.title("Confronto fasce dettaglio per giorno")
plt.show()

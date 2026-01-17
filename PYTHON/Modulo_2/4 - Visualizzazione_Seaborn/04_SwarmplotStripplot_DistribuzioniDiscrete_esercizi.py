"""
ESERCIZIO 1
- Creare uno stripplot della soddisfazione dei clienti suddivisa per giorno e fascia, utilizzando
colori distinte per fascia e regolando il jitter per migliorare leggibilità

ESERCIZIO 2
- Generare uno swarmplot della stessa distribuzione, confrontando i risultati con lo stripplot
e osservando differenze nella disposizione dei punti

ESERCIZIO 3
- Combinare swarmplot con boxplot per evidenziare mediana e quartili insieme ai singoli punti,
personalizzando colori e dimensione dei marker

ESERCIZIO 4
- Sperimentare con diverse palette di colori e orientamenti dei punti per rendere i grafici più
leggibili e adatti a un report professionale

"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

# Simulazione dataset
np.random.seed(42)
giorni = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven']
fasce = ['Mattina', 'Pomeriggio', 'Sera']
n_samples = 200

df = pd.DataFrame({
    'giorno': np.random.choice(giorni, size=n_samples),
    'fascia': np.random.choice(fasce, size=n_samples),
    'soddisfazione': np.random.randint(1, 11, size=n_samples)
})
ordine_fascia=['Mattina', 'Pomeriggio', 'Sera']
ordine_giorni= ['Lun', 'Mar', 'Mer', 'Gio', 'Ven']
fascia_colors = {
    "Mattina": "#A1C9F4",      # azzurrino
    "Pomeriggio": "#FFB482",   # arancino
    "Sera": "#8DE5A1"          # verdino
}


fig,axes=plt.subplots(2,2, figsize=(14,8),sharey=True)

"""
ESERCIZIO 1
- Creare uno stripplot della soddisfazione dei clienti suddivisa per giorno e fascia, utilizzando
colori distinte per fascia e regolando il jitter per migliorare leggibilità
"""

sns.stripplot(data=df,x="giorno",y="soddisfazione",hue="fascia", hue_order=ordine_fascia, jitter=0.2, palette=fascia_colors, size=5,ax=axes[0,0])
axes[0,0].set_title("Stripplot: Soddisfazione per giorno e fascia")
axes[0,0].set_xlabel("Giorni")
axes[0,0].set_ylabel("Soddisfazione")

"""
ESERCIZIO 2
- Generare uno swarmplot della stessa distribuzione, confrontando i risultati con lo stripplot
e osservando differenze nella disposizione dei punti

"""

sns.swarmplot(data=df,x="giorno",y="soddisfazione",hue="fascia", hue_order=ordine_fascia, palette=fascia_colors, size=5,ax=axes[0,1])
axes[0,1].set_title("Swarmplot: Soddisfazione per giorno e fascia")
axes[0,1].set_xlabel("Giorni")
axes[0,1].set_ylabel("Soddisfazione")

"""
ESERCIZIO 3
- Combinare swarmplot con boxplot per evidenziare mediana e quartili insieme ai singoli punti,
personalizzando colori e dimensione dei marker
"""
sns.swarmplot(data=df,x="giorno",y="soddisfazione",hue="fascia", hue_order=ordine_fascia, palette=fascia_colors, size=5,ax=axes[1,0])
sns.boxplot(data=df,x="giorno",y="soddisfazione",hue="fascia", hue_order=ordine_fascia,palette="tab10",ax=axes[1,0])
axes[0,1].set_title("Swarmplot combinato boxplot: Soddisfazione per giorno e fascia")
axes[0,1].set_xlabel("Giorni")
axes[0,1].set_ylabel("Soddisfazione")

"""
ESERCIZIO 4
- Sperimentare con diverse palette di colori e orientamenti dei punti per rendere i grafici più
leggibili e adatti a un report professionale
"""

sns.swarmplot(data=df,x="giorno",y="soddisfazione",hue="fascia", hue_order=ordine_fascia, palette=fascia_colors, size=6, alpha=0.8,ax=axes[1,1])
sns.boxplot(data=df,x="giorno",y="soddisfazione",hue="fascia", hue_order=ordine_fascia,palette=fascia_colors,fliersize=0,dodge=True,ax=axes[1,1])
axes[1,1].set_title("Swarmplot combinato boxplot: Soddisfazione per giorno e fascia")
axes[1,1].set_xlabel("Giorni")
axes[1,1].set_ylabel("Soddisfazione")


# --- LEGENDA UNICA ---
handles, labels = axes[0,0].get_legend_handles_labels()

# 2) Rimuovo le legende SOLO dai subplot fascia (non da quello con hue="giorno")
for a in [axes[0,0], axes[0,1],axes[1,1]]:   # aggiungi qui gli altri subplot che usano hue="fascia"
    leg = a.get_legend()
    if leg is not None:
        leg.remove()

# Deduplica (se serve)
uniq = dict(zip(labels, handles))

fig.legend(
    uniq.values(),
    uniq.keys(),
    title="Fascia oraria",
    loc="lower center",
    ncol=len(uniq),
    frameon=True
)

fig.suptitle("Soddisfazione per giorno e fascia: Boxplot vs Violinplot", y=1.02)
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

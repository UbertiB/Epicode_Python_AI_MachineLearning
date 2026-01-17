"""
ESERCIZIO 1
Crea un boxplot personalizzato della soddisfazione dei clienti suddivisa per fascia oraria
e giorno, usando palette di colori distinte e linee spesse per i box

ESERCIZIO 2
Genera un violnplot avanzato che mostri la  densità dei punteggi di soddisfazione per ogni
giorno, indludendo quartili interni e differenze tra fascia orarie.

ESERCIZIO 3
Confrontare categorie multiple usante hue e valute le differenze di distribuzione tra fascie
orarie, aggiungendo leggenda chiara e titolo descrittivo

ESERCIZIO 4
Crea un grafico combinato violinplot+boxplot personalizzando trasparenza, colori e larghezza
dei box per rendere immediata la lettura delle informazioni principali
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#punteggio di soddisfazione dei clienti diviso per giorno, fascia oraria
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

sns.set_theme(style="whitegrid")
ordine_giorni=["lun","mar","mer","gio","ven"]
ordine_fascia=["Mattina","Pomeriggio","Sera"]
fascia_colors = {
    "Mattina": "#A1C9F4",      # azzurrino
    "Pomeriggio": "#FFB482",   # arancino
    "Sera": "#8DE5A1"          # verdino
}

fig,axes=plt.subplots(2,2, figsize=(14,8),sharey=True)
"""
ESERCIZIO 1
Crea un boxplot personalizzato della soddisfazione dei clienti suddivisa per fascia oraria
e giorno, usando palette di colori distinte e linee spesse per i box
"""
sns.boxplot(data=df,x="giorno",y="soddisfazione",hue="fascia", hue_order=ordine_fascia, palette=fascia_colors,order=ordine_giorni, linewidth=2,ax=axes[0,0])
axes[0,0].set_title("Boxplot: Soddisfazione per giorno e fascia oraria")
axes[0,0].set_xlabel("Giorni")
axes[0,0].set_ylabel("Soddisfazione")

"""
ESERCIZIO 2
Genera un violnplot avanzato che mostri la  densità dei punteggi di soddisfazione per ogni
giorno, indludendo quartili interni e differenze tra fascia orarie.
"""
sns.violinplot(data=df,x="giorno",y="soddisfazione",order=ordine_giorni,inner="quartile", cut=0,hue="fascia",hue_order=ordine_fascia,palette=fascia_colors,ax=axes[0,1])
axes[0,1].set_title("Violinplot: soddisfazione per giorno e fasce")
axes[0,1].set_xlabel("Giorni")
axes[0,1].set_ylabel("") #già presente nel boxplot

"""
ESERCIZIO 3
Confrontare categorie multiple usando hue e valutare le differenze di distribuzione tra fascie
orarie, aggiungendo leggenda chiara e titolo descrittivo
"""
sns.boxplot(data=df,x="fascia",y="soddisfazione",hue="giorno", hue_order=ordine_giorni,order=["Mattina", "Pomeriggio", "Sera"],palette="tab10",ax=axes[1,0])
axes[1,0].set_title("Confronto fasce orarie: distribuzione della soddisfazione per giorno")
axes[1,0].set_xlabel("Fascia oraria")
axes[1,0].set_ylabel("Soddisfazione")

"""
ESERCIZIO 4
Crea un grafico combinato violinplot+boxplot personalizzando trasparenza, colori e larghezza
dei box per rendere immediata la lettura delle informazioni principali
"""
df_ps = df[df["fascia"].isin(["Pomeriggio", "Sera"])].copy()
#ordine categorico
df_ps["fascia"] = pd.Categorical(df_ps["fascia"],categories=["Pomeriggio", "Sera"],ordered=True)

sns.violinplot(data=df_ps,x="giorno",y="soddisfazione",order=ordine_giorni, hue="fascia",hue_order=["Pomeriggio","Sera"], split=True, palette=fascia_colors,alpha=0.6,cut=0, inner=None,ax=axes[1,1])
sns.boxplot(data=df_ps,x="giorno",y="soddisfazione",order=ordine_giorni,hue="fascia",hue_order=["Pomeriggio","Sera"], palette=fascia_colors,width=0.2,fliersize=3,linewidth=2,dodge=True,ax=axes[1,1])
axes[1,1].set_title("Boxplot sovrapposto a violinplot")
axes[1,1].set_xlabel("Giorno")
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


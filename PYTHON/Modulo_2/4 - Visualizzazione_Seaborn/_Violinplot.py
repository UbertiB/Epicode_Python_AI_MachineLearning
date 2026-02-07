"""
VIOLINPLOT
Il Violinplot è un boxplot con dentro la forma della distribuzione.
Mantiene l'idea del confronto tra gruppi, ma invce della sola scatola mostra anche la densità (di solito
una KDE) lungo l'asse dei valori.
E' importantissimo quando si sospetta che dentro lo stessa quartile ci siano popolazioni diverse.
Proprio perchè usa KDE eredita le sue trappole. La 'pancia' del violino dipende dalla bandwidth e dalla normalizzazione.
Mostra:
- Larghezza del violino a una certa quota (y): quanto è densa la distribuzione li, cioè dove si concentrano i valori
- Puo includere mediano e quartili
- Ti fa vedere multimodalità: due pance separate:due gruppi interni 

Quando usarlo:
- Leadtime fornitore: vede se un fornitore ha due modalità (pance) esempio consegna standard e spedizioni speciali.
- Margine per famiglia: scoprire se hai due fasce di marginalità dentro la stessa famiglia
- Ritardi consegna per vettore o reparto: distingue 
  'quasi sempre puntale ma a volte disastro' vs 'sempre un po in ritardo'
- Tempi ciclo per macchina: capire se hai set-up diversi o mix di prodotti
"""

#
# BOXPLOT VS VIOLIPLOT (lead time fornitore)
#

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(7)

n = 900
forn = np.random.choice(["Fornitore_A", "Fornitore_B", "Fornitore_C"], size=n, p=[0.45, 0.35, 0.20])

lead = np.empty(n)
lead[forn=="Fornitore_A"] = np.random.normal(loc=8,  scale=1.2, size=(forn=="Fornitore_A").sum())
lead[forn=="Fornitore_B"] = np.random.normal(loc=12, scale=1.5, size=(forn=="Fornitore_B").sum())

# Fornitore C: distribuzione "mista" (due modalità)
c_idx = (forn=="Fornitore_C")
nC = c_idx.sum()
leadC1 = np.random.normal(loc=8.5,  scale=1.0, size=nC//2)   # modalità veloce
leadC2 = np.random.normal(loc=13.0, scale=1.2, size=nC - nC//2) # modalità lenta
lead[c_idx] = np.concatenate([leadC1, leadC2])

lead = np.clip(lead, 0.2, None)
df = pd.DataFrame({"fornitore": forn, "leadtime_g": lead})

plt.figure(figsize=(8,4))
sns.boxplot(data=df, x="fornitore", y="leadtime_g")
plt.title("Boxplot: confronto robusto ma non vedi la forma completa")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,4))
sns.violinplot(data=df, x="fornitore", y="leadtime_g", inner="quartile", cut=0)
plt.title("Violinplot: vedi anche multimodalità (due pance)")
plt.tight_layout()
plt.show()
# il fornitore C il violino mostra due pance: due processi

#
# VIOLINPLOT + PUNTI 
#
#(punti=dati veri)
plt.figure(figsize=(8,4))
sns.violinplot(data=df, x="fornitore", y="leadtime_g", inner=None, cut=0)
sns.stripplot(data=df, x="fornitore", y="leadtime_g", alpha=0.25, jitter=0.25, size=3)
plt.title("Violinplot + stripplot: densità stimata + dati reali")
plt.tight_layout()
plt.show()

#
# VARIABILE A CODA LUNGA, USO DEL LOG
#
#come per il boxplot importo o quantità sul violino senza log diventano spesso innutili
np.random.seed(7)
small = np.random.lognormal(mean=4.0, sigma=0.6, size=700)
big   = np.random.lognormal(mean=6.0, sigma=0.4, size=300)
importo = np.concatenate([small, big])

canale = np.array(["B2B"]*700 + ["B2C"]*300)
df2 = pd.DataFrame({"canale": canale, "importo_ordine": importo})
df2["log_importo"] = np.log10(df2["importo_ordine"])

plt.figure(figsize=(8,4))
sns.violinplot(data=df2, x="canale", y="log_importo", inner="quartile", cut=0)
plt.title("Violinplot su log10(importo): confronto chiaro tra canali")
plt.tight_layout()
plt.show()



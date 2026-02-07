
"""
BOXPLOT
Il boxplot (diagramma a scatola e baffi) è un grafico 'da lavoro'. Serve per riassumere una distrubuzione
in modo robusto, soprattutto quando hai outlier e code lunghe.
Mostra:
- La linea dentro la scatola: mediana (50.percentile). E' il 'valore tipico'.
  Se la mediana non è al centro della scatola ed i baffi sono sbilanciati, non ho simetriaa
- Bordo basso della scatole e bordo alto della scatola: 1.quartile (25.percentile) e 3.quartile (75.percentile)
- Altezza della scatola: IQR=Q3-Q1 (intervallo interquartile). Misura dispersione robusta. 
  IQR piccolo=processo stabile
  IQR grande=processo variabile
- I baffi: di solito arrivano file a Q1-1.5/QR e Q3+1.5/QR
- Punti fuori i baffi: outlier, non significa errore, significa valore rare da approfondire
  Se ho tantissimi baffi spesso vuol dire che si stanno mischiando processi diversi o dati sporchi

Il boxplot riassume, ma i punti ti dicono se hai cluster o “gradini”.  
"""



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
lead[forn=="Fornitore_C"] = np.random.normal(loc=10, scale=3.0, size=(forn=="Fornitore_C").sum())
lead = np.clip(lead, 0.2, None)

df = pd.DataFrame({"fornitore": forn, "leadtime_g": lead})

plt.figure(figsize=(8,4))
sns.boxplot(data=df, x="fornitore", y="leadtime_g")
plt.title("Lead time per fornitore (boxplot)")
plt.tight_layout()
plt.show()
# Se C ha scatola alta e tanti outlier: processo instasbile o mix di condizioni (urgenze, articoli speciali, ecc)
# Se A ha scatola bassa e pochi outlier: fornitore prevedibile, ottimo per mrp e scorte strette
# Se B media alta: tempi medi lunghi, da gestire con leadtime o safety stock

#
# BOXPLOT +STRIPPLOT
#
plt.figure(figsize=(8,4))
sns.boxplot(data=df, x="fornitore", y="leadtime_g")
sns.stripplot(data=df, x="fornitore", y="leadtime_g", alpha=0.25, jitter=0.25, size=3)
plt.title("Boxplot + punti: controllo struttura (cluster, gradini, outlier veri)")
plt.tight_layout()
plt.show()
# i punti sono importanti per capire se hai lead-time a step (5,10,15 giorni), il boxplot da solo può nascondere
# che sono valori discreti


#
# BOXPLOT con scala LOG
#
np.random.seed(7)
small = np.random.lognormal(mean=4.0, sigma=0.6, size=800)
big   = np.random.lognormal(mean=6.0, sigma=0.4, size=200)
importo = np.concatenate([small, big])

canale = np.array(["B2B"]*700 + ["B2C"]*300)
df2 = pd.DataFrame({"canale": canale, "importo_ordine": importo})
df2["log_importo"] = np.log10(df2["importo_ordine"])

plt.figure(figsize=(8,4))
sns.boxplot(data=df2, x="canale", y="importo_ordine")
plt.title("Boxplot importo su scala originale (spesso poco leggibile)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,4))
sns.boxplot(data=df2, x="canale", y="log_importo")
plt.title("Boxplot su log10(importo): confronti molto più chiari")
plt.tight_layout()
plt.show()
#importi e quantità hanno quasi sempre code lunga, boxplot su scale normale schiaccia tutto.
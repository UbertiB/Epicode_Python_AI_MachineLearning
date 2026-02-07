"""
KDE (Kernel Density Estimation) 
è un modo “smussato” di stimare la distribuzione di una variabile continua. 
Invece di contare barre come un istogramma, somma tante “campanelle” centrate su ogni dato. 
Il risultato è una curva di densità: non mostra gli importi “presenti”, mostra dove i valori sono più probabili. 
L'area sotto la curva vale 1 (non è un conteggio)

KDE è bellissima per capire la forma della distribuzione, ma è facilissima da manipolare involontariamente 
con il parametro più importante, la bandwidth (larghezza del kernel). 
Troppo piccola: vedi mille picchi finti. Troppo grande: appiattisci e perdi multimodalità (più popolazioni)

"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(7)

#
# KDE+ ISTROGRAMMA
#

# Simulazione "ERP-like": importi con due popolazioni (piccoli + grandi), coda lunga
n1, n2 = 800, 200
small = np.random.lognormal(mean=4.0, sigma=0.45, size=n1)   # ordini piccoli
big   = np.random.lognormal(mean=6.0, sigma=0.35, size=n2)   # ordini grandi
importo = np.concatenate([small, big])

df = pd.DataFrame({"importo_ordine": importo})

plt.figure(figsize=(8,4))
sns.histplot(df["importo_ordine"], bins=40, stat="density", kde=False,color="blue")
sns.kdeplot(df["importo_ordine"], bw_adjust=1.0,color="red")
plt.title("Istogramma + KDE (bw_adjust=1.0)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,4))
sns.kdeplot(df["importo_ordine"], bw_adjust=0.4, label="bw_adjust=0.4")
sns.kdeplot(df["importo_ordine"], bw_adjust=1.0, label="bw_adjust=1.0")
sns.kdeplot(df["importo_ordine"], bw_adjust=2.2, label="bw_adjust=2.2")
plt.legend()
plt.title("Effetto della bandwidth: sotto-smussata vs sovra-smussata")
plt.tight_layout()
plt.show()


#
# TRASFORMAZIONI (LOG) per code lunghe
#
#Per importi, tempi, quantità: spesso la scala log rende la distribuzione leggibile e la kde più sensata.
#applicando il log, può capitare di vedere dati che sensa non erano visibili. Valori assurdi saltano fuori come gobbe isolate.
df["log_importo"] = np.log10(df["importo_ordine"])  #LOG

plt.figure(figsize=(8,4))
sns.kdeplot(df["importo_ordine"], bw_adjust=1.0)
plt.title("KDE su scala originale (spesso schiacciata dalla coda)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,4))
sns.kdeplot(df["log_importo"], bw_adjust=1.0)
plt.title("KDE su log10(importo): forma più interpretabile")
plt.tight_layout()
plt.show()

#KED per GRUPPI (segmentazione)

np.random.seed(7)

# Simuliamo 3 fornitori con lead time diversi (e uno con grande variabilità)
n = 900
forn = np.random.choice(["Fornitore_A", "Fornitore_B", "Fornitore_C"], size=n, p=[0.45, 0.35, 0.20])

lead = np.empty(n)
lead[forn=="Fornitore_A"] = np.random.normal(loc=8,  scale=1.2, size=(forn=="Fornitore_A").sum())
lead[forn=="Fornitore_B"] = np.random.normal(loc=12, scale=1.5, size=(forn=="Fornitore_B").sum())
lead[forn=="Fornitore_C"] = np.random.normal(loc=10, scale=3.0, size=(forn=="Fornitore_C").sum())
lead = np.clip(lead, 0.1, None)

df2 = pd.DataFrame({"fornitore": forn, "leadtime_g": lead})

plt.figure(figsize=(9,4))
sns.kdeplot(data=df2, x="leadtime_g", hue="fornitore", common_norm=False, bw_adjust=1.0)
plt.title("KDE per fornitore: confronti reali (common_norm=False)")
plt.tight_layout()
plt.show()

#Nota pratica: common_norm=False evita che un gruppo grande “schiacci” i piccoli. 
#È un dettaglio da esperto che cambia l’interpretazione

#KDE 2D (distribuzioni congiunte) per vedere cluster e pattern
#Quando hai due variabili continue, la KDE 2D mostra “dove vive” la massa dei dati. 
# In ERP: quantità vs lead time, importo vs sconto, ritardo vs resi.

np.random.seed(7)

# Simuliamo una relazione: lotti grandi richiedono più lead time, ma con due modalità (standard/urgenza)
n = 1200
qta = np.random.lognormal(mean=3.2, sigma=0.6, size=n)
modalita = np.random.choice(["standard", "urgenza"], size=n, p=[0.85, 0.15])

lead = 6 + 0.9*np.log(qta) + np.random.normal(0, 0.9, size=n)
lead[modalita=="urgenza"] -= 2.0  # urgenza spinge lead time più basso (ma costa altrove)
lead = np.clip(lead, 0.2, None)

df3 = pd.DataFrame({"qta": qta, "leadtime_g": lead, "modalita": modalita})
df3["log_qta"] = np.log10(df3["qta"])

plt.figure(figsize=(7,5))
sns.kdeplot(data=df3, x="log_qta", y="leadtime_g", fill=True, levels=20, thresh=0.05)
plt.title("KDE 2D: densità congiunta (log10(qta) vs lead time)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(7,5))
sns.scatterplot(data=df3.sample(500, random_state=7), x="log_qta", y="leadtime_g", hue="modalita", alpha=0.6)
plt.title("Scatter di supporto (non fidarti della sola KDE 2D)")
plt.tight_layout()
plt.show()

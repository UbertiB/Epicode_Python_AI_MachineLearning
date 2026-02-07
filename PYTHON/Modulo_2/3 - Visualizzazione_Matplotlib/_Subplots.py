"""
SUBPLOTS
Subplots utilizzato per avere più grafici nella stessa figura.
Si usa quando vuoi confrontare metriche sullo stesso dataset, senza aprire diverse finestre

Quando la dashboard deve avere un layout non uniforme utilizzare GRIDSPEC
"""

#ESEMPIO 1 1 RIGA 2 COLONNE

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 13)
vendite = np.array([10, 12, 9, 14, 15, 13, 16, 18, 17, 19, 22, 20])
margine = np.array([2.0, 2.2, 1.8, 2.5, 2.6, 2.4, 2.7, 2.9, 2.8, 3.0, 3.2, 3.1])

fig, ax = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)

ax[0].plot(x, vendite, marker="o")
ax[0].set_title("Vendite per mese")
ax[0].set_xlabel("Mese")
ax[0].set_ylabel("Quantità")

ax[1].plot(x, margine, marker="o")
ax[1].set_title("Margine per mese")
ax[1].set_xlabel("Mese")
ax[1].set_ylabel("Margine")

plt.show()

#ESEMPIO 2 2x2 (CLASSICO CRUSCOTTO KPI)

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
x = np.arange(1, 31)
vendite = np.random.poisson(20, size=30)
resi = np.random.binomial(5, 0.2, size=30)
giacenza = np.cumsum(np.random.randint(-3, 4, size=30)) + 200
lead_time = np.random.normal(7, 1.2, size=30)

fig, ax = plt.subplots(2, 2, figsize=(10, 6), constrained_layout=True)

ax[0, 0].plot(x, vendite)
ax[0, 0].set_title("Vendite giornaliere")

ax[0, 1].bar(x, resi)
ax[0, 1].set_title("Resi giornalieri")

ax[1, 0].plot(x, giacenza)
ax[1, 0].set_title("Giacenza (simulata)")

ax[1, 1].hist(lead_time, bins=10)
ax[1, 1].set_title("Distribuzione lead time")

for a in ax.flat:
    a.set_xlabel("Giorno" if a in [ax[0,0], ax[0,1], ax[1,0]] else "")
    a.grid(True, alpha=0.3)

plt.show()

#ESEMPIO 3 ASSI CONDIVISI

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 13)
a = np.array([100, 120, 90, 140, 150, 130, 160, 180, 170, 190, 220, 200])
b = np.array([80, 95, 85, 110, 115, 100, 120, 125, 118, 130, 140, 135])

fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True, constrained_layout=True)

ax[0].plot(x, a, marker="o")
ax[0].set_title("Serie A")

ax[1].plot(x, b, marker="o")
ax[1].set_title("Serie B")
ax[1].set_xlabel("Mese")

plt.show()



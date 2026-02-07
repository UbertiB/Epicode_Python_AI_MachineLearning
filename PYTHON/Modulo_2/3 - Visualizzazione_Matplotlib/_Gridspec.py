"""
GRIDSPEC
E' un modo per fare layout di subplot, in modo più potente rispetto a subplots (che permette
una griglia tutta uguale).

Gridspec crea una griglia logica e poi prendi porzionin di griglia ai vari assi (Axes).
"""

#ESEMPIO 1 GRIGLIA  2x2 identica (possibile anche con subplots)

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 5), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

ax1.set_title("0,0")
ax2.set_title("0,1")
ax3.set_title("1,0")
ax4.set_title("1,1")

plt.show()

#ESERCIZIO 2 GRIGLIA NON UNIFORME (due piccoli a destra, uno grande a sinistra)

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 13)
vendite = np.array([10, 12, 9, 14, 15, 13, 16, 18, 17, 19, 22, 20])
margine = np.array([2, 2.2, 1.8, 2.5, 2.6, 2.4, 2.7, 2.9, 2.8, 3.0, 3.2, 3.1])

fig = plt.figure(figsize=(10, 6), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax_main = fig.add_subplot(gs[:, 0])  # grande: 2 righe x 1 colonna
ax_top = fig.add_subplot(gs[0, 1])
ax_bottom = fig.add_subplot(gs[1, 1])

ax_main.plot(x, vendite, marker="o")
ax_main.set_title("Vendite (principale)")

ax_top.bar(x, margine)
ax_top.set_title("Margine")

ax_bottom.hist(margine, bins=8)
ax_bottom.set_title("Distribuzione margine")

plt.show()

#ESERCIZIO 3 GRIGLIA NON UNIFORME (uno grafico per tutta la larghezza, due sotto affincati)

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(1, 31)
serie = np.cumsum(np.random.randint(-3, 4, size=30)) + 100

fig = plt.figure(figsize=(10, 6), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax_top = fig.add_subplot(gs[0, :])
ax_left = fig.add_subplot(gs[1, 0])
ax_right = fig.add_subplot(gs[1, 1])

ax_top.plot(x, serie)
ax_top.set_title("Trend globale")

ax_left.hist(serie, bins=10)
ax_left.set_title("Distribuzione")

ax_right.scatter(x, serie)
ax_right.set_title("Scatter tempo-valore")

plt.show()

#ESERCIZIO 4 GRIGLIA NON UNIFORME (colonne con larghezze diverse, righe con altezze diverse)

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 6), constrained_layout=True)
gs = fig.add_gridspec(
    2, 3,
    width_ratios=[2, 1, 1],
    height_ratios=[1, 2]
)

ax_big = fig.add_subplot(gs[:, 0])     # colonna larga, tutte le righe
ax_a = fig.add_subplot(gs[0, 1])
ax_b = fig.add_subplot(gs[0, 2])
ax_c = fig.add_subplot(gs[1, 1:])
# nota: gs[1, 1:] prende colonna 1 e 2 nella riga 1

ax_big.set_title("Principale (2x altezza)")
ax_a.set_title("Box A")
ax_b.set_title("Box B")
ax_c.set_title("Box C (larga)")

plt.show()

#ESEMPIO 5 GRIGLIA NON UNIFORME (spazio tra i pannelli)

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 5))
gs = fig.add_gridspec(2, 2, wspace=0.3, hspace=0.4)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

plt.show()





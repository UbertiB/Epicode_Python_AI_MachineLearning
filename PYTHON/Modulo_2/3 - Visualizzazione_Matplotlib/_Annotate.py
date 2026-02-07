"""
ANNOTATE
1) xy è il punto che vuoi evidenziare
2) xyptext è dove vuoi mettere il testo. Se lo lasci uguale a xy, il testo finisce sul punto e si sovrappone
3) xycoords e textcoords dicono in che sistema di coordinate stai ragionando (dati, assi, figura, offset in punti, ecc)

"""

#ESERCIZIO 1 ANNOTAZIONE MINIMA

import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 15, 7, 18]

fig, ax = plt.subplots()
ax.plot(x, y, marker="o")

ax.annotate("Picco", xy=(4, 18))  # testo sul punto

plt.show()
"""
senza xytext, il testo sta su xy
"""

#ESERCIZIO 2: SPOSTARE IL TESTO

import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 15, 7, 18]

fig, ax = plt.subplots()
ax.plot(x, y, marker="o")

ax.annotate(
    "Picco",
    xy=(4, 18),              # punto reale
    xytext=(10, 10),         # spostamento
    textcoords="offset points"
)

plt.show()

#ESERCIZIO 3: AGGIUNGI UNA FRECCIA

import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 15, 7, 18]

fig, ax = plt.subplots()
ax.plot(x, y, marker="o")

ax.annotate(
    "PICCO",
    xy=(4, 18),
    xytext=(20, -30),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->")
)

plt.show()

#ESERCIZIO 4: ANNOTARE IL MASSIMO IN MODO AUTOMATICO

import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 15, 7, 18]

imax = max(range(len(y)), key=lambda i: y[i])
xp, yp = x[imax], y[imax]

fig, ax = plt.subplots()
ax.plot(x, y, marker="o")

ax.annotate(
    f"MAX={yp}",
    xy=(xp, yp),
    xytext=(10, 10),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->")
)

plt.show()

#ESERCIZIO 5: ANNOTARE PIU' PUNTI CON UN LOOP, ANNOTARE SOLO I PUNTI IMPORTANTI (SOPRA SOGLIA) NON TUTTO

import matplotlib.pyplot as plt

x = list(range(1, 13))
y = [10, 12, 9, 15, 11, 30, 14, 13, 8, 7, 16, 22]

fig, ax = plt.subplots()
ax.plot(x, y, marker="o")

soglia = 18
for xi, yi in zip(x, y):
    if yi >= soglia:
        ax.annotate(
            str(yi),
            xy=(xi, yi),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            arrowprops=dict(arrowstyle="->")
        )

plt.show()

#ESERCIZIO 6: TESTO FISSO, METTERE UNA NOTA DI KPI
#questa nota non deve muoversi quando cambiano i limiti dell'asse

import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [10, 15, 7, 18]

fig, ax = plt.subplots()
ax.plot(x, y, marker="o")

ax.annotate(
    "Fonte: ERP\nPeriodo: 2025",
    xy=(0.02, 0.98),
    xycoords="axes fraction",
    va="top"
)

plt.show()


#MARKER
#plt.scatter aggiunge marker mirati su set di dati

import matplotlib.pyplot as plt

mesi = list(range(1, 7))
vendite_A = [10, 12, 9, 15, 11, 14]
vendite_B = [8, 9, 7, 10, 9, 12]

fig, ax = plt.subplots()
ax.plot(mesi, vendite_A, marker="o", linestyle="-", label="Cliente A")
ax.plot(mesi, vendite_B, marker="s", linestyle="--", label="Cliente B")
ax.legend()
plt.show()


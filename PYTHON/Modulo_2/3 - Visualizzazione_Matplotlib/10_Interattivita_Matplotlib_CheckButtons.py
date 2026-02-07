"""
CHECKBUTTONS è un widget di Matplotlib per avere caselle spuntabili (on/off), quindi mostrare/nascondere serie 
o attivare opzioni del grafico.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons

# Dati (esempio coerente: 30 giorni)
giorni = pd.date_range("2025-01-01", periods=30, freq="D")
s1 = np.linspace(50, 100, len(giorni)) + np.random.normal(0, 5, len(giorni))
s2 = np.linspace(20, 60, len(giorni)) + np.random.normal(0, 8, len(giorni))
s3 = 80 + 10*np.sin(np.linspace(0, 4*np.pi, len(giorni))) + np.random.normal(0, 3, len(giorni))

df = pd.DataFrame({"S1": s1, "S2": s2, "S3": s3}, index=giorni)

fig, ax = plt.subplots(figsize=(10, 5))

plt.subplots_adjust(right=0.80)  # spazio a destra per i checkbox
# Linee
l1, = ax.plot(df.index, df["S1"], label="S1")
l2, = ax.plot(df.index, df["S2"], label="S2")
l3, = ax.plot(df.index, df["S3"], label="S3")
ax.legend(loc="upper left")

# Area per CheckButtons (un axes “dedicato”)
rax = plt.axes([0.82, 0.55, 0.16, 0.25])  # posizione e dimensine del contenitore [left, bottom, width, height]
labels = ["S1", "S2", "S3"]
visibility = [True, True, True]
check = CheckButtons(rax, labels, visibility) #raggruppo i 3 checkbuttons

# Mappa label -> linea
line_map = {"S1": l1, "S2": l2, "S3": l3} #dizionario che associa la label al grafico plot corrispondente

def toggle(label):
    line = line_map[label]
    line.set_visible(not line.get_visible())
    fig.canvas.draw_idle()

check.on_clicked(toggle)

ax.set_title("Serie temporali con CheckButtons (mostra/nascondi)")
plt.tight_layout()
plt.show()

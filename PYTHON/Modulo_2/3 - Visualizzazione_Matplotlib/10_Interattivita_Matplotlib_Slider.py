"""
SLIDER
lo slider è uno strumento interattivo, permette di cambiare un parametro del grafico muovendo una barra,
e vedere il risultato in tempo reale.
Lo slider non ricalcola i dati, sposta solo un riferimento, perfetto per analisi "what-if"
Non ricreare il grafico dentro "update" (lento ed instabile)
Lo slider non è una feature "da dashboard"
"""


#
# SLIDER SEMPLICE (ROLLING WINDOW)
#

#Esempio usa lo slider per capire cosa cambia cambiando la finestra della media mobile

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Serie temporale (vendite giornaliere simulate)
x = pd.date_range("2025-01-01", periods=50, freq="D")
y = np.linspace(50, 100, len(x)) + np.random.normal(0, 8, len(x))

fig, ax = plt.subplots(figsize=(10,5))
plt.subplots_adjust(bottom=0.25)  # spazio per lo slider

# Linea originale
line_data, = ax.plot(x, y, label="Vendite")

# Media mobile iniziale
window_init = 5
y_ma = pd.Series(y).rolling(window_init, min_periods=1).mean()
line_ma, = ax.plot(x, y_ma, label=f"MA {window_init}")

ax.legend()

#Asse dello slider
ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
#SLIDER
slider = Slider(ax=ax_slider, label="Finestra MA", valmin=1, valmax=15, valinit=window_init, valstep=1)

# Funzione che aggiorna il grafico
def update(val):
    w = int(slider.val) #valore dello slider (appena modificato)
    new_ma = pd.Series(y).rolling(w, min_periods=1).mean() #aggiorno media mobile con nuova finestra temporale (data dallo slider)
    line_ma.set_ydata(new_ma)  #aggiorno la linea sul grafico
    line_ma.set_label(f"MA {w}") #aggiorno label
    ax.legend()
    fig.canvas.draw_idle() #aggiorno grafico

slider.on_changed(update) #all'evento 'on_change' dello slider lancio la funzione update (creata sopra)

plt.show()


#
# SLIDER COME SOGLIA 
#

#from matplotlib.widgets import Slider

fig, ax = plt.subplots(figsize=(10,5))
plt.subplots_adjust(bottom=0.25)  #spazio per lo slider

line, = ax.plot(x, y)  #grafico .plot
threshold = np.mean(y)
hline = ax.axhline(threshold, linestyle="--")

ax_slider = plt.axes([0.15, 0.1, 0.7, 0.03])
slider = Slider(ax_slider, "Soglia", y.min(), y.max(), valinit=threshold)

def update(val):
    hline.set_ydata([val])
    fig.canvas.draw_idle() #ridisegna la figura ma lo fa quando ha tempo, raggruppando eventuali altri aggiornamenti

slider.on_changed(update)

plt.show()




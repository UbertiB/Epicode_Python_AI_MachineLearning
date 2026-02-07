"""
BUTTON
è un widget interattivo di matplotlib, concettualmente diverso dallo slider.
Serve quando vuoi eseguire un'azione discreta, non variare un parametro continuo
Il button ha sempre un asse (ax dedicato), un metodo click (on_clicked), una funzione che modifica oggetti 
già esistenti, un draw_idle() finale
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#ESEMPIO 1 BUTTON SEMPLICE (RESET)

x = np.arange(20)
y = np.random.randint(10, 50, size=20)

fig, ax = plt.subplots(figsize=(8,4))
plt.subplots_adjust(bottom=0.25)

line, = ax.plot(x, y, label="Serie")
ax.legend()

# Asse del bottone
ax_button = plt.axes([0.4, 0.1, 0.2, 0.08]) #posizione e dimensione del contenitore ax_button
btn1 = Button(ax_button, "RESET") #metto il pulsante all interno del contenitore

# Callback
def reset(event):
    line.set_ydata(y)
    line.set_label("Serie")
    ax.legend()
    fig.canvas.draw_idle()

btn1.on_clicked(reset)

#plt.show()


# ESEMPIO 2 BUTTON

import pandas as pd
#from matplotlib.widgets import Button

y_ma = pd.Series(y).rolling(5, min_periods=1).mean()

show_ma = False

ax_button = plt.axes([0.65, 0.1, 0.25, 0.08]) #posizione e dimensione del secondo pulsante, stessa dimensione del primo stessa linea y del primo, cambia la x
btn2 = Button(ax_button, "Toggle MA")

def toggle(event):
    global show_ma
    show_ma = not show_ma

    if show_ma:
        line.set_ydata(y_ma)
        line.set_label("Media mobile")
    else:
        line.set_ydata(y)
        line.set_label("Serie")

    ax.legend()
    fig.canvas.draw_idle()

btn2.on_clicked(toggle)

plt.show()


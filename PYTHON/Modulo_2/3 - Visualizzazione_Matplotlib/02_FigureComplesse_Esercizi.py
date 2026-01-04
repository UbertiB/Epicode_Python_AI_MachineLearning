"""
Crea una figura con 3x2 subplot dove:
- la prima riga contiene due grafici principali
- la seconda riga contiene un grafico verticale a sinistra che occupa due righe
- la seconda riga a destra contiene un grafico più piccolo 
- Usare tight_layout() per ottimizzare gli spazi
- Utilizzando GridSpec, creare una dashboard che includa:
  - grafico principale in alto
  - due grafici secondari una acconto all'altro in basso
- Aggiungere insert in grafico principale per evidenziare un picco dei dati
- Personalizzare colori, stili e marker per ciascun grafico, 
aggiungere leggende e titoli descrittivi.
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

if False:
  #
  # FIG.ADD_GRIDSPEC
  #
    
  np.random.seed(42)
  x = np.arange(1, 11)
  y1 = np.random.randint(10, 50, size=10)
  y2 = np.random.randint(20, 60, size=10)
  y3 = np.random.randint(5, 30, size=10)
  y4 = np.random.randint(15, 40, size=10)

  fig = plt.figure(figsize=(12,8))

  # Griglia 3x2
  gs = fig.add_gridspec(3,2)

  # Prima riga: due grafici principali
  ax1 = fig.add_subplot(gs[0,0])
  ax1.plot(x, y1, marker='o', color='blue', linestyle='-', label='y1')
  ax1.set_title("Grafico 1 - Linea principale")
  ax1.legend()

  ax2 = fig.add_subplot(gs[0,1])
  ax2.plot(x, y2, marker='s', color='green', linestyle='--', label='y2')
  ax2.set_title("Grafico 2 - Linea principale")
  ax2.legend()

  # Seconda riga: grafico verticale a sinistra che occupa due righe
  ax3 = fig.add_subplot(gs[1:,0])
  ax3.bar(x, y3, color='orange', label='y3')
  ax3.set_title("Grafico 3 - Barre verticali")
  ax3.legend()

  # Seconda riga: grafico più piccolo a destra
  ax4 = fig.add_subplot(gs[1,1])
  ax4.scatter(x, y4, color='red', marker='^', label='y4')
  ax4.set_title("Grafico 4 - Scatter piccolo")
  ax4.legend()

  plt.tight_layout()
  plt.show()

# Esercizio 2

#
# GRIDSPEC
#
if True:

  from matplotlib.gridspec import GridSpec

  np.random.seed(42)
  x = np.arange(1,21)
  y_main = np.random.randint(50,150,size=20)
  y_sub1 = np.random.randint(10,50,20)
  y_sub2 = np.random.randint(20,80,20)

  fig = plt.figure(figsize=(12,8))
  gs = GridSpec(2,2, height_ratios=[2,1], width_ratios=[2,1], hspace=0.4, wspace=0.3)

  # Grafico principale in alto (occupando entrambe le colonne)
  ax_main = fig.add_subplot(gs[0,:])
  ax_main.plot(x, y_main, color='blue', linestyle='-', marker='o', label='Traffico principale')
  ax_main.set_title("Grafico Principale")
  ax_main.set_ylabel("Valore")
  ax_main.legend()

  # Inset per evidenziare picco
  ax_inset = ax_main.inset_axes([0.6,0.5,0.3,0.3])
  ax_inset.plot(x, y_main, color='blue', marker='o')
  # Evidenzio picco
  max_idx = np.argmax(y_main)
  ax_inset.plot(x[max_idx], y_main[max_idx], 'ro', markersize=10)
  ax_inset.set_title("Picco evidenziato", fontsize=8)

  # Grafici secondari in basso
  ax_sub1 = fig.add_subplot(gs[1,0])
  ax_sub1.bar(x, y_sub1, color='orange', label='Sub1')
  ax_sub1.set_title("Grafico Secondario 1")
  ax_sub1.legend()

  ax_sub2 = fig.add_subplot(gs[1,1])
  ax_sub2.scatter(x, y_sub2, color='green', s=50, label='Sub2')
  ax_sub2.set_title("Grafico Secondario 2")
  ax_sub2.legend()

  plt.tight_layout()
  plt.show()
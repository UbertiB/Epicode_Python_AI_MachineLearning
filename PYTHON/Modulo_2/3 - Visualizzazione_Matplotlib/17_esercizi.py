"""
ESERCIZIO 1
* Genera una serie x=np.linspace(0,10,100) e le funzioni y1=sin(x), y2=cos(x), y3=sin(x)*cos(x)
* Crea un layout 2x2 dove:
  - subplot1 (top-left): grafico a linee di y1 e y2 con leggenda e griglia
  - subplot2(top-right): boxplot di y3
  - subplot3(bottom, tutta la larghezza): grafico combinato delle tre serie con annotazioni per i massimi
* Applica tight_layout() e aggiungi titoli chiari a ogni subplot

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec

x=np.linspace(0,10,100)
y1=np.sin(x) 
y2=np.cos(x) 
y3=np.sin(x)*np.cos(x)

fig=plt.figure(figsize=(12,6))
gs=gridspec.GridSpec(2,2,figure=fig)

ax1=fig.add_subplot(gs[0,0])
ax2=fig.add_subplot(gs[0,1])
ax3=fig.add_subplot(gs[1,:])

ax1.plot(x,y1,label="sin(x)")
ax1.plot(x,y2,label="cos(x)")
ax1.set_title("Funzioni trigonometriche")
ax1.legend()
ax1.grid(True)

sns.boxplot(y=y3,ax=ax2)
ax2.set_title("Boxplot vendite")

ax3.plot(y1,label="sin")
ax3.plot(y2,label="cos", marker="s")
ax3.plot(y3,label="sin + cos",marker="o")
ax3.set_title("Serie trigonometriche")
ax3.legend()
ax3.grid(True)

axes=[ax1,ax2,ax3]
plt.tight_layout()
for a in axes:
    t=a.get_title()
    a.set_title(t,fontsize=10,pad=10)

plt.show()

"""
ESERCIZIO 2
* Genera un array x=np.logspace(0.1,2,100) e y=x**2*random_noise
* Crea grafico con scale logaritmiche su entrambi gli assi, impostando ticks personalizzati per evidenziare valori critici
* Evidenzia con un'annotazione automatica il punto massimo di y
* Crea una matrice 5x5 casuale e visualizzala come heatmap con palette divergin (coolwarm) e annotazioni dei valori
"""
x=np.logspace(0.1,2,100)
y=x**2 * np.random(0,50,len(x))
y=x**2 * np.random.choi  #np.random_noise



"""
GRAFICI 3D
Nel mondo reale molti fenomini arrivano da 3 variabili
La posizione nello spazio (x,y,z), ed il tempo, o altre grandezze fisiche
Matplotlib con la libreria mpl_toolkits.mplot3d permette di rappresentare superfici, scatter e linne
nello spazio (x,y,z)
La profondità aggiunge informazioni sulla distribuzione dei dati nello spazio.
La scelta dell'angolo di visualizzazione è fondamentale per interpretare correttamente i dataset
Le linee 3d realistiche rappresentano delle traiettorie nello spazio (come percorsi di veicoli)
A differenza dei dati matematici questi dati provengono da osservazioni sperimentali e contengono 
spesso errori.
Gli scatter 3D realitsti vengo
"""
#esempio
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig=plt.figure()
ax=fig.add_subplot(111,projection="3d")
ax.set_title("Grafico 3D")
plt.show()
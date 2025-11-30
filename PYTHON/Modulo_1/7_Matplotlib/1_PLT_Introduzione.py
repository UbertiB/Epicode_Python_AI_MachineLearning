"""
MATPLOTLIB
ossia libreria di riferimento per esportare i dati verso grafici
Possiamo trasfomrare i numeri in grafici chiari ed intuitivi
La visualizzazione è una parte importante sia per comprendere i dati
sia per comunicare i risultati
Attraverso i grafici è possibile:
- individuare tendenze e patterne
- riconoscere valore anomali
- confrontare più serie di dati
- comunicare i risultati anche a chi non conosce python o l'analisi dei dati
Matplotlib è una libreria opensource nata in ambito scientifico,
crea grafici 2D, anche se supporta alcune visualizzazioni in 3D
Con pochi comandi è possibile generare diversi tipi di grafici
Il suo punto di forza è che è altamente personalizzabile
E' possibile controllare colori, stili, titoli, etichette e leggende
E' diventato la base per la visualizzazione dei dati in Python
PYPLOT è il cuore della libreria, e contiene tutte quelle funzioni che
servono per gestire i grafici
Si possono creare diversi grafici tra cui:
- Barre: bar
- Istogrammi: hist
- Scatter plot (scatter)
- Grafici a torta (pie)
Alcuni dei dettagli personalizzabili:
- Titoli:title
- Etichette sugli assi: plt.xlabel("Asse X"), plt.ylabel("Asse Y")
- Legenda: plt.legend()
- Colori e stili delle linee: color="red" linestyle="--"
I grafici possono essere salvati in diversi formati (png, jpg, svg, pdf)
plt.savefig("nomefile.png")
Sono poi nate librerie complementari che semplificano la creazione di grafici:
- Seaborn
- Plotly
"""

import matplotlib.pyplot as plt

x=[1,2,3,4]
y=[2,4,6,8]
plt.plot(x,y)
plt.show()

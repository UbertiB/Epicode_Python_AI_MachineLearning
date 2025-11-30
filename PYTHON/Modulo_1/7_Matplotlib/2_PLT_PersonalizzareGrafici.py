"""
I grafici possono essere creati e personalizzati per comunicare "meglio" i dati, adatto al contesto
colori, titoli, etichette, legende, ecc possono essere personalizzati
- titolo: plt.title ("Titolo grafico", fontsize=14, color="blue")
- personalizzare gli assi: plt.xlabel("Asse X", fontsize=12, color="red"), plt.ylabel("Asse Y",fontsize=12, color="blue")
- Legenda: plt.legend(loc="best") aggiunge automaticamente una legenda, funziona bene se ogni comando plot abbiamo un'etichetta con label
- Distinguere le serie attraverso i colori e gli stili: colore="green" linestyle="--" linewidth=2
- Evidenziare i singoli punti con i marcatori: marker="*" x croce s=quadrato *=stella o=punto
- Aggiungere la griglia plt.grid(True)  plt.grid(Ture, linestule="--", alpha=0.7)
- Dimensione del grafico: plt.figure(figsize=(8,6)) scelgo altezza e larghezza del grafico
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mesi=['gen','feb','mar','apr','mag','giu','lug','ago','set','ott','nov','dic']
vendite=[120,140,222,453,5334,655,422,75,11,567,23,53]
#df=pd.DataFrame({'Mese':mesi,'Vendite':vendite})

# GRAFICO A LINEE
#definisco il tipo di grafico e i dati
plt.plot(mesi,vendite,label="vendite 2025")
#titolo
plt.title ("grafico a linee PROVA",fontsize=14,color='red')
#griglia
plt.grid(True,linestyle='--',alpha=0.7)
#plt.marker='*'
#asse X
plt.xlabel("Mesi",fontsize=18,color='green')
#asse Y
plt.ylabel ("Vendite")
#legenda (gestire la proprietà label)
plt.legend( loc='upper left')
#dimensioni grafic
#plt.figure(figsize=(8,6))
#visualizzo grafico
plt.show ()
#salvo il grafico su file
plt.savefig('graficoprova.pdf',dpi=300)
"""
BAR CHAR .BAR
Un grafico a barre rappresenta una misura aggregata per categoria.
Esempi:
- Somma: fatturato per cliente, quantità per articolo, ore per reparto
- Media/mediana: lead time medio per fornitore, ritardo medio per vettore, prezzo medio 
  per famiglia.
- Conteggio: numero ordini per canale, numero non conformità per linea

Matplotlib non aggrega, disegna solo quello che gli dai. Quandi 'la verità' è nella tabella
aggregata che prepari prima (pandas group by)

Usa il grafico a barre quando:
- Hai categorie discrete (clienti, reparti, famiglie, stati ordine)
- Vuoi confrontare o ordinare (variabilità, outlier)
  Alternativa: scala log, oppure normalizza e spiega
- Stai confrontando 'media' senza contesto
"""

#ESEMPIO 1: BARRE SEMPLICE (GIà AGGREGATO)

import matplotlib.pyplot as plt

categorie = ["A", "B", "C"]
valori = [10, 7, 13]

plt.bar(categorie, valori)
plt.title("Barre semplici")
plt.xlabel("Categoria")
plt.ylabel("Valore")
plt.show()

#ESERCIZIO 2: DAI DATI GREZZI ALLA BARRA (COMME VS MEDIA VS MEDIANA)
#Qui vedi la differenza e split-combine

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "giorno": ["Lun","Lun","Mar","Mar","Mar","Mer"],
    "importo": [100, 120, 90, 200, 110, 130]
})

# 1) somma
somma = df.groupby("giorno", as_index=False)["importo"].sum()
# 2) media
media = df.groupby("giorno", as_index=False)["importo"].mean()
# 3) mediana (robusta)
mediana = df.groupby("giorno", as_index=False)["importo"].median()

plt.bar(somma["giorno"], somma["importo"])
plt.bar(media["giorno"], media["importo"])
plt.bar(mediana["giorno"], mediana["importo"])
plt.title("Importo TOTALE per giorno (somma/media/mediana)")
plt.ylabel("€")
plt.show()
"""
importi fatture potrebbero avere outlier, quindi media spesso è una scelta passima 
se non spieghi la distribuzione. Mediana spesso più difendibile.
Oggi con la fattura elettronica (solo Italia) se le fatture di acquisto arrivano tutte
dallo SDI gli importi sono corretti al 100% pertanto questo ragionamento non vale più
per le fatture, vale sempre per altri valori (esempio moviemnti di magazzino)
"""

#ESERCIZIO 3 TOP N ORDINATO

agg = df.groupby("giorno", as_index=False)["importo"].sum()
agg = agg.sort_values("importo", ascending=False)

plt.bar(agg["giorno"], agg["importo"])
plt.title("Totale per giorno (ordinato)")
plt.ylabel("€")
plt.show()

#ESERCIZIO 4 BAR ORIZZONTALE (quando le etichette sono lunghe)
#barh

import matplotlib.pyplot as plt

clienti = ["CLIENTE MOLTO LUNGO S.R.L.", "BETA SPA", "GAMMA SNC"]
fatt = [120000, 95000, 40000]

plt.barh(clienti, fatt)
plt.title("Fatturato per cliente")
plt.xlabel("€")
plt.show()

#ESERCIZIO 5 etichette sopra le barre

import matplotlib.pyplot as plt

categorie = ["A", "B", "C"]
valori = [10, 7, 13]

bars = plt.bar(categorie, valori)
plt.title("Barre con etichette")

for b in bars:
    h = b.get_height()
    plt.text(b.get_x() + b.get_width()/2, h, f"{h:.0f}", ha="center", va="bottom")

plt.show()

#ESERCIZIO 6 BARRE RAGGRUPPATE
#confronti due misure per la stessa categoria

import numpy as np
import matplotlib.pyplot as plt

mesi = ["Gen", "Feb", "Mar", "Apr"]
consuntivo = [120, 150, 130, 160]
budget =     [110, 140, 135, 155]

x = np.arange(len(mesi))
w = 0.4

plt.bar(x - w/2, consuntivo, width=w, label="Consuntivo")
plt.bar(x + w/2, budget, width=w, label="Budget")

plt.xticks(x, mesi)
plt.title("Budget vs Consuntivo")
plt.ylabel("k€")
plt.legend()
plt.show()

#ESERCIZIO 7 BARRE IMPILATE
#Buono per capire 'da cosa è fatto' il totale

import numpy as np
import matplotlib.pyplot as plt

mesi = ["Gen", "Feb", "Mar"]
fam_A = [50, 60, 55]
fam_B = [30, 20, 25]
fam_C = [40, 45, 35]

x = np.arange(len(mesi))

plt.bar(x, fam_A, label="Famiglia A")
plt.bar(x, fam_B, bottom=fam_A, label="Famiglia B")
plt.bar(x, fam_C, bottom=np.array(fam_A)+np.array(fam_B), label="Famiglia C")

plt.xticks(x, mesi)
plt.title("Composizione fatturato per mese (impilato)")
plt.ylabel("k€")
plt.legend()
plt.show()
"""
barre impilate non è utile per confrontare una famiglia tra i mesi, perchè non parte
sempre da zero. Se interessa confrontare i segmenti meglio barre raggruppate o
linee separate
"""

#ESERCIZIO 8 MEDIA CON VARIABILITA'

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "fornitore": ["A","A","A","B","B","C"],
    "lead_time": [12, 15, 9, 20, 18, 7]
})

stats = df.groupby("fornitore")["lead_time"].agg(["mean","std","count"]).reset_index()

plt.bar(stats["fornitore"], stats["mean"], yerr=stats["std"], capsize=6)
plt.title("Lead time medio per fornitore (con std)")
plt.xlabel("Fornitore")
plt.ylabel("Giorni")
plt.show()





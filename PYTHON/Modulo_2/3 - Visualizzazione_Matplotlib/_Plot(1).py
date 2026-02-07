"""
GRAFICO A LINEA
Un grafico a linea è uno strumento per raccontare come cambia una misura lungo un asse ordinato, 
quasi sempre il tempo.
Lo si usa quando si vuole vedere trend, stagionaità, cambi di livello, rotture di regime, anomalie
nel tempo. Esempi ERP: fatturato giornaliero, pezzi prodotti per settimana, giacenza media per
mese, lead time medio per fornitore nel tempo.
Puoi capire:
- Trend: sta salendo o scendendo, o è rumore?
- Staginalità: pattern che si ripete (mensile, settimana)
- Outlier: picchi, buchi (fermi impianto, promo, rotture stock)
- Cambi di regime: 'da qui in poi' succede qualcosa di diverso (nuovo fornitore, nuova politica scorte, ecc)

Non usarlo:
- Categorie senza ordine (clienti, articoli, reparti): usare barre
- Troppe serie insieme (20 linee): diventaspaghetti, meglio piccoli multipli o top N
- Dati troppo rumorosi senza smoothing
- Se vuoi confrontare distribuzioni: usa boxplot/istogramma
"""

#
#ESEMPIO 1 SEMPLICE
#

import matplotlib.pyplot as plt

y = [10, 12, 9, 15, 14]
x = [1, 2, 3, 4, 5]

plt.plot(x, y)
plt.title("Esempio base: valori nel tempo")
plt.xlabel("Periodo")
plt.ylabel("Valore")
plt.show()

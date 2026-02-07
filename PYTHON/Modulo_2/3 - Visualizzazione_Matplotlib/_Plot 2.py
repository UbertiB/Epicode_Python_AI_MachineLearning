"""
GRAFICO A LINEA (PLT)
Un grafico a linea è uno strumento che racconta come cambia una misura lungo un asse ordinato,
quasi sempre il tempo. L'asse X deve essere ordinato per mostrare dati corretti.

Il grafico a linea è da utilizzare se vuoi vedere trend, stagionalità, cambi di livello,
rotture di regime, anomalie nel tempo.
Da non utilizzarsi se hai categorie senza ordine (esempio clienti, articoli, reparti, in questo caso usa 
un grafico a barre), da non utilizzarsi se hai troppe serie (20 linee), diventa inleggibile, da non utilizzarsi
con dati troppo rumorosi senza smoothing, da non utilizzarsi se vuoi confrontare distribuzioni, in questo
caso utilizza boxplot/istogramma

"""

#
#ESEMPIO 1: GRAFICO A LINEA SEMPLICE 
#
import matplotlib.pyplot as plt

y = [10, 12, 9, 15, 14]
x = [1, 2, 3, 4, 5] 

plt.plot(x, y)
plt.title("Esempio base: valori nel tempo ")
plt.xlabel("Periodo")
plt.ylabel("Valore")
plt.show()

"""
se la x non è ordinata, prima di fare il grafico andrebbe ordinata.
"""

#
#ESEMPIO 2: SERIE TEMPORALE
#
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "data": pd.date_range("2026-01-01", periods=10, freq="D"),
    "fatturato": [1200, 1300, 900, 1600, 1550, 1700, 800, 1400, 1500, 1650]
}).sort_values("data")

plt.plot(df["data"], df["fatturato"])
plt.title("Fatturato giornaliero")
plt.xlabel("Data")
plt.ylabel("Euro")
plt.show()

"""
controlla sempre:
 - picchi e buchi: chiediti se sono eventi reali (fatture cumulative, chiusura mese, ecc) o fenomeni
   di business.
 - Se hai buchi (giorni senza vendite), decidi se sono 0 reali o dati mancanti
"""

#
#ESERCIZIO 3 (con più serie a confronto)
#
import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "data": pd.date_range("2026-01-01", periods=8, freq="D"),
    "Italia":  [100, 120, 80, 140, 135, 150, 90, 160],
    "Germania":[90, 110, 70, 130, 125, 145, 85, 150]
})

plt.plot(df["data"], df["Italia"], label="Italia")
plt.plot(df["data"], df["Germania"], label="Germania")
plt.title("Vendite giornaliere per paese")
plt.xlabel("Data")
plt.ylabel("Euro")
plt.legend()
plt.show()

"""
Contronti due trend insieme
"""

#ESERCIZIO 4 CON DATI RUMOROSI, (aggiunti media mobile)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "data": pd.date_range("2026-01-01", periods=30, freq="D"),
    "ordini": [12,14,9,20,18,11,10,25,22,13,9,15,17,30,28,12,11,26,24,14,10,16,18,29,27,13,12,23,21,15]
})
df["ma7"] = df["ordini"].rolling(7).mean()  #calcolo media mobile

plt.plot(df["data"], df["ordini"], label="Ordini (grezzo)")
plt.plot(df["data"], df["ma7"], label="Media mobile 7g")
plt.title("Ordini: grezzo vs trend")
plt.xlabel("Data")
plt.ylabel("N. ordini")
plt.legend()
plt.show()

"""
La linea 'grezza' spesso è rumore, aggiunti la media mobile, ti fa vedere la tendenza, ma introduce un ritardo
Non confondere smoothing con la realtà
Quando NON utilizzare smoothing:
- se devi identificare esattamente il giorno dell'evento
- se la serie è corta: la media mobile ti mangia metà dei dati
"""

#ESERCIZIO 5 EVIDENZIA ANOMALIE E SOGLIE

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "data": pd.date_range("2026-01-01", periods=14, freq="D"),
    "lead_time": [5,6,5,7,6,5,12,6,5,7,6,5,8,6]
})

soglia = 8

plt.plot(df["data"], df["lead_time"], label="Lead time (giorni)")
plt.axhline(soglia, linestyle="--", label="Soglia")
plt.title("Lead time e superamenti soglia")
plt.xlabel("Data")
plt.ylabel("Giorni")
plt.legend()
plt.show()


#ESERCIZIO 6: CONFRONTA SERIE CON ASSI DIVERSI

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "data": pd.date_range("2026-01-01", periods=10, freq="D"),
    "vendite": [100,120,110,130,160,150,170,165,180,190],
    "giacenza": [500,480,470,460,430,420,410,405,390,380]
})

fig, ax1 = plt.subplots(figsize=(12, 5))
ax2 = ax1.twinx()

ax1.plot(df["data"], df["vendite"], label="Vendite")
ax2.plot(df["data"], df["giacenza"], label="Giacenza")

ax1.set_title("Vendite vs Giacenza (attenzione: due assi)")
ax1.set_xlabel("Data")
ax1.set_ylabel("Vendite")
ax2.set_ylabel("Giacenza")

plt.show()

"""
Con più assi è meglio prima normalizzare e solo dopo confrontare il trend
"""
#COPIA 7: NORMALIZZAZIONE DEI DATI

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame({
    "data": pd.date_range("2026-01-01", periods=10, freq="D"),
    "vendite": [100,120,110,130,160,150,170,165,180,190],
    "giacenza": [500,480,470,460,430,420,410,405,390,380]
})

base_v = df["vendite"].iloc[0]
base_g = df["giacenza"].iloc[0]
df["vendite_idx"] = df["vendite"] / base_v * 100
df["giacenza_idx"] = df["giacenza"] / base_g * 100

plt.plot(df["data"], df["vendite_idx"], label="Vendite (base 100)")
plt.plot(df["data"], df["giacenza_idx"], label="Giacenza (base 100)")
plt.title("Confronto trend normalizzato (base 100)")
plt.xlabel("Data")
plt.ylabel("Indice")
plt.legend()
plt.show()



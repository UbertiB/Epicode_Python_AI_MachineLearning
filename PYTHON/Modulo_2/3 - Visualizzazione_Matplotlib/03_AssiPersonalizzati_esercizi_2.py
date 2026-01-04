"""

MultipleLocator = controllo dove mettere i tick (ogni 1, 2, 5…).

FuncFormatter = controllo come visualizzare i valori (€, K€, formati speciali).

PercentFormatter = comodissimo per KPI in percentuale.

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



#
#1) Locator semplice: tick ogni 2 sull’asse X
#
if False:
    x = np.arange(0, 11)            # 0,1,2,...,10
    y = x**2                        # giusto per avere una curva

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(x, y, marker="o")

    # Tick principali ogni 2 unità sull'asse X
    ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

    ax.set_xlabel("X")
    ax.set_ylabel("Y = X^2")
    ax.set_title("Esempio MultipleLocator: tick ogni 2")

    plt.tight_layout()
    plt.show()
#
#2) Formatter valuta: asse Y in euro
#
if False:

    # Dati finti: fatturato mensile
    mesi = list(range(1, 13))  # 1..12
    fatturato = [120000, 95000, 150000, 130000, 170000, 160000,
                140000, 155000, 180000, 190000, 210000, 220000]

    def euro_formatter(x, pos):
        # x è il valore numerico del tick
        # pos è l'indice del tick (non lo usiamo)
        return f"{x:,.0f} €".replace(",", ".")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mesi, fatturato, marker="o")

    ax.set_xlabel("Mese")
    ax.set_ylabel("Fatturato")

    # Applico il formatter all'asse Y
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(euro_formatter))

    ax.set_title("Fatturato mensile (formattato in euro)")

    plt.tight_layout()
    plt.show()

#
#3) Percentuali: KPI in %
#
if False:

    # Dati finti: tasso resi per mese (0 = 0%, 0.1 = 10%, ecc.)
    mesi = list(range(1, 13))
    tasso_resi = [0.02, 0.05, 0.03, 0.06, 0.04, 0.07,
                0.05, 0.03, 0.02, 0.04, 0.05, 0.03]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mesi, tasso_resi, marker="o")

    ax.set_xlabel("Mese")
    ax.set_ylabel("Tasso resi")

    # Formatter percentuale: xmax=1 perché i dati sono tra 0 e 1
    ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1, decimals=1))

    ax.set_title("Tasso resi mensile (%)")

    plt.tight_layout()
    plt.show()

#
#4) Formatter personalizzato per “K€” (migliaia di euro)
#
if False:

    # Dati finti: fatturato mensile
    mesi = list(range(1, 13))
    fatturato = [120000, 95000, 150000, 130000, 170000, 160000,
                140000, 155000, 180000, 190000, 210000, 220000]

    def keuro_formatter(x, pos):
        # x è il valore in euro
        return f"{x/1000:.0f} K€"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mesi, fatturato, marker="o")

    ax.set_xlabel("Mese")
    ax.set_ylabel("Fatturato (K€)")

    ax.yaxis.set_major_formatter(ticker.FuncFormatter(keuro_formatter))

    ax.set_title("Fatturato mensile (in K€)")

    plt.tight_layout()
    plt.show()

#
#5) Combinare Locator + Formatter (esempio completo “da report”)
# 
if True:

    mesi = list(range(1, 13))
    fatturato = [120000, 95000, 150000, 130000, 170000, 160000,
                140000, 155000, 180000, 190000, 210000, 220000]

    def keuro_formatter(x, pos):
        return f"{x/1000:.0f} K€"

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mesi, fatturato, marker="o")

    # Tick X: uno per ogni mese
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.set_xlabel("Mese")

    # Y in K€
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(keuro_formatter))
    ax.set_ylabel("Fatturato (K€)")

    ax.set_title("Fatturato mensile per anno")

    plt.tight_layout()
    plt.show()
        




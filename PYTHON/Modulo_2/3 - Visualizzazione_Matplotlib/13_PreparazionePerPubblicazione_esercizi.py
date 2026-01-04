"""
ESERCIZIO 1
Crea un grafico di funzioni matematica e salvalo in png e pdf, impostando la risoluzoine a 300dpi.
Confrota i due formati

ESERCIZIO 2
Prepara due grafici con dimensioni rispettivamente da una a due colonne (85mm e 180 mm)
verifica leggibilità dei testi

ESERCIZIO 3
Genera un grafico in bianco/nero utilizzando diversi stili di linea per distinguere almeno
tre serie di dati

ESERCIZIO 4
Aggiungere annotazioni a un grafico che evidenziano picchi o punti particolari, mantenendo coerenza
con font e stile complessivo

"""

import numpy as np
import matplotlib.pyplot as plt


# Esercizio 1
# Creare un grafico di funzione matematica e salvarlo in PNG e PDF, impostando la risoluzione a 300 DPI. Confrontare i due formati.


if False:
    # Dati
    x = np.linspace(0, 10, 500)
    y = np.sin(x)

    # Creazione grafico
    plt.figure(figsize=(6,4))
    plt.plot(x, y, label='sin(x)', color='blue', linewidth=2)
    plt.title("Funzione Sin(x)")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    plt.legend()
    plt.grid(True)

    # Salvataggio con alta risoluzione
    plt.savefig("grafico_sin.png", dpi=300)
    plt.savefig("grafico_sin.pdf", dpi=300)

    plt.show()

    print("Grafico salvato in 'grafico_sin.png' e 'grafico_sin.pdf' con risoluzione 300 DPI.")


# Esercizio 2
# Preparare due grafici con dimensioni rispettivamente da una e due colonne (85 mm e 180 mm), verificando la leggibilità dei testi.

if False:
    # Conversione da mm a pollici (1 pollice = 25.4 mm)
    col1 = 85 / 25.4
    col2 = 180 / 25.4

    x = np.linspace(0, 10, 200)
    y = np.exp(-x/3) * np.sin(2*x)

    # Grafico 1 colonna
    plt.figure(figsize=(col1, col1*0.7))
    plt.plot(x, y, color='darkorange', linewidth=1.5)
    plt.title("Grafico 1 colonna (85 mm)", fontsize=8)
    plt.xlabel("x", fontsize=7)
    plt.ylabel("y", fontsize=7)
    plt.tight_layout()
    plt.show()

    # Grafico 2 colonne
    plt.figure(figsize=(col2, col2*0.6))
    plt.plot(x, y, color='royalblue', linewidth=2)
    plt.title("Grafico 2 colonne (180 mm)", fontsize=10)
    plt.xlabel("x", fontsize=9)
    plt.ylabel("y", fontsize=9)
    plt.tight_layout()
    plt.show()   

# Esercizio 3
# Generare un grafico in bianco e nero utilizzando diversi stili di linea per distinguere almeno tre serie di dati.

if False:
    x = np.linspace(0, 10, 400)
    y1 = np.sin(x)
    y2 = np.cos(x)
    y3 = np.sin(x) * np.cos(2*x)

    plt.figure(figsize=(7,4))
    plt.plot(x, y1, linestyle='-', color='black', label='sin(x)')
    plt.plot(x, y2, linestyle='--', color='black', label='cos(x)')
    plt.plot(x, y3, linestyle='-.', color='black', label='sin(x)*cos(2x)')

    plt.title("Grafico in Bianco e Nero con Stili Diversi", fontsize=10)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.tight_layout()
    plt.show()



# Esercizio 4
# Aggiungere annotazioni a un grafico che evidenzino picchi o punti particolari, mantenendo coerenza con font e stile complessivo.

if True:

    x = np.linspace(0, 10, 500)
    y = np.sin(x) * np.exp(-x/5)

    plt.figure(figsize=(7,4))
    plt.plot(x, y, color='teal', linewidth=2)
    plt.title("Funzione con Annotazioni", fontsize=12, fontweight='bold')
    plt.xlabel("x", fontsize=10)
    plt.ylabel("y", fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)

    # Trova il picco massimo
    max_idx = np.argmax(y)
    x_max, y_max = x[max_idx], y[max_idx]

    # Aggiungi annotazione
    plt.scatter(x_max, y_max, color='red', zorder=5)
    plt.annotate(
        "Picco massimo",
        xy=(x_max, y_max),
        xytext=(x_max+1, y_max+0.2),
        arrowprops=dict(facecolor='red', shrink=0.05, width=1, headwidth=6),
        fontsize=9,
        color='darkred',
        fontweight='bold'
    )

    # Aggiungi un'altra annotazione su un punto notevole
    plt.annotate(
        "Smorzamento visibile",
        xy=(7, np.sin(7)*np.exp(-7/5)),
        xytext=(7.5, 0.3),
        arrowprops=dict(facecolor='gray', arrowstyle="->", lw=1),
        fontsize=9,
        color='gray'
    )

    plt.tight_layout()
    plt.show()    



"""
ESERCIZIO 1:
* Vendite settimanali: annota il massimo con freccia e marker

ESERCIZIO 2:
* Serie sportiva: evidenzia le vittorie con marker verdi e aggiungi annotazione sulla serie
più lunga di successi

ESERCIZIO 3:
* Dati finanziari: aggiunti testi statici che mostrino zone di guadagno e perdita, più
annotazione sul valore più recente

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#ESERCIZIO 1
if False: 
    settimane = pd.date_range("2025-01-01", periods=12, freq="W")
    vendite = np.random.randint(200, 800, len(settimane))
    df = pd.DataFrame({"settimana": settimane, "vendite": vendite})
    df.set_index("settimana")
    df.sort_index(ascending=True)
    fig,ax=plt.subplots(figsize=(10,6))
    ax.plot(df["settimana"], df["vendite"], marker="o", color="blue", label="Vendite Settimanali"   )

    max_idx = df["vendite"].idxmax()
    min_idx = df["vendite"].idxmin()
    ultimo_idx = (df.index[-1],df.columns[-1])
    #print(ultimo_idx)

    ax.annotate(
        f"Massimo: {vendite[max_idx]}",
        xy=(settimane[max_idx], vendite[max_idx]),
        xytext=(settimane[max_idx] + pd.Timedelta(weeks=1), vendite[max_idx] + 20),
        arrowprops=dict(facecolor="black", shrink=0.05),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
    )
    ax.annotate(
        f"Minimo: {vendite[min_idx]}",
        xy=(settimane[min_idx], vendite[min_idx]),
        xytext=(settimane[min_idx] + pd.Timedelta(weeks=1), vendite[min_idx] + 20),
        arrowprops=dict(facecolor="black", shrink=0.05),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
    )   
    ax.annotate(
        f"Ultimo: {df.iloc[-1,-1]}",
        xy=(settimane[-1], vendite[-1]),
        xytext=(settimane[-1] + pd.Timedelta(weeks=1), vendite[-1] + 20),
        arrowprops=dict(facecolor="black", shrink=0.05),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
    ) 
    ax.annotate(
        f"Primo: {df.iloc[0,0]}",
        xy=(settimane[0], vendite[0]),
        xytext=(settimane[0] + pd.Timedelta(weeks=1), vendite[0] + 20),
        arrowprops=dict(facecolor="black", shrink=0.05),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
    )         

    plt.show()


#ESERCIZIO 2
if False:
    partite = pd.date_range("2025-01-01", periods=20, freq="W")
    risultati = np.random.choice(["V", "P"], size=len(partite), p=[0.6, 0.4])
    df_sport = pd.DataFrame({"partita": partite, "risultato": risultati})
    df_sport.set_index("partita")
    df_sport.sort_index(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    print(df_sport)
    ax.plot(df_sport["partita"], np.arange(len(df_sport)), marker="None", color="blue", label="Partite Giocate")
    ax.plot(df_sport["partita"], np.arange(len(df_sport)), marker=".", color="red", label="Partite Giocate", linestyle="None")
    #non ricalcolo l'indice in questo modo rimane uguale al df df_sport
    #vittorie = df_sport[df_sport["risultato"] == "V"].reset_index(drop=True)
    vittorie = df_sport[df_sport["risultato"] == "V"]
    ax.plot(vittorie["partita"], vittorie.index, marker="o", color="green", label="Vittorie", linestyle="None")
    # Evidenzia la serie più lunga di vittorie
    max_streak = 0
    current_streak = 0
    start_idx = 0
    for i in range(len(df_sport)):
        if df_sport.loc[i, "risultato"] == "V":
            current_streak += 1
            if current_streak == 1:
                temp_start_idx = i
            if current_streak > max_streak:
                max_streak = current_streak
                start_idx = temp_start_idx
        else:
            current_streak = 0
    if max_streak > 0:
        end_idx = start_idx + max_streak - 1
        ax.annotate(
            f"Serie più lunga di vittorie: {max_streak}",
            xy=(df_sport.loc[end_idx, "partita"], end_idx),
            xytext=(df_sport.loc[end_idx, "partita"] + pd.Timedelta(weeks=1), end_idx + 2),
            arrowprops=dict(facecolor="black", shrink=0.05),
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3)
        )
    plt.show()  

#ESERCIZIO 3

if True:
    # Simuliamo prezzi giornalieri
    #np.random.seed(0)
    date = pd.date_range("2025-01-01", periods=60)
    prezzi = 100 + np.cumsum(np.random.randn(60))
    print(prezzi)

    # Calcola variazioni rispetto al valore iniziale
    iniziale = prezzi[0]
    variazioni = prezzi - iniziale
    #print(variazioni)
    quota_sotto = (prezzi < iniziale).mean()
    quota_sopra = (prezzi > iniziale).mean()
    print(f"quota sotto inizio: {quota_sotto}, quote sopra inizio: {quota_sopra}")

    # Grafico
    plt.figure(figsize=(10,6))
    plt.plot(date, prezzi, color='steelblue', linewidth=2, label="Prezzo")
    plt.fill_between(date, prezzi, iniziale, where=(prezzi >= iniziale),
                     color='green', alpha=0.2, label='Zona di guadagno')
    plt.fill_between(date, prezzi, iniziale, where=(prezzi < iniziale),
                     color='red', alpha=0.2, label='Zona di perdita')
    #riga quota iniziale
    plt.axhline(iniziale,color="black",linewidth=2, label="Iniziale")
    # Annotazione sul valore più recente
    ultimo_valore = prezzi[-1]
    plt.scatter(date[-1], ultimo_valore, color='black', s=100, zorder=5)
    plt.annotate(
        f"Valore attuale: {ultimo_valore:.2f}",
        xy=(date[-1], ultimo_valore),
        xytext=(date[-15], ultimo_valore + 3),
        arrowprops=dict(facecolor='black', arrowstyle='->'),
        fontsize=10, color='black'
    )
    print(len(date)/2)
    # Testi statici
    plt.text(date[5], iniziale + 1, "Zona di Guadagno", color='green', fontsize=10)
    plt.text(date[5], iniziale - 1, "Zona di Perdita", color='red', fontsize=10)

    plt.title("Andamento Finanziario con Zone di Guadagno e Perdita")
    plt.xlabel("Data")
    plt.ylabel("Prezzo (€)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()  


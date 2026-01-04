"""
ESERCIZIO 1
* Consumi energetici domestici: dataset con misurazioni orarie di consumi. Ricalcola
i valori medi giornalieri e settimanali, confronta i grafici e spiega come 
cambia la leggibilità dei picci di consumo

ESERCIZIO 2
* Serie epidemica: applica smoothing esponenziale a una serie di nuovi casi giornalieri
e confronta il risultato con la media mobile a 7 giorni. Quale dei due metodi è più
sensibile ai cambiamenti recenti=

ESERCIZIO 3
* Trasporto pubblico: prendi dati giornalieri di passeggerei e confrontali
con le temperature medie usanto doppi assi. Prova anche la normalizzazione e spiega
quale rappresentazione comunica meglio la relazione.

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if False:

    dates = pd.date_range("2025-01-01", periods=30*24, freq="H")
    consumo_watt = np.random.normal(300, 50, size=len(dates)) + np.sin(np.linspace(0, 20*np.pi, len(dates)))*50
    df_energy = pd.DataFrame({"datetime": dates, "consumo_W": consumo_watt})

    #calcolo valori medi giornalieri
    df_energy.set_index("datetime", inplace=True)
    #daily_mean = df_energy.resample("D", on="datetime").mean()
    daily_mean = df_energy.resample("D").mean().reset_index() #posso non indicare il campo su cui fare resample perchè data è indice
    weekly_mean = df_energy.resample("W").mean().reset_index()
    #Plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_mean["datetime"], daily_mean["consumo_W"], marker="o", label="Media Giornaliera", color="blue")
    ax.plot(weekly_mean["datetime"], weekly_mean["consumo_W"], marker="s", label="Media Settimanale", color="red", linewidth=2)
    ax.set_title("Consumi Energetici Domestici: Media Giornaliera vs Settimanale")
    ax.set_xlabel("Data")
    ax.set_ylabel("Consumo (Watt)")
    ax.legend()
    plt.show()
    print("Analisi:")
    print("La media giornaliera smussa le fluttuazioni orarie evidenziando picchi più chiari,")
    print("mentre la media settimanale riduce ulteriormente la variabilità rendendo meno visibili i picchi giornalieri ma più leggibile il trend complessivo.")


if False:
    # Genero dati fittizi
    dates = pd.date_range("2025-01-01", periods=60, freq="D")
    new_cases = np.random.poisson(200, size=60) + np.linspace(0, 1000, 60).astype(int)
    df_cases = pd.DataFrame({"date": dates, "new_cases": new_cases})

    # Media mobile 7 giorni
    df_cases["MA7"] = df_cases["new_cases"].rolling(window=7, min_periods=1).mean()

    # Smoothing esponenziale (alpha=0.3)
    df_cases["EWMA"] = df_cases["new_cases"].ewm(alpha=0.3,adjust=False).mean()
    #df_cases["EWMA"] = df_cases["new_cases"].ewm(alpha=0.3,adjust=True).mean()

    # Grafico confronto
    plt.figure(figsize=(12,5))
    plt.plot(df_cases["date"], df_cases["new_cases"], color='lightgray', alpha=0.5, label="Originale")
    plt.plot(df_cases["date"], df_cases["MA7"], color='blue', label="Media mobile 7 giorni")
    plt.plot(df_cases["date"], df_cases["EWMA"], color='red', label="Smoothing esponenziale")
    plt.title("Nuovi casi giornalieri - confronto smoothing")
    plt.xlabel("Data")
    plt.ylabel("Nuovi casi")
    plt.legend()
    plt.tight_layout()
    plt.show()  

    print("Analisi:")
    print("Lo smoothing esponenziale reagisce più rapidamente ai cambiamenti recenti rispetto alla media mobile,")
    print("che invece smussa uniformemente i valori su 7 giorni.")

if True:
    # Trasporto pubblico: prendi dati giornalieri di passeggeri e confrontali con le temperature medie usando doppi assi.
    # Prova anche la normalizzazione e spiega quale rappresentazione comunica meglio la relazione.

    np.random.seed(42)

    # Genero dati fittizi
    dates = pd.date_range("2025-01-01", periods=60, freq="D")
    passengers = np.random.randint(1000, 5000, size=60)
    temperature = np.random.uniform(-5, 25, size=60)

    df_transport = pd.DataFrame({"date": dates, "passengers": passengers, "temperature": temperature})

    # Doppio asse
    fig, ax1 = plt.subplots(figsize=(12,5))
    ax1.plot(df_transport["date"], df_transport["passengers"], color='blue', label='Passeggeri')
    ax1.set_xlabel("Data")
    ax1.set_ylabel("Passeggeri", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    ax2 = ax1.twinx()
    ax2.plot(df_transport["date"], df_transport["temperature"], color='red', linestyle='--', label='Temperatura')
    ax2.set_ylabel("Temperatura (°C)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.suptitle("Trasporto pubblico vs temperatura")
    fig.tight_layout()
    plt.show()

    # Normalizzazione 0-1
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    df_transport_norm = df_transport.copy()
    df_transport_norm[["passengers","temperature"]] = scaler.fit_transform(df_transport[["passengers","temperature"]])

    plt.figure(figsize=(12,5))
    plt.plot(df_transport_norm["date"], df_transport_norm["passengers"], color='blue', label='Passeggeri (norm)')
    plt.plot(df_transport_norm["date"], df_transport_norm["temperature"], color='red', linestyle='--', label='Temperatura (norm)')
    plt.title("Trasporto pubblico vs temperatura - normalizzati")
    plt.xlabel("Data")
    plt.ylabel("Valori normalizzati (0-1)")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print("Analisi:")
    print("Il doppio asse mostra chiaramente le scale differenti ma può confondere visivamente.")
    print("La normalizzazione porta entrambe le variabili su scala 0-1, evidenziando meglio la relazione tra passeggeri e temperatura")






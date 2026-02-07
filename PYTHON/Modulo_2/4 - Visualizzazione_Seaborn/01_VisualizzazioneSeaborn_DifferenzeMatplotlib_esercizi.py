

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Esercizio 1
# Crea un dataset sintetico con tre colonne: “Categoria”, “Valore” e “Gruppo”.
# Realizza un bar chart con Matplotlib mostrando il valore medio per categoria.
# Ripeti lo stesso grafico con Seaborn (sns.barplot()) utilizzando hue="Gruppo" e una palette personalizzata.
# Confronta il numero di righe di codice e descrivi in un commento le differenze.

if False:
    # Dataset sintetico
    np.random.seed(0)
    df = pd.DataFrame({
        "Categoria": np.repeat(["A", "B", "C"], 10),
        "Valore": np.random.randint(10, 100, 30),
        "Gruppo": np.tile(["X", "Y"], 15)
    })
    print(df)
    media_categoria = df.groupby("Categoria")["Valore"].mean()
    plt.figure(figsize=(6, 4))
    plt.bar(media_categoria.index, media_categoria.values, color="skyblue", edgecolor="black")
    plt.title("Valore medio per categoria (Matplotlib)")
    plt.xlabel("Categoria")
    plt.ylabel("Valore medio")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    plt.figure(figsize=(6, 4))
    sns.barplot(data=df, x="Categoria", y="Valore", hue="Gruppo", palette="viridis")
    plt.title("Valore medio per categoria e gruppo (Seaborn-barplot)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


# Esercizio 2
# Carica il dataset tips di Seaborn.
# Crea un sns.lmplot() per mostrare la relazione tra “total_bill” e “tip”, con regressione per sesso.
# Crea poi un sns.violinplot() per la distribuzione delle mance per giorno.
# Applica un tema e una palette.
# Commenta come Seaborn gestisce automaticamente legenda, regressione e formattazione.
if True:

    # Dataset integrato
    tips = sns.load_dataset("tips")

    # Tema e palette
    sns.set_theme(style="whitegrid", palette="tab10")
    sex_colors = {"Male": "deepskyblue", "Female": "hotpink"}

    # Relazione tra conto totale e mancia, suddivisa per sesso
    sns.lmplot(data=tips, x="total_bill", y="tip", hue="sex", palette=sex_colors, aspect=1.2, height=5)
    #sns.regplot(data=tips, x="total_bill", y="tip", hue="sex", aspect=1.2, height=5)
    plt.title("Relazione tra Total Bill e Tip per Sesso")
    plt.show()

    # Distribuzione delle mance per giorno (due violini per sesso)
    plt.figure(figsize=(6, 4))
    sns.violinplot(data=tips, x="day", y="tip", hue="sex", palette="coolwarm")
    plt.title("Distribuzione delle mance per giorno")
    plt.show()
    # Distribuzione delle mance per giorno (un violino per entrambi i sessi)
    plt.figure(figsize=(6, 4))
    sns.violinplot(data=tips, x="day", y="tip", hue="sex", palette="coolwarm",split=True,inner="quartile")
    plt.title("Distribuzione delle mance per giorno")
    plt.show()    

    sns.lineplot(data=tips, x="day", y="total_bill")
    plt.title("LINEPLOT su sequenza record (non è tempo reale)")
    plt.show()    


# Esercizio 3
# Carica il dataset penguins di Seaborn.
# Genera un pairplot con hue="species".
# Crea una heatmap di correlazione con sns.heatmap().
# Aggiungi annotazioni e una colormap personalizzata.
# Commenta nel codice come questi grafici aiutano a capire pattern e correlazioni multiple.
if False:

    # Dati
    df = sns.load_dataset("penguins").dropna()
    print(df.head(20))

    # Pairplot per relazioni tra variabili numeriche
    sns.pairplot(data=df, hue="species", diag_kind="kde", palette="Set2")
    plt.suptitle("Relazioni tra variabili numeriche nel dataset Penguins", y=1.02)
    plt.show()

    # Heatmap di correlazione
    corr = df.select_dtypes(include="number").corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, linewidths=0.5)
    plt.title("Matrice di correlazione delle variabili numeriche")
    plt.show()

# Esercizio 4 
# Immagina due visualizzazioni:
# Una dashboard interattiva per confrontare vendite e profitti mensili (usa Seaborn).
# Un grafico per pubblicazione scientifica con layout e annotazioni precise (usa Matplotlib).

if False:
    # Dati 
    np.random.seed(42)
    mesi = pd.date_range("2024-01-01", periods=12, freq="M").strftime("%b")
    df = pd.DataFrame({
        "Mese": np.tile(mesi, 2),
        "Valore": np.random.randint(1000, 5000, 24),
        "Tipo": ["Vendite"] * 12 + ["Profitti"] * 12
    })
    #print(df)

    sns.set_theme(style="whitegrid", palette="pastel")
    sns.catplot(data=df, x="Mese", y="Valore", hue="Tipo", kind="bar", height=5, aspect=1.5)
    plt.title("Dashboard: Vendite e Profitti mensili")
    plt.xticks(rotation=45)
    plt.show()

    x = np.linspace(0, 10, 200)
    y = np.sin(x) + np.random.normal(0, 0.1, 200)

    plt.figure(figsize=(7, 4))
    plt.plot(x, y, label="Segnale misurato", color="navy")
    plt.axhline(0, color="gray", linestyle="--", alpha=0.6)
    plt.annotate("Punto di interesse", xy=(7.8, y[156]), xytext=(8.5, 0.8),
                arrowprops=dict(arrowstyle="->", color="red"))
    plt.title("Grafico scientifico con annotazioni personalizzate")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Ampiezza")
    plt.legend()
    plt.tight_layout()
    plt.show()
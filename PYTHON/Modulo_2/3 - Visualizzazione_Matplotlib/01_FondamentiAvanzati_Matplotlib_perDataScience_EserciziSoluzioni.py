# Esercizio 1 — Consegna

# Confronto vendite mensili per prodotto: creare un dataset multi-store, multi-prodotto e visualizzare le vendite mensili con subplot per store, aggiungendo legenda e annotazioni sui picchi.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Parametri dataset
stores = ["Store_A", "Store_B", "Store_C"]
products = ["Prod_1", "Prod_2", "Prod_3"]
months = pd.date_range("2025-01-01", periods=12, freq="MS")

# Generazione dati
data = []
for store in stores:
    for product in products:
        for month in months:
            sales = np.random.randint(50, 500)
            data.append([store, product, month, sales])
df_sales = pd.DataFrame(data, columns=["store", "product", "month", "sales"])

# Plot subplot per store
fig, axes = plt.subplots(len(stores), 1, figsize=(10, 6), sharex=True)
for i, store in enumerate(stores):
    ax = axes[i]
    for product in products:
        subset = df_sales[(df_sales["store"]==store) & (df_sales["product"]==product)]
        ax.plot(subset["month"], subset["sales"], label=product, marker='o')
        # annotazione picco
        max_idx = subset["sales"].idxmax()
        max_val = subset.loc[max_idx, "sales"]
        max_month = subset.loc[max_idx, "month"]
        ax.annotate(f"{max_val}", xy=(max_month, max_val), xytext=(0,5), textcoords="offset points")
    ax.set_title(f"Vendite mensili {store}")
    ax.set_ylabel("Sales")
    ax.legend()
plt.xlabel("Mese")
plt.tight_layout()
plt.show()

# Esercizio 2 — Consegna

# Distribuzione utenti per categoria: simulare utenti e transazioni, usare scatter plot con color map per categorie, dimensioni dei marker proporzionali al numero di transazioni.

np.random.seed(42)
n_users = 100
categories = ["A", "B", "C"]

users = pd.DataFrame({
    "user_id": np.arange(1, n_users+1),
    "x": np.random.rand(n_users)*100,
    "y": np.random.rand(n_users)*100,
    "category": np.random.choice(categories, n_users),
    "transactions": np.random.randint(1, 50, n_users)
})

plt.figure(figsize=(8,6))
scatter = plt.scatter(
    users["x"], users["y"], 
    c=users["category"].map({"A":0,"B":1,"C":2}), 
    s=users["transactions"]*10, cmap="viridis", alpha=0.7
)
plt.colorbar(scatter, ticks=[0,1,2], label="Categoria").set_ticklabels(categories)
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Distribuzione utenti per categoria (dimensione = n transazioni)")
plt.show()

# Esercizio 3 — Consegna

# Serie temporali con media mobile e soglie: creare serie giornaliere di traffico web, aggiungere media mobile, soglia critica, e annotare i giorni con picchi.

dates = pd.date_range("2025-01-01", periods=60, freq="D")
traffic = np.random.randint(100, 500, size=len(dates))
df_traffic = pd.DataFrame({"date":dates, "visitors":traffic})

# Media mobile 7 giorni
df_traffic["moving_avg"] = df_traffic["visitors"].rolling(window=7, min_periods=1).mean()

# Soglia critica
threshold = 400
df_traffic["critical"] = df_traffic["visitors"] > threshold

plt.figure(figsize=(12,5))
plt.plot(df_traffic["date"], df_traffic["visitors"], label="Traffic", marker='o')
plt.plot(df_traffic["date"], df_traffic["moving_avg"], label="7-day MA", linestyle="--")
plt.axhline(threshold, color='red', linestyle=":", label="Soglia critica")
# Annotazioni picchi
for idx, row in df_traffic[df_traffic["critical"]].iterrows():
    plt.annotate(f'{row["visitors"]}', xy=(row["date"], row["visitors"]), xytext=(0,5), textcoords="offset points")
plt.xlabel("Date")
plt.ylabel("Visitors")
plt.title("Traffico web giornaliero con media mobile e soglia critica")
plt.legend()
plt.tight_layout()
plt.show()

# Esercizio 4 — Consegna

# Heatmap di correlazioni: calcolare correlazioni tra più metriche di vendita, visualizzarle con colormap, aggiungere annotazioni numeriche.

import seaborn as sns

# Genero dati fittizi
np.random.seed(42)
df_metrics = pd.DataFrame({
    "sales": np.random.randint(50,500,100),
    "units": np.random.randint(1,50,100),
    "revenue": np.random.uniform(1000,10000,100),
    "profit": np.random.uniform(100,5000,100)
})

corr = df_metrics.corr()

plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Correlazioni metriche di vendita")
plt.tight_layout()
plt.show()

# Esercizio 5 — Consegna

# Dashboard multi-subplot: combinare line plot, bar plot e scatter plot per visualizzare vendite, unità e fatturato per più store, con layout leggibile e legenda comune.

stores = ["Store_A", "Store_B", "Store_C"]
months = pd.date_range("2025-01-01", periods=12, freq="MS")

dashboard_data = []
for store in stores:
    for month in months:
        units = np.random.randint(50,500)
        revenue = np.round(units * np.random.uniform(10,50),2)
        dashboard_data.append([store, month, units, revenue])

df_dash = pd.DataFrame(dashboard_data, columns=["store","month","units","revenue"])
df_dash["sales"] = np.round(df_dash["revenue"]/10 + np.random.randint(0,50, len(df_dash)))

fig, axes = plt.subplots(3,1, figsize=(10,12), sharex=True)
for i, store in enumerate(stores):
    subset = df_dash[df_dash["store"]==store]
    axes[i].plot(subset["month"], subset["sales"], label="Sales", marker='o')
    axes[i].bar(subset["month"], subset["units"], alpha=0.3, label="Units")
    axes[i].scatter(subset["month"], subset["revenue"]/50, color='red', label="Revenue (scaled)")
    axes[i].set_title(f"{store}")
    axes[i].legend()
plt.xlabel("Month")
plt.tight_layout()
plt.show()
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("TkAgg") 

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------------
# 1) Dimensioni: clienti e prodotti
# -----------------------------
REGIONI = ["Nord", "Centro", "Sud", "Isole", "Estero"]
N_CLIENTI = 100
N_PRODOTTI = 5

clienti = pd.DataFrame({
    "ClienteID": np.arange(1, N_CLIENTI + 1, dtype=np.int32),
    "Regione": np.random.choice(REGIONI, size=N_CLIENTI, replace=True)
})

prodotti = pd.DataFrame({
    "ProdottoID": np.arange(1, N_PRODOTTI + 1, dtype=np.int16),
    "Descrizione": [f"Prodotto {i:02d}" for i in range(1, N_PRODOTTI + 1)]
})

# mapping veloce (no join pesante a ogni chunk)
cliente_to_regione = dict(zip(clienti["ClienteID"].astype(int), clienti["Regione"]))
print(cliente_to_regione)

# -----------------------------
# 2) Fatti: vendite enormi su CSV (streaming in scrittura)
# -----------------------------
FILE_VENDITE = "vendite_enormi.csv"

def genera_vendite_csv_streaming(
    filename: str,
    n_righe: int = 2_000_000,
    chunk_write: int = 200_000,
    start_date: str = "2025-01-01",
    end_date: str = "2025-12-31",
    seed: int = 42
):
    """
    Genera un CSV enorme senza caricarlo tutto in RAM.
    """
    rng = np.random.default_rng(seed)

    # intervallo date: generiamo giorni come stringa YYYY-MM-DD
    giorni = pd.date_range(start_date, end_date, freq="D")
    giorni_str = giorni.strftime("%Y-%m-%d").to_numpy()

    # sovrascrivo file
    if os.path.exists(filename):
        os.remove(filename)

    written = 0
    first = True

    while written < n_righe:
        n = min(chunk_write, n_righe - written)

        # "vendite" plausibili: molti ordini piccoli, pochi grandi
        qta = rng.integers(1, 6, size=n, dtype=np.int16)  # 1..5

        chunk = pd.DataFrame({
            "Data": rng.choice(giorni_str, size=n, replace=True),
            "ProdottoID": rng.integers(1, N_PRODOTTI + 1, size=n, dtype=np.int16),
            "ClienteID": rng.integers(1, N_CLIENTI + 1, size=n, dtype=np.int32),
            "Qta": qta
        })

        chunk.to_csv(filename, index=False, mode="a", header=first)
        first = False
        written += n

# Se non vuoi rigenerare ogni volta, lascia il file e non rigenerarlo.
if not os.path.exists(FILE_VENDITE):
    print("Genero CSV vendite enorme...")
    genera_vendite_csv_streaming(FILE_VENDITE, n_righe=1_000_000, chunk_write=200_000)
    print("CSV generato:", FILE_VENDITE)

# -----------------------------
# 3) Dashboard streaming: 1 grafico per prodotto, barre per regione
# -----------------------------
CHUNK_READ = 100_000
UPDATE_EVERY_N_CHUNKS = 1  # aggiorna grafico ogni N chunk letti

# accumulatore: matrice [prodotto, regione] -> qta cumulata
# indicizziamo prodotti 1..5 e regioni 0..4
acc = np.zeros((N_PRODOTTI, len(REGIONI)), dtype=np.int64)

# lettore a chunk
def chunk_reader():
    for chunk in pd.read_csv(
        FILE_VENDITE,
        chunksize=CHUNK_READ,
        usecols=["ProdottoID", "ClienteID", "Qta"]  # Data non serve per cumulata
    ):
        # tipi leggeri
        chunk["ProdottoID"] = chunk["ProdottoID"].astype(np.int16)
        chunk["ClienteID"] = chunk["ClienteID"].astype(np.int32)
        chunk["Qta"] = pd.to_numeric(chunk["Qta"], errors="coerce").fillna(0).astype(np.int16)
        yield chunk

reader = chunk_reader()
chunks_processed = 0

# --- figura: 5 subplots (uno per prodotto)
fig, axes = plt.subplots(nrows=1, ncols=N_PRODOTTI, figsize=(18, 4), sharey=True)
fig.suptitle("Vendite per Regione (streaming cumulato) - 1 grafico per prodotto")

if N_PRODOTTI == 1:
    axes = [axes]

# creiamo barre fisse (5 regioni) per ogni prodotto
bars_by_product = []
x = np.arange(len(REGIONI))

for p in range(1, N_PRODOTTI + 1):
    ax = axes[p - 1]
    bars = ax.bar(x, [0]*len(REGIONI))
    ax.set_title(f"Prodotto {p:02d}")
    ax.set_xticks(x)
    ax.set_xticklabels(REGIONI, rotation=45, ha="right")
    ax.set_ylim(0, 10)  # verrà autoscalato dopo
    bars_by_product.append(bars)

axes[0].set_ylabel("Quantità cumulata")

def update(frame):
    global chunks_processed

    # processa 1 chunk per frame (puoi aumentare per accelerare)
    try:
        chunk = next(reader)
    except StopIteration:
        anim.event_source.stop()
        return []

    # mappa ClienteID -> Regione (senza join)
    regioni_chunk = chunk["ClienteID"].map(cliente_to_regione)

    # aggiungo colonna Regione al chunk
    chunk = chunk.assign(Regione=regioni_chunk)
    chunk = chunk.dropna(subset=["Regione"])

    # aggrego nel chunk per (ProdottoID, Regione)
    grp = chunk.groupby(["ProdottoID", "Regione"])["Qta"].sum()

    # aggiorno accumulatore
    for (pid, reg), qta in grp.items():
        p_idx = int(pid) - 1
        r_idx = REGIONI.index(reg)  # 5 regioni: lookup ok
        acc[p_idx, r_idx] += int(qta)

    chunks_processed += 1

    # aggiorna grafico ogni N chunk (per performance)
    if chunks_processed % UPDATE_EVERY_N_CHUNKS != 0:
        return []

    artists = []
    max_y = acc.max()
    # evita asse piatto
    ymax = max(10, int(max_y * 1.1))

    for p_idx in range(N_PRODOTTI):
        ax = axes[p_idx]
        ax.set_ylim(0, ymax)

        bars = bars_by_product[p_idx]
        for r_idx, rect in enumerate(bars):
            rect.set_height(acc[p_idx, r_idx])
            artists.append(rect)

    fig.canvas.draw_idle()
    return artists

anim = FuncAnimation(fig, update, interval=250, blit=False)
plt.tight_layout()
plt.show()

# Se vuoi vedere le dimensioni create:
# print(clienti.head())
# print(prodotti)

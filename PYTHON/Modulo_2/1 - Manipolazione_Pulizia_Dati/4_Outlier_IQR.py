# 4_Outlier_IQR.py
# pip install pandas matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- DATI DI ESEMPIO ---
# Sostituisci con i tuoi: ad es. df = pd.read_csv("dati.csv")
data = [10, 12, 13, 15, 18, 19, 20, 22, 100]
df = pd.DataFrame(data, columns=["Valori"])

# --- CALCOLO IQR ---
Q1 = df["Valori"].quantile(0.25)
Q3 = df["Valori"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# Flag outlier
df["Outlier"] = (df["Valori"] < lower) | (df["Valori"] > upper)

print(f"Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f}, Lower={lower:.2f}, Upper={upper:.2f}")
print(f"Outlier trovati:\n{df[df['Outlier']]}")
print(f"Tabella di riferimento: {df}")

# --- GRAFICO A BARRE ---
x = np.arange(len(df))
colors = ["tab:red" if is_out else "tab:blue" for is_out in df["Outlier"]]

plt.figure(figsize=(9, 4))
plt.bar(x, df["Valori"], color=colors)

# Linee soglia
plt.axhline(lower, linestyle="--", label=f"Limite inferiore ({lower:.2f})")
plt.axhline(upper, linestyle="--", label=f"Limite superiore ({upper:.2f})")

# Etichette outlier
for i, (val, is_out) in enumerate(zip(df["Valori"], df["Outlier"])):
    if is_out:
        plt.text(i, val, " outlier", va="bottom", ha="left", fontsize=9)

plt.xticks(x, [f"Idx {i}" for i in x])
plt.ylabel("Valori")
plt.title("Visualizzazione Outlier con Metodo IQR")
plt.legend(loc="best")
plt.tight_layout()

plt.show()

# Salva e mostra
if False:
    out_path = "barplot_outlier_iqr.png"
    plt.savefig(out_path, dpi=150)
    print(f"Immagine salvata: {out_path}")





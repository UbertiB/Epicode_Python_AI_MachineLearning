"""
Progetto #3

Progetto #3 — Creare una Dashboard Avanzata di Visualizzazione
Traccia:
Realizzare una dashboard interattiva per analizzare i dati di vendita e redditività di
un negozio online, usando Python (Pandas + Plotly Dash / Streamlit / Matplotlib / Seaborn).
Struttura del dataset:
• Order Date → Data dell'ordine
• Ship Date → Data di spedizione
• Category → Categoria prodotto (es. Furniture, O'ice Supplies, Technology)
• Sub-Category → Sottocategoria prodotto
• vendite → Vendite (€)
• Profit → Utile (€)
• Region → Area geografica
• State → Stato/Regione
• Quantity → Quantità venduta
Consegna
Parte 1 - Pulizia dati
1. Convertire le colonne data (Order Date, Ship Date) in formato datetime.
2. Controllare valori nulli e duplicati.
3. Creare una nuova colonna Year dall'Order Date.
Parte 2 - Analisi Esplorativa (EDA)
4. Totale vendite e profitti per anno.
5. Top 5 sottocategorie più vendute.
6. Mappa interattiva delle vendite

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np

import tkinter as tk
from tkinter import ttk

# ============================================================
# 1) CREAZIONE DATASET 
# ============================================================

np.random.seed(0)

Date_order = pd.date_range("2024-01-01", periods=730, freq="D").to_series(index=None)
Date_order.iloc[0] = pd.NaT #aggiungo valore null per successiva pulizia

delta = pd.to_timedelta(np.random.randint(1, 10, len(Date_order)), unit="D")
Date_ship = Date_order + delta  #data_ship prendere null di data_order, per successiva pulizia

Category=[f"Categoria{i}" for i in range(1,5)]
Sub_category=[f"Sottocagetoria{i}" for i in range(1,5)]
Region=["Nord","Centro","Sud","Isole",None] #includo null (per successiva pulizia)
State=["Europa","Asia","Africa","America",None] #includo null (per successiva pulizia)

df=pd.DataFrame({
    "date_order": Date_order,
     "date_ship": Date_ship,
     "category":np.random.choice(Category,len(Date_order)),
     "sub_category":np.random.choice(Sub_category,len(Date_order)),
     "vendite":np.random.randint(10,200,len(Date_order)),
     "region":np.random.choice(Region,len(Date_order)),
     "state":np.random.choice(State,len(Date_order)),
     "quantity":np.random.randint(1,20,len(Date_order)),
    })
df["costi"]=df["vendite"]+np.random.randint(-20,5,len(df))
df["utile"]=df["vendite"]-df["costi"]
df = pd.concat([df, df.iloc[:10]], ignore_index=True)  #creo duplicati per successiva gestione

# ============================================================
# 2) PARTE 1: PULIZIA DATI
# ============================================================

#print (df.head())

#cancellazione valori duplicati
df = df.drop_duplicates() 
#Identificazione valori nulli
print(f"Valori nulli PRIMA della sistemazione: \n{df.isna().sum()}")
#cancellazione valori nulla colonna data_order
df = df.dropna(subset=["date_order"])
#gestione valori nulli con mediana
df["quantity"]=df["quantity"].fillna(df["quantity"].median())
#gestione valori nulli con stringa costante
df["region"]=df["region"].fillna("Sconosciuta")
df["state"]=df["state"].fillna("Sconosciuta")
print(f"Valori nulli DOPO la sistemazione: \n{df.isna().sum()}")
#coonvertire colonne nel formato corretto
df["date_order"]=pd.to_datetime(df["date_order"],errors="coerce")
df["date_ship"]=pd.to_datetime(df["date_ship"],errors="coerce")
#converto le altre colonne
df["category"]=df["category"].astype("category")
df["sub_category"]=df["sub_category"].astype("category")
df["region"]=df["region"].astype("category")
df["state"]=df["state"].astype("category")
df["vendite"]=df["vendite"].astype("float32")
df["utile"]=df["utile"].astype("float32")
df["costi"]=df["costi"].astype("float32")
df["quantity"]=df["quantity"].astype("int32")
#creo nuove colonne
df["month"]=df["date_order"].dt.to_period("M")
df["Year"] = df["date_order"].dt.year
#creo indicce
df = df.set_index("date_order")

print (df.head())

# ============================================================
# 3) PARTE 2: EDA (console interattiva)
# ============================================================

#Totale vendite e profitti per anno.
tot_anno = df.groupby(df.index.year)[["vendite", "utile"]].sum().reset_index(names="year")
print(f"Totali per anno: \n{tot_anno}")

#Top 5 sottocategorie più vendute.
n=5
tot_n_sottocategorie = (df.groupby("sub_category", as_index=False)["vendite"].sum().sort_values("vendite", ascending=False).reset_index(drop=True))

print(tot_n_sottocategorie.head(5))


#Mappa interattiva delle vendite
#NOT PER DOCENTE:
#NON HO CAPITO COSA SI INTENDE PER MAPPA INTERATTIVA, PERTANTO FACCIO INTERATTIVITA 
#E UNA HEATMAP (mappa)
#SPERANDO DI ESEGUIRE CORRETTAMENTE LA CONSEGNA


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()
root.state("zoomed") #massimizza la finstra
root.title("Schermata Interattiva")

#colonna 0 filtri, colonna 1 grafico, colonna 2 colorm
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

#filtri
frm = ttk.LabelFrame(root, text="Parametri", padding=10)
frm.grid(row=0, column=0, rowspan=50, sticky="nsw", padx=10, pady=10)

#label stati selezionati
lbl_out = ttk.Label(root, text="Stati selezionati:", padding=10, relief="solid")
lbl_out.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

#creo la colormap dei stati (in modo che il colore dello stato sia uguale sempre e per tutti i grafici)
stati = sorted(df["state"].astype(str).unique()) #prendo gli stati unici
base_cmap = plt.cm.get_cmap("tab20", len(stati))
color_map = {s: base_cmap(i) for i, s in enumerate(stati)} #mappa stato/colore

#figura
fig=Figure(figsize=(9, 6))

gs=fig.add_gridspec(3, 3)                     
ax1=fig.add_subplot(gs[0,0])   #Vendite
ax2=fig.add_subplot(gs[0,1])   #Utile
ax3=fig.add_subplot(gs[1,0:2]) #Top 5
ax4=fig.add_subplot(gs[2,0:2]) #heatmpap
cax=fig.add_subplot(gs[2, 2])  #colorbar 

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=1, rowspan=50, sticky="nsew", padx=10, pady=10)

#checkbox stati
vars_stati={}
stati=sorted(df["state"].astype(str).unique())

def colora_barre(ax, ordine_stati):
    for bar, stato in zip(ax.patches, ordine_stati):
        bar.set_facecolor(color_map.get(stato, (0.5, 0.5, 0.5, 1.0)))
        
def aggiorna_grafico():
    selezionati = [s for s, v in vars_stati.items() if v.get()]
    d = df.reset_index()
    if selezionati:
        d = d[d["state"].astype(str).isin(selezionati)]
    else:
        d = d.iloc[0:0]  #vuoto

    #preparo per i df
    d["state"] = d["state"].astype(str) #toglo da categoria altrimenti lascia spazi vuoti
    d["region"] = d["region"].astype(str) #toglo da categoria altrimenti lascia spazi vuoti
    d["sub_category"] = d["sub_category"].astype(str) #toglo da categoria altrimenti lascia spazi vuoti
    #calcolo i df
    df_state = (d.groupby("state", as_index=False).agg(vendite=("vendite", "sum"),utile=("utile", "sum")).sort_values("vendite", ascending=False))
    df_top5 = (d.groupby("sub_category", as_index=False)["vendite"].sum().sort_values("vendite", ascending=False).head(5))
    pivot = (d.pivot_table(index="region", columns="state", values="vendite", aggfunc="sum", fill_value=0))    

    if df_state.empty: #se vuoto azzero tutto
        for ax in (ax1, ax2, ax3):
            ax.set_title("Nessun dato")
            ax.text(0.5, 0.5, "Nessuno stato selezionato",ha="center", va="center", transform=ax.transAxes)
            ax.clear()
        canvas.draw_idle()
        return    

    ordine = df_state["state"].tolist()

    for ax in fig.axes:
        ax.clear()

    #GRAFICO 1: Vendite per stato
    sns.barplot(data=df_state, x="state", y="vendite", order=ordine, ax=ax1)
    colora_barre(ax1,ordine)
    ax1.set_title("Vendite per Stato")
    ax1.set_xlabel("")
    ax1.tick_params(axis="x", rotation=30)

    #GRAFICO 2: Utile per stato
    sns.barplot(data=df_state, x="state", y="utile", order=ordine, ax=ax2)
    colora_barre(ax2,ordine)
    ax2.set_title("Utile per Stato")
    ax2.set_xlabel("")
    ax2.tick_params(axis="x", rotation=30)

    #GRAFICO 3: Top 5 sottocategorie
    sns.barplot(data=df_top5, x="sub_category", y="vendite", ax=ax3)
    ax3.set_title("Top 5 Sottocategorie per Vendite (filtrate)")
    ax3.set_xlabel("")
    ax3.tick_params(axis="x", rotation=20)

    #GRAFICO 4: Mappa iterativa
    sns.heatmap(pivot, ax=ax4, cbar=True, cbar_ax=cax)
    ax4.set_title("Mappa vendite (heatmap Region x State)")
  

    fig.tight_layout()
    canvas.draw_idle()

def aggiorna_output():
    selezionati = [s for s, v in vars_stati.items() if v.get()]
    lbl_out.config(text="Stati selezionati:\n" + (", ".join(selezionati) if selezionati else "(nessuna)"))
    aggiorna_grafico()

def tutti():
    for v in vars_stati.values():
        v.set(True)
    aggiorna_output()

def nessuno():
    for v in vars_stati.values():
        v.set(False)
    aggiorna_output()  

#checkbox
for i, s in enumerate(stati):
    v = tk.BooleanVar(value=True)
    vars_stati[s] = v
    ttk.Checkbutton(frm, text=s, variable=v, command=aggiorna_output).grid(row=i, column=0, sticky="w", padx=6, pady=2)

#button
r = len(stati) + 1
ttk.Button(frm, text="Tutti", command=tutti).grid(row=r, column=0, sticky="we", pady=(10, 2))
ttk.Button(frm, text="Nessuno", command=nessuno).grid(row=r+1, column=0, sticky="we", pady=2)
ttk.Button(frm, text="Chiudi", command=root.destroy).grid(row=r+2, column=0, sticky="we", pady=(2, 0))

#primo
aggiorna_output()
#loop
root.mainloop()      
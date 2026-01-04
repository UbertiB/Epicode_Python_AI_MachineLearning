"""
ESERCIZIO 1
* Confronto vendite mensile per prodotto: crea un dataset multi-Mese,
multi-prodotto e visualizzare le vendite mensili con subplot per Mese,
aggiungendo legenda e annotazioni sui picchi

ESERCIZIO 2
* Distribuzione utenti per categoria: simulare utenti e transazioni, usare
scatter plot con color map per categorie, dimensioni dei market proporzionati al
numero di transazioni.

ESERCIZIO 3
* Serie temporali con media mobile e soglie: creare serie giornaliere di 
traffico web, aggiungere media mobile, soglia critica, e annotare i giorni con picchi

ESERCIZIO 4
* Heatmap di correlazioni: calcolare correlazioni tra più metriche di vendita,
visualizzare con colormap, aggiungere annotazioni numeriche

ESERCIZIO 5
* Dashboard multi-subplot: combinare linee plot, bar plot e scatter plot
per visualizzare vendite, unità e fatturato per più Mese, con layout 
leggibile e legenda comune

"""

#ESECUZIONE

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap

"""
ESERCIZIO 1
* Confronto vendite mensile per prodotto: crea un dataset multi-Mese,
multi-prodotto e visualizzare le vendite mensili con subplot per Mese,
aggiungendo legenda e annotazioni sui picchi

"""

#
# GRAFICO PLOT (linea)
#
if False:
        numero_vendite=20  #ogni negozio ha 20 registratori di cassa

        #Costruisco i dati
        Negozi = ["Store_A", "Store_B", "Store_C"]
        Prodotti = ["Prod_1", "Prod_2", "Prod_3"]
        Mesi = pd.date_range("2025-01-01", periods=12, freq="MS")

        data = []
        for n in Negozi:
                for p in Prodotti:
                        for m in Mesi:
                                for _ in range(numero_vendite):
                                        vendite=np.random.randint(1,200)
                                        data.append([n,p,m,vendite])
        #print(data)
        df_vendite=pd.DataFrame(data=data,columns=["Negozio","Prodotto","Mese","Vendite"])
        df = (df_vendite.groupby(["Negozio","Prodotto","Mese"], as_index=False)["Vendite"].sum().sort_values(["Negozio", "Prodotto", "Mese"]))
        #print(df.head(50))

        #Subplot per ogni negozio
        fig, axes = plt.subplots(len(Negozi), 1, figsize=(10, 8), sharex=True)
        for negozioID,negozio in enumerate(Negozi):
                #print (negozioID,negozio)
                for p in Prodotti:
                        #print(p)
                        subset=df[(df["Negozio"]==negozio) & (df["Prodotto"]==p)]
                        #print(subset)
                        subset = subset.sort_values("Mese")
                        axes[negozioID].plot(subset["Mese"], subset["Vendite"], label=p, marker='o')
                        # annotazione picco
                        if True:
                                max_idx = subset["Vendite"].idxmax()
                                max_val = subset.loc[max_idx, "Vendite"]
                                max_month = subset.loc[max_idx, "Mese"]
                                axes[negozioID].annotate(f"{max_val}", xy=(max_month, max_val), xytext=(0,5), textcoords="offset points")                
                axes[negozioID].set_title(f"Vendite mensili {negozio}")
                axes[negozioID].set_xlabel("Mese")
                axes[negozioID].set_ylabel("Vendite")
                axes[negozioID].legend()    
        plt.xlabel("Mese")
        plt.tight_layout()
        plt.show() 

"""
ESERCIZIO 2
* Distribuzione utenti per categoria: simulare utenti e transazioni, usare
scatter plot con color map per categorie, dimensioni dei marker proporzionati al
numero di transazioni.                           
"""
#
# GRAFICO SCATTER (a punti)
#
if False:

        categorie = ["A", "B", "C"]
        n_utenti = 100

        df_Utenti = pd.DataFrame({
                "UtenteID": np.arange(1, n_utenti + 1),
                "Categoria": np.random.choice(categorie, size=n_utenti),
                "Transazioni": np.random.randint(1, 20, size=n_utenti),
                "CoordinataX": np.random.rand(n_utenti) * 100,
                "CoordinataY": np.random.rand(n_utenti) * 100,
        })
        #print(df_Utenti)

        # PD.CATEGORICAL crea (o converte) una colonna di tipo categorical
        #tipo dati categoria da non utilizzare se la colonna ha dati quasi tutti diversi (tipo ragioni sosiali), 
        #la colonna deve avere pochi valori distinti
        #se è indicato un valore al di fuori delle categorie previste il valore diventa null
        cat = pd.Categorical(df_Utenti["Categoria"], categories=categorie, ordered=True)

        codes = cat.codes  # array di int: 0..3 (oppure -1 se categoria non prevista)
        #cat.categories   # Index(['A','B','C'], dtype='object')
        #cat.codes        # array([0,1,0,2,1,0], dtype=int8
        fig, ax = plt.subplots(figsize=(10, 6))

        #COLORI
        #prendo solo i primi colori della palette "tab10"
        #i colori che prendo sono quanti le categorie che nello scatter dovrò colorare, questo perchè se li prendo tutti e 10
        #gli altri colori (visualizzati nella colormap) sembrerebbero non utilizzati (in realtà non sono presenti categoria quindi non utilizati)
        #c=codes c associa i colori, quindi associo i colori in base alle categorie, poi con cmap definisco quali colori
        #s definisce la dimensione dei punti (scatter)
        base = plt.get_cmap("tab10")
        cmap3 = ListedColormap(base.colors[:3], name="tab3")  #prendo solo i primi 3 colori con [:3]
        scatter = ax.scatter(df_Utenti["CoordinataX"],df_Utenti["CoordinataY"], c=codes, s=df_Utenti["Transazioni"] * 10, cmap=cmap3, alpha=0.7)  

        #COLORBAR
        cb = plt.colorbar(scatter, ax=ax, ticks=range(len(categorie)))
        cb.set_label("Categoria")
        cb.set_ticklabels(categorie)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Distribuzione utenti per categoria (dimensione = n transazioni)")
        plt.show()

"""
ESERCIZIO 3
* Serie temporali con media mobile e soglie: creare serie giornaliere di
traffico web, aggiungere media mobile, soglia critica, e annotare i giorni con picchi.

"""

#
# FINESTRE TEMPORALI
#
if False:
        dates = pd.date_range("2025-01-01", periods=60, freq="D")
        traffic = np.random.randint(100, 500, size=len(dates))

        df_traffic = pd.DataFrame({"date":dates, "visitors":traffic})

        # Media mobile 7 giorni (finestre temporali)
        print(df_traffic.head(5))
        df_traffic["moving_avg"] = df_traffic["visitors"].rolling(window=7, min_periods=1).mean()
        print(df_traffic.head(5))

        # Soglia critica
        threshold = df_traffic["visitors"].median()#400
        df_traffic["critical"] = df_traffic["visitors"] > threshold
        print(df_traffic.head(5))

        #più grafici all'interno dello stesso grafico
        plt.figure(figsize=(12,5))
        plt.plot(df_traffic["date"], df_traffic["visitors"], label="Traffic", marker='o')
        plt.plot(df_traffic["date"], df_traffic["moving_avg"], label="7-day MA", linestyle="--")
        plt.axhline(threshold, color='red', linestyle=":", label="Soglia mediana")
        # # Annotazioni picchi
        for idx, row in df_traffic[df_traffic["critical"]].iterrows():
                plt.annotate(f'{row["visitors"]}', xy=(row["date"], row["visitors"]), xytext=(0,5), textcoords="offset points")
        plt.xlabel("Date")
        plt.ylabel("Visitors")
        plt.title("Traffico web giornaliero con media mobile e soglia mediana")
        plt.legend()
        plt.tight_layout()
        plt.show()

# # Esercizio 4 — Consegna

# # Heatmap di correlazioni: calcolare correlazioni tra più metriche di vendita, visualizzarle con colormap, aggiungere annotazioni numeriche.

#la MATRICE DI CORRELAZIONE restituisce un coefficiente tra  che misura quanto due variabili si muovono insieme
# ci sono diversi algoritmi, quello predefinito è 'pearson' (lineare)
#import seaborn as sns
if False:
        # Genero dati fittizi
        np.random.seed(42)
        df_metrics = pd.DataFrame({
        "sales": np.random.randint(50,500,100),
        "units": np.random.randint(1,50,100),
        "revenue": np.random.uniform(1000,10000,100),
        "profit": np.random.uniform(100,5000,100)})

        corr = df_metrics.corr()

        plt.figure(figsize=(6,5)),
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlazioni metriche di vendita")
        plt.tight_layout()
        plt.show()


if True:
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
            axes[i].plot(subset["month"], subset["sales"], label="Sales (plot)", marker='o')
            axes[i].bar(subset["month"], subset["units"], alpha=0.5, label="Units (bar)")
            axes[i].scatter(subset["month"], subset["revenue"]/50, color='red', label="Revenue (scatter)")
            axes[i].set_title(f"{store}")
            axes[i].legend()
        plt.xlabel("Month")
        plt.tight_layout()
        plt.show()        

 
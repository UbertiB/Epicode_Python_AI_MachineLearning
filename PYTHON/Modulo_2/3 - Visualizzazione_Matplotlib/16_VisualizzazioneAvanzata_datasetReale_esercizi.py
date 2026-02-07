# Esercizio 1
# Carica il dataset “AB_NYC_2019.csv” e crea un boxplot che mostri la distribuzione dei prezzi per quartiere, 
# confrontando Manhattan e Brooklyn.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Caricamento dataset
df = pd.read_csv("AB_NYC_2019.csv")

# Mostra colonne per sicurezza
print("Colonne dataset:", df.columns.tolist())

# Filtra i due quartieri richiesti
df_filtered = df[df['neighbourhood_group'].isin(['Manhattan', 'Brooklyn'])]

# Boxplot
plt.figure(figsize=(8,5))
sns.boxplot(data=df_filtered, x='neighbourhood_group', y='price', palette='coolwarm', showfliers=False)
plt.yscale('log')  # scala log per rendere leggibile (prezzi molto variabili)
plt.title("Distribuzione prezzi per quartiere (Manhattan vs Brooklyn)")
plt.xlabel("Quartiere")
plt.ylabel("Prezzo (scala log)")
plt.tight_layout()
plt.show()


# Esercizio 2
# Realizza una mappa scatter georeferenziata dei soli annunci con prezzo inferiore a 200 dollari, 
# per individuare le aree più economiche.

import matplotlib.pyplot as plt
import seaborn as sns

# Filtro annunci economici
cheap_df = df[df['price'] < 200]

plt.figure(figsize=(7,6))
plt.scatter(cheap_df['longitude'], cheap_df['latitude'],c=cheap_df['price'], cmap='viridis', s=8, alpha=0.5)
plt.colorbar(label='Prezzo ($)')
plt.title("Annunci con prezzo < 200$ (mappa NYC)")
plt.xlabel("Longitudine")
plt.ylabel("Latitudine")
plt.tight_layout()
plt.show()

# Esercizio 3
# Crea un grafico con regressione tra disponibilità annuale e prezzo, 
# analizzando se gli annunci più disponibili tendono a essere più economici.

import seaborn as sns
import matplotlib.pyplot as plt

# Filtro per evitare outlier estremi di prezzo
df_reg = df[df['price'] < 500]

plt.figure(figsize=(7,5))
sns.regplot(data=df_reg, x='availability_365', y='price',scatter_kws={'alpha':0.3, 's':10}, line_kws={'color':'red'}, ci=None)
plt.title("Relazione tra disponibilità annuale e prezzo")
plt.xlabel("Disponibilità annuale (giorni)")
plt.ylabel("Prezzo ($)")
plt.tight_layout()
plt.show()

# Esercizio 4

# Combina in un’unica figura i tre grafici principali (boxplot, scatter geospaziale, regressione) utilizzando un layout con più subplot.

import matplotlib.pyplot as plt
import seaborn as sns

# Prepara i dataset filtrati come sopra
df_box = df[df['neighbourhood_group'].isin(['Manhattan', 'Brooklyn'])]
df_map = df[df['price'] < 200]
df_reg = df[df['price'] < 500]

# Layout 2x2, con un riquadro vuoto in basso a destra
fig, axs = plt.subplots(2, 2, figsize=(12,10))

# Boxplot Manhattan vs Brooklyn
sns.boxplot(
    data=df_box, x='neighbourhood_group', y='price',
    ax=axs[0,0], palette='coolwarm', showfliers=False
)
axs[0,0].set_yscale('log')
axs[0,0].set_title("Distribuzione prezzi per quartiere")
axs[0,0].set_xlabel("")
axs[0,0].set_ylabel("Prezzo (log)")

# Scatter geospaziale
sc = axs[0,1].scatter(
    df_map['longitude'], df_map['latitude'],
    c=df_map['price'], cmap='viridis', s=6, alpha=0.5
)
axs[0,1].set_title("Annunci < 200$ (Mappa NYC)")
axs[0,1].set_xlabel("Longitudine")
axs[0,1].set_ylabel("Latitudine")
fig.colorbar(sc, ax=axs[0,1], label='Prezzo ($)', fraction=0.046)

# Regressione prezzo vs disponibilità
sns.regplot(
    data=df_reg, x='availability_365', y='price',
    ax=axs[1,0], scatter_kws={'alpha':0.3, 's':10}, line_kws={'color':'red'}
)
axs[1,0].set_title("Prezzo vs Disponibilità annuale")
axs[1,0].set_xlabel("Disponibilità (giorni)")
axs[1,0].set_ylabel("Prezzo ($)")

# Pannello vuoto (in basso a destra)
axs[1,1].axis('off')
axs[1,1].text(0.5, 0.5, "Airbnb NYC 2019\nAnalisi esplorativa", ha='center', va='center', fontsize=14, color='gray')

plt.suptitle("Analisi prezzi e disponibilità Airbnb NYC", fontsize=16)
plt.tight_layout(rect=[0,0,1,0.96])
plt.show()

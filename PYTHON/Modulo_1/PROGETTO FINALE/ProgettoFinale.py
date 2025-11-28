
""""
Scenario reale:
Una catena di negozi di elettronica vuole analizzare i dati delle vendite per migliorare la gestione e capire l’andamento del mercato. 
I dati vengono raccolti giornalmente e comprendono informazioni su prodotti, quantità vendute, prezzo, incassi e negozi.
Si richiede di sviluppare un programma in Python che utilizzi:
NumPy per elaborazioni numeriche velociPandas per la gestione 
e analisi di datasetMatplotlib per la visualizzazione dei dati in grafici
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("-------------------------------")
print("Parte 1 - Dataset di base:")
print("-------------------------------")

"""
Creare un file CSV chiamato vendite.csv con almeno 30 righe che contenga le seguenti colonne:
    Data (formato YYYY-MM-DD) 
    Negozio (stringa: es. Milano, Roma, Napoli…)
    Prodotto (stringa: es. Smartphone, Laptop, TV…)
    Quantità (intero)
    Prezzo_unitario (float)
Esempio riga:
2023-09-01, Milano, Smartphone, 5, 499.99
"""


# Creazione del dataset di esempio
data = {
    "Data": pd.date_range(start="2025-09-01", periods=30, freq='D').tolist() * 4,
    "Negozio": ["Milano"] * 30 + ["Roma"] * 30 + ["Napoli"] * 30 + ["Crema"] * 30,
    "Prodotto": (["Smartphone", "Laptop", "Bimby", "Frullatore"] * 30)[:120],
    "Quantita": np.random.randint(1, 20, size=120),
    "Prezzo_unitario": np.random.uniform(100, 1000, size=120).round(2)
}   
#Creazione file CSV
df = pd.DataFrame(data)
df.to_csv("vendite.csv", index=False)
##print("Dataset vendite.csv creato con successo.")


print("-------------------------------")
print ("Parte 2 - Importazione con Pandas:")
print("-------------------------------")
"""
Importare il file CSV in un DataFrame Pandas e stampare:
    le prime 5 righe (head())
    il numero di righe e colonne (shape)
    le informazioni generali (info())
"""

df_vendite=pd.read_csv("vendite.csv")
#print (df_vendite)
print("Prime 5 righe del dataset:")
print(df_vendite.head())    
print("\nNumero di righe e colonne:")
print(df_vendite.shape)
print("\nInformazioni generali sul dataset:")
print(df_vendite.info())



print("-------------------------------")
print ("Parte 3 - Elaborazioni con Pandas")
print("-------------------------------")
"""
Aggiungere una colonna Incasso calcolata come Quantità * Prezzo_unitario.
Calcolare con Pandas:
    l'incasso totale di tutta la catena
    l'incasso medio per negozioi 3 prodotti più venduti (in termini di quantità totale)
    Raggruppare i dati per Negozio e Prodotto e mostrare l'incasso medio.
"""

df_vendite["Incasso"]=df_vendite["Quantita"] * df_vendite["Prezzo_unitario"]
#print(df_vendite)
incasso_totale=df_vendite["Incasso"].sum()
print(f"\nIncasso totale di tutta la catena: {incasso_totale:.2f} Euro")
#Recupero i 3 prodotti più venduti (in termini di qta)
quantita_per_prodotto_top=df_vendite.groupby("Prodotto",as_index=False)["Quantita"].sum().head(3)
print(f"\nProdotti più venduti (qta): \n{quantita_per_prodotto_top}")
#Recupero le vendite, per negozio, degli articoli top
df_vendite_articoli_top=df_vendite[df_vendite["Prodotto"].isin(quantita_per_prodotto_top["Prodotto"])]
incasso_medio_negozio_prodotti_top=df_vendite_articoli_top.groupby("Negozio",as_index=False)["Incasso"].sum()
print(f"\nIncasso medio per negozio (articoli top qta)\n{incasso_medio_negozio_prodotti_top}")
#Recupero le vendite, per articolo, articoli top
incasso_medio_prodotti_top=df_vendite_articoli_top.groupby("Prodotto",as_index=False)["Incasso"].sum()
print(f"\nIncasso medio prodotti top (per qta)\n{incasso_medio_prodotti_top}")

print("-------------------------------")
print("Parte 4 - Uso di NumPy")
print("-------------------------------")
"""
Estrarre la colonna Quantità come array NumPy e calcolare:
    media, minimo, massimo e deviazione standard e percentuale di vendite sopra la media

Esempio parziale:
import numpy as np
q = df["Quantità"].to_numpy()
media = np.mean(q)
massimo = np.max(q)

Creare un array NumPy 2D che contenga solo Quantità e Prezzo_unitario e calcolare per ogni riga l'incasso. 
Confrontare i risultati con la colonna Incasso del DataFrame per verificarne la correttezza.
"""
quantita_array=df_vendite["Quantita"].to_numpy()
media_quantita=np.mean(quantita_array)  
minimo_quantita=np.min(quantita_array)
massimo_quantita=np.max(quantita_array)
deviazione_std_quantita=np.std(quantita_array)
print(f"\nStatistiche sulla colonna Quantità:")
print(f"Media: {media_quantita:.2f}, Minimo: {minimo_quantita}, Massimo: {massimo_quantita}, Deviazione Standard: {deviazione_std_quantita:.2f}")
percentuale_sopra_media=(np.sum(quantita_array > media_quantita) / len(quantita_array)) * 100
print(f"Percentuale di vendite sopra la media: {percentuale_sopra_media:.2f}%")

#Creazione array 2D con Quantità e Prezzo_unitario
array_2D=df_vendite[["Quantita","Prezzo_unitario"]].to_numpy()
#Calcolo incasso con NumPy
incasso_numpy=array_2D[:,0] * array_2D[:,1]
#Verifica con colonna Incasso del DataFrame
confronto_incasso=np.allclose(incasso_numpy, df_vendite["Incasso"].to_numpy())
print(f"\nConfronto tra incasso calcolato con NumPy e colonna Incasso del DataFrame: {'Corretto' if confronto_incasso else 'Errato'}")


print("-------------------------------")
print("Parte 5 - Visualizzazioni con Matplotlib")
print("-------------------------------")
""" 
Creare grafici per visualizzare:
    L'andamento delle vendite totali (incasso) nel tempo (line plot)
    La distribuzione delle quantità vendute per prodotto (bar chart)
    Un grafico a torta che mostri la percentuale di incasso per negozio
"""
risp=""
print(df_vendite)
while risp.upper() not in ("S","N"):
    risp=input("Vuoi visualizzare i grafici (parte 5) S/N? ")
if risp.upper()=="S":
    #
    #L'andamento delle vendite totali (incasso) nel tempo (line plot)
    #

    #raggruppo le vendite (incasso) per data
    df_vendite_incasso_tempo = df_vendite.groupby("Data")["Incasso"].sum().reset_index()
    #grafico a linee
    plt.figure(figsize=(12, 6))
    plt.plot(df_vendite_incasso_tempo["Data"],df_vendite_incasso_tempo['Incasso'], marker='o',color='green')
    plt.title('Andamento delle vendite')
    plt.xlabel('Data')
    plt.xticks(rotation=45)    
    plt.ylabel('Incasso (€)')
    plt.tight_layout() #sistema automaticamente i margini
    plt.show()

    #
    #La distribuzione delle quantità vendute per prodotto (bar chart)
    #

    #raggruppo le vendite (quantita) per prodotto
    quantita_per_prodotto = df_vendite.groupby("Prodotto")["Quantita"].sum()
    #grafico a barre
    plt.figure(figsize=(8, 5))
    plt.bar(quantita_per_prodotto.index, quantita_per_prodotto.values, color='skyblue')
    #ordino il risultato
    quantita_per_prodotto.sort_values(ascending=False).plot(kind='bar', color='orange')
    #Titoli e assi
    plt.title("Quantità vendute per prodotto")
    plt.xlabel("Prodotto")
    plt.ylabel("Quantità totale")
    plt.xticks(rotation=45, ha="right")  # ruota le etichette
    plt.tight_layout()
    plt.show()
    
    #
    #Un grafico a torta che mostri la percentuale di incasso per negozio
    #
    #raggruppo le vendite (incasso) per negozio
    Incasso_negozio = df_vendite.groupby("Negozio")["Incasso"].sum()    
    #grafico a torta
    plt.figure(figsize=(6, 6))
    plt.pie(Incasso_negozio,labels=Incasso_negozio.index
        ,autopct='%1.1f%%',      # mostra la percentuale
        startangle=90,          # ruota l’inizio del grafico
        colors=plt.cm.Paired.colors  # tavolozza carina
    )    
    plt.title("Percentuale di incasso per destinazione")
    plt.tight_layout()
    plt.show()  

print("-------------------------------")
print("Parte 6 - Analisi Avanzata")
print("-------------------------------")
"""
Creare una nuova colonna Categoria che raggruppi i prodotti in grandi famiglie (es. Smartphone e Laptop → Informatica, TV → Elettrodomestici).
Calcolare per ogni categoria:incasso totale, quantità media venduta
Salvare il DataFrame aggiornato con le nuove colonne in un nuovo file vendite_analizzate.csv.    
"""  
#["Smartphone", "Laptop", "Bimby", "Frullatore"]

#Creo categoria prodotti
categorie_prodotti = {"Smartphone": "Elettronica","Laptop": "Elettronica","Bimby": "Cucina","Frullatore": "Cucina"}

# Aggiungo la categoria al DataFrame delle vendite (tramite map)
df_vendite["Categoria"] = df_vendite["Prodotto"].map(categorie_prodotti).fillna("Altro")

vendite_analizzate = df_vendite.groupby("Categoria").agg(
    Incasso_totale=("Incasso", "sum"),
    Quantita_media=("Quantita", "mean")
).reset_index()

#Creazione file CSV
nomefile="vendite_analizzate.csv"
vendite_analizzate.to_csv(nomefile, index=False)
print(f"\nFile creato: {nomefile}")

print("-------------------------------")
print("Parte 7 - Estensioni")
print("-------------------------------")
"""
Creare un grafico combinato: 
    incasso medio per categoria (grafico a barre) 
    + linea della quantità media venduta.
Creare una funzione top_n_prodotti(n) che restituisca i n prodotti più venduti in termini di incasso totale.
"""

incasso_medio_categoria=df_vendite.groupby("Categoria",as_index=False)["Incasso"].mean().sort_values(by="Incasso",ascending=False)
quantita_media_categoria=df_vendite.groupby("Categoria",as_index=False)["Quantita"].mean().sort_values(by="Quantita",ascending=False)
#rinomino le colonne
incasso_medio_categoria = incasso_medio_categoria.rename(columns={"Incasso": "Incasso_medio"})
quantita_media_categoria = quantita_media_categoria.rename(columns={"Quantita": "Qta_media"})
#merge dei due df
incasso_quantita_medi_categoria = incasso_medio_categoria.merge(quantita_media_categoria, on="Categoria",how="inner")

fig, ax1 = plt.subplots(figsize=(10, 6))

categorie = incasso_quantita_medi_categoria["Categoria"]
x = range(len(categorie))

# Barre: incasso medio per categoria
ax1.bar(x, incasso_quantita_medi_categoria["Incasso_medio"])
ax1.set_xlabel("Categoria")
ax1.set_ylabel("Incasso medio per categoria")

# Secondo asse y per la linea
ax2 = ax1.twinx()
ax2.plot(x, incasso_quantita_medi_categoria["Qta_media"], marker="o", color="red")
ax2.set_ylabel("Quantità media venduta")

# Sistemiamo le etichette sull'asse X
ax1.set_xticks(x)
ax1.set_xticklabels(categorie, rotation=45, ha="right")

plt.title("Incasso medio e quantità media venduta per categoria")
plt.tight_layout()
plt.show()


def top_n_prodotti(df: pd.DataFrame, n: int = 2):
    """Restituisce i N prodotti più venduti in termini di incasso."""
    incasso_per_prodotto = (df.groupby("Prodotto", as_index=False)["Incasso"].sum().sort_values(by="Incasso", ascending=False).head(n))
    return incasso_per_prodotto

n = 2
print(f"\nTop {n} prodotti più venduti in termini di incasso: {top_n_prodotti(df_vendite, n)}")



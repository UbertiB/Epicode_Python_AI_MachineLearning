"""
Spesso i dati reali non sono semplici array di numeri (pd)
abbiamo tabelle, dataset eterogenei, non solo di numeri, ma testi, date,
categorie ed etichette.
Dati organizzati in colonne con un certo significato
PANDAS è una libreria che ci permette di lavorare con i dati
come fossero in excel ma con la potenza di python
Pandas libreria open source costruita sopra numpy
Ha l'obbiettivo di permettere di gestire i dati tabellari
E' la libreria standard per la data analiysis di python
Pandas introduce due strutture dati principali:
- Series: una colonna di dati (1 dimensione), comode quando vogliamo associare eithcette ai dati
- DataFrame: una tabella con righe e colonne (2 dimensioni) è come un foglio excel
Con Pandas non si lavora più solo con numeri.

PANDAS è lo standard per chi fa data science o analisi di dati in Python (è semplice, efficiente
versatile, compatibile con tante librerie python)
"""

import pandas as pd

print ("********************")
print ("SERIES PANDAS")
print ("********************")
s=pd.Series([10,20,30], index=["a","b","c"])
print (f"Series di pandas: \n{s}")

print ("********************")
print ("DATAFRAME PANDAS")
print ("********************")
data = {"Nome": ["Anna", "Luca","Marco"],
        "Eta": [12,50,32]}
df=pd.DataFrame(data)
print(f"DataFrame di pandas (tabella con due colonne) \n{df}")

data1 = {"Nome": ["Anna", "Luca","Marco"],
        "Eta": [12,50,32], 
        "Corso":["matematica","informatica","geografica"]}
df1=pd.DataFrame(data1)
print(f"DataFrame di pandas (tabella con 3 colonne) \n{df1}")

print ("********************")
print ("Accedere ai dati")

print (f"Accedere per colonna nome\n{df1["Nome"]}")
print (f"Accedere per riga 1\n{df1.loc[0]}")
print (f"Accedere per riga 1\n{df1.iloc[0]}")
print (f"Accedere per slice di righe o colonna (tutta la seconda riga)\n{df1[:1]}") #tutta la seconda riga
print (f"Accedere per slice di righe o colonna (tutta la seconda riga)\n{df1[1:]}") #le prime due righe (0 e 1)


print (f"FILTRARER I DATI")
print (f"dati filtrati \n{df[df["Eta"]>25]}")
print (f"ORDINARE I DATI")
print (f"dati filtrati \n{df.sort_values("Eta")}")
print (f"FARE STATISTICHE")
print (f"dati filtrati \n{df["Eta"].mean()}")
print (f"AGGIUNGERE COLONNE DERIVATE")
df["anno_nascita"]=2025-df["Eta"]
print(f"\n {df}")
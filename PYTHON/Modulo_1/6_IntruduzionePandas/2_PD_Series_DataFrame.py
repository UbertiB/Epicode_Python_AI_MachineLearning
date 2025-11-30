"""
SERIES
sono colonne singole. Sono i mattoni
E' una sequenza unidimensionale di dati, simile ad un array in np,
con l'aggiunta che ha etichette degli indici. Ogni elementi ho due componenti 
(un valore ed un indice che lo identifica)
E' una lista etichettata
Possono contenere non solo numeri ma anche stringhe, valori boolenai, valori misti
Hanno sempre un indice associato, che può essere numerico o personalizzato, rendendo più facile
l'accesso ai valori.
Supporta le operazioni vettoriali
Ci permette di trattare una colonna come un'oggetto intelligente. 
Ottime per gestire sequenze etichettate semplici ma potenti (esempio lista di nomi)
DATAFRAME
sono come delle tabelle. Sono la casa costruita con i mattoni (series) 
E' una struttura tabellare a due dimensioni, composta di righe e colonne. 
Ogni colonna è una series
Si può creare in diversi modi, ma il modo più semplice è con un dizionario.  
Le chiavi del dizionario diventano le colonne, i valori del dizionario diventano le righe
Si possono però creare dataframe anche da altre sorgenti, 
esempio csv, array np, liste di liste, excel
Il dataframe è una collezione ordinata di series che condividono lo stesso indice di riga
Sono idelai per dataset più complessi con righe e colonne contemporaneamente
"""

import pandas as pd

print ("----------------------------")
print ("SERIES")
print ("----------------------------")
s=pd.Series([10,20,30], index=["A","B","C"]) #10,20,30 sono valori A,B,C sono indici
print (s)

print ("----------------------------")
print ("DATAFRAME")
print ("----------------------------")
data={"Nome":["Anna","Luca","Marco"],
      "Eta":[23,30,27]}
df=pd.DataFrame(data)
print(df)

print ("----------------------------")
print ("ACCESSO AI DATI")
print ("----------------------------")
#CON LOC selezione per etichette
print(f"accesso con loc \n{df.loc[0]}") #prende la riga con etichetta 0, quindi la prima riga, in questo caso perchè non ho cambiato le etichette e corrispondono alla posizione
print(f"accesso con iloc \n{df.iloc[0]}") #prende la riga con posizione 0, quidni la prima sempre
#

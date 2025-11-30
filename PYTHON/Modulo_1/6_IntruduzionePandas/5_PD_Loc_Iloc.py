"""
LOC e ILOC
servono per accedere a righe e colonne di un df
LOC lavora con le etichette (nome di righe e colonne)
L'ultimo valore di uno slice è incluso con LOC (prendo tutte le colonne o righe elencate)
LOC da utilizzare quando ho dateset con indici o colonne significativi
ILOC lavora con le posizioni mumeriche (indici interi): prima riga 0, seconda riga 1, ecc
Possiamo prendere una riga, più colonne o una singola cella
Uso ILOC quando ragiono in termini di posizioni numeriche
Si può fare anche con metodi base, ma loc e iloc danno più flessibilità
Se ho indici parlanti utilizzo loc, se invece penso solo a posizioni,
magari in dataset senza etichette chiare, in questa cosa scelgo iloc.
L'ultimo valore di uno slice è escluso con ILOC
"""
import pandas as pd

data={"nome":["Anna","Luca", "Marco"],
        "eta":[23,27,25]}
df=pd.DataFrame(data, index=["a","l","m"])  #indici personalizzati, potrebbe aver senso utilizzare loc
print(df.loc["a"]) #riga con etichetta a
print(df.iloc[0,:]) #prima riga (0)

#LOC ci devono essere le etichette e devo conoscerle
print(f"UNA RIGA \n{df.loc["l"]}")
print(f"PIU' RIGHE \n{df.loc[["l","m"]]}")
print(f"UNA COLONNA \n{df.loc[:,"eta"]}")
print(f"PIU' COLONNE \n{df.loc[:,["eta","nome"]]}")
print(f"UNA CELLA \n{df.loc["l","eta"]}")

#ILOC posso non conoscere le etichette e potrebbero anche non esserci
print(f"UNA RIGA (seconda) \n{df.iloc[1]}")
print(f"PIU' RIGHE \n{df.iloc[[1,0]]}")
print(f"UNA COLONNA \n{df.iloc[:,1]}")
print(f"PIU' COLONNE \n{df.iloc[:,[1,0]]}")
print(f"UNA CELLA \n{df.iloc[1,1]}")
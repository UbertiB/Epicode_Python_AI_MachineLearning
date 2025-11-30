"""
i dati possono essere caricati da files esterni.
- CSV: dati tabellari, separati da virgole o altri delimitatori
- JSON: dasti strutturati ad albero, molto utilizzato nelle API e nel web
- DATABASE: esempio SQL o noSQL
- altro

CSV: formato più diffuso in assoluto. Importo i dati 
con readcsv
sep=";" permette di definire il delimitatore ;
header=none, se il file non ha intestazione
names=["col1"],["col2"] per dare nomi alle colonne
usecols=[0,2] per leggere solo alcune colonne
con tocsv per salvare i dati su file csv
JSON: formato diffuso su API o Web. Importo i dati 
con readcsv
Se il file jsno è in formato tabellare, pandas lo converte subito in dataframe
Se il file json ha una struttura annidata in questi casi devo utilizzare json_normalize
"""

import pandas as pd
from pandas import json_normalize

print("--------------------------")
print("CSV")
print("--------------------------")
df=pd.read_csv("dati.csv") #importo
print(df.head())
df.to_csv("output.csv",index=False) #exporto  index=false non salva l'indice come colonna extra
print("--------------------------")
print("JSON")
print("--------------------------")
df=pd.read_json("dati.json")
print(df.head())
data1={"persone":[{"nome":"Anna","eta":23},{"nome":"Luca","eta":30}]}
df1=json_normalize(data1,"persone")
print(df1)
df1.to_json("output.jsono",orient="records") #orient decide come organizzare i dati

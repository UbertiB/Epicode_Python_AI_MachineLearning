"""
ITERARE significa scorrere i dati uno alla volta riga per riga o colonna per colonna
Da utilizzare quando vogliamo applicare delle legiche particolare 
che non possono essere espresse con operazioni vettoriali
Oppure quando devo ispezionare i dati singolarmente (esempio stampare uno per uno)
ORDINARE
Riorganizzare il dataset in base ad uno o più criteri

Fondamentali sia in fase di analisi esplorativa sia in preparazione dei dati

"""

import pandas as pd

data={"nome":["Anna","Luca", "Marco"],
        "eta":[23,27,25]}
df=pd.DataFrame(data, index=["a","l","m"])  #indici personalizzati, potrebbe aver senso utilizzare loc

#
#LAVORARE CON LE RIGHE
#
print("---------------------")
print("LAVORARE CON RIGHE")
print("---------------------")
#ITERARE con ITERROWS
#permette di scorrere le righe ed a ogni iterazione ottengo
#l'indice della riga e il contenuto sotto forma di series
#scorre i dati uno alla volta, può risultare lento su dataset molto grandi
for index,row in df.iterrows():
    print(index,row) #visualizzo la riga
for index,row in df.iterrows():
    print(index,row["nome"],row["eta"]) #visualizzo colonne specifiche

#ITERARE con ITERTUPLES
#E' un'alternativa più efficiente, restitiusce ogni riga come una namedtuple, 
#più leggera ed efficiente
for row in df.itertuples():
    print(row.nome,row.eta) #visualizzo colonne specifiche

#
# LAVORARE CON LE COLONNE
#
print("---------------------")
print("LAVORARE CON COLONNE")
print("---------------------")
print("\nNomi colone")
for col in df:
    print(col) #ottengo i nomi delle colonne
    #print(df[col])
print("\nContenuto colone")
for col in df:
    print(df[col])  

#utile quando vogliamo fare trasformazioni colonna per colonna
#esempio normalizzare una colonna numerica
#o controllare che non ci siano valori mancanti
  
#
# ORDINARE
#
print("---------------------")
print("ORDINARE")
print("---------------------")

#ordinare per valori (SORT)
df_ordinato=df.sort_values("eta")
print(f"\nOrdinato per eta")
print(df_ordinato)
df_ordinato_d=df.sort_values("eta", ascending=False)
print(f"\nOrdinato per eta decrescente")
print(df_ordinato_d)

#utile per esplorare i dati, per esempio per capire il più giovane o il più anziano
#posso ordinare per più colonna
df_ordinato_p=df.sort_values(["eta","nome"])
print(f"\nOrdinato per due elementi (eta e poi nome)")
print(df_ordinato_p)

#ordinare per indice (SORT_INDEX)
df_ordinato_I=df.sort_index()
print(f"\nOrdinato per indice")
print(df_ordinato_I)
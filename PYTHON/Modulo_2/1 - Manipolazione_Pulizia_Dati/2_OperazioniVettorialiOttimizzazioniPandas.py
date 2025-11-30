import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
lavorare con pandas in maniera "vettorializzata" è fondamentale per velocizzare, 
la vettorializzazione ci permette di ridurre al minimo il codice iterativo
non ci serve ragionare elemento per elmento perchè il codice viene applicato a tutta la serie
Evitare apply quando possibile, applay è sicuramente più flessibile
ma richiamando una funzione per ogni riga o elemento è estremamente lento

Operazioni
lento: applay  = df["f"]=df["a"].apply(lambda x:x**2)
veloce: vettoriali (più veloce) = df["f"]=df["a"]**2

Operazioni vettoriali:
- somma: df["c"]=df["a"]+df["b"]
- scalare colonna: df["d"]=df["a"]*2
- funzione numpy: df["e"]=np.log(df["b"])

Gestione efficiente delle condizioni
lento: df["g"]=df["a"].apply(lambda c: "pari" if x%2==0 else "dispari")
veloce: df["g"]=np.where(df["a"]%2==0,"pari","dispari")

Aggregazioni e trasformazioni
Le aggregazioni riducono i dati, le trasformazioni non riducono i dati
- df["cum_sum"]=df["a"].cumsum() # somma cumulata
- df.groupby("g")["b"].mean() #  media per gruppo
- df["h"]=(df["a"]+df[2b"])/df["b"+.max()] #aggragazione
Le aggregazioni riasusmono, le trasformazioni preparano i dati ad ulteriori analisi

Ottimizzazione delle memoria:
la scelta del tipo di data appropriato permette di ottimizzare di molto la memoria, 
senza perdita di informazioni (se i valori lo permettono)
Questo oltre a liberare la memoria, rende più veloce le operazioni di calcolo

EVAL e QUERY per migliorare sia le performance sia la chiarezza del codice
EVAL si eseguono calcoli direttamente sulle colonne
df.eval("z=a*b+c",inplace=True)
QUERY permette di fare operazioni simili con linguaggio sql
df.query("a>2 and b<35")

"""

data={"Prezzo":[100,200,300,400,500]}
df=pd.DataFrame(data)
#colonna aggiuntiva calcolata: con semplice operazione matematica
df["Prezzo_Scontato"]=df["Prezzo"]*0.8
print(df)
#colonna aggiuntiva calcolata: con condizione IF, classificazione prezzi
#versione lenta perchè itera tutti i valori con il ciclo for
df["Tipo_Prezzo"]=["Alto" if x>250 else "Basso" for x in df["Prezzo"]]
print(df)
#colonna aggiuntiva calcolata: con condizione WHERE, classificazione prezzi
#versione ottimizzata, operazioni vettorializzate
df["Tipo_Prezzo_NP"]=np.where(df["Prezzo"]>250,"Alto","Basso")
print(df)

data2={"Prodotto":["A","B","C","D"],
       "Quantita": [10,5,3,8], 
       "Prezzo_unitario":[20,50,15,30]}
df2=pd.DataFrame(data2)
#colonna aggiunta
df2["Prezzo_Totale"]=df2["Quantita"]*df2["Prezzo_unitario"]
print(df2)


"""
Non ci si limita mai a leggere una sola fonte di dati.
i dati provengono da diverse fonti.
Per integrare tutti in un unico dataset è fondamentale conoscere le 
tecniche di concatenazione come merge e join.
--------------
CONCATENAZIONE
--------------
Unisce DataFrame per posizione, non per chiave. Attacca due dataframe in verticale (uno sotto l'altro)
o in orrizzontale (uno accanto all'altro)
Non guarda i valori, non confronta codici, non fa matching, ma semplicemente affianca
con il metodo CONCAT è possibile specificare l'asse lungo cui effettuare la concatenzazione.
axis=0 per aggiungere righe
axis=1 per affiancare colonne
Il parametro ignore_index permette di resettare gli indici del risultato finale, per 
fornire una sequenza ordinata.
Spesso utilizzato quando si devono combinare dati "simili" provenienti da diverse fonti
In caso di colonne mancanti, Pandas inserisce automaticamente i valori NaN 
-----
MERGE
-----
Equivale alla Join SQL basata su chiavi.
Confronta i valori di una o più colonne, allinea le righe in base ad una chiave comune.
Permette di combinare due o più dataset sulla base di chiavi comuni, 
tipo il join di SQL.
Le colonne da utilizzare come chiavi, sono specificate grazie ai parametri ON, LEFT_ON, RIGHT_ON
Il parametro HOW definisce il tipo di join
INNER: mantiene solo le chiavi comuni
LEFT: conserva tutte le righe del dataset di sinistra
RIGHT: conserva tutte le righe del dataset di destra
OUTER: unisce la righe da entrambi i dataset senza perdere nulla
JOIN
--------------
JOIN 
--------------
E' una scorciatoia di merge basata su indice, unisce automaticamenet usanto l'indice
del dataframe senza essere specificato
Esempio: 
df1=vendite.set_index("cliente")
df2=clienti.set_index("codice")
df=df1.join(df2)
Non specifico la chiave o i campi necessari per l'unione, 
prende automaticamente gli indici
---------------
JOIN COMPLESSI
---------------
permette di combinare concatenazioni e merge
"""

import pandas as pd
import numpy as np
import json

# --------------------
#CONCATENAZIONE VERTICALE (axis=0)
#---------------------
giornaliere=np.array([[1,100],[2,150]])
settimanali=np.array([[3,200],[4,250]])

df_giornaliere=pd.DataFrame(giornaliere,columns=["Giorno","Vendite"])
df_settimanali=pd.DataFrame(settimanali,columns=["Giorno","Vendite"])

df_totale=pd.concat([df_giornaliere,df_settimanali],axis=0,ignore_index=True)
print(df_totale)

# --------------------
#CONCATENAZIONE con concat left
#---------------------
data=[{"cliente":1,
       "transazioni":[{"prodotto":"P1","importo":100},{"prodotto":"P2","importo":50}]},
       {"cliente":2,
        "transazioni": [{"prodotto":"P3","importo":200}]}
    ]
records=[]
for item in data:
    cliente=(item["cliente"])
    for t in item["transazioni"]:
        prodotto=t["prodotto"]
        importo=t["importo"]
        records.append({"cliente":cliente,"prodotto":prodotto,"importo":importo})

df_transazioni=pd.DataFrame(records)
df_cliente=pd.DataFrame({"cliente":[1,2,3],"nome":["Anna","Luca","Paolo"]})
df_merge=pd.merge(df_cliente,df_transazioni,how="left", on="cliente")
print(f"Merge con dizionari annidati: \n{df_merge}")

#---------------------
#---------------------
#---------------------

json_data='''
[
    {"cliente":1,"negozio":"S1","promo":10},
    {"cliente":2,"negozio":"S2","promo":15}
]
'''
promozioni=pd.json_normalize(json.loads(json_data))
vendite=pd.DataFrame({"cliente":[1,2,3],
                      "negozio":["S1","S2","S3"],
                      "vendite":[100,200,150]})
df_finale=pd.merge(vendite, promozioni,on=["cliente","negozio"],how="left")
print(df_finale)

#---------------------
#---------------------
#---------------------
df3_clienti=pd.DataFrame({"cliente":[1,2,3],
                          "nome":["Anna","Luca","Paolo"]})
df3_transazioni=pd.DataFrame({"cliente":[1,2,3],
                        "importo":[100,150,200]})
df3_promo=pd.DataFrame({"cliente":[1,3], "sconto":[10,15]})
df3_bonus=pd.DataFrame({"cliente":[2,3],"bonus":[5,7]})

merge1=pd.merge(df_cliente,df_transazioni, on="cliente",how="outer")
merge2=pd.merge(merge1,df3_bonus, on="cliente",how="outer")
df_final=pd.merge(merge2,df3_bonus,on="cliente",how="outer")

print(merge1)
print(merge2)
print(df_final)
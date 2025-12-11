"""
ESERCIZIO 1:
* crea un array np di 5X4 con vendite di 5 negozi e 4 prodotti
Calcola somma totale e media per ogni riga e colonna
applica uno sconto progressivo diverso per ciascun prodotto
stampa i risultati

ESERCIZIO 2:
* Crea un dizionario annidato di 4 utenti, ognuno con contatti,
lista di acquisti e lista di categorie prodotti acquistati.
Calcola totale acquisti, numero ordini e numero categorie distinte acquistate per utente.
Stampa il risultato

ESERCIZIO 3:
Simula dati JSON annidati per 3 negozi, ciascuno con 3 prodotti e vendite settimanali
Normalizza in dataframe, calcola totale vendite per negozio, prodotto
e media settimanale di vendite per prodotto.
Stampa entrambi i dataframe
"""
import numpy as np
import pandas as pd
from pandas import json_normalize
import json

"""
ESERCIZIO 1:
* crea un array np di 5X4 con vendite di 5 negozi e 4 prodotti
Calcola somma totale e media per ogni riga e colonna
applica uno sconto progressivo diverso per ciascun prodotto
stampa i risultati
"""
if False:
    print("--------------------------")
    print("----- ESERCIZIO 1 --------")
    print("--------------------------")

    #array 5x4 (5 negozi 4 prodotti)
    vendite=np.array([[100,200,150,300],
                    [50,80,120,60],
                    [90,150,200,100],
                    [150,180,120,102],
                    [80,95,66,79]])
    print(vendite)
    totale_per_prodotto=np.sum(vendite,axis=0)
    print(f"Totale vendite per prodotto: {totale_per_prodotto}")
    totale_per_negozio=np.sum(vendite,axis=1)
    print(f"Totale vendite per negozio: {totale_per_negozio}")
    totale_media_prodotto=np.mean(vendite,axis=0)
    print(f"Totale vendite media prodotto: {totale_media_prodotto}")
    totale_media_negozio=np.mean(vendite,axis=1)
    print(f"Totale vendite media negozio: {totale_media_negozio}")

    sconto=np.array([[0.8,0.9,0.85,0.70]])
    vendite_scontate=vendite*sconto
    print(f"Vendite scontate: \n{vendite_scontate}")

"""
ESERCIZIO 2:
* Crea un dizionario annidato di 4 utenti, ognuno con contatti,
lista di acquisti e lista di categorie prodotti acquistati.
Calcola totale acquisti, numero ordini e numero categorie distinte acquistate per utente.
Stampa il risultato
"""
if False:
    print("--------------------------")
    print("----- ESERCIZIO 2 --------")
    print("--------------------------")    
    #dizionari annidati
    utenti={
                 "user1":{"nome":"Anna","contatti":{"email":"anna@mail.com"},"acquisti":[100,200,50],"categorie":["Elettrodomestici","Elettronica","Cancelleria","Casalinghi","Giardinaggio"]},
                 "user2":{"nome":"Luca","contatti":{"email":"luca@mail.com"},"acquisti":[20,80], "categorie":["Elettronica","Giardinaggio"]},
                 "user3":{"nome":"Paolo","contatti":{"email":"paolo@mail.com"},"acquisti":[150,120,30],"categorie":["Casalinghi","Cancelleria","Libri"]},
                 "user4":{"nome":"Ettore","contatti":{"email":"ettoore@mail.com"},"acquisti":[150,155,140],"categorie":["Libri"]}
            }  
    for user_id, user in utenti.items():
        print (f"\nUtente: {user_id}")
        print(f"Totale acquisti {sum(user["acquisti"])} ")
        print(f"Numero categorie {len(user["categorie"])} ")

"""
ESERCIZIO 3:
Simula dati JSON annidati per 3 negozi, ciascuno con 3 prodotti e vendite settimanali
Normalizza in dataframe, calcola totale vendite per negozio, prodotto
e media settimanale di vendite per prodotto.
Stampa entrambi i dataframe
"""
if True:
    print("--------------------------")
    print("----- ESERCIZIO 3 --------")
    print("--------------------------")        
    #json annidati    
    json_data="""
    [
        {"negozio":"N1","prodotti":[{"nome":"P1","vendite":[10,15,15]},{"nome":"P2","vendite":[5,7,5]},{"nome":"P3","vendite":[8,7,10]}]},
        {"negozio":"N2","prodotti":[{"nome":"P1","vendite":[20,0,5]},{"nome":"P2","vendite":[10,5,30]},{"nome":"P3","vendite":[5,15,50]}]},
        {"negozio":"N3","prodotti":[{"nome":"P1","vendite":[20,0,0]},{"nome":"P2","vendite":[10,5,5]},{"nome":"P3","vendite":[2,3,1]}]}        
    ]  
    """     
    #carico il json (json.loads())
    data=json.loads(json_data) 
    #normalizzo json annidato con cicli for
    records=[] 
    for negozio in data:
        for c,v in negozio.items():
            if c=="negozio":
                negozio=v
            if c=="prodotti":
                for vv in v:
                    for c1,v1 in vv.items():
                        if c1=="nome":
                            prodotto=v1
                        if c1=="vendite":
                            for q in v1:
                                quantita=q
                                records.append({"negozio":negozio,"prodotto":prodotto,"quantita":quantita})
    df=pd.DataFrame(records)
    print(df)
    totale_negozio=df.groupby("negozio")["quantita"].sum()
    print(f"totale per negozio: \n{totale_negozio}")
    totale_prodotto=df.groupby("prodotto")["quantita"].sum()
    print(f"totale per prodotto \n{totale_prodotto}")
    media_prodotto=df.groupby("prodotto")["quantita"].mean()              
    print(f"media settimanale per prodotto \n{media_prodotto}")
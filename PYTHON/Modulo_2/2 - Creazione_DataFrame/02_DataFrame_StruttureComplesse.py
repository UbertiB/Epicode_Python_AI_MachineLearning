"""
come lavorare con strutture complesse e come integrare dati provenienti da api rest in formato json
Obbiettivo imparare a gestire informazioni gerarchiche.

STRUTTURE COMPLESSE
Nella gestione dei dati reali e frequente imbattersi in dati con strutture complesse.
Le strutture complesse cioè dati che contengono più livelli di informazioni,
consentono di gestire insiemi di dati correlati tra di loro.
Liste, set e dizionari, sono combinazioni di più tipi
- Gli ARRAY NP sono uno strumentio centrale per l'elaborazione numerica. 
Sono ottimizzati in memoria e velocità ed offrono operazioni vettoriali.
Gli array possono essere mono o multi dimensionali. Consentendo di memorizzari matrici
di dati ma anche immagini.
- I DIZIONARI ANNIDATI utili quando si vuole rappresentare dati gerarchici o multi livell0
come informazioni degli utenti con contatti, acquisti e preferenze
In un dizionario annidato il valor può essere un altro dizionario o una lista
Lavorare con dizionari annidati richiede attenzione alle chiavi esistenti 
(usare metodo GET, per evitare errori se la chiave non esiste)
- API REST strumento standard per recuperare dati da servizi esterne. 
Spesso restituisce dati in json
Necessario gestire valori mancanti, tipi variabili, e profondita di annidamento

Validare sempre i dati caricati con type, len o dinfo, per avere info sulle dimensioni e tipi
normalizzare i dati annidati
utilizzare array per operazione numeriche intensive
documentare ogni trasformazioni
salva i dati originali e versioni intermedie per tracciabilità
applicare i controlli di coerenza dati, come valori positivi e date coerenti

"""
from pandas import json_normalize
import numpy as np
import pandas as pd
import json

#esempio DIZIONARIO ANNIDATO
if False:
    data={
            "id":[1,2],
            "info":
                [
                    {"nome":"Anna", "eta":25},
                    {"nome":"Luca","eta":30}
                ]
        }
    df=json_normalize(data,meta=["id"],record_prefix="info_")
    print(df)

#crea un matrice di vendite per più negozi e prodotti
#array tridimensionale
if False:
    #ARRAY ANNIDATI
    vendite=np.array([[100,200,150,300],
                    [50,80,120,60],
                    [90,150,200,100]])
    print(f"Vendite iniziali:\n{vendite}")
    totale_per_prodotto=np.sum(vendite,axis=0)
    print(f"Totale vendite per prodotto: {totale_per_prodotto}")
    totale_per_negozio=np.sum(vendite,axis=1)
    print(f"Totale vendite per negozio: {totale_per_negozio}")
    media_per_negizio=np.mean(vendite,axis=1)
    print(f"Media per negozio: {media_per_negizio}")

    sconti=np.array([0.9,0.8,0.95,0.85])
    vendite_scontate=vendite*sconti
    print(f"Vendite scontate: \n{vendite_scontate}")

if False:
    #DIZIONARI ANNIDATI
    utenti={
                 "user1":{"nome":"Anna","contatti":{"email":"anna@mail.com"},"acquisti":[100,200,50]},
                 "user2":{"nome":"Luca","contatti":{"email":"luca@mail.com"},"acquisti":[20,80]},
                 "user3":{"nome":"Paolo","contatti":{"email":"paolo@mail.com"},"acquisti":[150,120,30]},
            }
    #print(f"Utenti iniziali: \n{utenti}")
    for user,info in utenti.items():
        print (f"\nUSER: {user} INFO: {info}")
        totale=sum(info["acquisti"])
        numero_ordini=len(info["acquisti"])
        print(f"utente: {user} - Totale acquisti: {totale}, numero ordini: {numero_ordini}")

if True:
    #JSON ANNIDATI 
    json_data="""
    [
        {"negozio":"N1","prodotti":[{"nome":"P1","vendite":[10,15]},{"nome":"P2","vendite":[5,7]}]},
        {"negozio":"N2","prodotti":[{"nome":"P1","vendite":[20]},{"nome":"P2","vendite":[10,5]}]}
    ]  
    """
    #tramite il metodo jsonloads convertiamo  stringa json in lista di dizionari di python 
    data=json.loads(json_data)
    records=[] #records è una lista vuota
    for data1 in data:
        negozio=data1["negozio"]
        for data2 in data1["prodotti"]:
            prodotto=data2["nome"]
            for data3 in data2["vendite"]:
                records.append({"negozio":negozio,"prodotto":prodotto,"vendite":data3})
    df=pd.DataFrame(records)
    totali=df.groupby(["negozio","prodotto"])["vendite"].sum().reset_index()
    print(f"Vendite per negozio e prodotto: \n{totali}")

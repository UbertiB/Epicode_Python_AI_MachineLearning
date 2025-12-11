"""
ESERCIZIO 1
* Crea un multiindex con due livelli (citta, prodotto) e 
assegna vendite inventate. Stampa tutte le vendite di Milano
ESERCIZIO 2
* Crea un multiindex da prodotto cartesiano con 2 citta, 
3 prodotti e 2 mesi. Genera dati casuali e calcola la somma 
per citta e la media per prodotto
ESERCIZIO 3
* Crea un multiindex con 3 livelli (citta, negozio, trimestre).
Genera vendite casuali e: estrai tutte le venditedel trimestre Q2, 
scambia i livelli citta e trimestre, riporta il livello negozio a colonna,
calcola la media per citta
ESERCIZIO 4
* Crea un multiindex con 4 livelli (regione, citta, prodotto, mese).
Genera dati casuali e poi:
- estrai solo i dati della regione nord
- calcola la somma per ogni mese
- ordina l'indice per prodotto
- riportane due livelli a colonna
- trova il prodotto più venduto in ogni citta
"""
import pandas as pd
import numpy as np

"""
ESERCIZIO 1
* Crea un multiindex con due livelli (citta, prodotto) e 
assegna vendite inventate. Stampa tutte le vendite di Milano
"""
if False:
    print ("---------------------------------")
    print ("----------ESERCIZIO 1------------")
    print ("---------------------------------")
    index=pd.MultiIndex.from_tuples(
        [
        ("Roma","Pizza"),
        ("Roma","Pasta"),
        ("Milano","Gelato"),
        ("Milano","Pizza"),
        ("Milano","Pasta")
        ],
    names=["Citta","Prodotto"]
    )
    df=pd.DataFrame({"Vendite":[100,80,200,130,150]},index=index)
    print("DataFrame con MultiIndex:\n",df,"\n")    
    print(f"Vendite di Milano; \n {df.loc["Milano"]}")
    print(f"Vendite Pizza di Milano; \n {df.loc["Milano","Pizza"]}")

"""
ESERCIZIO 2
* Crea un multiindex da prodotto cartesiano con 2 citta, 
3 prodotti e 2 mesi. Genera dati casuali e calcola la somma 
per citta e la media per prodotto
"""
if False:
    print ("---------------------------------")
    print ("----------ESERCIZIO 2------------")
    print ("---------------------------------")    
    citta=["Roma","Milano"]
    prodotti=["Pizza","Pasta", "Gelato"]
    mesi=["Gennaio","Febbraio"]
    index=pd.MultiIndex.from_product([citta, prodotti, mesi],names=["Citta","Prodotto","Mese"])
    np.random.seed(123)
    df=pd.DataFrame({"Vendite":np.random.randint(50,200,size=len(index))},index=index)
    print(f"DataFrame originale: \n{df}")
    print(f"Somma per citta: \n {df.groupby(level="Citta").sum()}")
    print(f"Media per prodotto: \n{df.groupby(level="Prodotto").mean()}")
    print(f"Meida per citta/prodotto: \n{df.groupby(level=("Citta","Prodotto")).sum()}")

"""
ESERCIZIO 3
* Crea un multiindex con 3 livelli (citta, negozio, trimestre).
Genera vendite casuali e: estrai tutte le vendite del trimestre Q2, 
scambia i livelli citta e trimestre, riporta il livello negozio a colonna,
calcola la media per citta
"""
if False:
    print ("---------------------------------")
    print ("----------ESERCIZIO 3------------")
    print ("---------------------------------")   
    citta=["Milano","Roma", "Crema"]
    negozio=["N1","N2", "N3", "N4", "N5"]
    trimestri=["Q1","Q2"]
    index=pd.MultiIndex.from_product([citta, negozio, trimestri],names=["Citta","Negozio","Trimestre"])
    np.random.seed(123)
    df=pd.DataFrame({"Vendite":np.random.randint(50,300,len(index))},index=index)
    print(f"DataFrame originale: \n{df}")    
    print(f"Vendite trimestre Q2: \n {df.xs("Q2",level="Trimestre")}")
    print(f"Vendite totali trimestre Q2: \n {df.xs("Q2",level="Trimestre").sum()}")

    df_swapped=df.swaplevel("Citta","Trimestre").sort_index()
    print(f"Livelli scambiati citta/trimestre: \n{df_swapped}") 

    df_reset=df.reset_index(level="Negozio")
    print(f"Indice riorganizzato a negozio colonna: \n{df_reset}")
    print(f"Meida per citta: \n{df.groupby(level=("Citta")).mean()}")

"""
ESERCIZIO 4
* Crea un multiindex con 4 livelli (regione, citta, prodotto, mese).
Genera dati casuali e poi:
- estrai solo i dati della regione nord
- calcola la somma per ogni mese
- ordina l'indice per prodotto
- riportane due livelli a colonna
- trova il prodotto più venduto in ogni citta
"""
if True:
    print ("---------------------------------")
    print ("----------ESERCIZIO 4------------")
    print ("---------------------------------")   
    regioni=["Nord","Centro","Sud"]
    citta=["Milano","Roma","Palermo"]
    prodotti=["Pizza","Pasta","Gelato","Panini"]
    mesi=["Gennaio","Febbraio", "Marzo","Aprile","Maggio"]
    index=pd.MultiIndex.from_product([regioni,citta, prodotti, mesi],names=["Regione","Citta","Prodotto","Mese"])
    np.random.seed(123)
    df=pd.DataFrame({"Vendite":np.random.randint(50,300,size=len(index))},index=index)
    print(f"DataFrame originale: \n{df}")      
    print(f"Dati regione Nord: \n{df.xs("Nord",level="Regione")}")
    print(f"Somma per ogni mese: \n{df.groupby(level="Mese").sum()}")
   

"""
creazione e gestione avanzata di dataframe.
come creare un multiindiex, come accedere ai dati e come ottenere i dati dall'index, 
come manipolare i livelli dall'indice

MULTIINDEX è un indice che non si limita ad un solo livello.
Rappresenta i dati con struttura gerarchica
Ogni riga potrebbe contenere informazioni di citta, negozi, prodotti
Ogni citta potrebbe contenere più negozi
Ed ogni negozio potrebbe vendere più prodotti
Ed ogni prodotto genera vendite in diversi periodi
In questo casi Pandas ci mette a disposizione uno strumento fondamentale, il multi-index.
Il multi-index non si limita ad un solo livello ma ne sopporta più di uno, creando una
gerarchia tra livelli. La gerarchia ci aiutare a dare ordine logico ai dati.
Ogni riga non è identificata da un solo valore, ma da una tupla di valori, uno per ogni livello
Come un albero.
Alla radice dell'albero ho la citta, da cui partono rami che rappresentano i negozzi, da
cui partono altri rami che rappresentano i prodotti, fino ad arrrivare alle singole
foglie che rappresentano i periodi di osservazione.
Ci permette di navigare tra i livelli, ci permette di rappresentare dati complessi.
Penso ai dati in termini di livello, posso navigare tra livelli.
Ogni livello può avere nomi (quindi non li chiamo primo livello, secondo livello, ecc)
Questo rende la navigazione ancora più chiara.
Parlo di città, negozio, prodotto o settimana, non di primo livello, secondo livello, ecc
La creazione di un multiindex può avvenire in diversi modi:
- da tuple predefinite, 
- da array paralleli, 
- da prodotto cartesiano di insiemi 
- ottenere automaticamente un multi-index dopo groupby su più colonne.
In ogni caso, ho un dataframe il cui indice ha più livelli
Uno dei grandi vantaggi è l'accesso ai dati, non devo filtrare più colonne in contemporanea, 
basta specificare la tupla corrispondente.
Esempio se voglio sapere quante pizze ha venduto il negozio1 di Roma a gennaio posso farlo
direttamente tramite gli indici.
Il risultato è un dataframe il cui indice è a più livelli e quindi pù potenzialità di analisi
L'accesso ai dati non devo più essere filtrato più colonne basta specificare 
la tupla corrispondente
(esempio quante pizza ha venduto il negozio 1 di roma a gennaio, lo faccio tramite la tupla)
Inoltre posso accedere parzialmente ai dati , oppure posso usare una cross section
Posso passare dal generale al particolare con un solo comando
Ogni livello può essere manimpolato come dimensione indipendente
Posso cambiare l'ordine dei livelli, riportare un livello a colonna, ordinare le righe
Ogni livello può essere manimopalto come dimensione indipendente.
Rispecchia la realtà organizzativa dei dati, mantenendo i dati compatti e leggibili.

"""
import pandas as pd
import numpy as np
 #
 # CREAZIONE MANUALE MULTI-INDEX
 #
if False:
    print("-----------------------------------")
    print("---CREAZIONE MULTI-INDEX MANUALE---")
    print("-----------------------------------")
    #creazione manuale ed imparo ad accedere ai dati
    #definisco gli indici
    index=pd.MultiIndex.from_tuples(
        [
        ("Roma","Negozio1","Pizza"),
        ("Roma","Negozio1","Pasta"),
        ("Milano","Negozio2","Gelato"),
        ("Milano","Negozio2","Pizza")
        ],
    names=["Citta","Negozio","Prodotto"]
    )
    #creao il dataframe
    df=pd.DataFrame({"Vendite":[100,80,200,130]},index=index)
    print("DataFrame con MultiIndex:\n",df,"\n")
    #funzione .loc filtra le righe con primo livello ="Roma"
    print("tutte le vendite di Roma:\n", df.loc["Roma"])
    #funzione .loc filtra le righe con primo livello="Roma", secondo livello="Negozio1", terzo livello="Pizza"
    print("vendite di pizza a Roma Negozio 1:\n",df.loc["Roma","Negozio1","Pizza"])

#
#CREAZIONE MULTI-INDEX DA PRODOTTO CARTESIANO (tutte le combinazioni)
#
if False:
    print("-----------------------------------------------")
    print("---CREAZIONE MULTI-INDEX PRODOTTO CARTESIANO---")
    print("-----------------------------------------------")    
    citta=["Roma","Milano"]
    prodotti=["Pizza","Pasta"]
    mesi=["Gennaio","Febbraio"]
    index=pd.MultiIndex.from_product([citta, prodotti, mesi],names=["Citta","Prodotto","Mese"])
    np.random.seed(42)
    df=pd.DataFrame({"Vendite":np.random.randint(50,200,size=len(index))},index=index)
    print("DataFrame con vendite casuali:\n",df,"\n")
    print("Somma vendita per citta:\n",df.groupby(level="Citta").sum())
    print("Media vendite per prodotto:\n",df.groupby(level="Prodotto").mean())
    print("Somma vendite per mese:\n",df.groupby(level="Mese").sum())

#
#LAVORARE CON MULTIINDEX, SCAMBIARE LIVELLO E FARE SLICEING
#df.xs etrare info da qualsiasi livello (necessario indicarlo)
#
if False:
    index=pd.MultiIndex.from_tuples(
        [
            ("Roma","Pizza","Q1"),
            ("Roma","Pizza","Q2"),
            ("Milano","Gelato","Q1"),
            ("Milano","Pizza","Q2"),
            ("Milano","Gelato","Q2"),
            ("Milano","Pizza","Q3")
        ],
        names=["Citta","Prodotto","Trimestre"]
    )
    df=pd.DataFrame({"Vendite":[100,120,60,150,140,80]},index=index)
    print(f"DataFrame originale: \n{df}")
    print(f"Vendite trimestre Q1 di tutte le citta: \n{df.xs("Q1",level="Trimestre")}")
    print(f"Vendite Pizza di tutte le citta: \n{df.xs("Pizza",level="Prodotto")}")
    #scambiare livelli con funzione swaplevel
    df_swapped1=df.swaplevel("Citta","Trimestre").sort_index()
    print(f"Livelli scambiati citta/trimestre: \n{df_swapped1}")

    df_swapped2=df.swaplevel("Citta","Prodotto").sort_index()
    print(f"Livelli scambiati citta/prodotto: \n{df_swapped2}")

if True:
    regione=["Nord","Centro"]
    citta=["Milano","Roma"]
    prodotti=["Pizza","Pasta"]
    trimestri=["Q1","Q2"]
    index=pd.MultiIndex.from_product([regione,citta, prodotti, trimestri],names=["Regione","Citta","Prodotti","Trimestre"])
    np.random.seed(123)
    df=pd.DataFrame({"Vendite":np.random.randint(50,300,size=len(index))},index=index)
    print(f"DataFrame originale: \n{df}")
    print(f"Media vendite per regione e trimestre: \n{df.groupby(level=["Regione","Trimestre"]).mean()}")
    
    df_reset=df.reset_index(level="Prodotti")
    print(f"Indice riorganizzato: \n{df_reset}")

    df_reorder=df.swaplevel("Regione","Trimestre").sort_index()
    print(f"Indice riorganizzato; \n{df_reorder.head()}")
"""
ESERCIZI 1
* Crea un df con prodotti di un negozio,
seleziona quelli che prezzo >50 usando boolena indexing e
crea una copia indipendente.
Aggiungi colonna "costoso" (true se prezzo>100).
Oridna in-place per prezzo decrescente
ESERCIZI 2
* Crea un df con libri (titolo, autore, pagine, prezzo)
Seleziona libri con più di 300 pagine e crea una copia indipendnete
Aggiungi la colonna "lungo" (true se pagine>400)
Ordina per pezzo crescente in-place
ESERCIZI 3
* Crea un df con clienti (nome, citta, spesa totale)
Seleziona i clienti con spesa >1000, crea copia indipendente,
aggiunti colonna Vip (true se spesa >1500) ordina per spesa 
decrescente e resetta l'indice
"""

import pandas as pd
import numpy as np


"""
ESERCIZI 1
* Crea un df con prodotti di un negozio,
seleziona quelli che prezzo >50 usando boolena indexing e
crea una copia indipendente.
Aggiungi colonna "costoso" (true se prezzo>100).
Oridna in-place per prezzo decrescente
"""

if False:
    prodotti=pd.DataFrame({
        "nome":["P1","P2","P3","P4","P5"],
        "prezzo":[25,35,50,55,60]
    })
    prodotti_costosi=prodotti[prodotti["prezzo"]>50]
    prodotti_costosi["costoso"]=[True if x>55 else False for x in prodotti_costosi["prezzo"]]
    prodotti_costosi.sort_values("prezzo",ascending=False,inplace=True)
    prodotti_costosi.reset_index(drop=True,inplace=True)
    print(prodotti_costosi)
    print(prodotti)


"""
ESERCIZI 2
* Crea un df con libri (titolo, autore, pagine, prezzo)
Seleziona libri con più di 300 pagine e crea una copia indipendnete
Aggiungi la colonna "lungo" (true se pagine>300)
Ordina per pezzo crescente in-place
"""
if False:
    libri=pd.DataFrame({
        "titolo":["Titolo A","Titolo B","Titolo C","Titolo D","Titolo E"],
        "autore":["Autore 1","Autore 2","Autore 1","Autore 1","Autore 3"],
        "pagine":[250,350,400,150,180],
        "prezzo":[20,25,38,24,22]
    })
    libri_lunghi=libri[libri["pagine"]>=300]
    libri_lunghi["lungo"]=["si" if x>300 else "no" for x in libri_lunghi["pagine"]]
    libri_lunghi.sort_values("prezzo",ascending=True,inplace=True)
    libri_lunghi.reset_index(drop=True,inplace=True)
    print(libri_lunghi)
    print(libri)

"""
ESERCIZI 3
* Crea un df con clienti (nome, citta, spesa totale)
Seleziona i clienti con spesa >1000, crea copia indipendente,
aggiunti colonna Vip (true se spesa >1500) ordina per spesa 
decrescente e resetta l'indice    
"""
clienti=pd.DataFrame({
    "nome":["Anna","Luca","Ettore","Marco","Maria"],
    "citta":["Roma","Milano","Roma","Roma","Torino"],
    "spesa":[1200,1800,1400,1700,1000]
})
clienti_top=clienti[clienti["spesa"]>1000]
clienti_top["vip"]=[True if x>1500 else False for x in clienti_top["spesa"]]
clienti_top.sort_values("spesa",ascending=False,inplace=True)
clienti_top.reset_index(drop=True,inplace=True)
print(clienti_top)
print(clienti)
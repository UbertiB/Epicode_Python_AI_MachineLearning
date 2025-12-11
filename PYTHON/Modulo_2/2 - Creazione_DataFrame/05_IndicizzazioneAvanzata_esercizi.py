"""
ESERCIZIO 1
- crea un df con colonne: studente, materia, voto, classe, eta
- seleziona tutti gli studenti con voto maggiore di 28 in matematica usando loc e boolean indexing
- ordina i risultati per voto decrescente
- aggiunti una colonna che indica "ottimo" se voto >=30 "Buono" se voto >=28 e "Sufficiente" altrimenti.
- Calcola la media dei voti e crea una colonna booleana "Sopra Media"

ESERCIZIO 2
- Crea un df con colonne: prodotto, categoria, prezzo, quantita, disponibilita
- usa query per selezionare i prodotti della categoria "tecnologia" con prezzo tra 100 e 300
- dal risultato usa iloc per prendere le prime 3 righe e solo le colonne prodotto e prezzo
- aggiungi una colonna che calcola il fatturato (prezzo * quantita)
- ordina il df per fatturato decrescente e calcola la media del fatturato dei prodotti selezionati

ESERCIZIO 3
- crea un df con colonne dipendente, reparto, eta, stipendio, anniservizio
- usa boolean indexing per selezionare i dipendenti con eta>30 e stipendio >2000, oppure 
appartenenti al reparto IT
- mostra solo dipendnete, eta e stipendio
- aggiungi una colonna che indica "junion" se eta<35 e "senior" altrimenti
- raggruppa per reparto e calcola la media dello stipendio per reparto e per categoria
- ordina i risultati per stipendio medio decrescente
"""
import pandas as pd
import numpy as np

if False:
    print("-----------------------------------")
    print("-----------ESERCIZIO 1-------------")
    print("-----------------------------------")
    df=pd.DataFrame([
        {"Studente":"Luca","Materia":"Matematica","Voto":30,"Classe":"2C", "Eta":25},
        {"Studente":"Anna","Materia":"Fisica","Voto":18,"Classe":"2D", "Eta":24},
        {"Studente":"Ettore","Materia":"Matematica","Voto":28,"Classe":"2C", "Eta":22},
        {"Studente":"Maria","Materia":"Biologia","Voto":16,"Classe":"3C", "Eta":25}
    ])    
    filtro=(df["Materia"]=="Matematica")&(df["Voto"]>=28)
    risultato=df.loc[filtro,["Studente","Materia","Voto","Classe","Eta"]]
    risultato=risultato.sort_values(by="Voto",ascending=False)
    media_voto=df["Voto"].mean()
    risultato["Sopra_media"]=[True if x>=media_voto else False for x in risultato["Voto"]]
    print(risultato)

"""
- Crea un df con colonne: prodotto, categoria, prezzo, quantita, disponibilita
- usa query per selezionare i prodotti della categoria "tecnologia" con prezzo tra 100 e 300
- dal risultato usa iloc per prendere le prime 3 righe e solo le colonne prodotto e prezzo
- aggiungi una colonna che calcola il fatturato (prezzo * quantita)
- ordina il df per fatturato decrescente e calcola la media del fatturato dei prodotti selezionati
"""
if False:
    print("-----------------------------------")
    print("-----------ESERCIZIO 2-------------")
    print("-----------------------------------")    
    df=pd.DataFrame([{"Prodotto":"P1", "Categoria": "Tecnologia", "Prezzo":450, "Quantita":50, "Disponibilita":30},
                     {"Prodotto":"P2", "Categoria": "Tecnologia", "Prezzo":200, "Quantita":150, "Disponibilita":120},
                     {"Prodotto":"P3", "Categoria": "Tecnologia", "Prezzo":205, "Quantita":180, "Disponibilita":130},
                     {"Prodotto":"P4", "Categoria": "Tecnologia", "Prezzo":199, "Quantita":190, "Disponibilita":90},
                     {"Prodotto":"P5", "Categoria": "Libri", "Prezzo":50, "Quantita":200, "Disponibilita":45},
                     {"Prodotto":"P6", "Categoria": "Tecnologia", "Prezzo":150, "Quantita":40, "Disponibilita":80}])
    
    filtro_categoria="Tecnologia"
    risultato=df.query("Prezzo>=100 and Prezzo<=300 and Categoria==@filtro_categoria")[["Prodotto","Categoria","Prezzo","Quantita"]]
    risultato["fatturato"]=risultato["Prezzo"]*risultato["Quantita"]
    risultato=risultato.iloc[0:3,[0,2,4]]
    risultato=risultato.sort_values(by="fatturato",ascending=False)
    media_fatturato=risultato.groupby("Prodotto")["fatturato"].mean()
    print(risultato)
    print(media_fatturato)

"""
ESERCIZIO 3
- crea un df con colonne dipendente, reparto, eta, stipendio, anniservizio
- usa boolean indexing per selezionare i dipendenti con eta>30 e stipendio >2000, oppure 
appartenenti al reparto IT
- mostra solo dipendnete, eta e stipendio
- aggiungi una colonna che indica "junion" se eta<35 e "senior" altrimenti
- raggruppa per reparto e calcola la media dello stipendio per reparto e per categoria
- ordina i risultati per stipendio medio decrescente
"""
if True:
    print("-----------------------------------")
    print("-----------ESERCIZIO 3-------------")
    print("-----------------------------------")     
    df=pd.DataFrame([{"Dipendente":"Luca","Reparto":"IT","Eta":20,"Stipendio":1800,"Anni_servizio":1},
                     {"Dipendente":"Maria","Reparto":"Amministrazione","Eta":30,"Stipendio":1600,"Anni_servizio":2},
                     {"Dipendente":"Anna","Reparto":"IT","Eta":25,"Stipendio":2800,"Anni_servizio":16},
                     {"Dipendente":"Ettore","Reparto":"Commerciale","Eta":40,"Stipendio":1500,"Anni_servizio":4},
                     {"Dipendente":"Giancarlo","Reparto":"IT","Eta":65,"Stipendio":4800,"Anni_servizio":10},])
    filtro_categoria="IT"
    risultato=df.query("Eta>30 and Stipendio>=2000 or Reparto==@filtro_categoria")[["Dipendente","Eta","Stipendio"]]
    risultato["Categoria"]=["Junior" if x<35 else "Senior" for x in risultato["Eta"]]
    risultato_reparto=risultato.groupby("Categoria")["Stipendio"].mean().reset_index()
    print(risultato)
    print(risultato_reparto)
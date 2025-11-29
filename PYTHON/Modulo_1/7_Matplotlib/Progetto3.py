import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
# pip install Faker
from faker import Faker #generatore di nomi
from datetime import datetime

#----------------------------------------
#Parte 2 - Programmazione ad Oggetti (OOP)
#----------------------------------------

#Crea una classe Cliente con attributi: nome, età, vip.

class Cliente:

    _prossimo_codice=1

    def __init__(self, nome:str, eta:int, vip:bool=False):
        self.nome=nome
        if eta>0:
            self.eta=eta
        else:
            raise ValueError("L'età deve essere un numero positivo maggiore di zero!")
        self.vip=bool(vip)
        self.codice=Cliente._prossimo_codice
        Cliente._prossimo_codice+=1

#Aggiungi un metodo per stampare le informazioni.
    def __str__(self):
        return  f"({self.codice}) Nome: {self.nome} di età {self.eta}" + (" (utente VIP)." if self.vip == 1 else ".")
    
# Crea una classe Viaggio con attributi: destinazione, prezzo, durata in giorni.
class Viaggio:
    def __init__(self, destinazione:str, paese:str, prezzo:float, durata_giorni:int):
        self.destinazione=destinazione
        self.paese=paese
        if prezzo>0:
            self.prezzo=round(prezzo,2)
        else:
            raise ValueError("Il prezzo deve essere un numero float positivo maggiore di zero!")
        if durata_giorni>0:
            self.durata_giorni=durata_giorni
        else:         
            raise ValueError("La durata in giorni deve essere un numero intero positivo maggiore di zero!")
    
    def __str__(self):
        return f"Viaggio: {self.destinazione}" + (f" (prezzo {self.prezzo})" if self.prezzo>0 else "")

# Crea una classe Prenotazione che colleghi un cliente a un viaggio.Deve calcolare l’importo finale, con sconto del 10% se il cliente è VIP.Aggiungi un metodo dettagli() che stampa le informazioni complete.
class Prenotazione:
    def __init__(self, cliente:Cliente, viaggio:Viaggio, sconto_vip:float=0.20):
        self.sconto_vip=sconto_vip
        if not isinstance(cliente,Cliente):
            raise TypeError("cliente deve essere un'istanza di Cliente")
            self.cliente=cliente
        if not isinstance(viaggio,Viaggio):
            raise TypeError("viaggio deve essere un'istanza di Viaggio")
        
        self.cliente=cliente
        self.viaggio=viaggio

    def importoFinale(self):
        totale=round(self.viaggio.prezzo - ((self.viaggio.prezzo*self.sconto_vip) if self.cliente.vip else 0),2)
        return totale
    def dettagli(self):
        return f"Il cliente {self.cliente.nome}" + (" (VIP)" if self.cliente.vip else "") + f" ha prenotato il viaggio '{self.viaggio.destinazione}'"
    
    def __str__(self): return f"{self.cliente} -> {self.viaggio}"

print("************************")
print("********CLIENTI*********")
print("************************")
fake = Faker("it_IT")  # locale italiano
clienti=[]
for i in range(10):
    cli=Cliente((fake.first_name() + " " + fake.last_name()),((random.randint(18, 90))), random.randint(0,1))
    clienti.append(cli)
print(f"Aggiunti {i+1} clienti.")
#for c in clienti:
    #print (c)    
#oppure
#clienti=[Cliente("Cliente " + str((random.randint(1, 10))),random.randint(18, 90)) for _ in range(10)]
#oppure
#clienti_list=[("Maria",30),("Ettore",55,True)]
#clienti=[]
#for args in clienti_list:
    #try:
        #clienti.append(Cliente(*args))
    #except ValueError as e:
        #print(f"Cliente scasrtato {args}:{e}")


#----------------------------------------
#Parte 3 NumPy
#----------------------------------------

print("************************")
print("******DESTINAZIONI******")
print("************************")
#Genera un array NumPy di 100 prenotazioni simulate, con prezzi casuali fra 200 e 2000 €.
localita = {"it_IT": "Italia","fr_FR": "Francia","de_DE": "Germania","en_US": "Stati Uniti","es_MX": "Messico","pt_BR": "Brasile"}

#,"es_ES": "Spagna","pt_PT": "Portogallo","en_GB": "Regno Unito","nl_NL": "Paesi Bassi","pl_PL": "Polonia","cs_CZ": "Repubblica Ceca","th_TH": "Thailandia","hi_IN": "India","en_US": "Stati Uniti","es_MX": "Messico","pt_BR": "Brasile","es_AR": "Argentina","af_ZA": "Sudafrica","ar_EG": "Egitto","ar_MA": "Marocco","sw_KE": "Kenya"}
viaggi=[]
visti=set()
for _ in range(100):
    loc = random.choice(list(localita.keys()))
    fake = Faker(loc)
    citta = fake.city()
    paese = localita[loc]
    if (citta,paese) not in visti:
        visti.add((citta,paese))
        viaggi.append(Viaggio(citta,paese,round(random.uniform(200, 2000), 2),random.randint(1, 20)))
print(f"Aggiunte {len(viaggi)} destinazioni")
#for v in viaggi:
    #print(v)         
  
#oppure (paese aggiunto dopo)
#viaggi=[Viaggio("Viaggio " + str((random.randint(200, 2000))),round(random.uniform(200, 2000), 2),random.randint(1, 20)) for _ in range(10)]
#oppure
#viaggi_list = [("Roma",1,0),("Londra", 900.50, 5),("Parigi", 500,3), ("New York", 1500,10),("Milano",30,1),("Venezia",200,2)]
#viaggi = []
#for args in viaggi_list:
    #try:
        #viaggi.append(Viaggio(*args))
    #except ValueError as e:
        #print(f"Viaggio scartato {args}: {e}")
       
print("************************")
print("******PRENOTAZIONI******")
print("************************")
i=100
prenotazioni = np.array([Prenotazione(random.choice(clienti), random.choice(viaggi)) for _ in range(i)])
print(f"Aggiunte {i} prenotazioni")
#for p in prenotazioni:
    #print (p.dettagli())

#Calcola e stampa:prezzo medio,prezzo minimo e massimo,deviazione standard    

#estraggo i prezzi delle prenotazioni

print("************************")
print("******STATISTICHE******")
print("************************")
prezzi = np.array([p.viaggio.prezzo for p in prenotazioni], dtype=float)
#calcolo statistiche
media = prezzi.mean()      
minimo = prezzi.min()        
massimo = prezzi.max()       
dev_std = prezzi.std()    
perc_sopra_media = (np.sum(prezzi > media) / prezzi.size) * 100  
#stampo
print(f"Media: {media:.2f}€, minimo {minimo}€, massimo {massimo}€, deviazione standard {dev_std:.2f}, prenotazioni sopra media {perc_sopra_media:.2f}%")


#----------------------------------------
#Parte 4 – Pandas
#----------------------------------------

fake = Faker("it_IT")
#Crea un DataFrame Pandas con colonne:Cliente, Destinazione, Prezzo, Giorno_Partenza, Durata, Incasso.
data_inizio = datetime(2024, 1, 1)
data_fine = datetime(2025, 12, 31)
riga=[]
for p in prenotazioni:
    data_casuale = fake.date_between_dates(date_start=data_inizio, date_end=data_fine)    
    # sostituisco destinazione con paese perchè troppe destinazioni uniche
    riga.append({"cliente": p.cliente.nome,"destinazione": p.viaggio.paese,"prezzo": p.viaggio.prezzo, "giorno_partenza":data_casuale,"durata": p.viaggio.durata_giorni,"incasso": p.importoFinale()})
    #riga.append({"cliente": p.cliente.nome,"destinazione": p.viaggio.destinazione,"prezzo": p.viaggio.prezzo, "giorno_partenza":data_casuale,"durata": p.viaggio.durata_giorni,"incasso": p.importoFinale()})
df = pd.DataFrame(riga, columns=["cliente","destinazione","prezzo","giorno_partenza","durata","incasso"])
#print(df.head())

# Calcola con Pandas:incasso totale dell’agenzia,incasso medio per destinazione,top 3 destinazioni più vendute.
incasso_totale=round(df["incasso"].sum(),2)
print(f"Incasso totale: {incasso_totale}")
incasso_medio_destinazione=df.groupby("destinazione")["incasso"].mean()
print(f"Incasso medio per destinazione {incasso_medio_destinazione}")
top3_destinazioni=df["destinazione"].value_counts().head(3)
print(f"Top 3 destinazioni più vendute: \n{top3_destinazioni}")

#----------------------------------------
# Parte 5 – Matplotlib
#----------------------------------------

def risposta():
    risp=""
    while risp.upper() not in ("S","N"):
        risp=input("Vuoi visualizzare i grafici della parte 5 S/N")
    return risp.upper()

if risposta()=="S":
    #Crea un grafico a barre che mostri l’incasso per ogni destinazione.
    incasso_per_dest = (df.groupby("destinazione")["incasso"].sum().sort_values(ascending=False))
    print("\nIncasso per destinazione:")
    print(incasso_per_dest)

    plt.figure(figsize=(12, 6))
    plt.bar(incasso_per_dest.index, incasso_per_dest.values)
    plt.title("Incasso per destinazione")
    plt.xlabel("Destinazione")
    plt.ylabel("Incasso (€)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    #Crea un grafico a linee che mostri l’andamento giornaliero degli incassi.
    df_giornaliero = df.groupby("giorno_partenza")["incasso"].sum().reset_index()
    plt.figure(figsize=(12, 6))
    plt.plot(df_giornaliero["giorno_partenza"], df_giornaliero["incasso"], marker='o', linestyle='-')
    plt.title("Andamento giornaliero degli incassi")
    plt.xlabel("Giorno di partenza")
    plt.ylabel("Incasso (€)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    #Crea un grafico a torta che mostri la percentuale di vendite per ciascuna destinazione.
    incasso_per_dest = df.groupby("destinazione")["incasso"].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(incasso_per_dest, labels=incasso_per_dest.index, autopct="%1.1f%%", startangle=140)
    plt.title("Percentuale di incasso per destinazione")
    plt.tight_layout()
    plt.show()

#----------------------------------------
# Parte 6 – Analisi Avanzata
#----------------------------------------
#Raggruppa i viaggi in categorie:
# "Europa", "Asia", "America", "Africa".(Puoi usare un dizionario che associa ogni destinazione a una categoria).
categorie_destinazioni={
    "Italia": "Europa",
    "Francia": "Europa",
    "Spagna": "Europa",
    "Germania": "Europa",
    "Regno Unito": "Europa",
    "Portogallo": "Europa",
    "Paesi Bassi": "Europa",
    "Polonia": "Europa",
    "Repubblica Ceca": "Europa",
    "Cina": "Asia",
    "Giappone": "Asia",
    "Thailandia": "Asia",
    "India": "Asia",
    "Stati Uniti": "America",
    "Messico": "America",
    "Brasile": "America",
    "Argentina": "America",
    "Sudafrica": "Africa",
    "Egitto": "Africa",
    "Marocco": "Africa",
    "Kenya": "Africa"}
df["categoria"]=df["destinazione"].map(categorie_destinazioni)

#Calcola con Pandas:incasso totale per categoria
incasso_per_categoria = (df.groupby("categoria", dropna=True)["incasso"].sum().sort_values(ascending=False)) 
print("\nIncasso totale per categoria:")
print(incasso_per_categoria) 
# 
#durata media dei viaggi per categoria
durate_media_categoria = round((df.groupby("categoria", dropna=True)["durata"].mean().sort_values(ascending=False)),2)
print("\nDurata media dei viaggi per categoria:")
print(durate_media_categoria)

# 
# #Salva il DataFrame aggiornato in un CSV chiamato prenotazioni_analizzate.csv.
df.to_csv("prenotazioni_analizzate.csv", index=False)
print("\nDataFrame salvato in 'prenotazioni_analizzate.csv'")

#----------------------------------------
# Parte 7 – Estensioni
#----------------------------------------

#Crea una funzione che restituisce i N clienti con più prenotazioni.

def top_clienti(df: pd.DataFrame, n: int = 5):
    """Restituisce i N clienti con più prenotazioni."""
    return df["cliente"].value_counts().head(n)

n = 5
print(f"\nTop {n} clienti con più prenotazioni:")
print(df["cliente"].value_counts().head(n))

# Realizza un grafico combinato (barre + linea) che mostri:barre = incasso medio per categoria,linea = durata media per categoria.
# Allineo le categorie: uso l'ordine di incasso_per_categoria
# Realizza un grafico combinato (barre + linea) che mostri:
# barre = incasso totale per categoria
# linea = durata media per categoria

# Allineo le categorie sull'ordine di incasso_per_categoria

plt.figure(figsize=(8, 8))
# grafico a barre=incasso per categoria
plt.subplot(2, 1, 1)
categorie = incasso_per_categoria.index
durate_media_categoria.plot.bar(rot=0) 
plt.title("Incasso medio per categoria (grafico a barre)")
#grafico a linea=durata media per categoria
plt.subplot(2, 1, 2)
plt.plot(incasso_per_categoria, 'ro',)
plt.title("Durata media per categoria (grafico a linea)")
plt.xlabel("Categorie")
plt.ylabel("Durata")
#visualizzo
plt.tight_layout()  
plt.show()

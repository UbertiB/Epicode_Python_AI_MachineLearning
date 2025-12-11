"""
Creazione e gestione avanzata di dataframe
Quando si lavora con dataset di Pandas, spesso diamo per scontato che lemodifche vengono applicate
ai dati originali.
In realtà ci sono operazione che modificano i dati e operazione che portano a copie dei
dati originali.

VIEW
Riferimento diretto ai dati originali, memori efficiente e veloce, modifiche involontarie
ai dati originali
COPY
Crea un oggetto separato e indipendente ai dati, le modifiche non alterano i dati originali.
Occupa più memoria ed è più lenta la creazione, ma la creazione di copie ha il vantaggio di
essere più sicura per evitare di alterare il dataset originale

OPERAZIONE IN-PLACE
Molti metodi di Pandas (come drop, sort_values, reset_index ed altri) 
accettano il parametro in-place che se impostato a true la funzione modifica direttamente
il dataframe originale e non restituisce nulla, mentre se lasciato a false (default) 
restituisce una copia modificata lasciando inalterata la copia originale.
Usare operazioni in place è utile quando vogliamo risparmiare memoria 

Combinare slicing, boolen, indexing, e query o altre operazioni che restituiscono dei subset
in molti casi è una view implicita, per questo motivo, quando vogliamo alterare un
subset e sempre buona cosa creare una copia esplicita con copy

"""

import pandas as pd

#
#.CoPY (crea una copia dell'originale su cui lavorare)
#
df=pd.DataFrame({
    "Studente":["Anna","Luca","Marco","Giulia","Sara"],
    "Materia":["Matematica","Fisica","Matematica","Chimica","Matematica"],
    "Voto":[27,24,30,28,26],
    "Classe":["A","B","A","C","B"]
})
matematica=df[df["Materia"]=="Matematica"].copy()
matematica["Voto_arrotondato"]=matematica["Voto"].apply(lambda x: x +1 if x<28 else x)

print(matematica)
print(df)

#
#OPERAZIONI INPLACE=True  (cambia l'orignale senza avere una copia)
#
prodotti=pd.DataFrame({
    "Prodotto":["Laptop","Mouse","Tastiera","Monitor"],
    "Categoria":["Tecnologia","Accessori","Accessori","Tecnologia"],
    "Prezzo":[1200,24,45,300],
    "Quantita":[5,50,30,10]
})
prodotti.drop(columns=["Categoria","Quantita"],inplace=True)
prodotti.sort_values("Prezzo",ascending=False,inplace=True)
prodotti["Fatturato"]=prodotti["Prezzo"]*2
print(prodotti)

#
#Pipeline sicura con boolean indexing
#
dipendenti=pd.DataFrame({
    "Dependente":["Mario","Laura","Gianni","Elena","Paolo"],
    "Reparto":["IT","HR","IT","Marketing","IT"],
    "Eta":[40,30,28,35,50],
    "Stipendio":[2500,2000,1800,2200,3000]
})
top_dipendenti=dipendenti[dipendenti["Stipendio"]>2000].copy()
top_dipendenti["Senior"]=["Vero" if x>=35 else "Falso" for x in top_dipendenti["Eta"]]
#top_dipendenti["Senior"]=top_dipendenti["Eta"].apply(lambda x: True if x>=35 else False)
top_dipendenti.sort_values("Stipendio",ascending=False,inplace=True)
top_dipendenti.reset_index(drop=True,inplace=True)
print(top_dipendenti)
print(dipendenti)

#Combinazione di copy ed inplace
df_clienti=pd.DataFrame({
    "Cliente":["Alice","Bob","Carla","Daniele","Elisa"],
    "Spesa":[1200,800,950,1500,2000],
    "Citta":["Roma","Milano","Roma","Torino","Milano"]
})
top_clienti=df_clienti[df_clienti["Spesa"]>1000].copy()
top_clienti["Vip"]=[True if x>1500 else False for x in top_clienti["Spesa"]]
top_clienti.sort_values("Spesa",ascending=False,inplace=True)
top_clienti.reset_index(drop=True,inplace=True)
print(top_clienti)
print(df_clienti)
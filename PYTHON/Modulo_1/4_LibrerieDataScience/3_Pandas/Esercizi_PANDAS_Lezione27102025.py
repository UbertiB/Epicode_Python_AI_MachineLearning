import pandas as pd
import numpy as np

class Prodotto:
    def __init__(self, nome, prezzo, quantita, categoria):
        self.nome=nome
        self.prezzo=prezzo
        self.quantita=quantita
        self.categoria=categoria

    def ricavo_totale(self):
        return self.prezzo*self.quantita
    

vendite_dati={"Nome":["Mouse","Tastiera","Zaino","Notebook","Penna","Quaderno","Monitor"],
            "Prezzo":  [25.99,45.50,50.00,799.99,1.50,2.00,199.00] ,           
            "Quantita":[4,2,3,1,20,15,2],
            "Categoria": ["Elettronica","Elettronica","Acessori","Informatica","Cancelleria","Cancelleria","Elettronica"]}

df=pd.DataFrame(vendite_dati)
df["Ricavo"]=df["Prezzo"]*df["Quantita"]
media_ricavi=df["Ricavo"].mean()
somma_ricavi=df["Ricavo"].sum()
massimo_ricavi=df["Ricavo"].max()
minimo_ricavi=df["Ricavo"].min()
deviazione_str=np.std(df["Ricavo"])

print (f"Statistiche su ricavi:")
print(f"Media: {media_ricavi}")
print(f"Somma ricavi: {somma_ricavi}")
print(f"Massimo ricavo: {massimo_ricavi}")
print(f"Minomo ricavo: {minimo_ricavi}")
print(f"deviazione standard: {deviazione_str} \n")

vendite_per_categoria=df.groupby("Categoria")["Ricavo"].sum()
print("Totale vendite per categoria:")
print(vendite_per_categoria,"\n")

prodotto_top=df.loc[df["Quantita"].idxmax()]
print(f"Prodotto più venduto: {prodotto_top["Nome"]} {prodotto_top["Quantita"]} unita)\n")



              
    
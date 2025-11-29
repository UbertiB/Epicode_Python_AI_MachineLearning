"""
crea file csv
"""

import csv

#scrivi file con .writer (passando lista)
with open("studenti_lista.csv","w",newline="",encoding="utf-8") as f:
    scrivi=csv.writer(f)
    #devo passare una lista quindi utilizzo le parentesti []
    scrivi.writerow(["nome","eta","corso"])
    scrivi.writerow(["Luca","18","Informatica"])
    scrivi.writerow(["Anna","22","Matematica"])
    scrivi.writerow(["Cristian","28","Fisica"])
    scrivi.writerow(["Paolo","18","Informatica"])

#leggi file con .reader (ricevendo lista)
with open("studenti_lista.csv","r",encoding=("utf-8")) as f:
    leggi=csv.reader(f)
    for riga in leggi:
        print(riga)

#scrivi file con .writer (passando dizionario)
with open("studenti_dict.csv","w",newline="",encoding="utf-8") as f:
    campi=["nome","eta","corso"]
    scrivi=csv.DictWriter(f,fieldnames=campi)
    scrivi.writeheader() #scrive la riga di intestazione preparata con la riga precedente
    #devo passare una lista quindi utilizzo le parentesti []
    scrivi.writerow({"nome":"Luca","eta":"18","corso":"Informatica"})
    scrivi.writerow({"nome":"Anna","eta":"22","corso":"Matematica"})
    scrivi.writerow({"nome":"Cristian","eta":"28","corso":"Fisica"})
    scrivi.writerow({"nome":"Paolo","eta":"18","corso":"Informatica"})

#leggi file con .reader (ricevendo dizionario)
with open("studenti_dict.csv","r",encoding=("utf-8")) as f:
    leggi=csv.DictReader(f)
    for riga in leggi:
        print(riga["nome"],riga["corso"])        

#filtrare i dati
with open("studenti_dict.csv","r",encoding=("utf-8")) as f:
    leggi=csv.DictReader(f)
    for riga in leggi:
        if riga["corso"]=="Informatica":
            print(riga["nome"])

#crea un nuovo csv solo con dati filtrati
with open("studenti_dict.csv","r",encoding=("utf-8")) as f_in,open("studenti_csv_filtrati.csv","w",newline="", encoding="utf-8") as f_out:
    leggi=csv.DictReader(f_in)
    scrivi=csv.DictWriter(f_out,fieldnames=["nome", "eta","corso"])
    scrivi.writeheader()
    for riga in leggi:
        if riga["corso"]=="Informatica":
            scrivi.writerow(riga)
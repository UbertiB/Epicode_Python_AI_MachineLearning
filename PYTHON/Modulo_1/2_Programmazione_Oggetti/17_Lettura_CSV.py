"""
CSV uno dei formati file più uilizzati
file di testo con il valori separati da una virgola o altro separatore.
Utilizzato per scambiare dati tra programmi diversi, è utile per salvare dati, è semplice da utilizzare e leggibile a occhio nudo
Posso avere una prima riga di intestazione e successivamente i dati veri e propri
Separatore spesso la virgola, nei files italiani spesso il punto e virgola perchè la virga è il separatore decimale.
Python ha una libreria intera per files csv
"""

import csv
#con csv.reader ogni riga diventa una lista di stringhe
with open(r"c:\Users\uberti\iCloudDrive\Barbara\EPICODE\PYTHON\MODULO 1\2_Programmazione_Oggetti\nomefile.csv","r") as f:
    testo=csv.reader(f)
    for riga in testo:   #ogni riga diventa una lista di valori (stringa) ogni campo della lista sono i campi del file
        print(riga)

#con csv.DictReader ogni riga diventa un dizionario, si accede ai campi con il nome di colonna
with open(r"c:\Users\uberti\iCloudDrive\Barbara\EPICODE\PYTHON\MODULO 1\2_Programmazione_Oggetti\nomefile.csv","r") as f:
    testo=csv.DictReader(f)
    for riga in testo:
        print(riga["nome"],riga["corso"])


#incapsulare in una classe (consigliato)
class GestoreCSV:
    def __init__(self,file):
        self.file=file
    def leggi(self):
        try:
            with open(self.file,"r",encoding=("utf-8")) as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            print("File non trovato")
            return
f1=GestoreCSV(r"c:\Users\uberti\iCloudDrive\Barbara\EPICODE\PYTHON\MODULO 1\2_Programmazione_Oggetti\nomefile.csv")
for l in (f1.leggi()):
    print(f"nome:{l["nome"]} - corso: {l["corso"]}")

#gestione errori

    
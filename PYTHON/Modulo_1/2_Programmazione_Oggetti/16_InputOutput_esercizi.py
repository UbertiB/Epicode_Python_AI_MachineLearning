"""
- crea una class Studente che chiede nome, eta ed abbia un metodo presentati()
- aggiungi a Studnete un medoto __str__ che restituisce una stringa leggibile
- crea una classe Diario che salvi su un file un messaggio passato dall'utente
- Aggiunti un metodo che legga dal file e stampi i messaggi
"""

import json

class Studente():
    def __init__(self, nome, eta):
        self.nome=nome
        self.eta=eta
    def presentati(self):
        print(F"Ciao, mi chiamo {self.nome} ed ho {self.eta} anni.")

class Diario:
    def __init__(self, nome_file):
        self.nome_file = nome_file

    def messaggio(self, testo=None):
        if testo is None:
            testo = input("Scrivi il messaggio: ")
        with open(self.nome_file, "w", encoding="utf-8") as f:
            json.dump({"messaggio": testo}, f)

    def leggi_messaggi(self):
        with open(self.nome_file, "r", encoding="utf-8") as f:
            dati = json.load(f)
        print(dati["messaggio"])

d1 = Diario("c://temp//temp.txt")
d1.messaggio("Ciao dal diario")
d1.leggi_messaggi()
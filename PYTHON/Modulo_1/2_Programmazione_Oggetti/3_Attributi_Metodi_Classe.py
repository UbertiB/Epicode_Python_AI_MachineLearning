"""
una classe è un modello che descrive gli oggetti
oltre agli oggetti (istanze) possiamo associare attributi e metodo direttamente
alle classe stesssa, cioè condivisi da tutte le istanze
Un attributo è una variabile collegata a una classe o a un oggetto

- Attributi di istanza: appartengono al singolo oggetto
- Attributi di classe: appartengono alla classe e sono condivisi da tutte le istanze
- Metodi di istanza
- Metodo di classe
- Metodo statici

"""

#attributi di istanza: variabile collegata ad un oggetto, 
# il loro valore cambia da oggetto ad oggetto
class Cane:
    def __init__(self,nome):
        self.nome=nome
fido=Cane("Fido")
luna=Cane("Luna")
print(fido.nome)
print(luna.nome)

#attributi di classe: non appartiene al singolo oggetto, ma alla classe in generale
#condiviso da tutti gli oggetti, esempio tutti i cani appartengono alla stessa specie
class Cane:
    specie="Canis lupus familiaris"
    def __init__(self, nome):
        self.nome=nome
fido=Cane("Fido")
luna=Cane("Luna")
print(fido.specie)
print(luna.specie)

#se modifico un attrinuto di classse, la modifica si riflette su tutte le istanze
#a meno che l'istanza non abbia un attributo con lo stesso nome (diventa prioritario)

#Metodi di istanza: funzioni definite all'interno di una classe. 
#ricevono self ed operano sull'oggetto
#sono i più comuni e identificano l'oggetto stesso e lavorano con dati
#specifici dell'oggetto (self.)
class Persona:
    def __init__(self, nome):
        self.nome=nome
    def saluta(self):
        print(f"Ciao, mi chiamo {self.nome}.")
p=Persona("Barbara")
p.saluta() #Ciao mi chiamo Barbara

#Metodi di classe: funzioni definite all'interno di una classe
#ricevono cls
#se definiscono con il decoratore @classmethod, servono per lavorare sugli attributi di classe
#per gestire informazioni globali
class Cane:
    numero_cani=0
    def __init__(self,nome):
        self.nome=nome
        Cane.numero_cani+=1
    @classmethod
    def conta_cani(cls):
        return cls.numero_cani

#Metodi di statici: funzioni definite all'interno di una classe
#non ricevono cls e non ricevono self
#sono funzioni normali definite nella classe solo perchè hanno un legame logico con essa
#sono un modo per organizzare meglio il codice (invece di creare funzioni sparse di qua e di la)
class Matematica:
    @staticmethod
    def somma(a,b):
        return a+b
print(Matematica.somma(3,5)) #8



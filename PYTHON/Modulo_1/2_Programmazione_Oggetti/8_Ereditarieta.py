"""
strumento potente per creare nuove classi basate su classi già esistenti
riutilizzando metodi ed attributi già scritti e presenti.
Questo migliora organizzazione del codice, riduce i bug, la manutenzione e la leggibilità
Se più classi condividono alcune caratteristiche invece di riscrivere il codice,
possiamo creare una classe con ereditarietà
Possiamo creare una classe generale che raggruppa le caratteristiche comuni (attributi e metodo)
poi definiamo classi più specifiche che riprendono attributi e metodi dalla classe generale
ed andiamo a specificare gli attributi e metodo solo della "nuova classe" la classe più specifica

"""
class Autoveicoli:
    def __init__(self, tipo):
        self.tipo = tipo

    def muovi(self):
        return "mi muovo"

    def __str__(self):
        return f"tipo: {self.tipo}"


class Ruote:
    def __init__(self, numero):
        self.numero = numero

    def __str__(self):
        return f"n. di ruote: {self.numero}"


class Macchine(Autoveicoli, Ruote):
    def __init__(self, marca, nome, targa, numero_ruote):
        # inizializzo le classi base
        Autoveicoli.__init__(self, tipo="macchina")
        Ruote.__init__(self, numero_ruote)

        # attributi propri di Macchine
        self.marca = marca
        self.nome = nome
        self.targa = targa

    def __str__(self):
        # uso esplicitamente gli __str__ delle basi
        base_veicolo = Autoveicoli.__str__(self)
        base_ruote = Ruote.__str__(self)
        return f"{base_veicolo}, {base_ruote}, marca: {self.marca}, nome: {self.nome}, targa: {self.targa}"


a = Macchine("Fiat", "500X", "AA000AA", 4)
print(a)


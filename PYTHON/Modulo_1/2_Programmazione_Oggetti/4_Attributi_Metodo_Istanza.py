
"""
attributi che riguardano il singolo oggetto e la sua identità.
cos'è un'istanza: una classe è un progetto, quando utilizziamo la classe, 
creamo un oggetto concreto, quello si chiama istanza (esempio cane fido, cane è la classe, fido è l'istanza)
Quando creamo un'istanza, ogni istanza ha i propri valori (propri attributi) che li caratterizzano.
All'inerno del motodo init vanno definiti gli attributi di istanza, quelli che appartengono ad un oggetto specifico
la parola chiave self, raggruppa tutti gli attributi di istanza.
Cambiare un attributo di istanza non cambia lo stesso attributo per tutti gli altri che utilizzano la classe (a diversità degli attributi di classe)
Possiamo creare nuovi attributi anche su un istanza già esistente (attributi creati "al volo"), non sono consigliati.
Quindi nell'esempio sotto, fido può avere attributi di istanza non previsti in luna.
Oltre ai dati, ogni oggetto ha dei comportamenti, questi sono i metodi di istanza.
Un metodo è una funziona scritta all'interno di una classe, prende come primo parametro self
Quando utilizzo un motodo di istanza, il parametro self è il collegamento che ha invocato il metodo e non devo passarlo, si ne occupa python

"""
class Cane:
    n=0
    def __init__(self,Nome):
        self.nome=Nome
        Cane.aggiungicane()
    def presentati(self):
        return f"Mi chiamo: {self.nome.title()}"
    @classmethod
    def aggiungicane(cls):
        cls.n+=1
    @classmethod
    def contatore(cls):
        return(cls.n)
fido=Cane("fido")
luna=Cane("luna")
print(fido.presentati())
print(luna.presentati())
fido.soprannome="fil" #attributo creato al volo esiste solo in fido e non in luna
print(f"{fido.presentati()} soprannome ({fido.soprannome})")
print(Cane.contatore())







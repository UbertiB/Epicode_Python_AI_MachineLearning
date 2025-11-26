"""
crea due classi
product con nome e prezzo
e shopping card deve permettere di aggiungere rimuovere prodotti
per simulare un carrello
implemente + unione carrelli len e str
"""

class Prodotto:
    def __init__(self, nome, prezzo:float):
        self.nome=nome
        self.prezzo=prezzo
    def __str__(self):
        return f"Prodotto: {self.nome} - prezzo: {self.prezzo}"
    def __eq__(self, altro):
        if not isinstance(altro, Prodotto):
            return False
        return self.nome==altro.nome and self.prezzo==altro.prezzo
    
class ShoppingCard:
    def __init__(self):
        self.elementi=[] #lista vuota
    def aggiungi_prodotto(self, prodotto:Prodotto):
        self.elementi.append(prodotto)
    def rimuovi_prodotto(self,prodotto:Prodotto):
        if prodotto in self.elementi:
            self.elementi.remove(prodotto)
    def totale_prezzo(self):
        #return sum(p.prezzo for p in self.elementi)
        prezzo=0.00
        for p in self.elementi:
            prezzo+=p.prezzo
        return prezzo
    def __len__(self):
        return len(self.elementi)
    def __str__(self):
        if not self.elementi:
            return "Carrello vuoto"
        linea=""
        for p in self.elementi:
            linea=linea + f"{p} "
        linea=(f"{linea} \nTotale: {self.totale_prezzo()}")
        return linea
    def __add__(self, altro):
        new_card=ShoppingCard()
        new_card.elementi=self.elementi+altro.elementi
        return new_card
    
if __name__=='__main__':
    penna=Prodotto("Penna",1.50)
    quaderno=Prodotto("Quaderno",2)
    libro=Prodotto("Libro",15.45)

    car1=ShoppingCard()
    car2=ShoppingCard()

    car1.aggiungi_prodotto(penna)
    car1.aggiungi_prodotto(quaderno)
    car2.aggiungi_prodotto(libro)
    car2.aggiungi_prodotto(penna)

    print ("Carrello 1:")
    print(car1)
    print ("Carrello 2:")
    print(car2)

    print("Aggiungo a carrello 1")
    car2.aggiungi_prodotto(libro)
    print("Carrello 2:")
    print(car2)

    print("Rimuovo da carrello 1")
    car1.rimuovi_prodotto(libro)
    print("Carrello 1:")
    print(car1)    



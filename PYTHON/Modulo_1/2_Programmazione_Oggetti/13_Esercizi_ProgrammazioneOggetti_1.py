
from abc import ABC, abstractmethod

"""
Crea una classe astratta che rappresenta un conto bancario generico, non può essere istanzionata direttamente
"""

class Conto(ABC):
    def __init__(self, intestatario, saldo_iniziale=0) -> None:
        self._intestatario = intestatario
        self._saldo = saldo_iniziale
    @property #permette di accedere al saldo in sola lettura
    def saldo(self): #restituisce il saldo, allo stesso tempo non posso impostarlo (devo prelevare o depositare)
        return self._saldo
    
    @staticmethod #metodo che non fa riferimento nè a cls nè a self
    def valuta_importo(importo):
        return importo>0
    @abstractmethod
    def deposita(self, importo):
        pass
    @abstractmethod
    def preleva(self, importo):
        pass
    def __str__(self):
        return f"Conto di {self._intestatario} - Saldo: {self._saldo:.2f} Euro"
class ContoCorrente(Conto):
    commissione=1.5
    def __init__(self, intestatario, saldo_iniziale=0):
        super().__init__(intestatario, saldo_iniziale)
    def deposita(self, importo):
        if self.valuta_importo(importo):
            self._saldo+=importo
        else:
            print(f"Importo non valido ({importo}) per il deposito!")
    def preleva(self,importo):
        totale=importo+ContoCorrente.commissione
        if self.valuta_importo(importo) and self._saldo>=totale:
            self._saldo-=totale
        else:
            print(f"Saldo insufficiente o importo non valido")
    def __add__(self,altro):
        Nuovosaldo=self._saldo+altro._saldo
        return f"Conto corrente di: (({self._intestatario} e {altro._intestatario} & {altro._intestatario})"
    
if __name__ == "__main__":
    cc1=ContoCorrente("Luca",1000)
    cc2=ContoCorrente("Giulia",500)
                      
cc1.deposita(200)
cc1.preleva(50)
print(cc1)
conto_fuso=(cc1+cc2)
print(conto_fuso)

        

"""
crea una classe ContoBancario con 
- attibuto provato __saldo
- metodo deposita(importo) che aggiunge solo se >0
- metodo preleva (importo) che riduse saldo solo se sufficiente
"""

class ContoBancario:
    def __init__(self, nome):
        self.nome=nome
        self.__saldo=0
    def deposita(self, importo):
        if importo>0:
            self.__saldo-=importo
        else:
            raise NameError ("Importo negativo")
    def preleva(self,importo):
        if self.__saldo>=importo:
            self.__saldo-=importo
        else:
            raise NameError ("fondi insufficenti")

    def get_importo(self):
        return self.__saldo
    
c1=ContoBancario("Mario Rossi")
c1.deposita(3000)
try:
    c1.preleva(200)
except ValueError as e:
    print("Errore prelievo:", e)

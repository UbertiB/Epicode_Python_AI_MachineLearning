"""
ECCEZIONI PERSONALIZZATE
in certi contesti, soprattutto all'interno di programmazione ad oggetti, ci possiamo
trovare davanti a situazioni particolari che non rientrano nei casi già previsti
da Python, possiamo creare nuove eccezioni con due vantaggi, il primo per dare messaggi
di errore molto più chiari rispetto allo standard, il secondo di rapprensetare
errori specifici per il nostro contesto.

"""
#creaiamo una classe che eredita da exception
class MioErrore(Exception):
    pass
#per sollevare un errore utilizzo rais MioErrore ("descrizione errore")

class SaldoInsufficienteErrore(Exception):
    pass
class ContoBancario:
    def __init__(self, saldo):
        self.saldo=saldo
        
    def preleva(self,importo):
        if importo>self.saldo:
            raise SaldoInsufficienteErrore("Saldo insufficiente")
        self.saldo-=importo

c1=ContoBancario(500)
try:
    c1.preleva(600)
except ValueError as e:
    print(e)

"""
le eccezioni personalizzate non devono essere vuote, possiamo arricchirle
con più informazioni
E' possibile passare informazioni "extra", per avere a disposizione
attributi riferiti al contesto
"""
class SaldoInsufficienteError(Exception):
    def __init__(self,saldo,importo):
        super().__init__(f"Saldo {saldo}, tentato prelievo {importo}")
        self.saldo=saldo
        self.importo=importo

try:
    c1=ContoBancario(100)
    c1.preleva(200)
except SaldoInsufficienteError as e:
    print("Errore personalizzato {e}")

"""
le eccezioni personalizzate sono molto utili nella programmazione ad oggetti
perchè si modellano in base al contesto della classe e non genericamente come le eccezioni standard
Con messaggi chiari aiutiamo l'utente ma anche nella fase di debug.
"""
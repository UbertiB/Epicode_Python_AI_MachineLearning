"""
crea una classe Veicolo con metodo astratto muovi()
crea due classi derivate:
- Auto - muovi() stampa "l'auto si muove su strada"
- Aereo - muovi() stampa "l'aereo vola nel cielo"
scrivi una funzione che accetti un generico veicolo e chiami muovi()
"""

from abc import ABC,abstractmethod
class Veicolo(ABC):
    @abstractmethod
    def muovi(self):
        pass
class Auto(Veicolo):
    def __init__(self, targa):
        self.targa=targa
    def muovi(self):
        print("L'auto si muove per strada")
class Aereo(Veicolo):
    def __init__(self, telaio):
        self.telaio=telaio
    def muovi(self):
        print ("L'aereo vola in cielo")

a1=Auto("qw234re")
a2=Auto("oi854po")
a3=Auto("nb741ew")
a11=Aereo("wewefgdgdhfghfghfgnfg")
a12=Aereo("sdfgsddfsdfsdghdfhjfg")
a13=Aereo("qadascksdgidfbdfgdfgh")

def muoviti(v:Veicolo):
    print (v.muovi())

muoviti(a1)
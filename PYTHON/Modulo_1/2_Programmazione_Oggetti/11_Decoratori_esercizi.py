"""
crea una classe Studente che abbia:
- @classbethod per creare uno studente a partire da una stringa, tipo: "Luca-20-Matematica"
- @property per calcolare automaticamenet l'anno di nascita a partire dall'età
- @property con setter per impedire età negative
"""

class Studente:
    def __init__(self, nome, eta, corso):
        self.nome=nome
        self.eta=eta
        self.corso=corso
    @classmethod
    def from_string(cls, data_str):
        nome, eta, corso = data_str.split('-')
        return cls(nome, int(eta), corso)
    @property
    def anno_nascita(self):
        anno_corrente = 2025
        return anno_corrente - self.eta 
    #@anno.setter
    def eta(self, valore):
        if valore < 0:
            raise ValueError("L'età non può essere negativa.")
        self._eta = valore

studente1 = Studente.from_string("Luca-20-Matematica")
print(studente1.nome)  # Output: Luca
print(studente1.eta)   # Output: 20
print(studente1.anno_nascita)  # Output: 2005
.




from abc import ABC, abstractmethod
import math

# ==============================
# CLASSE ASTRATTA
# ==============================
class Forma(ABC):
    """
    Classe astratta che definisce un contratto:
    ogni forma geometrica deve implementare i metodi area() e perimetro().
    """
    
    @abstractmethod
    def area(self):
        """Metodo astratto: calcola l'area della forma."""
        pass

    @abstractmethod
    def perimetro(self):
        """Metodo astratto: calcola il perimetro della forma."""
        pass

    # Overloading dell'operatore == per confrontare le aree
    def __eq__(self, altra):
        """
        Due figure sono considerate uguali se hanno la stessa area.
        math.isclose() serve per confrontare numeri decimali con una piccola tolleranza.
        """
        return math.isclose(self.area(), altra.area())

    # Metodo comune per stampare le informazioni in modo leggibile
    def __str__(self):
        return f"{self.__class__.__name__} - Area: {self.area():.2f}, Perimetro: {self.perimetro():.2f}"


# ==============================
# CLASSE RETTANGOLO
# ==============================
class Rettangolo(Forma):
    """Classe concreta che rappresenta un rettangolo."""
    
    def __init__(self, base, altezza):
        # Inizializzo i lati del rettangolo
        self.base = base
        self.altezza = altezza

    def area(self):
        # Formula area rettangolo: base * altezza
        return self.base * self.altezza

    def perimetro(self):
        # Formula perimetro rettangolo: somma di tutti i lati
        return 2 * (self.base + self.altezza)


# ==============================
# CLASSE CERCHIO
# ==============================
class Cerchio(Forma):
    """Classe concreta che rappresenta un cerchio."""
    
    def __init__(self, raggio):
        # Uso un attributo protetto per mostrare buona pratica
        self._raggio = raggio

    @property
    def raggio(self):
        """Restituisce il raggio del cerchio (solo lettura)."""
        return self._raggio

    @property
    def diametro(self):
        """Diametro calcolato automaticamente: raggio * 2."""
        return self._raggio * 2

    def area(self):
        # Formula area cerchio: π * raggio^2
        return math.pi * self._raggio ** 2

    def perimetro(self):
        # Formula circonferenza: 2 * π * raggio
        return 2 * math.pi * self._raggio


# ==============================
# FIGURA COMPOSTA (OVERLOADING DI +)
# ==============================
class FiguraComposta(Forma):
    """
    Figura che rappresenta la combinazione di due forme.
    Serve per dimostrare l'overloading di +.
    """
    def __init__(self, forma1, forma2):
        self.forma1 = forma1
        self.forma2 = forma2

    def area(self):
        # Area totale = somma delle aree delle due forme
        return self.forma1.area() + self.forma2.area()

    def perimetro(self):
        # Perimetro totale = somma dei perimetri delle due forme
        return self.forma1.perimetro() + self.forma2.perimetro()

    def __str__(self):
        return f"FiguraComposta - Area Totale: {self.area():.2f}"


# Aggiungiamo l'operatore + alla classe base "Forma"
Forma.__add__ = lambda self, altra: FiguraComposta(self, altra)


# ==============================
# DEMO FINALE
# ==============================
if __name__ == "__main__":
    # Creo due figure: un rettangolo e un cerchio
    rett = Rettangolo(4, 6)
    cerchio = Cerchio(3)

    # Stampo le informazioni di base
    print("=== Figure iniziali ===")
    print(rett)
    print(f"Diametro del cerchio: {cerchio.diametro}")
    print(cerchio)

    # Polimorfismo: lista con oggetti di classi diverse
    print("\n=== Polimorfismo ===")
    figure = [rett, cerchio]
    for figura in figure:
        # Qui non importa quale sia il tipo di figura,
        # Python sa chiamare i metodi corretti di area() e perimetro()
        print(figura)

    # Confronto tra figure usando ==
    print("\n=== Confronto aree ===")
    print("Il rettangolo e il cerchio hanno la stessa area?", rett == cerchio)

    # Combinazione di figure con l'operatore +
    print("\n=== Combinazione con + ===")
    figura_totale = rett + cerchio
    print(figura_totale)


        

    
    




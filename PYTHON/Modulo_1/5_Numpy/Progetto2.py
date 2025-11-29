# laboratorio_medico.py
# Requisiti: Python 3.10+ e numpy
# pip install numpy

from __future__ import annotations
from typing import List, Tuple, Optional
import numpy as np


# =========================
# Parte 1 – Variabili e Tipi di dati
# =========================

#Definire le variabili necessarie per rappresentare:Nome, cognome e codice fiscale di un paziente (stringhe).Età e peso del paziente (interi e float).Lista delle analisi effettuate (lista di stringhe).

nome1, cognome1, codice_fiscale1 = "Mario", "Rossi", "RSSMRO753ED8889DDD21"
eta1, peso1 = 45, 78.5
analisi1 = ["emocromo", "glicemia", "colesterolo"]

nome2, cognome2, codice_fiscale2 = "Anna", "Bianchi", "BNCHNA873ED8889DDD43"
eta2, peso2 = 33, 60.2
analisi2 = ["ferritina", "emocromo", "vitamina D"]

nome3, cognome3, codice_fiscale3 = "Marco", "Verdi", "VRDMRC873ED8889DDD44"
eta3, peso3 = 52, 85.0
analisi3 = ["glicemia", "colesterolo", "trigliceridi"]


# =========================
# Parte 2 – Classi e OOP
# =========================


#Creare una classe Analisi che contenga:
#Tipo di analisi (es. glicemia, colesterolo).
#Risultato numerico.
#Metodo valuta() che stabilisca se il valore è nella norma (criteri inventati da voi).
class Analisi:
    """
    Rappresenta una singola analisi di laboratorio.
    - analisi: stringa (es. 'glicemia', 'colesterolo', ...)
    - valore: float (risultato numerico)
    - intervallo_riferimento: tupla (minimo, massimo) opzionale
    """
    def __init__(self, analisi: str, valore: float, intervallo_riferimento: Optional[Tuple[float, float]] = None):
        self.analisi = analisi
        self.valore = float(valore)
        self.intervallo_riferimento = intervallo_riferimento
     
    def valuta(self) -> str:
        """
        Determina se il valore è nella norma.
        Se è definito intervallo_riferimento=(min,max), usa quello.
        Altrimenti applica criteri di default (inventati ma plausibili).
        """

        valore_minimo=0.00
        valore_massimo=0.00
        if self.intervallo_riferimento is not None:
            valore_minimo, valore_massimo = self.intervallo_riferimento
        
        if valore_minimo==0 or valore_massimo==0:
            # Criteri standard, da utilizzare se non fornito il range
            criteri_default = {
                "glicemia": (70, 99),        
                "colesterolo": (0, 200),    
                "trigliceridi": (0, 150),    
                "emocromo": (4.0, 5.5),    
                "ferritina": (20, 250),     
                "vitamina D": (20, 50),     
                }
            valore_minimo, valore_massimo = criteri_default.get(self.analisi, (0.0, 9999.0))

        if self.valore < valore_minimo:
            return f"BASSO (val={self.valore}, rif={valore_minimo}-{valore_massimo})"
        if self.valore > valore_massimo:
            return f"ALTO (val={self.valore}, rif={valore_minimo}-{valore_massimo})"
        return f"NELLA NORMA (val={self.valore}, rif={valore_minimo}-{valore_massimo})"   
           
    def __str__(self) -> str:
        return f"Analisi: {self.analisi}, valore={self.valore} "    
    def __repr__(self) -> str:
        return f"Analisi(analisi='{self.analisi}', valore={self.valore})"

#Creare una classe Paziente con:
#Attributi: nome, cognome, codice_fiscale, eta, peso, analisi_effettuate.
#Metodo scheda_personale() che restituisca una stringa con i dati principali del paziente.
class Paziente:
    """
    Rappresenta un paziente del centro.
    - analisi_effettuate: lista di oggetti Analisi
    - risultati_analisi: array NumPy dei soli valori numerici (sincronizzato su richiesta)
    """
    def __init__(self, nome: str, cognome: str, codice_fiscale: str, eta: int, peso: float):
        self.nome = nome
        self.cognome = cognome
        if len(codice_fiscale)==20:
            self.codice_fiscale = codice_fiscale
        else:    
            self.codice_fiscale=""
            raise ValueError ("Valorizzare correttamente il codice fiscale")
        if int(eta)<=0:
            self.eta=0
            raise ValueError ("Valorizzare correttamente l'età'")
        else:
            self.eta = int(eta)
        if int(peso)<=0:
            self.peso=0
            raise ValueError ("Valorizzare correttamente il peso")
        else:    
            self.peso=peso
        self.analisi_effettuate: List[Analisi] = []  # lista di analisi (vuota)
        self.risultati_analisi: np.ndarray = np.array([], dtype=float)  ##array np (vuto)

    def aggiungi_analisi(self, analisi: Analisi) -> None:
        self.analisi_effettuate.append(analisi)

    def sincronizza_array(self) -> None:
        """Aggiorna l'array NumPy dai valori nelle analisi_effettuate."""
        if self.analisi_effettuate:
            self.risultati_analisi = np.array([a.valore for a in self.analisi_effettuate], dtype=float)
        else:
            self.risultati_analisi = np.array([], dtype=float)

    def scheda_personale(self) -> str:
        return (
            f"Paziente: {self.nome} {self.cognome} (CF: {self.codice_fiscale})\n"
            f"Età: {self.eta} anni | Peso: {self.peso} kg\n"
            f"Analisi: {[a.analisi for a in self.analisi_effettuate]}"
        )

    def statistiche_analisi(self) -> Optional[dict]:
        """
        Calcola media, min, max, deviazione standard sui risultati (NumPy).
        Ritorna None se non ci sono analisi.
        """
        self.sincronizza_array()
        if self.risultati_analisi.size == 0:
            return None
        return {
            "media": float(np.mean(self.risultati_analisi)),
            "minimo": float(np.min(self.risultati_analisi)),
            "massimo": float(np.max(self.risultati_analisi)),
            "dev_std": float(np.std(self.risultati_analisi, ddof=0)),  # popolazione
        }

#Creare una classe Medico con:
#Attributi: nome, cognome, specializzazione.
#Metodo visita_paziente(paziente) che stampi quale medico sta visitando quale paziente.
class Medico:
    def __init__(self, nome: str, cognome: str, specializzazione: str):
        self.nome = nome
        self.cognome = cognome
        self.specializzazione = specializzazione

    def visita_paziente(self, paziente: Paziente) -> None:
        print(f"Il Dr./D.ssa {self.nome} {self.cognome} ({self.specializzazione}) visita {paziente.nome} {paziente.cognome}.")


# =========================
# Parte 3 – Uso di NumPy
# =========================

def statistiche_campione_glicemia(valori_glicemia: np.ndarray) -> dict:
    """
    Dato un array NumPy con i valori di glicemia per 10 pazienti,
    calcola media, max, min, std.
    """
    if not isinstance(valori_glicemia, np.ndarray):
        valori_glicemia = np.array(valori_glicemia, dtype=float)
    return {
        "media": float(np.mean(valori_glicemia)),
        "massimo": float(np.max(valori_glicemia)),
        "minimo": float(np.min(valori_glicemia)),
        "dev_std": float(np.std(valori_glicemia, ddof=0)),
    }


# =========================
# Parte 5 – Applicazione
# =========================

#Creare un piccolo programma principale (main) che:
def main():
    #Inserisca almeno 3 medici e 5 pazienti.

    # Medici
    medici = [
        Medico("Giulia", "Ferrari", "Medicina Interna"),
        Medico("Paolo", "Neri", "Cardiologia"),
        Medico("Sara", "Russo", "Endocrinologia"),
    ]

    # Pazienti 
    #Ogni paziente deve avere almeno 3 risultati di analisi.
    p1 = Paziente("Mario", "Rossi", "RSSMRO753ED8889DDD21", 45, 78.5)
    p1.aggiungi_analisi(Analisi("glicemia", 92))
    p1.aggiungi_analisi(Analisi("colesterolo", 210))
    p1.aggiungi_analisi(Analisi("trigliceridi", 140))

    p2 = Paziente("Anna", "Bianchi", "BNCHNA873ED8889DDD43", 33, 60.2)
    p2.aggiungi_analisi(Analisi("glicemia", 88))
    p2.aggiungi_analisi(Analisi("vitamina D", 18))   # sotto al range default 20–50
    p2.aggiungi_analisi(Analisi("ferritina", 55))

    p3 = Paziente("Marco", "Verdi", "VRDMRC873ED8889DDD44", 52, 85.0)
    p3.aggiungi_analisi(Analisi("glicemia", 105))    # leggermente alto su range 70–99
    p3.aggiungi_analisi(Analisi("colesterolo", 180))
    p3.aggiungi_analisi(Analisi("trigliceridi", 160))  # sopra 150

    p4 = Paziente("Lucia", "Conti", "CNTLCU873ED8889DDD55", 29, 54.8)
    p4.aggiungi_analisi(Analisi("glicemia", 76))
    p4.aggiungi_analisi(Analisi("vitamina D", 32))
    p4.aggiungi_analisi(Analisi("emocromo", 4.8))

    p5 = Paziente("Davide", "Moretti", "MRTDVD873ED8889DDD66", 61, 90.3)
    p5.aggiungi_analisi(Analisi("glicemia", 130))
    p5.aggiungi_analisi(Analisi("colesterolo", 240))
    p5.aggiungi_analisi(Analisi("ferritina", 15))  # basso rispetto al default 20–250

    pazienti = [p1, p2, p3, p4, p5]

    # Stampi la scheda di ogni paziente
    print("\n=== SCHEDA PAZIENTI E VALUTAZIONI ===")
    for paz in pazienti:
        print("\n" + paz.scheda_personale())
        for a in paz.analisi_effettuate:
            print(" -", a.valuta())

    # Associazioni semplici medico->pazienti (dimostrazione)
    print("\n=== VISITE ===")
    medici[0].visita_paziente(p1)
    medici[1].visita_paziente(p3)
    medici[2].visita_paziente(p2)
    medici[0].visita_paziente(p4)
    medici[1].visita_paziente(p5)

    # Statistiche per ogni paziente
    print("\n=== STATISTICHE ANALISI PER PAZIENTE (NumPy) ===")
    for paz in pazienti:
        stats = paz.statistiche_analisi()
        if stats is None:
            print(f"{paz.nome} {paz.cognome}: nessuna analisi")
        else:
            print(
                f"{paz.nome} {paz.cognome} -> "
                f"media={stats['media']:.2f}, "
                f"min={stats['minimo']:.2f}, "
                f"max={stats['massimo']:.2f}, "
                f"dev_std={stats['dev_std']:.2f}"
            )

    # Parte 3 – statistica su 10 pazienti per un esame (esempio: glicemia)
    print("\n=== STATISTICHE CAMPIONE GLICEMIA (10 pazienti) ===")
    glicemie_10 = np.array([92, 88, 105, 76, 130, 99, 101, 85, 97, 110], dtype=float)
    ris = statistiche_campione_glicemia(glicemie_10)
    print(
        f"media={ris['media']:.2f}, min={ris['minimo']:.2f}, "
        f"max={ris['massimo']:.2f}, dev_std={ris['dev_std']:.2f}"
    )

if __name__ == "__main__":
    main()

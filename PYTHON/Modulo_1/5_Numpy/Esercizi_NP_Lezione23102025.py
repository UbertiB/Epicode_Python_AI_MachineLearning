import numpy as np


class Pianeta:
    def __init__(self, nome, massa, posizione, velocita):
        self.nome=nome
        self.massa=massa  #massa 
        self.posizione=np.array(posizione,dtype=float)  #posizione come array numpy
        self.velocita=np.array(velocita,dtype=float)  #velocita come array numpy
    
    def muovi(self,dt):
        self.posizione+=self.velocita*dt
    
    def distanza_da(self,altro_pianeta):
        return np.linalg.norm (self.posizione-altro_pianeta.posizione)
    
    def __str__(self):
        return f"Pianeta {self.nome}: posizione={self.posizione}, velocità={self.velocita}"
    
class SistemaSolare:
    def __init__(self):
        self.pianeti=[]

    def aggiungi_pianeta(self, nome, massa, posizione, velocita):
        self.pianeti.append(Pianeta(nome, massa, posizione, velocita))

    def simula(self,dt,passi):
        for _ in range (passi):
            for pianeta in self.pianeti:
                pianeta.muovi(dt)  
    def stampa_distanze(self):
        print("\n ---- Distanze tra pianeti ---") 
        for i in range(len(self.pianeti)):
            for j in range(i+1,len(self.pianeti)):
                p1=self.pianeti[i]
                p2=self.pianeti[j]
                distanza=p1.distanza_da(p2)
                print(f"Distanza tra {p1.nome} e {p2.nome}: {distanza:.2f} unità")
    def stampa_posizioni(self):
        print("\n --- Posizioni dei pianeti ---")
        for pianeta in self.pianeti:
            print(f"{pianeta.nome}: posizione={pianeta.posizione}") 

    

# Esempio di utilizzo
sistema=SistemaSolare()
#pianeta1=Pianeta("Terra",100.444,[0,0],[0.01,0.02])
sistema.aggiungi_pianeta("Terra",100.444,[0,0],[0.01,0.02])
sistema.aggiungi_pianeta("Marte",200.444,[1,1],[-0.01,0.005])
sistema.aggiungi_pianeta("Giove",300.42334,[-1,-1],[0.02,-0.01])

sistema.simula(dt=1, passi=100)
sistema.stampa_posizioni()
sistema.stampa_distanze()

mailto:schoolmanagement@epicode.com
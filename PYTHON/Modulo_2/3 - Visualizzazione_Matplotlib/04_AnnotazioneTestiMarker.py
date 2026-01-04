"""
Tra annotazioni, testi e marker possiamo trasformare un semplice grafico in un potente mezzo di 
comunicazione che può reccontare una storia

* ANNOTAZIONI dinamiche
consentono di evidenziare eventi o valori specifici all'interno di un grafico.
Pssono essere delle freccie, dei testi, ecc che puntano ad un punto dati
Si aggiornano in funzione dai dati mostrati.
Esempio evidenziare il massimo di una serie, il valore recente, il minimo, superamenti di soglie, ecc.
Buona pratica mantenerli concisi con un testo minimo che non coprano i dati
Si possono usare degli sfondi trasparenti
Efficaci perchè guidano lo sguardo

* TESTI statici o dinamici: (plt.annotate). 
Possono chiarire significati, etichette aggiuntive, unità di misure o soglie
E' possibile inserire anche dei testi all'interno del grafico, per indicare intervalli come
zone di rischio o particolari punti.
Si possono aggiungere anche note operative.
I testi dinamici sono legati ai valori di un dataset, si aggiornano in base ai dati.

MARKER automatici 
Sono simbnoli che identificano i punti dati all'interno del grafico. 
Rappresentati con diversi simboli, cerchi, quadrati, triangoli.
Possono essere generati automaticamente come picchi, minima o superamenti di soglia.
Ad esempio, un cerchio per il punto massimo, un quadrato per il minimo, una stella per un valore soglia.
I marker possono essere posizionati in modo automatico in base ai dati, o manualmente specificando le coordinate.

Il MARKER individua un dato l'ANNOTAZIONI lo spiega. 
Utilizzare le annotazioni solo per i dati chiave, 
e non per ogni punto del grafico, altrimenti si crea confuzione visiva.
Generare market automatici solo per eventi significativi (massimi, minimi, soglie superate).
Documentare i criteri con cui si è scelto di evidenziare determinati punti

Le migliori pratiche
utilizzare le annotazioni solo per dati chiave (e non per ogni punto)
Mantenere testi brevi e consici
evitare sovrapposizioni
Generare marker automatici solo per eventi significativi (massimi, minimi o superamenti di soglie)
Testare la leggibilità su diversi supporti, monitore, stampe, pdf

Le annotazioni (.annotate) sono agganciate ad un punto e può disegnare anche la freccia per indicare il punto
I testi sono semplici testi in un punto (non ha il concetto di 'punto a quel punto')

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Esempio di ANNOTAZIONI DINAMICHE
if False:
    #Visualizza il massimo di un dataset

    x=np.linspace(0,10,100)
    y=np.sin(x)*np.exp(-0.1*x)
    
    fig,ax=plt.subplots()
    ax.plot(x,y,label="Serie attenuata")

    max_idx=np.argmax(y) #restituisce la posizione (x,y) del massimo di y
    ax.plot(x[max_idx],y[max_idx], marker="o",color="red",label="Massimo") #disegno il punto massimo (plot)
    #Annotazione dinamica (arrowprops=freccia)
    ax.annotate(
        f'Massimo: {y[max_idx]:.2f}',
        xy=(x[max_idx], y[max_idx]),
        xytext=(x[max_idx]+1, y[max_idx]+0.2),
        arrowprops=dict(facecolor='black', shrink=0.05),
        fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))
    
    ax.set_title("Annotazoine dinamica sul massimo")
    ax.legend()
    plt.show()

# Esempio di MARKET AUTOMATICI
if True:
    x=np.linspace(0,20,200)
    y=np.cos(x)+0.1*x

    fig,ax=plt.subplots()
    ax.plot(x,y, color="blue")
    #testo statisto
    ax.text(5,1.5,"Zona di stabilita",fontsize=12,color="green",bbox=dict(facecolor="white",alpha=0.6))
    #testo dinamico (cambia a seconda dei dati)
    ax.text(x[-1],y[-1],f"Valore finale: {y[-1]:.2f}",fontsize=10,ha="right",va="bottom",color="red")
    ax.text(x[1],y[1],f"Valore iniziale: {y[1]:.2f}",fontsize=10,ha="right",va="bottom",color="red")
    ax.set_title("Testi statici e dinamici")
    plt.show()  

"""
GESTIONE DELLE FIGURE COMPLESSE

Visualizzazione dei dati complessi, spesso non è sufficiente creare un singolo grafico lineare o a barre
, sono necessari informazioni multidimensionali, serie dimensionali multiple o variabili correlate tra di loro, 
diventa pertanto necessario rappresentare più prospettive nello stesso contesto visivo.
La gestione di figure complesse nasce da questa esigenza, 
poter visualizzare simultaneamente diversi aspetti di un dataset senza sacrificare la chiarezza.
Per questo matplotlib offre strumenti complessi per poter visualizzare figure ognuna come un grafico specifico.
Il concetto fondamentale è la distinìzione tra figure ed assi, 
la FIGURA è lo spazio complessivo su cui saranno posizionati tutti grafici, 
mente gli ASSI sono le singole area in cui i singoli grafici prenderanno forma.
Questa distinzione è importante perchè posso avere un controlla granulare sia sul controllo dell'intera figura sia
sui singoli grafici.
Ho diverse modabilità per crare subplots.
Il metodo più semplice è SUBPLOT CLASSICO metodo semplice ma rigido, tutti gli assi hanno la stessa dimensione.
Posso definire la posizione del grafico all'interno della griglia tramite un numero. Diventa limitante quando la complessità 
aumenta.
Per gestire casi più complessi si utilizza PLT.SUBPLOTS restituisce un oggetto figura ed un array di assi consentendo di iterare
facilmente sui singoli grafici e di applicare personalizzazioni specifiche a ciascuno di essi.
Posso modificare dimensioni, proporzioni e spazi dei subplot in maniera dinamica
Quando le esigenze diventano ancora più sofisticate entra in gioco GRIDSEC consente di dividere la figura in una griglia
flessibile (import matplotlib.gridspec as gridspec) e di assegnare più celle ad un singolo grafico, 
qui ho il massimo controllo su dimensioni e posizionamento
Posso creare figure da cui alcuni grafici principali occupano porzioni più grandi mentre altri graifci secondari si 
adattano interno a quelli principali. Utile quando voglio dare maggiore rilevanza ad un grafico chiave e supportare 
l'analisi con grafici aggiuntivi che mostrano dettagli secondari. 
Oltre alla gestione del layout è importante considerare la leggibilità dei grafici stessi prestando attenzione alla parte grafica
scelta dei colori e stili è fondamentale
Uso degli INSERT (add_axes), grafici inseriti all'interno di altri grafici principali, che permettono di mostrasre confronti senza
dover creare figure separate. Gli insert sono posizionati tramite coordinate frazionari della figura.

"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

#SUBPLOT BASE

x=np.linspace(0,10,100)
y1=np.sin(x)
y2=np.cos(x)
y3=np.sin(2*x)
y4=np.exp(-0.1*x*np.sin(x))

#SUBPLOT BASE 2X2   SUBPLOTS
if False:
    fig, axes=plt.subplots(2,2,figsize=(10,8))
 
    axes[0,0].plot(x,y1,color="red",label="sin(x)")
    axes[0,0].set_title("Grafico sin(x)")
    axes[0,0].legend()
 
    axes[0,1].plot(x,y2,color="blue",label="cos(x)")
    axes[0,1].set_title("Grafico cos(x)")
    axes[0,1].legend()
 
    axes[1,0].plot(x,y3,color="gray",label="sin(2*x)")
    axes[1,0].set_title("Grafico sin(2*x)")
    axes[1,0].legend()
 
    axes[1,1].plot(x,y4,color="magenta",label="exp(-0.1*x*np.sin(x))")
    axes[1,1].set_title("Grafico exp(-0.1*x*np.sin(x))")
    axes[1,1].legend()

    plt.show()

#SUBPLOT 1X2  GRIDSPEC
if False:
    fig=plt.figure(figsize=(10,8))
    gs=gridspec.GridSpec(3,3,figure=fig)

    #utilizza tutta la prima riga completa
    ax1=fig.add_subplot(gs[0,:])
    ax1.plot(x,y1,"r")
    ax1.set_title("Grafico 1 - Riga intera")

    #della seconda linea occupa 1/3
    ax2=fig.add_subplot(gs[1:,0])
    ax2.plot(x,y2,"b")
    ax2.set_title("Grafico 2 - Colonna estesa")
    #della seconda linea occupa 2/3
    ax3=fig.add_subplot(gs[1:,1:])
    ax3.plot(x,y3,"g")
    ax3.set_title("Grafico 3 - Resto della griglia")

    plt.show()

# Grafico inserito in un altro    INSERT
if True:
    fig,ax=plt.subplots(figsize=(8,6))
    ax.plot(x,y1,color="blue", linestyle="-", label="sin(x)")
    ax.set_title("Grafico principale con insert")
    ax.legend()

    ax_insert=fig.add_axes([0.6,0.5,0.25,0.35])
    ax_insert.plot(x,y2,color="red",label="cosX")
    ax_insert.set_title("grafico insert")
    ax_insert.legend()

    plt.show()









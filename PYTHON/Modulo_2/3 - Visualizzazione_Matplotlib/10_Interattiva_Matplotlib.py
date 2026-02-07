"""
L'interattività com matplotlib grazie ai widgets, slider, e GUI

La visualizzazoine dei dati non si limita a grafici statici, spesso è fondamentale permettere 
interazioni dinamiche per esplorare dei dataset complessi, oppure per modificare parametri
al volo o testare scenari diversi.
Matplotlib oltre ai grafici statici, può offrirci widget nativi, slider o pulsanti o checkbox che ci consentono 
di aggiornare i grafici in tempo reale.
Si possono utilizzare anche librerie come ipywidgets per creare dashboard interattive, inoltre
matplotlib può essere integrato con guidesktop con Tkinter o PyQt.
Vedremo come rendere i grafici interattivi facilitando esplorazione, confronto scenari e la
comunicazione dei risultati.

Matplotlib dispone di widgets incorporati che si possono aggiungere direttamente ai grafici, i principali 
widgets sono:
    - Slider: consentono di modificare valori di parametri in tempo reale
    - Button: eseguono azioni al click, come aggiornare, resettare o cambiare visualizzazione
    - ChekButtons: che abilitano/disabilitano linee o layer del grafico
l'approccio è utile quando desideriamo interagire con un dataset senza riscrivere il codice

SLIDER
Gi slider ci consentono di modificare parametri numerici direttamente sul grafico, possono
controllare valore come ampiezza, frequenza o la finestra mobile di una funzione o di un dataset.
L'aggiornamento è istantaneo, la curva si ridisegna ogni volta che lo slider cambia posizione
Gli slider possono essere combinati tra di loro per controllare più parametri simultaneamente, 
permettendo esplorazioni multidimensionali. Utile nelle analisi scientifiche ed ingegneristiche, per esempio
per modificare i parametri di un modello matematico ed osservare output.

BUTTON
I pulsanti permettono di eseguire operazioni discrete, come resettare un grafico o cambiare il 
dataset che stiamo andando a visualizzare

CHECKBOX
I checkbo gestiscono la visibilità di curve multiple o layer di informazioni. possono anche essere combinati 
con slider per creare interfaccie più complesse
Contentono di attivare/disattivare gli elementi che stiamo visualizzando senza dover riscrivere tutto il grafico.

Rendono l'esperienza interativa, intuitiva ed immediata.

Matplotlib può essere integrati in interfaccie grafiche con Tkinter
Questa interazione permette di costruire strumenti completi di analisi dei dati

Se utilizzo JUPYTER è possibile utilizzare ipywidgets
che offre degli slider avanzati con valori discreti o continui dei batton o drop down, e selettori multipli
funzioni di linking tra widget e grafici che aggiornano dinamicamente le figure ed in generale l'integrazione
e particolarmente potente quando vogliamo creare delle dashboard interattive

Matplotlib può essere integrato in GUI desktop per applicazioni professionali, con Tkinter (semplice e leggero)
e con PyQt e PySide, più potente e layout complessi.
Questa integrazione permette di costruiere strumenti completi di analisi dei dati,
dove i grafici sono interattivi e non statici e l'input dell'utente utenti e calcoli numerici convivono in 
un'unica applicazione.

Matplotlib suporta interativà leggera con i suoi widget
Con Ipywidgets diventa potente quando si lavora con notebook, grafici iterativi molto più potenti
In GUI (Tkinter/PyQt) si possono costruire applicazoni complete
L'utilizzo di questi strumenti dipende dal contesto

"""
#Esempio 1  SLIDER
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

x = np.linspace(0, 10, 500)
y = np.sin(x)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25) #lascia spazio in basso (bottom)
line, = ax.plot(x, y) #creo una linea

ax_amp = plt.axes([0.25, 0.1, 0.65, 0.03]) #definisco un contenitore in cui inseriro' gli slider
slider_amp = Slider(ax_amp, 'Ampiezza', 0.1, 5.0, valinit=1) #lo slider lo metto dentro ax_amp

def update(val):  #funziona chiamata ogni volta che cambia lo slider
    amp = slider_amp.val  #leggo il valore corrente dello slider
    line.set_ydata(amp * np.sin(x)) #ricalcolo la linea
    fig.canvas.draw_idle() #riaggiorno il grafico senza bloccare l'esecuzione del prg

slider_amp.on_changed(update)
#plt.show()

#Esempio 2  PULSANTE (per resettare lo slider)
from matplotlib.widgets import Button

def reset(event):
    slider_amp.reset() #riporta lo stato dello slider a quando è stato generato

slider_amp.on_changed(update) #creo il bottone
ax_button = plt.axes([0.8, 0.025, 0.1, 0.04])   #creo lo spazio del bottono
button = Button(ax_button, 'Reset')  #creo bottone
button.on_clicked(reset)



#Esempio 3  CHEKBOX (per visualizzare curve multiple)
from matplotlib.widgets import CheckButtons

y2 = np.cos(x)  #seconda variabile che check dalla prima linea alla seconda
lines = [line, ax.plot(x, y2, label="cos")[0]]  #nuova linea

ax_check = plt.axes([0.025, 0.5, 0.1, 0.15])  #spazion dove inserire' checkbox
check = CheckButtons(ax_check, ['sin', 'cos'], [True, True])  #creo checkbox

def func(label):
    index = 0 if label == 'sin' else 1  #deciale curva modificare  0=curva del seno 1=curva del coseno
    lines[index].set_visible(not lines[index].get_visible())
    fig.canvas.draw_idle()

check.on_clicked(func)

plt.show()

if True:
    #Esempio 4   INTEGRAZIONE IN TKINTER
    import ipywidgets as widgets
    from IPython.display import display

    amp_slider = widgets.FloatSlider(value=1, min=0.1, max=5.0, step=0.1, description='Ampiezza')
    display(amp_slider)

    def update_plot(change):
        line.set_ydata(amp_slider.value * np.sin(x))
        fig.canvas.draw_idle()

    amp_slider.observe(update_plot, names='value')

    #Esempio 5
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    root = tk.Tk()
    root.title("Grafico interattivo Tkinter")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

    root.mainloop()  #finestra che rimane aperta ed ascolta gli eventi
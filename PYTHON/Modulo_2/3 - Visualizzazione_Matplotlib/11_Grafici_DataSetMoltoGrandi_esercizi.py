"""
ESERCIZIO 1
Dataset enorme: crea un dataset sintetico da 5 milioni di punti. Visualizzalo usando
sampling casuale e poi sampling stratificato per una colonna categoriale.
Confronta la leggibilità

ESERCIZIO 2
Streaming di dati sintetici: costruisci un grafico che mostra in tempo reale 
l'andamento di due funzioni matematiche (es sin e cos), mantenendo un buffer di 200 punti

ESERCIZIO 3
Dashboard streaming: integra uno slider che permette di modificare la finestra del buffer in tempo reale e osserve
come cambia il grafico

ESERCIZIO 4
Visualizzazione aggregata: prendi un dataset enorme e crea un grafico ocn medie mobili o aggregazioni per finestre al posto 
di punti singoli. Confronta performance e leggibilità con il grafico non aggregato.

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

#
#ESERCIZIO 1
#

if False:

    #
    #sampling casuale
    #
    x=np.random.choice(["cat1","cat2","cat3","cat4"],size=5_000_000)
    y=np.linspace(1,100,5_000_000)
    df=pd.DataFrame({"categoria":x,"valore":y})
    print(df.head())
    #prendo lo 0.1% di valori e con random_state mi assicuro che i valori presi sono sempre gli stessi
    df_sample=df.sample(frac=0.00001, random_state=42).sort_values("categoria")
    print(df["categoria"].value_counts(normalize=True))
    print(df_sample["categoria"].value_counts(normalize=True))     

    #
    #sampling stratificato
    #
    #prendo  una % di tutto il dataset 
    df_balance=(df.groupby("categoria",group_keys=False).apply(lambda x:x.sample(frac=0.00001,random_state=42))) 

    #(le proporzioni tra le categorie non sono cambiate)
    print(df["categoria"].value_counts(normalize=True))
    print(df_balance["categoria"].value_counts(normalize=True))

    #visualizzazione
    fig,axes=plt.subplots(1,2,figsize=(12,5),sharey=True)
    axes[0].scatter(df_sample['categoria'], df_sample['valore'], c=df_sample['categoria'].map({'cat1':'blue','cat2':'orange','cat3':'green','cat4':'red'}), s=2)
    axes[0].set_title("Sampling casuale")

    axes[1].scatter(df_balance['categoria'], df_balance['valore'], c=df_balance['categoria'].map({'cat1':'blue','cat2':'orange','cat3':'green','cat4':'red'}), s=2)
    axes[1].set_title("Sampling stratificato")   

    for ax in axes:
        ax.set_xlabel("categoria") 
        ax.set_ylabel("valore") 

    plt.suptitle("Confronto tra sampling casuale e stratificato (5M punti totali)")
    plt.tight_layout()
    plt.show()

if False:

    # Esercizio 2

    # Costruisci un grafico che mostra in tempo reale l’andamento di due funzioni matematiche (es. sin e cos), mantenendo un buffer di 200 punti.

    plt.ion()  #aggiorna i grafici subito senza dover chiamare il metodo show()
    fig, ax = plt.subplots(figsize=(8,4))
    xdata, y1data, y2data = [], [], []
    line1, = ax.plot([], [], label='sin')
    line2, = ax.plot([], [], label='cos')
    ax.set_xlim(0, 200)
    ax.set_ylim(-1.5, 1.5)
    ax.legend()
    ax.set_title("Streaming dati sintetici — buffer 200 punti")

    buffer_size = 200
    t = 0

    while True:
        # aggiungi nuovo punto
        xdata.append(t)
        y1data.append(np.sin(t/10))
        y2data.append(np.cos(t/10))

        # mantieni solo ultimi 200
        if len(xdata) > buffer_size:
            xdata = xdata[-buffer_size:]
            y1data = y1data[-buffer_size:]
            y2data = y2data[-buffer_size:]

        # aggiorna grafico
        line1.set_data(xdata, y1data)
        line2.set_data(xdata, y2data)
        ax.set_xlim(min(xdata), max(xdata) if max(xdata)>buffer_size else buffer_size)

        plt.pause(0.01)
        t += 1


if True:
    # Esercizio 3

    # Integra uno slider che permette di modificare la finestra del buffer in tempo reale e osserva come cambia il grafico.

    import numpy as np
    import matplotlib.pyplot as plt
    import ipywidgets as widgets
    from IPython.display import display, clear_output
    import time

    # Slider per dimensione del buffer
    buffer_slider = widgets.IntSlider(value=200, min=50, max=1000, step=50, description='Buffer')
    display(buffer_slider)

    # Output del grafico
    out = widgets.Output()
    display(out)

    xdata, y1data, y2data = [], [], []
    t = 0

    plt.ion()
    fig, ax = plt.subplots(figsize=(8,4))
    line1, = ax.plot([], [], label='sin')
    line2, = ax.plot([], [], label='cos')
    ax.legend()
    ax.set_ylim(-1.5, 1.5)
    ax.set_title("Dashboard streaming — modifica buffer in tempo reale")

    while True:
        with out:
            clear_output(wait=True)
            # aggiorna buffer
            buffer_size = buffer_slider.value
            xdata.append(t)
            y1data.append(np.sin(t/10))
            y2data.append(np.cos(t/10))

            if len(xdata) > buffer_size:
                xdata = xdata[-buffer_size:]
                y1data = y1data[-buffer_size:]
                y2data = y2data[-buffer_size:]

            # aggiorna grafico
            line1.set_data(xdata, y1data)
            line2.set_data(xdata, y2data)
            ax.set_xlim(min(xdata), max(xdata) if len(xdata)>buffer_size else buffer_size)
            plt.show()
        time.sleep(0.05)
        t += 1   


if False:
    # Esercizio 4

    # Prendi un dataset enorme e crea un grafico con medie mobili o aggregazioni per finestre al posto di punti singoli. Confronta performance e leggibilità con il grafico non aggregato.

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    # Dataset sintetico grande (3 milioni di punti)
    n = 3_000_000
    x = np.linspace(0, 1000, n)
    y = np.sin(x/20) + np.random.normal(0, 0.3, size=n)
    df = pd.DataFrame({'x': x, 'y': y})

    # Grafico originale (usando sample per non bloccare)
    sample = df.sample(20000, random_state=1)

    # Calcolo media mobile su finestre di 5000 punti
    window = 5000
    df['y_mean'] = df['y'].rolling(window).mean()
    df_down = df.iloc[::window, :]  # riduci punti per grafico aggregato

    # Confronto grafico
    fig, axes = plt.subplots(1, 2, figsize=(12,5))
    axes[0].scatter(sample['x'], sample['y'], s=1, alpha=0.5, label='Punti singoli (sample)')
    axes[0].set_title("Grafico non aggregato (sample 20k)")
    axes[1].plot(df_down['x'], df_down['y_mean'], color='red', label='Media mobile (window=5000)')
    axes[1].set_title("Grafico con medie mobili (aggregato)")

    for ax in axes:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()

    plt.suptitle("Confronto: punti singoli vs media mobile su dataset enorme")
    plt.tight_layout()
    plt.show()    




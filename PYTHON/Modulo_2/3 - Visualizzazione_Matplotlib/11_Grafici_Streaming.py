
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation

#il CHUNK è una tecnica di streaming prima di fare il grafico

MAX_POINTS = 100            # punti massimi mostrati (rolling window)
# Buffer in memoria (ultimi MAX_POINTS)
x_buf = deque(maxlen=MAX_POINTS)
y_buf = deque(maxlen=MAX_POINTS)

file_ordini_csv="11_datasetenormi.csv"

#Genero il file enorme
if False:
    n_righe=1_000
    ordini=pd.DataFrame({
        "OrdineID":np.arange(1,n_righe+1),
        "ClienteID": np.random.randint(1,21,n_righe),
        "ProdottoID":np.random.randint(1,11,n_righe),
        "Quantita":np.random.randint(1,5,n_righe)
    })
    ordini.to_csv(file_ordini_csv,index=False)

#Leggo il file di dati (enorme)

n_chunk=100
i=0
out_file=[]

def chunk_reader():
    for chunk in pd.read_csv(file_ordini_csv,chunksize=n_chunk,usecols=["OrdineID","ProdottoID","Quantita"]):
        #downcasting per ridurre dimensioni
        chunk["OrdineID"]=chunk["OrdineID"].astype("int32")
        chunk["ProdottoID"]=chunk["ProdottoID"].astype("int16")
        chunk["Quantita"]=chunk["Quantita"].astype("int8")
        yield chunk # consegno chunk al chiamante, sospendo la funzione, alla richiesta successiva (chunk) parta dalla riga dopo yield

reader=chunk_reader()

fig,ax=plt.subplots(figsize=(10,5))
line,=ax.plot([],[],label="valore")
ax.set_title("Streaming plot (rooling window)")
ax.set_xlabel("ProdottoID")
ax.set_ylabel("Quantita")
ax.legend()

def init():
    line.set_data([],[])
    return line,

def update(frame):
    try:
        chunk=next(reader)
    except StopIteration:
        #fine file: fermo l'animazione
        anim.event_source.stop()
        return line,
    #aggiungo i nuovi punti al buffer
    for prodotto, quantita in zip(chunk["ProdottoID"],chunk["Quantita"]):
        x_buf.append(prodotto)
        y_buf.append(quantita)
    # aggiorno la linea
    line.set_data(list(x_buf), list(y_buf))     
    # aggiorno limiti asse (semplici)
    ax.relim()
    ax.autoscale_view() 

    return line,   

# interval in ms: ogni quanto prova a leggere un chunk e aggiornare
anim = FuncAnimation(fig, update, init_func=init, interval=300, blit=False)

plt.show()       

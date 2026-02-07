"""
SAMPLING
Significa prendo una parte dei dati invece di tutti, in modo controllato, per poter analizzare e soprattutto 
visualizzare senza mandare in crisi RAM, tempi e visualizzazioni.
Se campioni male, il grafico racconta una storia falsa.

Perchè serve:
Un monito ha un numero finito di pixel. Quindi, oltre un certo numero, visualizzare i punti sul grafico non 
aggiunge informazione visiva ma solo tempo e rumore.Sampling e aggregazione servono proprio a comprimere 
l'informazione in modo fedele.

Con il sampling devo scegliere quali righe osservare, con una regola.
Le regoli più comuni sono:
- Casuale: prendo righe a caso.
- Sistematico: prendo 1 riga ogni K
- Stratificato: prendo campioni per gruppo (clienti, articoli, classi) per non perdere i rari.
- Intelligente: per serie temporali: riduco i punti ma preservo i picchi e forma del segnale
- Streaming: mantengo un campione aggiornato mentre arrivano nuovi dati.
"""
#
# ESEMPIO 1: SAMPLING CASUALE IN PANDAS
#

#ogni riga ha la stessa probabilità di essere scelta
df_s = df.sample(n=200_000, random_state=42)   # oppure frac=0.01

#se invece vuoi dare maggiore probabilità ad alcune righe, utilizzi weights
#quindi alcune righe hanno più probabilità di finire nel campione rispetto ad altre, in base ai pesi che gli dai
df_s = df.sample(n=200_000, weights="peso", random_state=42)
#pesco le righe che hanno la colonna 'peso' più alto
#attenzione perchè potresti ottenere una visione distorta della realtà, perchè hai volutamente sovra-rappresentato
#una parte dei dati

#
#ESEMPIO 2 SAMPLING SISTEMATICO (1 RIGA OGNI K)
#

k = 100
df_s = df.iloc[::k]
#attenzione che se il dato è ciclico potresti agganciare sempre la stessa 'fase' e falsare.
#suponiamo di avere 100 fasi, prendere una riga ogni 100 potrebbe prendere sempre la stessa fase.

#potresti prendere una riga ogni k ma partendo non dall'inizio ma da una posizione iniziale 
#calcolata causalmente
import numpy as np
k = 100
start = np.random.randint(0, k)
df_s = df.iloc[start::k]

#
#ESEMPIO 3 SAMPLING STRATIFICATO
#
#L'obbiettivo è non perdere categorie importanti. In ERP è fondamentale perchè la distirbuzione è quasi 
#sempre sbilanciata: pochi articoli fanno tanto fatturato, molti articoli fanno poco, pochi clienti grandi,
#tanti clienti piccoli.

#esempio prendo il 2% per ogni categoria (cliente), con un minimo di righe per ogni categoria
g = "cliente"
df_s = (
    df.groupby(g, group_keys=False)
      .apply(lambda x: x.sample(
          n=min(len(x), max(100, int(len(x)*0.02))),
          random_state=42
      ))
)
#raggruppo il df per g (per cliente), con group by
#per ogni gruppo (cliente) pandas calcola il 'mini' dataframe e fai un sample sul quel gruppo prendendo 
#il 2% di dati

#
#ESERCIZIO 4 SERIE TEMPORALI: DOWNSAMPLING CHE PRESERVA I PICCHI (NON 'A CASO')
#

#Se stai osservendo, per ogni giorni, i consumi (le giacenze, ecc) i picchi spesso sono la cosa che 
#interessa (rotture stock, ordini anomali), quindi il sampling casuali è una pessima idea.
#Questa tecnica, prende per ogni intervallo, minimo e massimo. Così i picchi non spariscono
import numpy as np

def minmax_downsample(x, y, bins=3000):
    x = np.asarray(x); y = np.asarray(y)
    n = len(x)
    if n <= bins * 2:
        return x, y

    edges = np.linspace(0, n, bins+1).astype(int)
    xs, ys = [], []

    for i in range(bins):
        a, b = edges[i], edges[i+1]
        if b <= a:
            continue
        yy = y[a:b]
        ii_min = a + np.argmin(yy)
        ii_max = a + np.argmax(yy)
        for ii in sorted([ii_min, ii_max]):
            xs.append(x[ii]); ys.append(y[ii])

    return np.array(xs), np.array(ys)





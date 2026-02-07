"""
COLORMAP

Una colormap è una funzione che mappa valori numerici a colori specifici.
Se la mappatura è sbagliata, il grafico diventa una distorsione delle realtà.
Ogni dato numerico viene trattato in una tonalità che rappresenta la sua intensità o la posizione nella scala.
Una scelta accurata dei colori permette di enfatizzare pattern, anomalie, e le tendenze presenti 
nel dataset.

In matplotlib le colormap possono essere applicate a diversi elementi, offrendo flessibilità per visualizzare
dati complessi in modo coerente.

Ogno colormap può essere applicata:
- heatmap
- scatterplot
- sarfaceplot
- grafici 3D

Hai sempre 3 'pezzi' va valutare:
1) Dati (valori reali)
2) Normalizzazione: trasforma i dati in un intervallo 0..1 (o in indici discreti)
3) Colormap: mappa 0..1 in colori.
Matplotlib da sia colormap pronte sia strumenti per crearle e per normalizzare in modo avanzato.

Matplotlib raggruppa le colormap in categorie 'funzionali'
1) SEQUENTIAL (sequenziali, monotone): per dati ordinati dal minimo al massimo (alto basso), con sfumatore 
che vanno dal chiaro al scuro, ideale per rappresentare quantità crescenti come densità o insentità 
(viridis, plasma). 
I valori vanno dal basso all'alto (o viceversa) senza un centro logico.
Da evitare se i dati sono categorici o se si vogliono confronti precisi valore per valore
2) DIVERGING (divergenti): Due colori opposti con un centro neutro, per valori positivi/negativi con punto 
centrale. Registra scostamenti rispetto a un target o uno zero (centro)
Qui ha senso una colormap con centro evidenziato e due lati simmetrici o quasi
Da utilizzare quando esiste un punto, che può essere uno zero, una media, un target ed interessa la deviazione 
(quello che c'è sopra e quello sotto). Esempio scostamento da budget, differenza previsto/consuntivo, 
margine positivo/negativo, ecc
Da non utilizzare se non si ha un centro al di sotto o al di sopra del quale si vogliono evidenziare i dati
Evidenziando deviazioni positivi o negativi rispetto al centro scelto (coolwarm,seismic)
3) CATEGORICAL (categoriali/qualitative): per categorie, non per numeri. 
Palette per dati discreti senza ordine numerico, ogni categoria ha un colore unico (tab10, Set3) utile per
distringuere i gruppi o i cluster,
Non utilizzare per dati numerici continui, la luminisità della palette non cresce in modo ordinato
4) CYCLIC (colormap cicliche): Per dasti periodici. Sono colormap in cui l'inizio e la fine coincidono, 
il colore all'estremo minimo è identico a quello all'estremo massimo.
Da utilizzare quando il dato è periodico, ciclico, si ripete in modo circolare, non è un vero minimo o massimo 
assoluto. 
E' un cerchio non una retta
per dati periodici (ore del giorno, stagioni, angoli), le palette si ripetono ciclicamente 
sottolineando la continuità del ciclo.

Regola generale: se vuoi ch e'più=più' usa una colormap con luminosita crescente (perceptually uniform)
Se vuoi 'sopra/sotto un target' usa diverging con centro fissato. 
Se hai classi usa categorical

Matplotlib, permette di creare una colormap personalizzata per adattarla alle esigenze specifiche del dataset
che stiamo andando a lavorare.
Si possono definire sequenze di colori o interpolazioni tra tonalità diverse, 
possono essere continue (per gradienti di valori) o discrete (per valori specifici o intervalli).

La NORMALIZZAZIONE trasforma i dati grezzi in valori compatibili con le colormap.
La normalizzazione standard porta i dati in un range da 0 a 1, ma spesso serve un approcio più a avanzato 
(tipo logaritmica, percentili (per ridurre effetto degli outlet estremi), normalizzazione centrata su un valore 
di riferimento, può tornare utile con una colormap divergin.
Questo permette di utilizzare la stessa colormap anche su dati diversi, mantenendo sempre la coerenza visiva e
la stessa leggibilità

PALETTE CONTINUE:
si sfumano gradualmente tra i colori adattandosi ai dati numerici continui
PALETTE DISCRETE:
assegnano colori distinti a valori o intervalli specifici, ideali per categorie o intervalli limitati.

INVERSIONE
inversione di una colormap permette di invertire la scala dei colori, per enfatizzare i valori bassi al posti 
di quelli alti 
SHIFTING
Lo shifting sposta il range di colori rispetto ai dati, adattando la mappa ad un subset di valori

Queste tecniche consentono una maggior flessibilità e migliorano le comunicazioni visive senza andare a 
modificare i dati.

Una colorbar avanzata può uncludere, etichette personalizzate, ticks intermedi per evidenziare le soglie 
importanti, gradienti multipli o sezioni evidenziate, per sottolineare range critici. 

L'uso efficacie della colorbar è fondamentale per permettere all'osservatore di interpretare correttamente 
i colori

plt.imshow(matrice, cmap="viridis")  # sequenziale
plt.imshow(matrice, cmap="RdBu")     # diverging
plt.imshow(matrice, cmap="twilight") # ciclica

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import colors
from matplotlib.colors import ListedColormap

#
#ESEMPIO COLORMAP SEQUENZIALE
#

#come esempio si pososno prendere i giorni di copertura magazzino, è perfetto per una colormap sequenziale 
# perchè:
#1) è un numero 2) è ordinabile 3) valori più alti hanno significato più chiaro 4) non è ciclico 
# 5) non ha un centro neutro
#considera KPI: giorni di copertura=giacenza/consumo medio giornaliero
#valutiamo 10 gg=ok 40gg=attenzione 120gg=immobilizzo
#qui una colormap sequenziale è perfetta


#
#COLORMAP PERSONALIZZATA
#
data=np.random.rand(6,6)
colori=["blue","white","red"]

custom_cmap=LinearSegmentedColormap.from_list("blue_white_red",colori) #blue_white_red è il nome scelto per la colormap personalizzata

plt.matshow(data,cmap=custom_cmap) #crea una heatmap  cmap=custom_cmap associa la colorbar
plt.colorbar() #mostra la colorbar
plt.title("Heatmap con colormap personalizzata")
plt.show()

#
#COLORMAP CON NORMALIZZAZIONE LOGARITMICA
#
data=np.random.rand(6,6)*1000
plt.matshow(data,cmap="viridis",norm=colors.LogNorm())
#plt.matshow(data,cmap="viridis")
plt.colorbar()
plt.title("Heatmap con normalizzazione logaritmica")
plt.show()

#
#PALETTE DISCRETA
#
data=np.random.randint(0,5,(6,6))
discrete_map=ListedColormap(["red","green","blue","yellow","purple"]) #array di colori personalizzati
plt.matshow(data,cmap=discrete_map)
plt.colorbar(ticks=range(5))
plt.title("Heatmap con colormap discreta")
plt.show()

#
#INVERSIONE DI UNA COLORBAR AVANZATA
#
data=np.random.rand(6,6)
plt.matshow(data,cmap="coolwarm_r")  #con r inverto la colorbar
cbar=plt.colorbar()
cbar.set_label("Intensità")
cbar.set_ticks([0,0.5,1])
plt.title("Heatmap con colormap invertita e colorbar avanzata")
plt.show()



#Esempio 1
articoli = ["A100", "A120", "B055", "C010", "D777"]
copertura_giorni = [12, 35, 78, 5, 120]  # giorni di copertura magazzino

df = pd.DataFrame(
    {"Copertura_giorni": copertura_giorni},
    index=articoli
)

plt.figure(figsize=(4, 3))
img = plt.imshow(df, cmap="viridis", aspect="auto")
plt.colorbar(img, label="Giorni di copertura")

plt.yticks(range(len(articoli)),articoli)
plt.xticks([0], ["Magazzino"])

plt.title("Copertura magazzino per articolo")
plt.tight_layout()
plt.show()

#Esempio 2

articoli = ["A100", "A120", "B055", "C010", "D777"]
mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu"]

# Giorni di copertura (esempio coerente con dinamiche reali)
dati = [
    [15, 18, 20, 22, 25, 28],    # A100 cresce
    [40, 42, 45, 47, 50, 55],    # A120 sovrastock cronico
    [90, 85, 80, 78, 75, 70],    # B055 in smaltimento
    [5, 6, 7, 6, 5, 4],          # C010 sano
    [120, 130, 125, 140, 150, 160]  # D777 critico
]

df = pd.DataFrame(dati, index=articoli, columns=mesi)

fig, ax = plt.subplots(figsize=(8, 4))

# Trova valore minimo/massimo per la scala
#vmin, vmax = 0, 180
vmin=min(min(riga) for riga in dati)
vmax=max(max(riga) for riga in dati)

img = ax.imshow(df, cmap="viridis", vmin=vmin, vmax=vmax)

# Assi
ax.set_xticks(range(len(mesi)))
ax.set_xticklabels(mesi)
ax.set_yticks(range(len(articoli)))
ax.set_yticklabels(articoli)

ax.set_title("Giorni di copertura magazzino per articolo")

# Colorbar
cbar = fig.colorbar(img, ax=ax)
cbar.set_label("Giorni di copertura")

# Valori nelle celle (per pochi articoli)
for i in range(len(articoli)):
    for j in range(len(mesi)):
        ax.text(j, i, df.iloc[i, j], ha="center", va="center", fontsize=9)

plt.tight_layout()
plt.show()


#
#ESEMPIO COLORMAP DIVERGING
#

#da utilizzare solo quando si ha un punto di riferimento centrale e si vuole visualizzare
#quello che sta sotto o al di sopra di questo punto centrale
#quindi questa colormap utilizza due colori apposti che si allontanano da un valore centrale 

#esempio confronto venduto reale con forecast

articoli = ["A100", "A120", "B055", "C010", "D777"]

# Scostamento in pezzi rispetto al forecast
scostamento = [-20, -5, 0, +12, +35]

df = pd.DataFrame(
    {"Scostamento": scostamento},
    index=articoli
)

plt.figure(figsize=(4, 3))
img = plt.imshow(df, cmap="RdBu", vmin=-40, vmax=40, aspect="auto")
plt.colorbar(img, label="Scostamento vendite (pezzi)")

plt.yticks(range(len(articoli)), articoli)
plt.xticks([0], ["Mese corrente"])

plt.title("Scostamento vendite vs forecast")
plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(8, 4))

# Scala simmetrica rispetto allo zero
max_abs = abs(df.values).max()

img = ax.imshow(
    df,
    cmap="RdBu",
    vmin=-max_abs,
    vmax=+max_abs
)

# Assi
ax.set_xticks(range(len(mesi)))
ax.set_xticklabels(mesi)
ax.set_yticks(range(len(articoli)))
ax.set_yticklabels(articoli)

ax.set_title("Scostamento vendite vs forecast (pezzi)")

# Colorbar
cbar = fig.colorbar(img, ax=ax)
cbar.set_label("Scostamento (pezzi)")

# Valori nelle celle
for i in range(df.shape[0]):
    val=df.iloc[i,0]
    ax.text(j, i, val, ha="center", va="center", fontsize=9)

plt.tight_layout()
plt.show()

#
# COLORMAP CATEGORIALE
#

#assegna un colore distinto a ogni categoria, senza ordine nè intensità, non esiste un colore
#più 'forte' di un altro
#il colore non misura, identifica

articoli = ["A100", "A120", "B055", "C010", "D777"]
classe_abc = ["A", "A", "B", "C", "C"]

df = pd.DataFrame(
    {"Classe_ABC": classe_abc},
    index=articoli
)

plt.figure(figsize=(4, 3))

img = plt.imshow(
    pd.Categorical(df["Classe_ABC"]).codes.reshape(-1, 1),
    cmap="tab10",
    aspect="auto"
)

plt.yticks(range(len(articoli)), articoli)
plt.xticks([0], ["Classe ABC"])

plt.title("Classificazione ABC articoli")
plt.tight_layout()
plt.show()



# più completo

import pandas as pd
import matplotlib.pyplot as plt

ordini = ["O1001", "O1002", "O1003", "O1004"]
mesi = ["Gen", "Feb", "Mar", "Apr"]

stati = [
    ["Aperto", "In lavorazione", "Chiuso", "Chiuso"],
    ["Aperto", "Bloccato", "Bloccato", "Chiuso"],
    ["In lavorazione", "In lavorazione", "In lavorazione", "Chiuso"],
    ["Aperto", "Aperto", "Aperto", "Bloccato"]
]

df = pd.DataFrame(stati, index=ordini, columns=mesi)

#mappatura categorie
mappa_stati = {
    "Aperto": 0,
    "In lavorazione": 1,
    "Bloccato": 2,
    "Chiuso": 3
}

df_num = df.replace(mappa_stati)


#grafico
fig, ax = plt.subplots(figsize=(6, 3.5))

img = ax.imshow(df_num, cmap="tab10")

ax.set_xticks(range(len(mesi)))
ax.set_xticklabels(mesi)
ax.set_yticks(range(len(ordini)))
ax.set_yticklabels(ordini)

ax.set_title("Stato ordini nel tempo")

# Legenda manuale (fondamentale per categoriali)
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=plt.cm.tab10(0), label="Aperto"),
    Patch(facecolor=plt.cm.tab10(1), label="In lavorazione"),
    Patch(facecolor=plt.cm.tab10(2), label="Bloccato"),
    Patch(facecolor=plt.cm.tab10(3), label="Chiuso"),
]

ax.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc="upper left")

plt.tight_layout()
plt.show()




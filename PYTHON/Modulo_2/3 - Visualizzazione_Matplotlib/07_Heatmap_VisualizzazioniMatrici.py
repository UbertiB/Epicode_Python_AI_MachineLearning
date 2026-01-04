"""
HEATMAP
Sono rappresentazioni grafiche di dati bidimensionali in cui il colore di ciascuna cella indica l'intensità
o il valore numerico. 
Ideali per matrici o per tabelle di correlazione.
* righe e colonne sono le dimensioni (esempio articoli x mesi)
* colore è il valore (esempio basso=colore chiaro, alto=colore scuro)
Hanno la capacità di trasformare grandi quantità di numeri in un'immagine immediatamente interpretabile.
Non è un grafico di precisone, è uno strumento di percezione rapida dei pattern.
Matplotlib permette di creare heatmap a partire da matrici o array bidimensionali funzioni come imshow o matshow convertono
i valori numerici in colori, consentendo di misurare l'intensità di ciascuna cella.
Seaborn estende le capacità di matblotlib consentendo la creazione di heatmap più sofisticate, generando grafici con 
annotazioni, scale automatiche ed annotazioni avanzate.
Le heatmap sono particolarmente utili quando:
- si vuole evidenziare/indivisuare PATTERN NASCOSTI
- scoprire CONCENTRAZIONI, 
- evidenziare ANOMALIE
- confrontare MOLTI VALORI INSIEME
Funzionano bene quando:
- i numeri sono COMPARABILI
- l'obbiettivo è VEDERE, non misurare al decimale
- la domanda è: DOVE SUCCEDE QUALCOSA DI STRANO?

HEATMAP COME 'TABELLA COLORATA'
    Esempio:
        1) MAGAZZINO (articolo, mesi, quantità media)
            - indivisuare articoli sempre "caldi" o sempre "freddi"
            - vedi stagionalità che una tabella di numeri non mostra
            Le heatmap sono utilizzate per 1) individuare obsolescenza, 2) individuare stagionalità, 3) controllo dati sporchi
            Qui con le heatmap non faccio ML ma cerco di capire il comportamento dei dati prima di qualsiasi modello
        2) QUALITA'/ANOMALIE (articolo, causale, numero rettifiche)
            Quando non serve sapere il valore preciso ma serve sapere dove guardare

HEATMAP DI CORRELAZIONE (la più usata in ML)
    Qui righe e colonne sono variabili (non articoli). Il colore indica quanto due variabili si muovono insieme.
    Esempio magazzino:
        - giacenza media
        - indice di rotazione
        - giorni da ultimo scarico
        - totali scarichi anno
    Le heatmap rispondono alla domanda QUALI VARIABILI DICONO LA STESSA COSA?
    Permettono di SCOPRIRE RIDONDANZE, evitare di dare al modello ML informazioni duplicate. permettono di ridurre il rumore.
    Qui le heatmap sono uno STRUMENTO DI IGIENE DEI DATI

HEATMAP FEATURE SELECTION 'GUIDATA'
(si inizia a ragionare da ml)
    Vuoi prevedere obsoleto si/no.
    Hai 20 variabili:
        - con le heatmap individui gruppi di variabili che si muovono insieme 
        - scegli una rappresentante per gruppo
    Non scegli 'a sentimento', scegli per evidenza visiva.
    Questo permette di: - semplificare il modello, - miglioare stabilità - ridurre overfitting
    La heatmap non devide, aiuta a non fare errori grossolani

ANALISI DI ERRORE DEL MODELLO
(qui pochi la usano ma è potente)
    Qui la heatmap serve non a capire i dati, ma a capire perchè il modello sbaglia.
    Non sto più guardando il magazzino, sto guardando il cervello del modello quando va in confusione.

NON USARE LE HEATMAP per dimostarre causalità (mostra solo correlazione), per prendere decisioni automatiche, 
come output finale per il busness

IN ML LA HEATMAP è UNO STRUMENTO PER CHI COSTRUISCE IL MODELLO, NON PER CHI LO USA

Usa la heatmap prima del modello, non dopo, 
Usa la heatmap per togliere variabili non per aggiungerle
Non utilizzare la heatmap a chi non sa leggerla, crea confusione
Ogni heatmap deve rispondere ad una solo domanda

Le heatmap NON SONO DA USARE quando ci hanno pochi dati (meglio una tabella), quando i valori hanno scale molto diverse,
quando il colore diventa l'informazione primaria, quando devi confrontare precisione e non pattern. 
Le heatmap vengono utilizzate come PRIMO LIVELLO DI ANALISI, e andrebbero sempre accompagnate da un'interpretazione scritta

Ampiamente usate in ambito scientifico, statistico, finanziario e industriale.
Le heatmap hanno la capacità di trasformare grandi quantità di numeri in un'immagine immediatamente interpretabile.
Matplotlib permette di creare heatmap semplici a partire da matrici o array bidimensionali, convertendo 
i valori numerici in colori, consentendo di visualizzare l'intensità di ciascuna cella, E' possibile regolare 
la scala cromatica con colormap predefinite, scegliere la dimensione della figura, aggiungere barre dei colori
per indicare la leggenda dei valori.
Utili per analisi esplorative, per confrontare dati tra righe e colonne, ed individuare rapidamente aree di interesse 
o valori estremi.
Seaborn estende le capacità di matplotlib semplificando la creazione di hetmap più sofisticate, grafici con 
annotazioni numeriche, scale cromatiche automatiche, ed opzioni di formattazione avanzate. Posso gestire facilmente
i dataframe pandas, evidenziare valori massimi e minimi e utilizzare palette di colori predefinite per migliorare 
la leggibilità.

Le heatmap sono uno struemnto prezioso nel machine learning per rappresentare MATRICI DI CONFUSIONE.
Le matrici di confusione confrontano le predizioni di un modello con i valori reali, mostrando le corrette classificazioni
e gli errori; permette di osservare immediatamente quali classi vengono predette correttamente e quelli  
vengono confuse più frequentamente (tramite la scala cromatrica), migliorando l'interpretazione delle 
performance di un modello. 
La personalizzazione avanzata delle heatmap, comprende l'uso di colormap specifiche etichette, dimensioni e formattazioni delle celle.
Si possono applicare stili aziendali.

Le heatmap sono ideali anche per rappresentare le MATRICI DI DISTANZA, indicano quanto ciascun elemento di un dataset 
è simile o diverso dagli altri. 
Le matrici di distanza sono comuni in clustering, analisi gerarchica e comparazioni tra campioni.
Visualizzarle con una heatmap, permette di individuare gruppi di elementi simili, patner strutturali o anomalie che
potrebbero non emergere dalla semplice osservazione numerica. 
Colori più intensi possono indicare maggiore distanza mentre tonalità più chiare indicano similarità, 
rendendo più immediata la comprensione delle relazione tra i dati.
Utili nell'analisi esplorativa dei dati, nella valutazione di performance aziendali, e 
nello studio di correlazioni statistiche, nella rappresentazione di dati spaziali o temporali.
Confrontando heatmap derivanti da dataset diversi è possibile osservare patner comuni o differenze significative.

Grazie alla loro versalità sono sturmenti indispensabili per l'analisi visiva dei dati, 
la comunicazione dei risultati complessi, e la decisione basata su informazioni quantitative.

"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from scipy.spatial.distance import pdist, squareform

#
#MATRICE SEMPLICE (matshow)
#
data=np.random.randint(0,100, (6,6))
#print(data)

fig,ax=plt.subplots(figsize=(8,6))

cax=ax.matshow(data, cmap='viridis')
plt.colorbar(cax) #utilizza automaticamente i colori della heatmap
plt.show()

#
#MATRICE DI CONFUSIONE
#
y_true=[0,1,2,2,0,1,1,0]  #valori reali
y_pred=[0,2,1,2,0,1,1,0] #valori predetti

cm=confusion_matrix(y_true,y_pred) #matrice di confusione

fig,ax=plt.subplots(figsize=(6,5))
cax=ax.matshow(cm,cmap='Blues')
#aggiungo valori numeri su ogni cella
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j,i,str(cm[i,j]),va="center",ha="center", color="white")
plt.colorbar(cax)
ax.set_title("Matrice di confusione")
ax.set_xlabel("Valori predetti")
ax.set_ylabel("Valore reali")
plt.show()

#
#MATRICE DI DISTANZA
#
points=np.random.rand(6,2)
dist_matrix=squareform(pdist(points, metric='euclidean'))

fig,ax=plt.subplots(figsize=(8,6))
cax=ax.matshow(dist_matrix,cmap='magma')

for i in range(dist_matrix.shape[0]):
    for j in range(dist_matrix.shape[1]):
        ax.text(j,i,f"{dist_matrix[i,j]:.2f}",va="center",ha="center", color="white")

plt.colorbar(cax)
ax.set_title("Heatmap - matrice di distanza")
plt.show()


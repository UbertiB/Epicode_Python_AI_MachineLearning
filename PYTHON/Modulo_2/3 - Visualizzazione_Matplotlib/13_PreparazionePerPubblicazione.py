"""
La preparazione delle figura per pubblicazione e stampa è una fase importante per chi si occupa 
di data science, analisi, e visualizzazione dei dati.
Un bel grafico a video, potrebbe non avere lo stesso aspetto su carta o pdf.
Vediamo come ottimizzare i grafici creati con matplotlib per renderli pronti alla pubblicazione
rispettando standard editoriali, le corrette dimensioni da adottare, la scelta 
di caratteri e dimensioni, ecc.

RISOLUZIONE:
è uno dei primi aspetti da considerare, un'immagine con pochi pixel può risultare sfuocata,
allo stesso tempo un immnagine con troppo pesante può creare problemi nell'invio del file 
e nella gestione editoriale.
Per le pubblicazioni si consiglia una risoluzione di almeno 300 dpi
Per il web può bastare 72 o 96 dpi
In matplotlib si può impostare la risoluzione direttamente al momento del salvataggio con l'opzione dpi

FORMATO
- Rastser (pnt, jpeg) sono utili per il web o presentazioni
- Vettoriali (pdf, svg, eps) utili per pubblicazioni scientifiche, mantengono la qualità 
indipendentemente dall'ingrandimento
Scegliere il formato giusti significa garantire leggibiltà anche si riviste con standad grafici elevati

la leggibiltà di un grafico non dipende solo dalla risoluzione ma anche dalla
DIMENSIONE spesso richieste figura a 1 o 2 cvolonna con larghezza standard (85 mm o 95)
pagina inter (circa 170 mm)

Importante pianificare lo spazio disponibile, un grafico troppo grande può risultare sproporzionato
mentre un troppo piccolo rende difficile decifrare i dati.
Per questo motivo utilizzare FIGSIZE per impostare larghezza e altezza in pollici

I FONT hanno un ruolo fondamentale nella leggibilità
Testo troppi piccoli o caratteri decorativi, possono rendere difficile interpretazione dei dati
utilizzare font chiari e leggibili come arial helvetica o times new roman, comunemente accettati in abienti accademici o prefessionali
Oltre al tipo di fonr bisogna creare LA DIMENSIONE delle etichette stesse che devono avere
proporzioni adeguate rispetto al grafico. 

La scelta dei COLORI è importante per la stampa, alcuni colori che si vedono bene sullo
schermo possono risultare sbiaditi sulla carta, inoltre molte riveste accettano solo bianco/nero

Importante anche ACCESSIBILITA' CROMATICA combinazioni come rosso/verde possono essere
probblematiche per persone daltoniche, cosigliabile utilizzare palette color friendly disponibile direttamente anche in matplotlib.

Le LINEE e MARKET devono essere scelti in modo da garantire chiarezza. linee torppo sottili
rischiano di scomparire in fase di stampa, idem per i market, preferibili utilizzare linee
con spessore intermedio (lineguide 0.5) e market ben visibili (cerchi, triangoli, quadrati)
l'oibbiettivo è quello di comunicare informazioni senza generare confusione visiva

le ANNOTAZIONI servono a visualizzare punti specifici o a spiegare dettagli all'interno di un grafico,
devono essere brevi, chiare e non coprire le informazioni principali

la COERENZA è importante, se si preparano più grafici per lo stesso articolo, è importante 
mantenere lo stesso stili font, colori, dimensioni, ecc

"""

#salvataggo con risoluzione e formati corretti

import matplotlib.pyplot as plt
import numpy as np

if False:
    x=np.linspace(0,5,20)
    y=np.exp(x)

    fig,ax=plt.subplots(figsize=(3.35,2.5)) #circa 85 mm X 63 mm
    ax.plot(x,y,linewidth=1.5, label="Crescita esponenziale")
    ax.set_title("Crescita esponenziale",fontsize=10)
    ax.set_xlabel("Tempo",fontsize=9)
    ax.set_ylabel("Valore",fontsize=9)
    ax.legend(fontsize=8)

    # Salvataggio in formati diversi
    plt.savefig("grafico_pubblicazione.png", dpi=300, bbox_inches="tight")  # Raster
    plt.savefig("grafico_pubblicazione.pdf", dpi=300, bbox_inches="tight")  # Vettoriale
    plt.show()

if True:
    #grafici con colori e contrasti per una stampa in bianco/nero
    x=np.linspace(0,20,100)
    y1=np.sin(x)
    y2=np.cos(x)
    y3=np.sin(x)+np.cos(x)

    fig, ax=plt.subplots(figsize=(3.35,2.5))

    ax.plot(x,y1,linestyle="-",linewidth=1.5, label="Seno")
    ax.plot(x,y2,linestyle="--",linewidth=1.5, label="Coseno")
    ax.plot(x,y3,linestyle=":",linewidth=1.5, label="Seno+Coseno")

    ax.set_title("Fuzioni trigonometriche", fontsize=10)
    ax.set_xlabel("Asse X", fontsize=9)
    ax.set_ylabel("Valore", fontsize=9)
    ax.legend(fontsize=8)

    plt.savefig("Grafico_bn.png",dpi=300,bbox_inches="tight")
    plt.show()
"""
ASSI PERSONALIZZATI con SCALE LOGARITMICHE, TICKS CUSTOM , FORMATTER AVANZATI

La rappresentazione visiva non si limita alla scelta del grafico o ai colori, gli assi sono la cornice 
interpretative principale per rendere i grafici pià leggibili ed informativi, anche quando i dati coprono
ordini di grandezze diverse.

SCALE LOGARITMICHE
Le scale logaritmiche sono appropriate quando i valori coprano più ordini di grandezza o seguono dei trand 
esponenziali.
In una scala logartmica la differenza che c'è tra 10 e 100 è la stessa tra 100 e 1000. 
Perchè ogni passo corrisponde ad una moltiplicazione, questo mette in evidenza le variazioni relative 
piusttosto che differenze assolute.
e rende leggibili pattern che in scala lineare apparirebbero schiacciati.
Prima di applicare la scale logaritmiche è necessario verificare la presenza di zeri o negativi, il logaritimo 
non è definito per questi.
In questo caso richiede interventi di filtraggi, shift additivo, trasformazioni alternativa se non risolte
Anche gli outlier possono cambiare l'interpretazione, un valore alto, anche in logaritmo, può attirare 
l'attenzione, valutare la rimozione o l'evidenziazione separata, potrebbe essere una buona scelta.
Documentare sempre la scelta della scala logaritmica direttamente nel grafico, in modo che il lettore possa 
non interpretare erroneamente le visualizzazioni
plt.xscale('log'), plt.yscale('log'), oppure ax.set_xscale('log')

TICKS
I ticks sono le tacche sugli assi (x e y), con le relative etichette. Il layout automatico spesso non coincide con 
i punti semantici della analisi, potenza di 10, soglie operative, date significative, o intervalli mensili, 
sono esempi di ticks utili.
Definire i ticks custom consente di evitare le sovapposizione, riducendo il rumore visivo e guidando 
l'attenzione sui valori importanti.
Per le serie temporali spesso si sceglie inizio settimana, o inizio mese, ecc. i dati categorici 
posizionarli al centro delle barre.
Le etichette associate ai ticks devono essere corte e quando opportuno abbreviare.
La gestione corretta si basa su 3 cose: 1) dove mettere i tick (locator), 2) come scriverli (formatter), 3) come
farli apparire (tick_params)
Possono essere impostati nei seguenti modi:
1) Manuale: ok per grafici singoli e range ridotti, ma è una soluzione fragile
   ax.set_xticks([1,2,3])
   ax.set_xticklabels(["Q1","Q2","Q3])
2) Semi-automatico Locator e Formatter. I locator decidono le posizioni, i formatter decidono il testo.
   ax.xaxis.set_major_locator(ticker.MaxNLocator(6))  # massimo 6 tick principali
2b) tick a passo fisso (MultipleLocator)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))  # 0,10,20,30,40.
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(2))   # tick minori ogni 2.
    Major e minor tick sono diversi: i major sono quelli “importanti” con label; i minor aiutano la lettura (soprattutto con griglia)
3) Formattare i numeri
   a) percentuale:
      ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1.0))
   b) migliaia e valuta:
      ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda v, pos: f"{v:,.0f} €"))
L'aspetto dei tick, qui controlli direzione, spessore, distanza label, dimensioni testo
  ax.tick_params(axis="both", which="major", direction="out", length=6, width=1, pad=8)
  ax.tick_params(axis="both", which="minor", direction="out", length=3, width=1)
Rotazione delle label:
  plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

FORMATTER
i formatter trasformano i valori numeri del tick in etichetta leggibile. 
Esempio arrotondare quando il numero supera una soglia
Formatter ben progettati gestiscono not a number e internazionalizzazione (virgola per i decimali)
Scrivere formatter modulari e riutilizzabili (tramite funzioni) ci permette di avere lo stesso formato 
per tutto il grafico

Importante documentare sempre le trasformazioni applicate agli assi e non manipolare le scale per ottenere 
un effetto voluto che distorca il messaggio. 
Mantiene sempre la coerenza tra grafici simili, usa ticke semantici ed etichette concise.
Mostra esplicitamente quando la scala è logaritmica
Testa la leggibiltà su monitor diversi, l'esportazione in pdf, verifica la resa in bianco e nero, e 
l'accessibilità a chi ha difficoltà visive (considera daltonici). 
Aggiungi annotazioni per spiegare soglie, outlier, o trasformazioni non ovvie.
Integrando annotazioni, segnando punti chiavi con testi brevi, aiuta il lettore a comprendere gli improvvisi 
cambi di scala, modifiche di unità o soglie operative. 
La annotazioni devono essere concise e non coprire i dati

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Esempio di SCALA LOGARITMICA
if False:

    x=np.arange(1,31)
    y=np.exp(0.2*x)

    fig,ax=plt.subplots()

    ax.plot(x,y,marker="o")
    ax.set_yscale("log")  #SCALA LOGARITMICA
    ax.set_title("Casi giornalieri con scala logaritmica")
    ax.set_xlabel("Giorno")
    ax.set_ylabel("Casi (log)")
    ax.grid(True,which="both",linestyle="--")  #GRIGLIA (sottolinea i punti dei valori del dataset)

# Esempio di TICKS custom con formatter personalizzato
if False:

    value=[1_200,15_000,2_300_000,5_000_000_000]
    labels=["A","B","C","D"]

    fig,ax=plt.subplots()

    ax.bar(labels,value)

    def thousands(x,pos):
        if x>=1e9: return f"{x/1e9:.1f}B"  #b=miliardi
        if x>=1e6: return f"{x/1e6:.1f}M"   #m=milioni
        if x>=1e3: return f"{x/1e3:.1f}K" #k=mila
        return f"{int(x)}"
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousands)) #FORMATTER PERSONALIZZATO
    ax.set_ylabel("Ricavi")
    ax.set_xlabel("Vendite (tics abbreviati)")


# Esempio di TICKS personalizzati + SCALA LOGARITMICA
if True:

    value=[1_200,15_000,2_300_000,5_000_000_000]
    labels=["A","B","C","D"]

    fig,ax=plt.subplots()

    ax.bar(labels,value)

    def thousands(x,pos):
        if x>=1e9: return f"{x/1e9:.1f}B"  #b=miliardi
        if x>=1e6: return f"{x/1e6:.1f}M"   #m=milioni
        if x>=1e3: return f"{x/1e3:.1f}K" #k=mila
        return f"{int(x)}"
    
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(thousands)) #FORMATTER PERSONALIZZATO
    ax.set_yscale("log")  #SCALA LOGARITMICA
    ax.set_ylabel("Ricavi")
    ax.set_xlabel("Vendite (tics abbreviati)")    

    
plt.show()

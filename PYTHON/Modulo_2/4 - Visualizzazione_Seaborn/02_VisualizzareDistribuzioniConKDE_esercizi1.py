"""
KDE (Kernel Density Estimation) 
è un modo per disegnare una curva liscia che rappresenta come sono distribuiti i valori di una variabile numerica.

Ho una colonna di numeri, KDE risponde alla domanda: come sono distribuiti questi valori?
Ho due metodi per fare questo:
1) Istogramma (risposta discreta): divido l'intervallo dei valori in fasce e conto quante osservazioni
cadono in ciascuna fascia (bins). Quindi mostra conteggi reali in ogni bins
2) KDE (risposta continua): stimo una funziona continua che descrive dove i valori si concentrano
KDE non disegna i valori, ma come i valori di concentrano (quindi quante x ci sono con valore y)
Con KDE stimi una cura che rappresenta la densità dei valori
Quindi la y della KDE non identifica quanti record ma la densità. La probabilità di trovare un valore
tra 2 e 3 è l'area sotto la curva tra 2 e 3

come distingue tra continuo e discreto:
chiediti: 'Ha senso dire 2.5?
Si: continuo
No: discreto

Quindi KDE ha senso solo con valori continui, per descrivere i dati con una 'campana' assume continuità
tra valori vicini, altrimenti si inventa valori che non esistono.
Per valore discriti si possono usare altri grafici, come countplot (che conta quanti dati sono presenti 
in un determinato valore di variabile)

Perchè usare la KDE?
* Per capire dove si concentrano i valori (zona più probabile)
* Per capire se la distribuzione è asimmetrica (coda lunga)
* Per capire se ci sono più popolazioni mescolate (più picchi)
* Per confrontare gruppi (esempio Lunch vs Dinner) (come si farebbe con tanti istogrammi sovrappposti)

QUANDO usare la KDE?
* la variabile è continua (o quasi continua), esempio soldi, tempi, misure
* hai un numero di osservazioni decente (non 20 righe)
* vuoi confrontare gruppi e ti interessa la forma delle distribuzioni
EVITA di usare la KDE
* La variabile è disceta con pochi valori
* Dataset piccolo
* Vuoi "contare" eventi: per quello meglio istogramma o countplot

COME LEGGERE una KDE
Quandi guardi una KDE chiediti:
A) Dove sta il picco principale? 
   E' la zona dove i valori sono più concentrati. Non significa "valore 
più frequente esatto" significa "zona più intensa"
B) La curva è simmetrica o ha una coda?
   - coda a destra (tipico): pochi casi molto alti
   - coda a sinistra: pochi casi molto bassi
C) Ci sono picchi?
   Più picchi possono significare:
   - ci sono due popolazioni (esempio pranza e cena, maschio e femmina)
   - bandwidth troppo bassa
D) La curva varia molto se vari lo smoothing?
   Se cambiando lo smoothing la storia cambia, il patterna non è robusto

COSA PUOI CAPIRE da una  KDE
Puoi capire:
   - forma della distibuzione
   - presenza di code assimetriche
   - confronto tra gruppi (spostamenti a destra/sinistra, variabilità)
   - indizzi di 'mescolanza' (multimodalità)
Non puoi capire:
   - causalità
   - significatività statistica (serve test o bootstra)
   - quanti record ci sono (se la KDE è normalizzata: due gruppi possono avere curve 'simili'
     anche con numerosità molto diversa)
   - performance predittiva di un modello

SMOOTHING (BANDWIDTH)  
La KDE dipende da quanto 'spalmi' i punti. In Seaborn li controlli con: BW_ADJUST

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import seaborn as sns

tips = sns.load_dataset("tips")

# controllo colonne e prime righe (serve per sapere cosa stai plottando)
print(tips.columns)
print(tips.head())
#Perché farlo: in analisi dati, se non sai le colonne e i tipi, i grafici possono mentirti.

#1) KDE base: distribuzione di una sola variabile (tip)
plt.figure(figsize=(6,4))
sns.kdeplot(data=tips, x="tip")
plt.title("KDE 1D: distribuzione di tip")
plt.xlabel("tip")
plt.ylabel("densità")
plt.show()
#osserva il picco (zona della mancie più comuni, coda a destra (poche mance molto alte (outlier)))

#2) Istogramma + KDE (check anti illusioni)
plt.figure(figsize=(6,4))
sns.histplot(data=tips, x="tip", stat="density", bins=20, alpha=0.3)
sns.kdeplot(data=tips, x="tip")
plt.title("Istogramma (density) + KDE")
plt.xlabel("tip")
plt.ylabel("densità")
plt.show()
#l'istrogramma ti ancorda ai dati reali (conteggio per intervallo)
#la KDE è una stima liscia: senza istogramma rischi di credere che siano dati reali (e non la densità)

#3) Effetti di BW_ADJUST (capire curva liscia)
plt.figure(figsize=(6,4))
sns.kdeplot(data=tips, x="tip", bw_adjust=0.5, label="bw=0.5")
sns.kdeplot(data=tips, x="tip", bw_adjust=1.0, label="bw=1.0")
sns.kdeplot(data=tips, x="tip", bw_adjust=2.0, label="bw=2.0")
plt.title("Smoothing: bw_adjust cambia la storia")
plt.xlabel("tip")
plt.ylabel("densità")
plt.legend()
plt.show()
#se a bw=0.5 vedi picchi ma a bw=2 spariscono, probabilmente erano rumore
#se la forma (un picco + coda) resta simile, è un pattern robusto

#4) Confronto tra gruppi HUE (Lunch vs Dinner)
plt.figure(figsize=(6,4))
sns.kdeplot(data=tips, x="tip", hue="time", fill=True, alpha=0.4, common_norm=False)
plt.title("KDE tip per time (Lunch vs Dinner) - confronto forma")
plt.xlabel("tip")
plt.ylabel("densità")
plt.show()
#se la curva Dinner è più a destra: a cena le mance tendono ad essere più alte
#se è più larga: più variabilità
#Non concludere che Dinner è più importante: la KDE non ti dice quanti record ci sono, ti dice la forma

#5)Vincolo di dominio e bordo (CUT)
#Per variabili non negative utilizza cut=0 per evitare che la KDE sconfini oltre il bordo sinistro (perchè prende i valori vicini)
plt.figure(figsize=(6,4))
sns.kdeplot(data=tips, x="tip", fill=True, cut=0)
plt.title("KDE con cut=0 (non extrapola oltre i dati)")
plt.xlabel("tip")
plt.ylabel("densità")
plt.show()

#6) KDE 2D (densità di coppie)
plt.figure(figsize=(6,4))
sns.kdeplot(data=tips, x="total_bill", y="tip", fill=True)
plt.title("KDE 2D: dove si concentrano le coppie (conto, mancia)")
plt.xlabel("total_bill")
plt.ylabel("tip")
plt.show()
#Diventa un disegno a 3D dove la terza dimensione è la numerisità (prima sulla Y)
#capisci dove stanno la maggior parte dei casi (zone più intense)
#capisci se esistono "regimi" o "modalità operative" (conti alti con mance più disperse)

"""
Raccomandazioni operative (da analista serio)
KDE mai da sola: fai almeno istogramma + KDE.
Prova sempre 2-3 bw_adjust. Se la storia non regge, non fidarti.
Per confronti tra gruppi usa di default common_norm=False e poi controlla la numerosità 
con value_counts().
Se stai analizzando KPI ERP, KDE è ottima per vedere code e stabilità; 
poi passi a statistiche robuste (mediana, quantili, IQR).
"""

if False: 
    sns.countplot(data=tips, x="size")
    plt.title("Countplot su variabile discreta: size")
    plt.show()



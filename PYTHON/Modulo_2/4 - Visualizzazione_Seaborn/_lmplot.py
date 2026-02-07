"""
LMPLOT (“scatter + retta”)

sns.lmplot() 
fa uno scatter più una stima di modello lineare (di default una regressione lineare) 
spesso si aggiunge l'intervallo di confidenza. 
lm = linear model, cioè “modello lineare”.
Per verificare che ci sia una relazione lineare puoi utilizzare lo scatter, se una nube inclinata
abbastanza dritta allora è lineare
E' polimoniale quando lo scatter evidenzia una curva (U), in questo caso bisogna cambiare modello

Da utilizzare tra due variabili numeriche (continua vs continua)
Vedi la relazione tra queste due variabili (numeriche), aggiungendo una linea di tendenza (regressione lineare).
E puoi confrontare quel trend tra gruppi distinti (usando hue, col, row).
L'asse x rappresenta la variabile indipendente, mentra l'asse y la variabile dipendente 
(la x determina i valori della y). Non dimostra in nessun caso l'esistenza di una relazione
causa-effetto tra due variabili. La relazione deve essere già nota per poter considerare una
variabile come dipendente da un'altra. Oppure deve essere dimostrata successivamente all'analisi
grafica. Lo scatterplot mostra semplicemente come si distribuiscono le coppie di valori
per un campione di osservazione.

Il suo scopo non è visualizzare i punti (scatterplot) ma mostrare la relazione stimata
tra due variabili. I punti ci sono, ma sono secondari rispetto alla linea di tendenza.
Può essere usato per:
- Visualizzare la relazione tra due variabili numeriche, mostrando la tendenza generale
- Confrontare la relazione tra due variabili in diversi gruppi (usando hue o col)
- Valutare la bontà di adattamento di un modello lineare ai dati osservati
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Creiamo un dataset di esempio
np.random.seed(0)
df = pd.DataFrame({
    "x": np.random.rand(400) * 10,
    "y": np.random.rand(400) * 20 + 5,
    "categoria": np.random.choice(["A", "B"], size=400)
})  
# Aggiungiamo una relazione lineare con rumore
df["y"] += 2 * df["x"] + np.random.randn(400)

#Esempio base di lmplot
#In questo esempio di base, creiamo un lmplot per visualizzare la relazione tra due variabili numeriche,
#aggiungendo una linea di regressione lineare con intervallo di confidenza.  


# Creiamo l'lmplot
sns.lmplot(data=df, x="x", y="y", aspect=1.5, height=5, ci=95)
plt.tight_layout()
plt.title("Esempio di lmplot: relazione tra x e y")
plt.show()

#Personalizzazione avanzata
"""
sns.lmplot() offre molte opzioni per personalizzare il grafico:
- hue: per colorare i punti e le linee di regressione in base a una variabile categoriale
- col e row: per creare griglie di grafici separati per diverse categorie
- order: per specificare il grado del polinomio della regressione (default è 1 per lineare)
- ci: per mostrare o nascondere l'intervallo di confidenza
- scatter_kws e line_kws: per personalizzare l'aspetto dei punti e della linea di regressione
- se hai tanti punti usa alpha per la trasparenza, in questo modo si vede meglio la densità dei punti
Ecco un esempio avanzato che utilizza alcune di queste opzioni: 
"""
 
# Aggiungiamo una relazione lineare con rumore diversa per ciascuna categoria
df.loc[df["categoria"] == "A", "y"] += 2 * df["x"] + np.random.randn(400)
df.loc[df["categoria"] == "B", "y"] += 3 * df["x"] + np.random.randn(400)
# Creiamo l'lmplot con personalizzazioni avanzate
sns.lmplot(data=df, x="x", y="y", hue="categoria", aspect=1.5, height=5, ci=95, order=1,scatter_kws={"s": 50, "alpha": 0.6},line_kws={"linewidth": 2})
plt.title("Esempio avanzato di lmplot con categorie")
plt.show()
"""
Vantaggi di sns.lmplot()
- Automatizza la creazione di grafici di regressione, riducendo il codice necessario rispetto a Matplotlib puro.
- Gestisce automaticamente la legenda, i colori e l'aspetto del grafico.    
- Permette di esplorare facilmente relazioni tra variabili in diversi gruppi o categorie.
- Offre molte opzioni di personalizzazione per adattarsi a diverse esigenze di visualizzazione.
"""
#esempi con row e col
sns.lmplot(data=df, x="x", y="y", hue="categoria", col="categoria", aspect=1, height=4, ci=None,scatter_kws={"alpha":0.2})
plt.suptitle("Esempio di lmplot con col per categorie", y=1.02)
plt.show()
sns.lmplot(data=df, x="x", y="y", hue="categoria", row="categoria", aspect=1, height=4, ci=None)
plt.suptitle("Esempio di lmplot con row per categorie", y=1.02)
plt.show()

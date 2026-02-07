"""
HEATMAP
Una heatmap è un modo di mostrare una tabella di numeri come una griglia di colori: ogni cella ha un valore, 
il colore rappresenta 'quanto è grande' quel valore.
Serve a vedere pattern che in una tabella a occhi sfuggono. 
Con la heatmap trovo zone calde/fredde e anomalie, non dimostra cause, ti indica dove guardare.

HEATMAP DI CORRELAZIONE
L'analisi dati le heatmap più usata è quella della
matrice di correlazione: ti dice quali variabili 'si muovono insieme'.
Una correlazione alta NON significa causa-effetto, significa solo associazione statistica. 
E' uno strumento di screening, non è realtà pura, va poi verificato
Una heatmap di correlazione è una matrice (variabile x variabile) dove ogni cella contiene un 
coefficiente di correlazione e il colore fa vedere 'subito' pattern e blocchi di variabili che 
si muovono insieme.

Come si legge:
* Valori in genere da -1 a +1
    - +1: relazione perfetta creacente (all'aumentare di x, y cresce)
    - 0: nessuna relazione lineare (ma può esserci altro tipo di relazione)
    - -1: relazione lineare perfetta decrescente (all'aumentare di x y decresce)
* La diagonale: sempre 1 (una variabile correlata con se stessa)
* Blocchi di colore simili: variabili che si 'assomigliano'
* Attenzione alle unità: la correlazione è adimensionale, ma outlier e codifiche sbagliate
  la 'drogano'
* Se vedi correlazioni 'forte' assurde: prima sospetta i dati (duplicati, valori default, 0
, importi segno errato, data sbagliate)

Diversi TIPI DI CORRELAZIONE:
* PEARSON (defaul): misura relazione lineare tra due variabili numeriche, soffre outlier. 
  Misura quando la relazone tra x e y è lineare. Quando x aumenta, y aumenta o diminuisce?
  Da usare quando ci si aspetta una relazione lineare. Scopri bene collinearità (variabili quasi duplicate),
  driver lineari, ridondanze. Attenzione agli outlier che falsificano la relazione, 
  attenzione a relazioni non lineari (person non adatta), cambiare tipo.
* SPARMAN: usa i ranghi; vede relazioni monotone anche non lineari, ed è più robusta con outlier. 
  Misura quanto la relazione è monotona utilizzando i ranghi 
  (ordina i valori, non usa gli importi nudi e credi). Quanto x aumenta y aumenta 
  (anche in modo non lineare)? Da utilizzare se interessa sapere solo se sale x sale/scende y
  Da utilizzarsi quando la relazione c'è ma non è lineare (es. più sconto più vendite ma fino 
  ad un certo punto, poi le vendite o rimangono stabili), oppure quando
  si hanno outlier (e meno influenzata dagli outlier). Scopri trend monotoni. Attenzione alle relazioni
  a U (sale e poi scende), può dare relazione vicino a 0 anche se c'è struttura (relazione).
* KENDALL: alternativa robusta su campioni piccoli con tanti pareggi. 
  Misura concordanza tra ordinamenti guardando coppie di osservazioni (concordanti vs discordanti). 
  Vuol dire: quanto volte, prendendo due righe a caso, l'ordine di x e l'ordine di y
  vanno nella stessa direzione?
  Ha un'interpretazione più probabilistica ed è spesso più stabile con campioni piccoli 
  o con molti pareggi. Da utilizzarsi con dataset piccoli

Attenzione: sparman e kendal non 'vedono' bene relazioni non monotone. 
Se Y cresce fino ad un punto e poi decresce, anche se la relazione è forte, 
queste correlazioni possono risultare vicino a 0 (es sconto vs vendita: aumenta fino ad 
un certo livelo poi non aumenta più)

RACCOMANDAZIONI:
- pulizia dati
- stesse unità, stessi periodi, stessi criteri di calcolo
- Attenzione alle variabili derivate (venduto=qta*prezzo). 
  E' normale che sia correlato con entrembi i valori
- Attenzione outlier e segmentezioni. 
  Una commessa enorme distorce Pearson

Sintetizza grandi quantità di dati numerici
Mostra un matrici di valori codificata con una scala di colori.
Integrando informazioni statistiche si va oltre una semplice 
rapopresentazione visiva (p valued cluster e relazioni complesse
tra variabili)

Fondamentale interpretare correttamente le heatmap per trarre informazioni
solide dai dati.

Una delle applicazioni più comuni della heatmap è la rappresentazione delle
matrici di correlazione, tuttavia mostrare solo i coefficienti di correlazione
può essere fuorviante, poiche non tutte le correlazioni osservate possono
essere significative, per questo motivo si puù aggiungere annotazioni che
indicano il p-values, aggiungendo stelle di significatività 
Combino informazione numerica e statistica, distinguendo relazioni forti ma casuali
da relazione effettivamente robuste

Seabor, combinato con scipy stats permette di calcolare automaticamente coefficente
di correlazione p-values per ciascuna coppia di variabili, così da creare matrici
annotate. Per capire quali associazioni sono effettivamente rilevanti.

Un'evaluzione naturale delle heatmap classiche è la CLUSTERED HEATMAP con dendogrammi
permette di raggruppare variabili simili
organizza automaticamente righe e colonne in base alla somiglianza tra variabili.
Calcola le distanze tra variabili, esegue il clustering e riordina la matrice di conseguenza.
Il dendogramma laterale, mostra la gerarchia dei cluster, aiutando a rilevare relazioni
complesse in dataset importanti.

Un altro uso avanzato delle heatmap consiste nel rappresentare valori aggregati (come media e
la deviazione standard). invece di visualizzare dati grezzi, possiamo calcolare indicatori
riassuntivi e mostrali in forma di mappa di calore. La deviazione standard può essere
mostrata come testo all interno delle celle colorate. Rendono immediata la comprensione della
variabilità interna ai gruppi.

Quandi si calcola decine o centinaia di correlazioni aumenta il rischio di trovare relazioni
apparentemente significative solo per effetto del caso, per quesot motivo è fondamentale 
applicare una correzione per confronti multipli come Bonferroni o FDR (false discovery rate)
per controllare la probabilità di errori, dopo possiamo indicare le celle significative con il
loro colore
In questo modo la heatmap mostra la forza delle relazioni e la loro validità statistica 

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# matrice 4x4
df = pd.DataFrame(
    [[10, 12, 9,  4],
     [ 7,  3, 2,  1],
     [ 0,  5, 8, 11],
     [ 6,  6, 6,  6]],
    index=["R1","R2","R3","R4"],
    columns=["C1","C2","C3","C4"]
)

#
# HEATMAP BASE su matrice piccola (capire cella-colore)
#
plt.figure(figsize=(6,4))
sns.heatmap(df, annot=True, linewidths=0.5) #annot valori in cella, fmt="d"
plt.title("Heatmap base: valori in cella")
plt.show()

#
# da tabella dei movimenti a pivo poi heatmap
#
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(7)

# tabella "movimenti" finta
n = 800
mov = pd.DataFrame({
    "data": pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0, 365, n), unit="D"),
    "famiglia": np.random.choice(["A_FRUTTI", "B_MECC", "C_ELETTR", "D_RICAMBI"], size=n, p=[0.25,0.35,0.25,0.15]),
    "qta": np.random.poisson(lam=20, size=n)
})

mov["mese"] = mov["data"].dt.to_period("M").astype(str)

# pivot: righe=famiglia, colonne=mese, valori=somma qta
pt = pd.pivot_table(mov, values="qta", index="famiglia", columns="mese", aggfunc="sum", fill_value=0)

plt.figure(figsize=(12,4))
sns.heatmap(pt, annot=False, linewidths=0.2)
plt.title("Quantità vendute per famiglia e mese")
plt.show()
# si nota mesi con più vendite, famiglie di prodotti che muoiono o che hanno vendite alte, buchi di vendita 
# (possibili problemi stock-out, listini, anagrafiche, ecc)

#stessa heatmap  con numeri
plt.figure(figsize=(12,4))
sns.heatmap(pt, annot=True, fmt="d", linewidths=0.2, cbar=True)
plt.title("Stesso pivot, con annotazioni numeriche")
plt.show()

#
# HEATMAP DI CORRELAZIONE (e triangolare)
#

df = pd.DataFrame({
    "qta_venduta":   [10, 12, 9, 20, 18, 15, 30, 28, 25, 22],
    "prezzo_unit":   [100, 98, 102, 95, 96, 97, 90, 92, 91, 93],
    "sconto_pct":    [2,  3,  1,  5,  4,  3,  8,  7,  6,  5],
    "costo_unit":    [70, 71, 69, 72, 71, 70, 73, 72, 72, 71],
    "lead_time_g":   [5,  6,  5,  8,  7,  6,  10, 9,  9,  8],
    "stock_giac":    [120,110,130,100,105,108,90, 95, 92, 98],
})

# margine unitario e fatturato come in un'analisi ERP
df["margine_unit"] = df["prezzo_unit"]*(1-df["sconto_pct"]/100) - df["costo_unit"]
df["fatturato"] = df["qta_venduta"] * df["prezzo_unit"]*(1-df["sconto_pct"]/100)

corr = df.corr(numeric_only=True, method="pearson")
#maschero il triangolo superiore (ridondante)
mask = np.triu(np.ones_like(corr, dtype=bool))

plt.figure(figsize=(9,6))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", vmin=-1, vmax=1, center=0, cmap="coolwarm")
plt.title("Heatmap triangolare di correlazione")
plt.tight_layout()
plt.show()

#
#HEATMAP di correlazione esempio 2
#

np.random.seed(0)
kpi = pd.DataFrame({
    "rotazione": np.random.normal(5, 1.2, 300),
    "copertura_giorni": np.random.normal(30, 8, 300),
    "leadtime": np.random.normal(12, 4, 300),
    "ritardi_pct": np.random.beta(2, 8, 300) * 100,
    "scarti_pct": np.random.beta(2, 15, 300) * 100
})

corr = kpi.corr(numeric_only=True)

# maschero il triangolo superiore (ridondante)
mask = np.triu(np.ones_like(corr, dtype=bool))


plt.figure(figsize=(7,5))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", center=0, linewidths=0.5)
plt.tight_layout()
plt.title("Correlazione tra KPI")
plt.show()

#
#Attenzione agli OUTLIER
#
pt_out = pt.copy()
pt_out.iloc[1, 5] = pt_out.iloc[1, 5] * 15  # finto outlier

plt.figure(figsize=(12,4))
sns.heatmap(pt_out, linewidths=0.2)
plt.title("Con outlier: la scala schiaccia tutto")
plt.show()

plt.figure(figsize=(12,4))
sns.heatmap(pt_out, linewidths=0.2, robust=True)
plt.title("Con robust=True: lettura più stabile")
plt.show()

#
#CLUSTERMAP
#

#clustermap non accetta NA: devi riempire o pulire
#con clustermap scopri gruppi simili, Questo è gia quasi analytics avanzata: raggruppa righe
#e colonne simili
import seaborn as sns

# standard_scale=1 scala per colonna (mesi), così confronti pattern e non livelli assoluti
g = sns.clustermap(pt, standard_scale=1, figsize=(12,6), linewidths=0.1)
g.fig.suptitle("Clustering: famiglie con pattern mensili simili", y=1.02)
plt.show()

#
#CONFUSION MATRIX come heatmap (ML)
#

#Caso realistico: classificare “consegna in ritardo” (1) vs “in tempo” (0) 
#usando feature tipo lead time, quantità, storico ritardi fornitore.

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

np.random.seed(42)
n = 1200

X = pd.DataFrame({
    "leadtime": np.random.normal(12, 4, n).clip(1, None),
    "qta": np.random.poisson(20, n),
    "storico_ritardi_fornitore": (np.random.beta(2, 6, n) * 100),
    "urgenza": np.random.binomial(1, 0.2, n)
})

# target “ritardo”: costruito con una logica plausibile
score = (
    0.15 * X["leadtime"] +
    0.03 * X["qta"] +
    0.05 * X["storico_ritardi_fornitore"] +
    1.2 * X["urgenza"] +
    np.random.normal(0, 1.5, n)
)
y = (score > np.percentile(score, 65)).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=7, stratify=y)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

pred = model.predict(X_test)
cm = confusion_matrix(y_test, pred)

plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", linewidths=0.5)
plt.title("Confusion matrix: ritardo (1) vs ok (0)")
plt.xlabel("Predetto")
plt.ylabel("Reale")
plt.show()

#
#HEATMAP PEARSON + P-VALUES + STELLINE (esempio 1)
#


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# -------------------------
# 1) Dataset finto "ERP KPI"
# -------------------------
np.random.seed(7)
n = 250

df = pd.DataFrame({
    "rotazione": np.random.normal(5, 1.2, n),
    "leadtime": np.random.normal(12, 4, n).clip(1, None),
    "copertura_giorni": np.random.normal(30, 8, n),
    "ritardi_pct": (np.random.beta(2, 8, n) * 100),
    "scarti_pct": (np.random.beta(2, 15, n) * 100),
})

# Creo una relazione plausibile: più leadtime -> meno rotazione (un po')
df["rotazione"] = df["rotazione"] - 0.08 * df["leadtime"] + np.random.normal(0, 0.6, n)

# -------------------------
# 2) Correlazioni + p-value
# -------------------------
cols = df.columns
corr = df.corr(numeric_only=True)

pvals = pd.DataFrame(np.ones((len(cols), len(cols))), index=cols, columns=cols)
for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        r, p = pearsonr(df[cols[i]], df[cols[j]])
        pvals.iloc[i, j] = p
        pvals.iloc[j, i] = p
np.fill_diagonal(pvals.values, 0.0)

# -------------------------
# 3) Stelline di significatività
# -------------------------
def p_to_stars(p: float) -> str:
    if p < 1e-4:
        return "****"
    if p < 1e-3:
        return "***"
    if p < 1e-2:
        return "**"
    if p < 5e-2:
        return "*"
    return ""

annot = corr.copy().astype(str)
for r in cols:
    for c in cols:
        annot.loc[r, c] = f"{corr.loc[r,c]:.2f}{p_to_stars(pvals.loc[r,c])}"

# Maschero triangolo superiore ma lascio la diagonale visibile
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

plt.figure(figsize=(9,6))
sns.heatmap(
    corr, mask=mask, annot=annot, fmt="",
    center=0, linewidths=0.5, cbar=True
)
plt.title("Correlazione (Pearson) con stelline da p-value")
plt.show()

#
#HEATMAP PEARSON + P-VALUES + STELLINE (esempio 2)
#
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def benjamini_hochberg(p_values: np.ndarray, alpha: float = 0.05):
    """
    Restituisce p-value aggiustati (q-value) con procedura Benjamini-Hochberg (FDR).
    """
    p = np.array(p_values, dtype=float)
    m = p.size
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * m / (np.arange(1, m+1))
    # monotonicità: q(i) = min_{j>=i} q(j)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0, 1)
    q_back = np.empty_like(q)
    q_back[order] = q
    return q_back

cols = df.columns
corr = df.corr(numeric_only=True)

# p-value matrix (Pearson)
pvals = pd.DataFrame(np.ones((len(cols), len(cols))), index=cols, columns=cols)
for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        r, p = pearsonr(df[cols[i]], df[cols[j]])
        pvals.iloc[i, j] = p
        pvals.iloc[j, i] = p
np.fill_diagonal(pvals.values, 0.0)

# Applico BH solo ai test unici (triangolo inferiore esclusa diagonale)
pairs = []
pair_idx = []
for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        pairs.append(pvals.iloc[i, j])
        pair_idx.append((i, j))

q = benjamini_hochberg(np.array(pairs), alpha=0.05)

# ricostruisco q-value matrix simmetrica
qvals = pvals.copy()
for (k, (i, j)) in enumerate(pair_idx):
    qvals.iloc[i, j] = q[k]
    qvals.iloc[j, i] = q[k]
np.fill_diagonal(qvals.values, 0.0)

def p_to_stars(p: float) -> str:
    if p < 1e-4:
        return "****"
    if p < 1e-3:
        return "***"
    if p < 1e-2:
        return "**"
    if p < 5e-2:
        return "*"
    return ""

annot = corr.copy().astype(str)
for r in cols:
    for c in cols:
        # qui uso q-value (p corretto)
        annot.loc[r, c] = f"{corr.loc[r,c]:.2f}{p_to_stars(qvals.loc[r,c])}"

mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

plt.figure(figsize=(9,6))
sns.heatmap(
    corr, mask=mask, annot=annot, fmt="",
    center=0, linewidths=0.5, cbar=True
)
plt.title("Correlazione Pearson con stelline su q-value (FDR Benjamini-Hochberg)")
plt.show()



#
#HEATMAP DI TUNING (iperparametri) ML
#

#qui la  heatmap diventa una 'mappa di performance'
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=7)

n_estimators_list = [50, 100, 200, 400]
max_depth_list = [3, 5, 8, 12, None]

rows = []
for ne in n_estimators_list:
    for md in max_depth_list:
        clf = RandomForestClassifier(
            n_estimators=ne,
            max_depth=md,
            random_state=7,
            n_jobs=-1
        )
        score = cross_val_score(clf, X, y, cv=cv, scoring="f1").mean()
        rows.append({"n_estimators": ne, "max_depth": str(md), "f1": score})

grid = pd.DataFrame(rows).pivot(index="max_depth", columns="n_estimators", values="f1")

plt.figure(figsize=(8,4))
sns.heatmap(grid, annot=True, fmt=".3f", center=grid.values.mean(), linewidths=0.3)
plt.title("Tuning RandomForest: F1 medio in cross-validation")
plt.xlabel("n_estimators")
plt.ylabel("max_depth")
plt.show()


if False:

  df = pd.DataFrame({
      "qta_venduta":   [10, 12, 9, 20, 18, 15, 30, 28, 25, 22],
      "prezzo_unit":   [100, 98, 102, 95, 96, 97, 90, 92, 91, 93],
      "sconto_pct":    [2,  3,  1,  5,  4,  3,  8,  7,  6,  5],
      "costo_unit":    [70, 71, 69, 72, 71, 70, 73, 72, 72, 71],
      "lead_time_g":   [5,  6,  5,  8,  7,  6,  10, 9,  9,  8],
      "stock_giac":    [120,110,130,100,105,108,90, 95, 92, 98],
  })

  # margine unitario e fatturato come in un'analisi ERP
  df["margine_unit"] = df["prezzo_unit"]*(1-df["sconto_pct"]/100) - df["costo_unit"]
  df["fatturato"] = df["qta_venduta"] * df["prezzo_unit"]*(1-df["sconto_pct"]/100)

  #
  # HEATMAP relazione lineare con PEARSON
  #

  corr = df.corr(numeric_only=True, method="pearson")

  plt.figure(figsize=(9,6))
  sns.heatmap(corr, annot=True, fmt=".2f", vmin=-1, vmax=1, center=0, cmap="coolwarm")
  plt.title("Heatmap di correlazione (Pearson)")
  plt.tight_layout()
  plt.show()



  import numpy as np
  from scipy.stats import pearsonr
  from statsmodels.stats.multitest import multipletests

  cols = df.select_dtypes("number").columns
  n = len(cols)

  pvals = []
  pairs = []
  rmat = df[cols].corr(method="pearson")

  for i in range(n):
      for j in range(i+1, n):
          r, p = pearsonr(df[cols[i]], df[cols[j]])
          pairs.append((cols[i], cols[j]))
          pvals.append(p)

  # correzione FDR (meno “punitiva” di Bonferroni in esplorazione)
  rej, p_adj, _, _ = multipletests(pvals, alpha=0.05, method="fdr_bh")

  # costruisco una matrice booleana di “significatività”
  sig = pd.DataFrame(False, index=cols, columns=cols)
  for (a,b), ok in zip(pairs, rej):
      sig.loc[a,b] = ok
      sig.loc[b,a] = ok

  # heatmap che mostra solo le correlazioni “significative”
  filtered = rmat.where(sig, other=np.nan)

  plt.figure(figsize=(9,6))
  sns.heatmap(filtered, annot=True, fmt=".2f", vmin=-1, vmax=1, center=0, cmap="coolwarm")
  plt.title("Correlazioni (Pearson) significative dopo FDR")
  plt.tight_layout()
  plt.show()



  # RELAZIONE LINEARE: PEARSON è PERFETTO
  import numpy as np, pandas as pd
  np.random.seed(0)
  x = np.arange(1, 21)
  y = 3*x + np.random.normal(0, 3, size=len(x))

  df = pd.DataFrame({"x": x, "y": y})
  print(df.corr(method="pearson").loc["x","y"],
        df.corr(method="spearman").loc["x","y"],
        df.corr(method="kendall").loc["x","y"])


  # RELAZIONE MONOTONA MA NON LINARE (SATURAZIONE) 
  # SPEARMAN/KENDALL SPESSO MEGLIO DI PEARSON

  x = np.arange(1, 51)
  y = np.log(x) + np.random.normal(0, 0.05, size=len(x))  # cresce ma “si satura”
  df = pd.DataFrame({"x": x, "y": y})
  print(df.corr(method="pearson").loc["x","y"],
        df.corr(method="spearman").loc["x","y"],
        df.corr(method="kendall").loc["x","y"])


  # OUTLIER (TIPICO ERP) PERSON SI ROMPE FACILMENTE

  x = np.arange(1, 21)
  y = 2*x + np.random.normal(0, 1, size=len(x))
  y[-1] = 500  # “commessa fuori scala”
  df = pd.DataFrame({"x": x, "y": y})
  print(df.corr(method="pearson").loc["x","y"],
        df.corr(method="spearman").loc["x","y"],
        df.corr(method="kendall").loc["x","y"])

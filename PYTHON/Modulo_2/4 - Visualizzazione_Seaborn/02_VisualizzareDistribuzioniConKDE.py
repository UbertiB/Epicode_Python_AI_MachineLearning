"""
Visualizzazione di distribuzioni complesse con KDE ed approcci avanzati
La stima della densità di probbabilità è uno strumento fondamentale per capire la forma reale dei dati, 
al dila di istogrammi grezzi.
La Kernel Density Estimation (KDE) permette di ottenere una stima continua e liscia della distribuzione
dei dati, utile per individuare modalità, code e pattern nascosti.
Nella datascience moderna conoscere la KDE è essenziale, perchè fornisce una visualizzazione più robusta
rispetto ad istrogrammi a backet fissi

Il KERNEL è la forma della collina
il BANDWIDTH larghezza delle collina
Bandwidth piccola: campane strette, curva nervosa, segui il rumero
Bandwidth grande: campane larghe, curva liscia, perdi il dettaglio
la domanda è: a che distanza due valori smettono di essere 'simili' per il mio business?
quella distanza è la bandwidth.
La bandwidth pertanto è una questione delicata. 
Se non specifichi la bandwidth sns.kdeplot(data=df, x="colonna")
Seaborn la può scegliere automaticamente:
- Seaborn delega a SciPy
- SciPy usa una regola automatica (Scott o simile)
- tu non vedi la bandwidth ma c'è
Se indichi sns.kdeplot(data=df, x="colonna", bw_adjust=1.5)
Stai dicendo di prendere la bakdwidth automatica e moltiplicarla per 1.5

METODI PER LA BANDWIDTH AUOTMATICA
- Scott's Rule (in Seaborn/SciPy è spesso il default)
- Silverman's Rule (più conservativa)
- Cross-Validation (CV) (la più pura)
- Plug-in methods (Sheather-Jones, ecc)

Ma non è la verità è una scelta ragionevole

Il vero parametro critico della KDE è il bandwidth

KDE BASE o UNIVARIATA (una sola variabile continua)
Risponde alla domanda: 'come sono distribuiti i valori di questa variabile?'
La KDE univariata costruisce una funzione di densità sommando kernel concentrati su ciascun punto campioni 
normalizzato, ogni kernel ha una larghezza determinata dal benwith 
(piccolo: stime rumorose, grande:stime troppo lisce). La scelta del benwith è spesso il punto critico,
esisteono regole pratiche e metodi di cross validation, in pratica, per visualizzare una KDE 
si usa spesso si usa seaborn con snskdeplot o syspytstats (fornisce un'interfaccia alta 
e styling automatico), mentre gausian kde  e scikitlearn permetto un controllo più fine.
Per dataset piccoli la KDE è eccellente per rivelare modalità multiple
Per dataset molto grandi può essere utili cambionamento o smothing
Un buon workflow è:
- ispezionare i dati come outlier e range
- standarizzare se necessario
- provarre diverse benwith o usare regole automatice
- verificare coerenza con la conoscenza di dominio

KDE MULTIVARIATA (bivariata)
La KDE multivariata estenede il concetto a pù dimensioni, la densità viene stimata nello spazio 
con kernel multidimensionali.
La difficoltà principale è la dimensione del dastaset, con l'aumentare delle dimensioni la densità si
disperde e sono necessari dataset molto grandi. Per questo motivo, si preferisce guardare a KDE multidimensionata
per due o 3 variabili al massimo o usare tecniche di dimension redaction (come pca o tsne)
Risponde alla domanda: 'dove si concentrano le coppie (x,y)?'
Non guardo più una sola colonna, ma la densità nello spazion x-y
Zone più scure  indicano coppie più frequenti
Per due o 3 varibili al massimo o utlizzare tecniche di dimension redaction prima della kde, come pca o dsme
kdeplot con filtrue e levels per disegnare i controrni e sns.joinplot per coppie di variabili


KDE CONDIZIONATA
La KDE condizionata significa stimare la densità di una variabile dato il valore di un altra, 
si usa molto in analisi esplorativa (come hue in seaborn)
Permette di vedere come cambia la forma della distribuzione in segmenti diversi.
Risponde alla domanda: 'come cambia la distribuzione di X dato un gruppo?'
In Seaborn è spesso fatta con hue

Esistono diverse estensioni pratiche della kde, la bendwith selecion che oltre a  regole automatiche 
è utile utilizzare crossvalidation per scegliere il bendwith ottimale rispetto ad un criterio
e skilean


Per visualizzare KDE in 3d si può valutare la densità su una griglia 3d ed utilizzare mpl toolkits
"""

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity

tips = sns.load_dataset("tips")

#FORMA DEL BANDWIDTH

sns.kdeplot(data=tips, x="total_bill", bw_adjust=0.3)
plt.title("Bandwidth piccola (curva nervosa)")
plt.show()

sns.kdeplot(data=tips, x="total_bill", bw_adjust=2)
plt.title("Bandwidth grande (curva molto liscia)")
plt.show()

sns.kdeplot(data=tips, x="total_bill")
plt.title("Bandwidth automatico (..)")
plt.show()

#KDE BASE o UNIVARIATA

sns.kdeplot(data=tips, x="total_bill", fill=True)
plt.title("KDE BASE (UNIVARIATA): total_bill")
plt.show()

#KDE MULTIVARIATA
sns.kdeplot(data=tips, x="total_bill", y="tip", fill=True)
plt.title("KDE MULTIVARIATA: total_bill vs tip")
plt.show()

#KDE CONDIZIONATA BASE

sns.kdeplot(data=tips, x="total_bill", hue='sex', fill=True)
plt.title("KDE BASE CONDIZIONATA: total_bill vs tip")
plt.show()

#KDE CONDIZIONATA MULTIVARIATA
sns.kdeplot(data=tips, x="total_bill", y="tip", hue='sex', fill=True)
plt.title("KDE MULTIVARIATA CONDIZIONATA: total_bill vs tip")
plt.show()

x=np.concatenate([np.random.normal(-2,0.5,300),
                  np.random.normal(1.5,0.8,500),
                  np.random.normal(4,0.4,200)])

plt.figure(figsize=(8,4))
sns.histplot(x,bins=40,stat="density", alpha=0.3,label="Istogramma")
sns.kdeplot(x,bw_method="scott",label="KDE (Scott)") # SCOTT metodo per calcolare automaticamente la larghezza di banda (bandwidth)
sns.kdeplot(x,bw_adjust=0.5,linestyle="--", label="KDE (bw x0.5)")
sns.kdeplot(x,linestyle=":", color="red", label="KDE (automatico)")
#bw_adjust=0.5 riduce la larghezza della banda a metà
plt.legend()
plt.title("Distribuzione con KDE univariata")
plt.show()

x=np.random.normal(loc=0,scale=1, size=1000)
y=0.5*x + np.random.normal(scale=0.8,size=1000)
plt.figure(figsize=(6,6))
sns.kdeplot(x=x,y=y, fill=True,cmap="mako", thresh=0.05, levels=8)
plt.scatter(x[::50],y[::50],s=10, alpha=0.4, label="Campione (sottocamp)")
plt.title("KDE bidimensionale (countour + fill)")
plt.xlabel("X"), plt.ylabel("Y"), plt.legend()
plt.show()

tips=sns.load_dataset("tips")
plt.figure(figsize=(8,4))
sns.kdeplot(data=tips,x="total_bill",hue="time",common_norm=False,fill=False)
plt.title("KDE di total_bill condizionata a 'time' (Lunch/Dinner)")
plt.show()

x = np.concatenate([np.random.normal(0,1,300), np.random.normal(5,0.5,200)])[:, None]

params = {'bandwidth': np.logspace(-1,1,20)}
grid = GridSearchCV(KernelDensity(kernel='gaussian'), params)
grid.fit(x)
best_bw = grid.best_estimator_.bandwidth
print("Miglior bandwidth (CV):", best_bw)

kde = KernelDensity(bandwidth=best_bw).fit(x)
X_plot = np.linspace(x.min()-1, x.max()+1, 500)[:, None]
log_dens = kde.score_samples(X_plot)
plt.figure(figsize=(8,4))
plt.fill_between(X_plot[:,0], np.exp(log_dens), alpha=0.6)
plt.title("KDE con bandwidth ottimizzato (CV)")
plt.show()

#Esempio 5
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import gaussian_kde

x = np.random.normal(size=1000)
y = 0.8*x + np.random.normal(scale=0.7,size=1000)

xy = np.vstack([x,y])
kde = gaussian_kde(xy)

xi, yi = np.mgrid[x.min():x.max():100j, y.min():y.max():100j]
coords = np.vstack([xi.ravel(), yi.ravel()])
zi = kde(coords).reshape(xi.shape)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xi, yi, zi, cmap='viridis', linewidth=0, antialiased=True, alpha=0.8)
ax.set_title("KDE 3D (superficie)")
ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Density")
plt.show()



#Esempio A
import seaborn as sns
tips = sns.load_dataset("tips")

plt.figure(figsize=(10,5))
sns.kdeplot(data=tips, x="total_bill", hue="day", common_norm=False, fill=True, alpha=0.4)
plt.title("KDE di total_bill per giorno della settimana")
plt.xlabel("Total bill ($)")
plt.show()

# #Esempio B
# import numpy as np
# import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from sklearn.neighbors import KernelDensity

x = np.concatenate([np.random.normal(-2, 0.4, 300), np.random.normal(2,0.6,300)])[:, None]

fig, ax = plt.subplots(figsize=(8,4))
plt.subplots_adjust(bottom=0.25)
X_plot = np.linspace(x.min()-1, x.max()+1, 400)[:, None]

line, = ax.plot([], [], lw=2)
ax_hist = ax

ax_hist.hist(x.flatten(), bins=40, density=True, alpha=0.3)

ax_bw = plt.axes([0.2, 0.1, 0.65, 0.03])
slider = Slider(ax_bw, 'bandwidth', 0.01, 1.0, valinit=0.3)

def update(val):
    bw = slider.val
    kde = KernelDensity(bandwidth=bw).fit(x)
    log_dens = kde.score_samples(X_plot)
    line.set_data(X_plot.flatten(), np.exp(log_dens))
    fig.canvas.draw_idle()

slider.on_changed(update)

update(slider.val)
plt.title("KDE interattiva: cambia bandwidth")
plt.show()






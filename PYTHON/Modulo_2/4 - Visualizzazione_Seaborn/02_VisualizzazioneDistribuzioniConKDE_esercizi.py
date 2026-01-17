import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

#
# Esercizio 1
#

# Carica un dataset a scelta (qui uso penguins e tips di seaborn).
# Traccia istogramma + KDE con almeno tre bandwidth diversi (regole: Silverman, Scott, e una scelta manuale).
# Confronta i risultati e scrivi 5 righe sulle differenze osservate.


if False:
    sns.set_theme(style="whitegrid")

    penguins = sns.load_dataset("penguins").dropna()
    print (penguins.head(20))

    data = penguins["body_mass_g"].values

    def silverman_bw(x):
        std = np.std(x, ddof=1)
        n = len(x)
        return 1.06 * std * n ** (-1 / 5)

    def scott_bw(x):
        std = np.std(x, ddof=1)
        n = len(x)
        return 1.06 * std * n ** (-1 / 5) * ( (n ** (-1/5)) / (n ** (-1/5)) )

    kde_auto = gaussian_kde(data)
    bw_scott = kde_auto.factor * np.std(data, ddof=1)
    bw_silverman = silverman_bw(data)
    bw_manual = bw_silverman * 0.5

    x_grid = np.linspace(np.min(data) - 2, np.max(data) + 2, 400)

    kde_scott = gaussian_kde(data)
    pdf_scott = kde_scott.evaluate(x_grid)

    kde_silver = gaussian_kde(data)
    kde_silver.set_bandwidth(kde_silver.factor * (bw_silverman / (kde_silver.factor * np.std(data, ddof=1))))
    pdf_silver = kde_silver.evaluate(x_grid)

    kde_manual = gaussian_kde(data)
    kde_manual.set_bandwidth(kde_manual.factor * (bw_manual / (kde_manual.factor * np.std(data, ddof=1))))
    pdf_manual = kde_manual.evaluate(x_grid)

    plt.figure(figsize=(10,5))
    plt.hist(data, bins=18, density=True, alpha=0.4, color='gray', edgecolor='black', label='Istogramma')
    plt.plot(x_grid, pdf_scott, label=f'KDE (Scott) bw≈{bw_scott:.2f}', lw=2)
    plt.plot(x_grid, pdf_silver, label=f'KDE (Silverman) bw≈{bw_silverman:.2f}', lw=2)
    plt.plot(x_grid, pdf_manual, label=f'KDE (Manual 0.5*Silverman) bw≈{bw_manual:.2f}', lw=2, linestyle='--')
    plt.title("KDE univariata: bill_length_mm (penguins) — confronto bandwidth")
    plt.xlabel("bill_length_mm")
    plt.ylabel("Densità")
    plt.legend()
    plt.show()

    # Breve confronto (5 righe)
    confronto = """
    Osservazioni:
    1) Scott (kde_auto) produce una curva relativamente liscia che bilancia bias/varianza.
    2) Silverman tende a dare un bandwidth molto simile (regola simile a Scott); spesso le curve sono quasi sovrapposte.
    3) La scelta manuale (più piccola) mostra più dettagli e più modelli locali ma aumenta il rumore.
    4) Bandwidth grandi lisceranno troppo (perdita di piccole caratteristiche), bandwidth piccoli evidenziano piccole modalità ma possono creare artefatti.
    5) La scelta dipende dall'obiettivo: scoperta di sottostrutture (bw piccolo) vs stima generale della densità (bw grande).
    """
    print(confronto)

if False:
    sns.set_theme(style="whitegrid")

    penguins = sns.load_dataset("penguins").dropna()    
    data = penguins["body_mass_g"].values
    plt.figure(figsize=(10,5))
    plt.hist(data, bins=18, density=True, alpha=0.4, color='gray', edgecolor='black', label='Istogramma')
    sns.kdeplot(data=penguins,x="body_mass_g",bw_method="scott",fill=True, label="Scott") #scott (automatico, buno per partire)
    sns.kdeplot(data=penguins,x="body_mass_g",bw_method="silverman",fill=True, label="Silverman") #silverman (più produnte, meno rumore)
    sns.kdeplot(data=penguins,x="body_mass_g",bw_adjust=0.5,fill=True, label="Manuale piccolo") #manuale piccolo 
    sns.kdeplot(data=penguins,x="body_mass_g",bw_adjust=2,fill=True, label="Manuale grande") #manuale grande
    plt.legend()
    plt.title("KDE - Scott (default)")
    plt.show()

#
# Esercizio 2
#

# Prendi due variabili numeriche correlate (es. sepal_length vs sepal_width in iris).
# Costruisci una KDE bidimensionale con contour e riempimento; aggiungi scatter sottocampionato.
# Calcola la densità massima stimata e identifica il punto mediano della griglia.

from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

if True:
    iris = sns.load_dataset("iris").dropna()
    X = iris[["sepal_length", "sepal_width"]].values

    rng = np.random.default_rng(0)
    idx = rng.choice(len(X), size=min(100, len(X)), replace=False)
    X_sample = X[idx]

    bw = 0.3
    kde2 = KernelDensity(bandwidth=bw, kernel='gaussian')
    kde2.fit(X)

    xmin, ymin = X.min(axis=0) - 0.5
    xmax, ymax = X.max(axis=0) + 0.5
    xx, yy = np.meshgrid(np.linspace(xmin, xmax, 200), np.linspace(ymin, ymax, 200))
    grid_coords = np.vstack([xx.ravel(), yy.ravel()]).T

    log_d = kde2.score_samples(grid_coords)
    d = np.exp(log_d).reshape(xx.shape)

    max_idx = np.unravel_index(np.argmax(d), d.shape)
    max_point = (xx[max_idx], yy[max_idx])
    # Punto mediano della griglia (centro della grid cell)
    median_idx = (xx.shape[0]//2, xx.shape[1]//2)
    median_point = (xx[median_idx], yy[median_idx])

    plt.figure(figsize=(8,6))
    plt.contourf(xx, yy, d, levels=20, cmap='magma', alpha=0.7)
    cs = plt.contour(xx, yy, d, levels=8, colors='k', linewidths=0.5)
    plt.scatter(X_sample[:,0], X_sample[:,1], s=30, c='white', edgecolor='k', alpha=0.9, label='sample points')
    plt.scatter([max_point[0]], [max_point[1]], color='cyan', s=100, marker='X', label='Densità massima')
    plt.title("KDE 2D (sepal_length vs sepal_width) con contour e densità massima")
    plt.xlabel("sepal_length")
    plt.ylabel("sepal_width")
    plt.legend()
    plt.show()

    print(f"Densità massima stimata in: {max_point}, valore densità max (approx): {d.max():.5f}")
    print(f"Punto mediano della griglia: {median_point}")

#
# Esercizio 3
#

# Su tips, disegna KDE di total_bill condizionate per smoker (Yes/No).
# Ripeti con common_norm=True e common_norm=False e spiega la differenza pratica in 3 righe.
# Implementa GridSearchCV per trovare il bandwidth ottimale su dati univariati usando KernelDensity.
# Riporta il miglior bandwidth e mostra la KDE corrispondente su griglia.

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity

if True:
    tips = sns.load_dataset("tips").dropna()
    x_yes = tips.loc[tips.smoker == "Yes", "total_bill"].values
    x_no  = tips.loc[tips.smoker == "No", "total_bill"].values

    plt.figure(figsize=(10,4))

    plt.subplot(1,2,1)
    sns.kdeplot(x_yes, label='smoker=Yes', fill=True)
    sns.kdeplot(x_no, label='smoker=No', fill=True)
    plt.title("KDE (common_norm default=True) — densità su scala comune")
    plt.legend()

    plt.subplot(1,2,2)
    sns.kdeplot(x_yes, label='smoker=Yes', fill=True, common_norm=False)
    sns.kdeplot(x_no, label='smoker=No', fill=True, common_norm=False)
    plt.title("KDE (common_norm=False) — densità normalizzate singolarmente")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Spiegazione (3 righe)
    explain_common_norm = """
    Con common_norm=True le densità dei gruppi sono normalizzate rispetto allo stesso totale:
    le aree sotto le curve sono proporzionali alla frazione di punti del gruppo e permettono confronto della probabilità complessiva.
    Con common_norm=False ciascuna curva è normalizzata separatamente (area=1), facilitando il confronto della forma ma perdendo info sulla relativa frequenza.
    """
    print(explain_common_norm)

    # GridSearchCV per bandwidth su totale_bill (univariato)
    X = tips["total_bill"].values[:, None]
    params = {'bandwidth': np.linspace(0.1, 5.0, 40)}
    grid = GridSearchCV(KernelDensity(kernel='gaussian'), params, cv=5)
    grid.fit(X)
    best_bw = grid.best_params_['bandwidth']
    print(f"Bandwidth ottimale (GridSearchCV): {best_bw}")

    # Fit KDE con best bandwidth e plottalo
    kde_best = KernelDensity(bandwidth=best_bw)
    kde_best.fit(X)
    x_grid = np.linspace(X.min()-5, X.max()+5, 300)[:, None]
    log_d = kde_best.score_samples(x_grid)
    d = np.exp(log_d)

    plt.figure(figsize=(8,4))
    plt.hist(X.ravel(), bins=30, density=True, alpha=0.3, color='gray', label='Istogramma')
    plt.plot(x_grid.ravel(), d, lw=2, label=f'KDE bw={best_bw:.2f}')
    plt.title("KDE univariata con bandwidth ottimale (GridSearchCV)")
    plt.xlabel("total_bill")
    plt.ylabel("Densità")
    plt.legend()
    plt.show()

# # Esercizio 4

# # Costruisci una KDE 3D (o, se la 3D non è leggibile, costruisci più slice condizionate su intervalli di X) e commenta quando la 3D è utile e quando no.

# from mpl_toolkits.mplot3d import Axes3D
# from scipy.stats import gaussian_kde

# # Prendiamo due variabili da iris + terza: petal_length for 3D demo
# df3 = iris[['sepal_length','sepal_width','petal_length']].dropna().values
# X3 = df3

# # Per leggibilità realizziamo slice condizionate su sepal_length (terzo asse come densità)
# # Creiamo bins su sepal_length e per ogni bin compute KDE su sepal_width vs petal_length e plotti come contour slices

# sepal_length = X3[:,0]
# sepal_width = X3[:,1]
# petal_length = X3[:,2]

# bins = np.linspace(sepal_length.min(), sepal_length.max(), 6)  # 5 slice
# plt.figure(figsize=(10,8))
# for i in range(len(bins)-1):
#     mask = (sepal_length >= bins[i]) & (sepal_length < bins[i+1])
#     if mask.sum() < 5:
#         continue
#     data2 = np.vstack([sepal_width[mask], petal_length[mask]])
#     kde2 = gaussian_kde(data2)
#     xx = np.linspace(sepal_width.min()-0.5, sepal_width.max()+0.5, 60)
#     yy = np.linspace(petal_length.min()-0.5, petal_length.max()+0.5, 60)
#     XX, YY = np.meshgrid(xx, yy)
#     grid_coords = np.vstack([XX.ravel(), YY.ravel()])
#     zz = kde2(grid_coords).reshape(XX.shape)
#     offset = i * (zz.max() * 1.5)
#     plt.contourf(XX, YY + offset, zz, levels=8, alpha=0.6)
#     plt.text(xx[0], yy[-1] + offset, f'sep_len in [{bins[i]:.2f},{bins[i+1]:.2f}]', fontsize=8)
# plt.title("Slice condizionate: KDE su sepal_width vs petal_length per range di sepal_length")
# plt.xlabel("sepal_width")
# plt.ylabel("petal_length (offset per slice)")
# plt.show()

# # Commento:
# comment_3d = """
# 3D vs slice:
# - La KDE 3D può essere utile per esplorare densità su tre variabili continue, ma è spesso difficile da leggere (occlusioni, prospettiva).
# - Le slice condizionate permettono confronti più chiari: fissando una variabile si osserva la distribuzione bidimensionale rimanente.
# - Per pubblicazione/analisi visiva si preferiscono slice o più proiezioni piuttosto che una superficie 3D piena.
# """
# print(comment_3d)

# # Esercizio 5

# # Implementa slider del bandwidth e per la sottocampionatura; spiega come cambia la KDE al variare dei parametri.

# import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider, Button

# vals = penguins['bill_length_mm'].values

# bw0 = 0.6
# sub0 = 1.0

# fig, ax = plt.subplots(figsize=(8,5))
# plt.subplots_adjust(left=0.1, bottom=0.25)

# def compute_density(data, bw):
#     kde = KernelDensity(bandwidth=bw, kernel='gaussian')
#     kde.fit(data[:, None])
#     xg = np.linspace(data.min()-2, data.max()+2, 300)[:, None]
#     logd = kde.score_samples(xg)
#     return xg.ravel(), np.exp(logd)

# sample_idx = rng.choice(len(vals), size=int(len(vals)*sub0), replace=False)
# xg, d = compute_density(vals[sample_idx], bw0)
# hist = ax.hist(vals, bins=18, density=True, alpha=0.25, color='gray')
# line, = ax.plot(xg, d, lw=2, color='navy')
# ax.set_title("Interattivo: bandwidth e subsampling")
# ax.set_xlabel("bill_length_mm")
# ax.set_ylabel("Densità")

# # Slider axes
# ax_bw = plt.axes([0.15, 0.12, 0.7, 0.03])
# ax_sub = plt.axes([0.15, 0.06, 0.7, 0.03])
# slider_bw = Slider(ax_bw, 'Bandwidth', 0.05, 2.0, valinit=bw0)
# slider_sub = Slider(ax_sub, 'Subsample fraction', 0.1, 1.0, valinit=sub0)

# def update(val):
#     bw = slider_bw.val
#     frac = slider_sub.val
#     n = max(3, int(len(vals) * frac))
#     idx_s = rng.choice(len(vals), size=n, replace=False)
#     xg, dnew = compute_density(vals[idx_s], bw)
#     line.set_xdata(xg)
#     line.set_ydata(dnew)
#     ax.relim()
#     ax.autoscale_view()
#     fig.canvas.draw_idle()

# slider_bw.on_changed(update)
# slider_sub.on_changed(update)

# # Reset button
# resetax = plt.axes([0.8, 0.01, 0.1, 0.04])
# button = Button(resetax, 'Reset', hovercolor='0.975')
# def reset(event):
#     slider_bw.reset()
#     slider_sub.reset()
# button.on_clicked(reset)

# plt.show()

# # Spiegazione di come cambiano KDE:
# explain_interactive = """
# Variando il bandwidth:
# - bandwidth piccolo => curve più dettagliate, possibili picchi spurii (alta varianza).
# - bandwidth grande => curve molto lisce, possibili sotto-smussature delle feature (alto bias).

# Variando la sottocampionatura:
# - meno punti => stima meno precisa, maggior rumore e variabilità tra campioni;
# - più punti => stima più stabile ma anche maggiore costo computazionale.
# """
# print(explain_interactive)
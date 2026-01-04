"""
ESERCIZIO 1
Crea un file .mplstvenditele per un report azienda di vendite mensili,
indludendo font, colori aziendali, e dimensioni di linee coerenti. Applica lo stile
a un grafico di esempio

ESERCIZIO 2
Definire una palete aziendale con almeno quattro colori e utilizzarla in un grafico
che confronti vendite e acquisti su un periodo di 12 mesi. Verifica che i colori siano 
coerenti e leggibili

ESERCIZIO 3
Integrare font aziendali e loghi in un grafico: modifica il font, aggiungi un titolo
con il nome del brand, e inserisci eventuali annotazioni per evidenziare punti chiave.

ESERCIZIO 4
Crea un report pdf con tabelle e grafici: genera almeno un grafico e una tabella integrata in 
un unico lavenditeout coerente con il brandig aziendale

"""

# Esercizio 1 — Creare un file .mplstyle per un report aziendale di vendite mensili, includendo font, colori aziendali e dimensioni di linee coerenti. Applica lo stile a un grafico di esempio.

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams, style


# 1) Creo un file .mplstyle nella cartella corrente
style_filename = "company_report.mplstyle"
style_content = """
company_report.mplstyle
font.family: sans-serif
font.sans-serif: DejaVu Sans, Arial, Helvetica
font.size: 12
marker="o"
axes.titlesize: 14
axes.labelsize: 11
lines.linewidth: 2.0
lines.markersize: 6
axes.grid: True
grid.alpha: 0.3
figure.figsize: 10, 5
axes.prop_cycle: cycler('color', ['#004c97', '#00a3e0', '#f39c12', '#7fb800'])
legend.frameon: False
savefig.dpi: 150
"""

if False:
    with open(style_filename, "w", encoding="utf-8") as f:
        f.write(style_content)

    print(f"File .mplstyle creato: {os.path.abspath(style_filename)}")

    # 2) Dati di esempio 
    months = pd.date_range("2024-01-01", periods=12, freq="MS").strftime("%b")
    sales = np.array([120, 150, 130, 170, 180, 200, 210, 190, 170, 160, 155, 180])

    # 3) Applico lo stile e disegno il grafico
    style.use(style_filename)

    fig, ax = plt.subplots()
    #ax.plot(months, sales, marker='o', label='Vendite')
    ax.plot(months, sales, label='Vendite')
    ax.set_title("Vendite Mensili - Esempio (Stile Aziendale)")
    ax.set_xlabel("Mese")
    ax.set_ylabel("Vendite (k€)")
    # ax.grid(True, linestyle='--', linewidth=0.7, alpha=0.4)
    ax.legend()
    plt.tight_layout()
    plt.show()

# # Esercizio 2 — Definire una palette aziendale con almeno quattro colori e utilizzarla in un grafico che confronti vendite e acquisti su un periodo di 12 mesi. Verifica che i colori siano coerenti e leggibili.

if True:

    # Palette aziendale
    palette = {
        "primary": "#0B5FA5", 
        "accent":  "#00A3E0",   
        "warn":    "#F39C12",   
        "success": "#7FB800"    
    }

    # Stampa la palette (hex) per verifica leggibilità
    print("Palette aziendale:", palette)

    # Dati di esempio (12 mesi)
    months = pd.date_range("2024-01-01", periods=12, freq="MS").strftime("%b")
    sales = np.array([120,150,130,170,180,200,210,190,170,160,155,180])
    purchases = np.array([80,90,85,95,100,110,120,115,105,100,98,110])

    # Grafico comparativo: barre affiancate + line per trend
    x = np.arange(len(months))
    width = 0.38

    fig, ax = plt.subplots(figsize=(10,5))
    bars1 = ax.bar(x - width/2, sales, width, label='Vendite', color=palette['primary'], alpha=0.95)
    bars2 = ax.bar(x + width/2, purchases, width, label='Acquisti', color=palette['accent'], alpha=0.95)

    # aggiungo medie come linee usando colori della palette
    ax.plot(x, np.convolve(sales, np.ones(3)/3, mode='same'), linestyle='--', label='Media mobile Vendite', color=palette['warn'])
    ax.plot(x, np.convolve(purchases, np.ones(3)/3, mode='same'), linestyle='-.', label='Media mobile Acquisti', color=palette['success'])

    ax.set_xticks(x)
    ax.set_xticklabels(months)
    ax.set_xlabel("Mese")
    ax.set_ylabel("Valore (k€)")
    ax.set_title("Confronto Vendite vs Acquisti (12 mesi) — Palette Aziendale")
    ax.legend()

    # verifica semplice di contrasto: calcolo luminanza e stampo
    def luminance(hexcol):
        h = hexcol.lstrip('#')
        r, g, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
        return 0.2126*r + 0.7152*g + 0.0722*b

    for name, hexcol in palette.items():
        print(f"{name}: {hexcol}, luminanza={luminance(hexcol):.1f}")

    plt.tight_layout()
    plt.show()

# # Esercizio 3 — Integrare font aziendali e loghi in un grafico: modifica il font, aggiungi un titolo con il nome del brand e inserisci eventuali annotazioni per evidenziare punti chiave.

# import os
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib import font_manager

# # Sostituisci con il percorso del font aziendale (.ttf) se disponibile
# font_path = "path/to/your/CompanyFont-Regular.ttf" 
# logo_path = "path/to/your/logo.png"    

# # Provo ad aggiungere il font se esiste, altrimenti fallback a DejaVu Sans
# if os.path.isfile(font_path):
#     font_manager.fontManager.addfont(font_path)
#     prop = font_manager.FontProperties(fname=font_path)
#     font_name = prop.get_name()
#     plt.rcParams['font.family'] = font_name
#     print("Font registrato:", font_name)
# else:
#     print("Font aziendale non trovato. Usando font di sistema (fallback).")

# # Dati di esempio
# months = pd.date_range("2024-01-01", periods=12, freq="MS").strftime("%b")
# sales = np.array([120,150,130,170,180,200,210,190,170,160,155,180])

# # Palette di esempio
# primary = "#0B5FA5"

# fig, ax = plt.subplots(figsize=(10,5))
# ax.plot(months, sales, marker='o', color=primary, linewidth=2)
# ax.set_title("ACME Corp — Vendite Mensili", fontsize=18, fontweight='bold')  # titolo con nome brand
# ax.set_ylabel("Vendite (k€)")
# ax.set_xlabel("Mese")

# # Evidenzio punto top con annotazione
# top_idx = np.argmax(sales)
# ax.scatter([months[top_idx]], [sales[top_idx]], s=120, facecolors='none', edgecolors='red', linewidths=2)
# ax.annotate(f"Picco: {sales[top_idx]}k€", xy=(months[top_idx], sales[top_idx]),
#             xytext=(top_idx, sales[top_idx]+25),
#             arrowprops=dict(arrowstyle="->", color="red"),
#             ha='center', fontsize=10, color='red')

# # Inserisco logo in alto a destra come immagine
# if os.path.isfile(logo_path):
#     from matplotlib.offsetbox import OffsetImage, AnnotationBbox
#     img = plt.imread(logo_path)
#     imagebox = OffsetImage(img, zoom=0.12)  # regola lo zoom del logo
#     ab = AnnotationBbox(imagebox, (0.95, 0.95), xycoords='axes fraction', frameon=False)
#     ax.add_artist(ab)
#     print("Logo inserito dal percorso:", logo_path)
# else:
#     print("Logo non trovato; per inserire un logo, sostituisci 'logo_path' con il percorso del file.")

# plt.tight_layout()
# plt.show()

# # Esercizio 4 — Creare un report PDF con tabelle e grafici: genera almeno un grafico e una tabella integrata in un unico layout coerente con il branding aziendale.

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages

# # Dati mensili di esempio
# months = pd.date_range("2024-01-01", periods=12, freq="MS").strftime("%b")
# sales = np.array([120,150,130,170,180,200,210,190,170,160,155,180])
# purchases = np.array([80,90,85,95,100,110,120,115,105,100,98,110])
# profit = sales - purchases

# df = pd.DataFrame({
#     "Mese": months,
#     "Vendite (k€)": sales,
#     "Acquisti (k€)": purchases,
#     "Profitto (k€)": profit
# })

# # Stile e palette coerenti
# plt.style.use("company_report.mplstyle")  # usa lo stile creato all'es.1
# primary = "#0B5FA5"
# accent  = "#00A3E0"

# # Creo il PDF
# out_pdf = "report_brand.pdf"
# with PdfPages(out_pdf) as pdf:
#     fig = plt.figure(constrained_layout=True, figsize=(11,8.5))
#     gs = fig.add_gridspec(2, 2, height_ratios=[2, 1])

#     # Grafico (occupando la riga superiore)
#     ax0 = fig.add_subplot(gs[0, :])
#     ax0.plot(months, sales, marker='o', label='Vendite', color=primary)
#     ax0.plot(months, purchases, marker='o', label='Acquisti', color=accent)
#     ax0.set_title("Vendite vs Acquisti — Report Mensile")
#     ax0.set_ylabel("Valore (k€)")
#     ax0.legend(loc='upper left')
#     ax0.grid(True, linestyle='--', alpha=0.4)

#     # Tabella (sotto, a sinistra)
#     ax1 = fig.add_subplot(gs[1, 0])
#     ax1.axis('off')
#     table = ax1.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
#     table.auto_set_font_size(False)
#     table.set_fontsize(9)
#     table.scale(1, 1.3)
#     ax1.set_title("Dati Mensili")

#     # Box riepilogo (sotto, a destra)
#     ax2 = fig.add_subplot(gs[1, 1])
#     ax2.axis('off')
#     # statistiche semplici
#     summary = {
#         "Fatturato Totale (k€)": f"{sales.sum()}",
#         "Acquisti Totali (k€)": f"{purchases.sum()}",
#         "Profitto Totale (k€)": f"{profit.sum()}"
#     }
#     txt = "\n".join([f"{k}: {v}" for k, v in summary.items()])
#     ax2.text(0, 0.7, txt, fontsize=12, va='top')
#     ax2.set_title("Riepilogo")

#     pdf.savefig(fig)  # salva la pagina
#     plt.close(fig)

#     fig2, ax = plt.subplots(figsize=(11,8.5))
#     ax.plot(months, sales, label='Vendite', alpha=0.4, color=primary)
#     ax.plot(months, pd.Series(sales).rolling(3, center=True).mean(), label='Media Mobile (3)', color=primary, linewidth=2.5)
#     ax.set_title("Trend Vendite - Media Mobile")
#     ax.set_ylabel("Vendite (k€)")
#     ax.grid(True, linestyle='--', alpha=0.3)
#     ax.legend()
#     pdf.savefig(fig2)
#     plt.close(fig2)

# print(f"Report PDF creato: {out_pdf}")
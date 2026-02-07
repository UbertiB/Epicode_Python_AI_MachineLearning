import tkinter as tk
from tkinter import ttk

#sticky=
#"w" = allinea a sinistra
#"e" = destra
#"ew" = si allunga orizzontalmente
#"nsew" = occupa tutta la cella


root = tk.Tk()
root.title("Esempio 3+2 - Frame + griglia linee")
root.geometry("700x350")

# Root: 2 colonne (sinistra controlli, destra output)
#una riga 2 colonna
root.grid_rowconfigure(0, weight=1)  #RIGA1
root.grid_columnconfigure(0, weight=0) #COLONNA1 controlli: larghezza fissa/“naturale”
root.grid_columnconfigure(1, weight=1)  #COLONNA2 output: si espande

controls = ttk.Frame(root, padding=10)
controls.grid(row=0, column=0, sticky="nsw") #riga 1 colonna 1 metto il frame controls che sarà dove andrò a mettere tutti i controlli
controls.grid_columnconfigure(0, weight=1) #frame con una colonna
"""
n = North = alto
s = South = basso
w = West = sinistra
e = East = destra
"""

output = ttk.Frame(root, padding=10) #secondo frame dove mette l'output
output.grid(row=0, column=1, sticky="nsew")  #nsew riempie tutta le cella disponibile
output.grid_rowconfigure(0, weight=1) #frame con una riga che si adatta
output.grid_columnconfigure(0, weight=1) #frame con una colonna che si adatta

# ----------------- CONTROLS (solo grid) -----------------
r = 0
ttk.Label(controls, text="Controlli", font=("Segoe UI", 12, "bold")).grid(row=r, column=0, sticky="w", pady=(0, 10))
r += 1
ttk.Label(controls, text="Seleziona linee (4 colonne)").grid(row=r, column=0, sticky="w")

r += 1
# Frame griglia checkbutton
grid_linee = ttk.Frame(controls)  #aggiungo ulteriore frame
grid_linee.grid(row=r, column=0, sticky="ew", pady=(5, 10))  #pady=(5, 10) aggiunte spazio sopra (5) e sotto (10) al frame
r += 1

cols = 4
for c in range(cols):  #definisco le cols (4) colonne tutta dimensionabili
    grid_linee.grid_columnconfigure(c, weight=1)

linee = [f"{i:02d}" for i in range(1, 15)]  # 01..14
vars_linee = {}  #lista di valori boolean che qui definisco vuota e vado a riepire dopo quando faccio for i,linea in enumerate (linee)...

def aggiorna_output():
    selezionate = [l for l, v in vars_linee.items() if v.get()]
    testo = "Linee selezionate:\n" + (", ".join(selezionate) if selezionate else "(nessuna)")
    lbl_out.config(text=testo)

for i, linea in enumerate(linee):
    var = tk.BooleanVar(value=True)     # tutte selezionate all’avvio
    vars_linee[linea] = var

    rr, cc = divmod(i, cols)  # rr=divisione intera cc=resto
    ttk.Checkbutton(grid_linee,text=linea,variable=var, command=aggiorna_output).grid(row=rr, column=cc, sticky="w", padx=6, pady=3)

# Frame per i pulsanti tutte/nessuna
btns = ttk.Frame(controls)
btns.grid(row=r, column=0, sticky="ew")
btns.grid_columnconfigure(0, weight=1)
btns.grid_columnconfigure(1, weight=1)
r += 1

def tutte():
    for v in vars_linee.values():
        v.set(True)
    aggiorna_output()

def nessuna():
    for v in vars_linee.values():
        v.set(False)
    aggiorna_output()

ttk.Button(btns, text="Tutte", command=tutte).grid(row=0, column=0, sticky="ew", padx=(0, 5))
ttk.Button(btns, text="Nessuna", command=nessuna).grid(row=0, column=1, sticky="ew", padx=(5, 0))

# ----------------- OUTPUT (solo grid) -----------------
lbl_out = ttk.Label(output, text="", padding=10, relief="solid")
lbl_out.grid(row=0, column=0, sticky="nsew")

aggiorna_output()
root.mainloop()

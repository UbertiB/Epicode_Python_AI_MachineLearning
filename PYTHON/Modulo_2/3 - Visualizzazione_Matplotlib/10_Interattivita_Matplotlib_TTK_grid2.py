import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Esempio 2 - form con grid")
root.geometry("350x150")

# griglia: 2 colonne
root.grid_columnconfigure(0, weight=0)  # colonna label (fissa)
root.grid_columnconfigure(1, weight=1)  # colonna input (si allarga) wwight=1

#sticky=
#"w" = allinea a sinistra
#"e" = destra
#"ew" = si allunga orizzontalmente
#"nsew" = occupa tutta la cella

# riga 0
ttk.Label(root, text="Nome").grid(
    row=0, column=0, sticky="w", padx=10, pady=5
)
nome = tk.StringVar()
ttk.Entry(root, textvariable=nome).grid(
    row=0, column=1, sticky="ew", padx=10, pady=5
)

# riga 1
ttk.Label(root, text="Cognome").grid(
    row=1, column=0, sticky="w", padx=10, pady=5
)
cognome = tk.StringVar()
ttk.Entry(root, textvariable=cognome).grid(
    row=1, column=1, sticky="ew", padx=10, pady=5
)

# riga 2: bottone che usa entrambe le colonne
def stampa():
    print(nome.get(), cognome.get())

ttk.Button(root, text="Stampa").grid(
    row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10
)

root.mainloop()

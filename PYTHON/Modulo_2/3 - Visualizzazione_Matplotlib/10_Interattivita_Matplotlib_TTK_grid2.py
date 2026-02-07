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
ttk.Label(root, text="Nome").grid(   #aggiungo una label colonna 0 riga 0
    row=0, column=0, sticky="w", padx=10, pady=5
)
nome = tk.StringVar()  #aggiungo un campo testo colonna 1 riga 0
ttk.Entry(root, textvariable=nome).grid(
    row=0, column=1, sticky="ew", padx=10, pady=5
)

# riga 1
ttk.Label(root, text="Cognome").grid(  #aggiungo una label colonna 0 riga 1
    row=1, column=0, sticky="w", padx=10, pady=5
)
cognome = tk.StringVar()   #aggiungo un campo testo colonna1 riga 1
ttk.Entry(root, textvariable=cognome).grid(
    row=1, column=1, sticky="ew", padx=10, pady=5
)

# riga 2: bottone che usa entrambe le colonne
def stampa():
    print(nome.get(), cognome.get())

btn = ttk.Button(root, text="Stampa", command=stampa, width=200) #aggiungo un pulsante e definisco il comportamento con command, definisco anche la sua dimensione (larghezza) con width
btn.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=10) #posizione il pulsante

root.mainloop()

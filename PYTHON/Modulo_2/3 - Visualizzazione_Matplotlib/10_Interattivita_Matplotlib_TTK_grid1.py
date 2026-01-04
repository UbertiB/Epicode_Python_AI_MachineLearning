import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Esempio 1 - grid base")
root.geometry("300x120")

# 1 colonna che si allarga
root.grid_columnconfigure(0, weight=1)

lbl = ttk.Label(root, text="Ciao, sono una Label")
lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10)

btn = ttk.Button(root, text="Chiudi", command=root.destroy)
btn.grid(row=1, column=0, sticky="w", padx=10, pady=10)

root.mainloop()

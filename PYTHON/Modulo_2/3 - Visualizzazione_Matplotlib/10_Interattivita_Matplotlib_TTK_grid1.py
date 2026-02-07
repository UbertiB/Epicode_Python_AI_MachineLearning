"""
TKINTER
Tkinter è la libreria standard di python per GUI.
ttk è un sottomodulo di Tkinter (from tkinter import ttk) ed offre widget con aspetto più recente rispetto 
alla classica tk, con ttk ho un look più 'nativo'
Architettura minima di un GUI:
   * root=tk.Tk() crea la finestra principale
   * crei i widget (frame, label, entry, button, ecc)
   * li posizioni (consiglio grid)
   * root.mainloop() avvia i loop eventi
"""
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Esempio 1 - grid base")
root.geometry("300x120")

# 1 colonna che si allarga
root.grid_columnconfigure(0, weight=1)

lbl = ttk.Label(root, text="Ciao, sono una Label") #aggiungo una label 
lbl.grid(row=0, column=0, sticky="w", padx=10, pady=10) #posizione la label

btn = ttk.Button(root, text="Chiudi", command=root.destroy) #aggiungo un pulsante e definisco il comportamento con command
btn.grid(row=1, column=0, sticky="w", padx=10, pady=10) #posizione il pulsante

root.mainloop() #avvio loop eventi

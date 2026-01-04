import tkinter as tk
from tkinter import ttk

root = tk.Tk()                  # finestra principale
root.title("Esempio base")
root.geometry("300x150")

label = ttk.Label(root, text="Ciao Barbara")
label.pack(pady=10)

def on_click():
    label.config(text="Hai cliccato!")

btn = ttk.Button(root, text="Clicca", command=on_click)
btn.pack()

root.mainloop()

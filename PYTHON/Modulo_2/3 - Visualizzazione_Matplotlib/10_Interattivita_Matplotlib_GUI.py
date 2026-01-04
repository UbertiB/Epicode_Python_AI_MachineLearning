"""
GUI
GUI=Graphical User Interface
E' qualunque interfaccia in cui l'utente interagisce con il sw tramite elemnti grafici, invece
che scrivendo comandi.
Esempi: finestra, pulsanti, slider, checkbox, menu, campi di input
Una GUI non serve per produrre dati, serve per decidere sui dati.

GUI Tkinter
Tkinter gestisce finestra, layout e widget, matplotlib disegna dentro la GUI
"""

if False: 
        
    import pandas as pd
    from IPython.display import display

    articoli = ["Art 01", "Art 02", "Art 03", "Art 04", "Art 05",
                "Art 06", "Art 07", "Art 08", "Art 09", "Art 10"]

    mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott"]

    # Vendite (pezzi) - esempio, puoi sostituire con i tuoi dati reali
    dati = [
        [12, 15, 18, 20, 22, 25, 30, 28, 24, 19],
        [5,  7,  6,  9,  8,  10, 12, 11, 9,  6],
        [0,  1,  0,  2,  1,  0,  3,  2,  1,  0],
        [20, 18, 22, 25, 28, 30, 35, 33, 29, 24],
        [9,  10, 11, 12, 13, 15, 16, 14, 12, 10],
        [3,  2,  4,  5,  6,  8,  7,  6,  5,  4],
        [14, 13, 15, 16, 18, 19, 21, 20, 17, 15],
        [1,  0,  2,  1,  0,  3,  2,  1,  0,  2],
        [7,  8,  9,  10, 11, 12, 13, 12, 10, 9],
        [4,  5,  6,  6,  7,  8,  9,  8,  7,  6]
    ]

    df = pd.DataFrame(dati, index=articoli, columns=mesi)

    # Totali utili ERP
    df["Totale_Articolo"] = df.sum(axis=1)
    totali_mese = df.sum(axis=0).to_frame().T
    totali_mese.index = ["Totale_Mese"]

    df_finale = pd.concat([df, totali_mese], axis=0)

    # display mostra la tabella bene in Jupyter
    display(df_finale)

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib

# Backend per integrare Matplotlib in Tkinter
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter + Matplotlib: Sinusoide interattiva")
        self.geometry("900x520")

        # --- Stato (valori iniziali) ---
        self.amp_init = 1.0
        self.freq_init = 1.0

        self.amp = tk.DoubleVar(value=self.amp_init)
        self.freq = tk.DoubleVar(value=self.freq_init)
        self.show_cos = tk.BooleanVar(value=False)

        # Dati X fissi
        self.x = np.linspace(0, 2*np.pi, 500)

        # --- Layout: pannello controlli a sinistra, grafico a destra ---
        self.controls = ttk.Frame(self, padding=10)
        self.controls.pack(side=tk.LEFT, fill=tk.Y)

        self.plot_frame = ttk.Frame(self, padding=10)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._build_controls()
        self._build_plot()
        self.update_plot()

    def _build_controls(self):
        ttk.Label(self.controls, text="Controlli", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 10))

        # Slider Ampiezza
        ttk.Label(self.controls, text="Ampiezza").pack(anchor="w")
        amp_scale = ttk.Scale(self.controls, from_=0.1, to=5.0, variable=self.amp, command=lambda _: self.update_plot())
        amp_scale.pack(fill=tk.X, pady=(0, 10))

        # Slider Frequenza
        ttk.Label(self.controls, text="Frequenza").pack(anchor="w")
        freq_scale = ttk.Scale(self.controls, from_=0.1, to=5.0, variable=self.freq, command=lambda _: self.update_plot())
        freq_scale.pack(fill=tk.X, pady=(0, 10))

        # Checkbox Coseno
        cos_check = ttk.Checkbutton(
            self.controls,
            text="Mostra coseno",
            variable=self.show_cos,
            command=self.update_plot
        )
        cos_check.pack(anchor="w", pady=(0, 10))

        # Pulsanti
        btn_frame = ttk.Frame(self.controls)
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        ttk.Button(btn_frame, text="Salva PNG", command=self.save_png).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # Stato/Info
        self.info = ttk.Label(self.controls, text="", wraplength=240)
        self.info.pack(anchor="w", pady=(15, 0))

    def _build_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6.5, 4))
        self.ax.set_title("Sinusoide")
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        # Linee (create una volta)
        (self.line_sin,) = self.ax.plot([], [], label="sin")
        (self.line_cos,) = self.ax.plot([], [], label="cos")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_plot(self):
        amp = float(self.amp.get())
        freq = float(self.freq.get())
        y_sin = amp * np.sin(freq * self.x)

        self.line_sin.set_data(self.x, y_sin)

        if self.show_cos.get():
            y_cos = amp * np.cos(freq * self.x)
            self.line_cos.set_data(self.x, y_cos)
            self.line_cos.set_visible(True)
        else:
            self.line_cos.set_visible(False)

        # Limiti asse dinamici (semplici e robusti)
        ymax = max(1.0, amp) * 1.2
        self.ax.set_xlim(self.x.min(), self.x.max())
        self.ax.set_ylim(-ymax, ymax)

        # Legenda dinamica: si aggiorna in base a cosa è visibile
        self.ax.legend(loc="upper right")

        self.info.config(text=f"Ampiezza: {amp:.2f} | Frequenza: {freq:.2f} | Coseno: {self.show_cos.get()}")

        self.canvas.draw_idle()

    def reset(self):
        self.amp.set(self.amp_init)
        self.freq.set(self.freq_init)
        self.show_cos.set(False)
        self.update_plot()

    def save_png(self):
        # Salva nella cartella da cui lanci lo script
        filename = "grafico_tkinter.png"
        self.fig.savefig(filename, dpi=200)
        self.info.config(text=f"Salvato: {filename}")

if __name__ == "__main__":
    app = App()
    app.mainloop()




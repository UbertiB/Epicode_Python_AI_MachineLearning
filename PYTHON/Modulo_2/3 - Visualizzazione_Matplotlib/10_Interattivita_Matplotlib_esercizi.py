"""
ESERCIZIO 1
* Slider multipli: crea un grafico di una funzione sinusoidale con ampiezza e frequenza controllate 
da due slider. Aggiungi una checkbox per mostrare/nascondere una curva coseno
ESERCIZIO 2
* Pulsanti con reset e salvataggio: aggiunti un pulsante per resettare il grafico e uno per salvare l'immagine in PNG
ESERCIZIO 3
* Dashboard in Jupyter: usa ipywidgets per creare un piccolo dashboard con due slider e un dropdown per selezionare dataset
diversi (simulati con numpy). Il grafico deve aggiornarsi in tempo reale.
ESERCIZIO 4
*GUI Tkinter: costruisci un'interfacia con slider, checkbox e pulsanti, che permette di modificare e salvare grafici di dataset
sintetici. Inserisci anche una legenda dinamica che si aggiorna in base alla selezione dei chekbox
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.widgets import Button

#
# ESERCIZIO 1  (SLIDER MULTIPLI)
#

#* Slider multipli: crea un grafico di una funzione sinusoidale con ampiezza e frequenza controllate 
#da due slider. Aggiungi una checkbox per mostrare/nascondere una curva coseno
if False:

    x = np.linspace(0, 10, 500)
    y = np.sin(x)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    line, = ax.plot(x, y)

    ax_amp = plt.axes([0.25, 0.1, 0.65, 0.03])
    ax_freq = plt.axes([0.25, 0.05, 0.65, 0.03])
    slider_amp = Slider(ax_amp, 'Ampiezza', 0.1, 5.0, valinit=1)
    slider_freq = Slider(ax_freq, 'Frequenza', 0.1, 5.0, valinit=1)

    def update_amp(val):
        amp = slider_amp.val
        line.set_ydata(amp * np.sin(x))
        fig.canvas.draw_idle()

    def update_freq(val):
        freq = slider_freq.val
        line.set_ydata(freq * np.sin(x))
        fig.canvas.draw_idle()        

    slider_amp.on_changed(update_amp)
    slider_freq.on_changed(update_freq)

    plt.show()


#
# ESERCIZIO 2  BUTTON  (due pulsante reset e salvataggio)
#

#* Pulsanti con reset e salvataggio: aggiunti un pulsante per resettare il grafico e uno per salvare l'immagine in PNG
if False:

    x = np.linspace(0, 10, 500)
    y = np.sin(x)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)
    line, = ax.plot(x, y)

    ax_amp = plt.axes([0.25, 0.1, 0.65, 0.03])
    slider_amp = Slider(ax_amp, 'Ampiezza', 0.1, 5.0, valinit=1)

    ax_button1 = plt.axes([0.65, 0.01, 0.25, 0.08])
    btn1 = Button(ax_button1, "Reset")
    ax_button2 = plt.axes([0.10, 0.01, 0.25, 0.08])
    btn2 = Button(ax_button2, "Salvataggio")    


    def update(val):
        amp = slider_amp.val
        line.set_ydata(amp * np.sin(x))
        fig.canvas.draw_idle()
    def reset(event):
        slider_amp.reset()
    def save(event):
        fig.savefig('10_Matplotlib_save.png')
   

    slider_amp.on_changed(update)
    btn1.on_clicked(reset)
    btn1.on_clicked(save)

    plt.show()


#
#ESERCIZIO 4  GUI TKINTER
#

#*GUI Tkinter: costruisci un'interfacia con slider, checkbox e pulsanti, che permette di modificare e salvare grafici di dataset
#sintetici. Inserisci anche una legenda dinamica che si aggiorna in base alla selezione dei chekbox

if True:
    
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    t = np.linspace(0, 2*np.pi, 1000)

    def make_sin(A, f): return A * np.sin(f * t)
    def make_cos(A, f): return A * np.cos(f * t)
    def make_noise(A, f):
        rng = np.random.default_rng(123)
        return A * (rng.normal(scale=0.5, size=t.shape) + 0.2*np.sin(f*t))

    class PlotApp:
        def __init__(self, root):
            self.root = root
            root.title("Plotter Tkinter")
            # frame controllo
            ctrl = ttk.Frame(root)
            ctrl.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

            #LABEL
            ttk.Label(ctrl, text='Ampiezza').grid(row=0, column=0, sticky='w')
            self.amp_var = tk.DoubleVar(value=1.0)
            amp_scale = ttk.Scale(ctrl, from_=0.0, to=2.0, orient='horizontal', variable=self.amp_var, command=lambda _: self.update_plot())
            amp_scale.grid(row=0, column=1, sticky='ew', padx=5)

            ttk.Label(ctrl, text='Frequenza').grid(row=1, column=0, sticky='w')
            self.freq_var = tk.DoubleVar(value=1.0)
            freq_scale = ttk.Scale(ctrl, from_=0.1, to=5.0, orient='horizontal', variable=self.freq_var, command=lambda _: self.update_plot())
            freq_scale.grid(row=1, column=1, sticky='ew', padx=5)

            #CHECKBOX per dataset
            boxframe = ttk.Frame(ctrl)
            boxframe.grid(row=0, column=2, rowspan=2, padx=10)
            self.show_sin = tk.IntVar(value=1)
            self.show_cos = tk.IntVar(value=0)
            self.show_noise = tk.IntVar(value=0)
            ttk.Checkbutton(boxframe, text='Sin', variable=self.show_sin, command=self.update_plot).pack(anchor='w')
            ttk.Checkbutton(boxframe, text='Cos', variable=self.show_cos, command=self.update_plot).pack(anchor='w')
            ttk.Checkbutton(boxframe, text='Noise', variable=self.show_noise, command=self.update_plot).pack(anchor='w')

            #BUTTON 
            btnframe = ttk.Frame(ctrl)
            btnframe.grid(row=0, column=3, rowspan=2, padx=5)
            ttk.Button(btnframe, text='Reset', command=self.reset).pack(fill='x', pady=2)
            ttk.Button(btnframe, text='Salva PNG', command=self.save_png).pack(fill='x', pady=2)
            ttk.Button(btnframe, text='Esci', command=root.quit).pack(fill='x', pady=2)

            #FIGURA MATPLOTLIB
            self.fig = Figure(figsize=(7,3))
            self.ax = self.fig.add_subplot(111)
            self.canvas = FigureCanvasTkAgg(self.fig, master=root)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

            self.lines = {}
            self.update_plot()

        def update_plot(self):
            A = self.amp_var.get()
            f = self.freq_var.get()
            self.ax.clear()
            legend_items = []
            if self.show_sin.get():
                y = make_sin(A, f)
                l1, = self.ax.plot(t, y, label='sin')
                self.lines['sin'] = l1
                legend_items.append(l1)
            if self.show_cos.get():
                y = make_cos(A, f)
                l2, = self.ax.plot(t, y, label='cos')
                self.lines['cos'] = l2
                legend_items.append(l2)
            if self.show_noise.get():
                y = make_noise(A, f)
                l3, = self.ax.plot(t, y, label='noise')
                self.lines['noise'] = l3
                legend_items.append(l3)

            if legend_items:
                self.ax.legend()
            self.ax.set_ylim(-2.5, 2.5)
            self.ax.set_xlabel('t')
            self.ax.set_title('Dataset sintetici — legenda dinamica')
            self.canvas.draw_idle()

        def reset(self):
            self.amp_var.set(1.0)
            self.freq_var.set(1.0)
            self.show_sin.set(1)
            self.show_cos.set(0)
            self.show_noise.set(0)
            self.update_plot()

        def save_png(self):
            fpath = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG file','*.png')], title='Salva grafico come...')
            if fpath:
                self.fig.savefig(fpath, dpi=150, bbox_inches='tight')
                messagebox.showinfo("Salvataggio", f"Grafico salvato in:\n{fpath}")

    if __name__ == '__main__':
        root = tk.Tk()
        app = PlotApp(root)
        root.mainloop()
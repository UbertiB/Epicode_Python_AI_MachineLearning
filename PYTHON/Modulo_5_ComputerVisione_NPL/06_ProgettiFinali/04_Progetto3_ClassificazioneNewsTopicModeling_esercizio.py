"""
ESERCIZIO:
Implementa la logica di calcolo dei pesi delle clasi per un dataset news sbilanciato

1. Crea un dizionario dei conteggi: Politica:800, Tecnologia:150, Cultura:50
2. Calcola i pesi inversamente proporzionali alla frequenza usando scikit-learn o manualmente
3. Simula la creazoine di un layer finale in Keras per 3 classi e commenta come passeresti questi pesi durante il model.fit()

Suggerimento: usa il parametro 'class_weight' per equilibrare l'impatto delle classi rare sulla funzione di perdita.

"""

"""
FILE: news_weight_balancer.py
DESCRIZIONE: Calcolo pesi delle classi e integrazione in pipeline Keras 3.
BACKEND: PyTorch
"""

import os
import numpy as np

# Configurazione Backend Keras 3
os.environ["KERAS_BACKEND"] = "torch"

import keras
from keras import layers
from sklearn.utils.class_weight import compute_class_weight

def solve_imbalance():
    # --- 1. CREAZIONE CONTEGGI (Dataset Sbilanciato) ---
    # Politica è la classe dominante (maggioritaria)
    # Cultura è la classe rara (minoritaria)
    counts = {'Politica': 800, 'Tecnologia': 150, 'Cultura': 50}
    
    # Prepariamo i dati per il calcolo
    class_labels = np.array(list(counts.keys()))
    # Creiamo una lista piatta di label per simulare il dataset reale y_train
    y_simulated = np.array(['Politica']*800 + ['Tecnologia']*150 + ['Cultura']*50)

    # --- 2. CALCOLO PESI INVERSAMENTE PROPORZIONALI ---
    # Utilizziamo scikit-learn per calcolare i pesi secondo la formula:
    # peso = n_campioni / (n_classi * n_campioni_classe_i)
    weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_simulated),
        y=y_simulated
    )
    
    # Creiamo il dizionario finale mappato sugli INDICI delle classi (0, 1, 2)
    # Fondamentale per Keras: il dizionario deve avere chiavi intere
    class_weight_dict = {i: weight for i, weight in enumerate(weights)}
    
    print("--- Analisi Pesi delle Classi ---")
    for idx, label in enumerate(class_labels):
        print(f"Classe {idx} ({label}): Peso {class_weight_dict[idx]:.2f}")

    # --- 3. LAYER FINALE KERAS ---
    # Simuliamo un'architettura funzionale per 3 classi
    # Supponiamo che l'input provenga da un backbone BERT (vettore da 128)
    inputs = layers.Input(shape=(128,))
    x = layers.Dense(64, activation="relu")(inputs)
    
    # LAYER FINALE: 3 neuroni (uno per classe) con Softmax
    # La Softmax normalizza i logit in probabilità [0, 1] la cui somma è 1
    outputs = layers.Dense(3, activation="softmax", name="news_classifier")(x)
    
    model = keras.Model(inputs=inputs, outputs=outputs)
    
    # Compilazione standard
    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )
    
    return model, class_weight_dict

# --- SPIEGAZIONE PER IL DEPLOYMENT ---
"""
Per passare i pesi durante l'addestramento, utilizziamo il parametro 
'class_weight' nel metodo .fit(). 

Esempio:
model.fit(
    x_train, 
    y_train, 
    epochs=10, 
    class_weight=class_weight_dict  # <--- Integrazione qui
)

COSA SUCCEDE SOTTO IL COFANO:
Durante il calcolo della Loss (Cross-Entropy), l'errore commesso su un campione 
di 'Cultura' verrà moltiplicato per il suo peso (circa 6.67). 
L'errore sulla 'Politica' peserà solo 0.42. 
Questo forza i gradienti di PyTorch ad aggiornare i pesi del modello con molta 
più decisione quando sbaglia le classi rare.
"""

if __name__ == "__main__":
    model, weights = solve_imbalance()
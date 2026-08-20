#!/usr/bin/env python
# coding: utf-8

# PROGETTO 3: CLASSIFICAZIONE AUTOMATICA DI NEWS E TOPIC MODELING
# 
# Classificazione automatica: conosco già le categorie
# Topic Modeling: non conosco necessariamente i temi e voglio farli emergere dai documenti.
# 
# Come passare da un testo grezzo ad un categorizzazione automatica.
# 
# Immagina 50.000 articoli di giornale, se dici a priori: politica, sport, economia, tecnologia, spettacolo, e vuoi che il modello assegni ogni articolo a una di queste categorie, stai facendo Classificazione supervisonata.
# Se invece dici: Ho 50.000 articoli, dimmi quali grandi argomenti trattano da soli, stai facendo Topic Modelling, normalmente non supervisionato.
# 
# Per la classificazione automatica la pipeline tipica è:
# articolo -> preprocessing -> rappresentazione numerica -> classificatore -> categoria
# Come sempre, il modello non può lavorare direttamente sulle parole, deve prima rappresentarle numericamente.
# Con NLP classico potresti avere:
# testo -> TF-IDF -> vettore numerico -> Logistic Regression / SVM / Naive Bayes -> Categoria
# Con il Deep Learning potresti avere:
# testo -> tokenizzazione -> embedding -> LSTM/CNN -> Dense -> Categoria
# Con un Transformer potresti avere:
# testo -> tokenizzazione -> BERT -> rappresentazione contestuale -> classificazione head -> Categoria
# 
# La differenza quindi non è tanto l'obbiettivo finale, che resta documento -> categoria
# ma il modo in cui il testo viene rappresentato e interpretato
# 
# Per addestrare un classificatore supervisionato servono esempi già etichettati
# durante il training il modello confronta la predizione con la categoria reale, calcola la loss e con la backpropagation aggiorna i pesi.
# Poi in inference arriva una notizia nuova e il modello produce un vettore di probabilità per ogni categoria (che in questo caso sono già previste a priori)
# 
# Il Top Modelling invece fa qualcosa di molto diverso
# Supponiamo di avere i nostri 50.000 artiocli senza etichette, il sistema cerca strutture ricorrenti nel linguaggio e potrebbe scoprire gruppi simili a:
# categoria 1: governo, parlamento, ministro, elezioni, legge
# categoria 2: partita, squadra, gol, campionato, allenatore
# categoria 3: borsa, inflazione, banca, tassi, economia
# categoria 4: software, intelligenza artificiale, chip, cloud
# Poi siamo noi umani ad interpretare le categorie in: 
# categoria 1 = politia, 
# categoria 2 = sport, 
# categoria 3 = economia, 
# categoria 4 = tecnologia
# 
# Quindi il Topic Modelling scopre strutture tematiche, ma non necessariamente restituisce direttamente una bella etichetta umana come "sport"
# 
# L'Architettura
# Dall'Input testuale alla categoria tematica.
# per classificare le news non possiamo limitarci a cercare le parole chiave, se un articolo parla di tiri in porta è sport, ma se parla di tiri della banca centrale è economia.
# Abbiamo bisogno di modelli capaci di catturare il contesto globale del testo. I Transformer permettono di mappare ogni notizia su un set predefinito di categorie, generando una distribuzione di probabilità su k classi distinte.
# Prendiamo l'articolo, lo passiamo attraverso BERT, e chiediamo al modello di classificare su un set di etichette fisse.
# E' come insegnare ad una macchina a leggere un intero sommario per decidere in quale sezione del giornale impaginare la notizia
# 
# Per trasformare BERT in un classificatore di news ci servono 4 componenti
# 1) Feature Extraction: utilizzo degli hidden states del token CLS di BERT per ottenere una rappresentazione densa dell'intero articolo. Invece di guardare ogni singola parola, ci concentriamo sul token CLS che agisce come un riassunto semantico di tutto l'articolo
# 2) Output Layer:  un layer lineare finale con un numero di neuroni  pari al numero di categorie nel dataset di news. 
# 3) Softmasx Activation: funzione fondamentale per interpretare i logit in uscita come probabilità normalizzate tra 0 e 1
# 4) Cross-Entropy Loss: funzione obbiettivo che misura la discerpanza tra la categoria predetta e quella reale assegnata dal giornalista.
# 
# Ma il testo giornalistico ha delle trappole nascoste.
# - Lunghezza del Contesto: Lunghezza del testo, BERT ha un limite di 512 token, se l'articolo è più lungo dobbiamo decidere cosa tagliare, solitamente il cuore della notizia è nel titolo
# - Entità Nominate: mantenere le maiuscole (cased models) per distinguere i nomi propri di politici o aziende che definiscono il topic. Esempio Apple (maiuscolo) è un'azienda tech, mentre apple (minuscolo) è unfrutto
# - Overlapping Topics: strategie per gestire notizie che appartengono a più categorie, come un articolo su una IPO tecnologica (Economia e Tech)
# 
# La sfida è addestrare il modello a distinguere queste sfumature.
# 
# Matematia che normalizza queste decisioni
# La funzione softmaz è la chiave per la interpretabilità
# Vogliamo sapere quanto sia sicuro il modello della sua scelt.a
# 
# Ma cosa succede se il nostro dataset è pieno di politica e poco di cultura?
# 
# Gestione del Dataset Sbilanciato
# Il probelma delle classi dominanti
# Nelle news, alcune categorie sono naturalmente più frequenti di altre. Un modello ingenuo tenderà a predire sempre la classe maggioritaria per minimizzare l'errore globale (imparando la scorciatoia).
# Possiamo forzare la rete a prestare attenzione alle classi rare (es. cronaca locale o cultura) tramite tecniche di pesatura mirata.
# 
# Ma quali manovre possiamo fare per equilibrare le classi?
# 
# Esistono diverse strategie:
# - Class Weights: assegnare un peso maggiore alla loss delle classi minoritarie durante il calcolo del gradiente
# - Random Over-sampling: duplicare campioni delle classi meno frequenti per bilanciare il batch di addestramento
# - Under-sampling: ridurre il numero di campioni delle classi dominanti per evitare il bias del modello
# - Focal Loss: variante della cross-entropy che penalizza maggiormente gli errori sulle istasnze difficili e rare. Come un insegnante che ignora le domande facili che lo studente giù conosce e si concentra sui casi più difficili.
# 
# Metriche Oltre l'Accuratezza
# Matrice di Confusione: per visualizzare degli errori di scambio tra classi simili (es. scambiare sport con la salute per articoli sulla medicina sportiva)
# F1-Score Macro e Weighted: utilizzo di medie che pesano correttamente l'impatto di ogni categoria indipendentemente dal numero di articoli. Da lo stesso peso ad ogni categoria indipendentemente da quanti articoli contiene.
# Precision-Recall Curve: analisi del compromesso tra la capacità di trovare tutti gli articoli di una nicchia e la precisone nel farlo.
# 
# Loss Functor Pesata
# Integrare i Class Weights
# Modifichiamo la Cross-Entropy standard moltiplicando il contributo di ogni classe per un peso w, inversamente proporzionale alla sua frequenza nel dataset.
# In questo modo, un errore sulla classe minoritario "cultura" pesarà di più di un errore sulla classe maggioritaria "politica"
# 
# Se un modello è addestrato equo dobbiamo renderlo visibile
# 
# Dashboard di Visualizzazione
# Monitorare i flussi di informazione
# Un progetto di news classification termina con la creazione di un'interfaccia che permetta agli editori di vedere quali topic stanno emergendo nel tempo.
# Utilizzando strumenti di data visualization rappresentiamo graficamente la distribuzione delle notizie e l'incertezza del modello.
# Un ingeniere ai sa che deve comunicare i dati in modo pulito, per un editore vedere una lista di files json non serve a nulla, dobbiamo creare un interfacci che mostri i dati in tempo reale, mostrando cosa il modello ha capito e dove sta esitando.
# 
# Quali sono i widget indispensabili per questo progetto
# 
# Una dashboard professionale deve avere 4 componenti visivi:
# - Topic Distribution: grafici a torta o a barre che mostrano il volume di articoli per ogni categoria predetta.
# - Confidence Heatmap: analisi di quanto il modello sia sicuro delle sue scelte per indivisuare notizie ambigue. Fondamentale per la manutenzione
# - Time-series Trends: monitoraggio dell'evoluzione di un topic specifico (es. picchi di notizie su 'elezioni' o 'pandemia')
# - Word Clouds per Topic: estrazione delle parole chiave più influenti che hanno portato il modello a scegliere una determinata classe. Ci danno una validazione visiva
# 
# Ma come integriamo questo software nel flusso di lavoro reale
# 
# Integrazione e Deployment
# Utilizzermo Streamlit per NLP, creazione rapida di web app in Python per testare il modello caricando un URL di un articolo o incollando il testo
# Human-in-the-loop permette ai giornalisti di correggere le etichette errate nella dashboard per rifinire il modello in futuro.
# 
# Valutazione dell'analisi
# F1-Score ci fornisce un bilancio armonioso che vedremo sulla nostra dashboard
# ma questo è da calcolare per ogni singolo topic 
# Se f1score resta alto su tutti i topic abbiamo vinto.

# In[ ]:


"""
================================================================================
DASHBOARD DI CLASSIFICAZIONE NEWS CON ARCHITETTURA IBRIDA (PYTORCH + KERAS 3)
================================================================================

Questo script implementa una pipeline completa di Intelligenza Artificiale:
1.  CONFIGURAZIONE: Imposta Keras 3 per usare PyTorch come motore di calcolo (Backend).
2.  INTEGRAZIONE: Utilizza un modello Transformer (DistilBERT) di Hugging Face come "Feature Extractor".
3.  ARCHITETTURA: Costruisce un modello Keras "Functional" che include una classe PyTorch personalizzata.
4.  ADDESTRAMENTO: Gestisce lo sbilanciamento dei dati tramite pesi delle classi (Class Weights).
5.  INTERFACCIA: Crea una dashboard interattiva con Streamlit per visualizzare metriche e fare inferenza.

Interazione chiave: Keras gestisce la struttura della rete e il training, mentre PyTorch 
esegue i calcoli pesanti del modello Transformer.
"""

import os

# --- 1. CONFIGURAZIONE BACKEND (Il "Motore") ---
# Comunichiamo a Keras di non usare TensorFlow (default) ma PyTorch.
# Questa riga deve essere eseguita PRIMA di importare keras.
os.environ["KERAS_BACKEND"] = "torch"

import torch
import numpy as np
import keras
from keras import layers
from transformers import AutoTokenizer, AutoModel
from sklearn.utils import class_weight
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# --- CONFIGURAZIONE PAGINA STREAMLIT ---
# Imposta il titolo della tab del browser e usa tutta la larghezza dello schermo.
st.set_page_config(page_title="News AI Dashboard", layout="wide")

# --- 2. LOGICA DEL MODELLO E DEI DATI ---

@st.cache_resource # Evita di ricaricare tutto ogni volta che l'utente interagisce con la UI
def load_and_train_model():
    """
    Gestisce l'intera pipeline: Caricamento -> Preprocessing -> Creazione Modello -> Training.
    """
    from datasets import load_dataset

    # --- CARICAMENTO DATI ---
    # Prendiamo un piccolo campione (1000 esempi) del dataset AG News (notizie classificate)
    ds = load_dataset("wangrongsheng/ag_news", split="train[:1000]")
    texts, labels = ds["text"], ds["label"]
    names = ["Mondo", "Sport", "Business", "Sci/Tech"]

    # --- SIMULAZIONE SBILANCIAMENTO (Scenario Reale) ---
    # Riduciamo drasticamente gli esempi della categoria "Sci/Tech" (solo 15)
    # per testare come il modello gestisce classi rare.
    t_final, l_final, count_tech = [], [], 0
    for t, l in zip(texts, labels):
        if l == 3: # 3 = Sci/Tech
            if count_tech < 15:
                t_final.append(t); l_final.append(l); count_tech += 1
        else:
            t_final.append(t); l_final.append(l)

    y_true = np.array(l_final)

    # --- TOKENIZER (Traduttore Testo -> Numeri) ---
    # Carichiamo il tokenizer di DistilBERT che trasforma le parole in ID numerici leggibili dalla rete.
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    # --- CLASSE CUSTOM: IL PONTE FRA KERAS E PYTORCH ---
    class SimpleTransformer(layers.Layer):
        """
        Questa classe permette a Keras di "ospitare" un modello PyTorch puro (Hugging Face).
        """
        def __init__(self, model_name, **kwargs):
            super().__init__(**kwargs)
            # 1. Carichiamo l'encoder PyTorch originale
            self.encoder = AutoModel.from_pretrained(model_name)

            # 2. CONGELAMENTO (Freeze): Diciamo a PyTorch di NON calcolare i gradienti qui.
            # Non vogliamo ri-addestrare BERT (molto pesante), vogliamo solo usarlo così com'è.
            self.encoder.requires_grad_(False)

            # 3. Diciamo a Keras che questo layer non deve essere modificato durante il training.
            self.trainable = False

        def call(self, inputs):
            """
            Il passaggio dei dati: 
            Keras passa i token -> PyTorch li elabora -> Restituiamo il vettore CLS (il riassunto del testo).
            """
            # inputs[0] sono i token ID, inputs[1] è la maschera di attenzione
            outputs = self.encoder(input_ids=inputs[0], attention_mask=inputs[1])

            # Estraiamo l'embedding del token [CLS] (indice 0).
            # È un vettore che rappresenta il significato semantico dell'intera frase.
            return outputs.last_hidden_state[:, 0, :]

    # --- ARCHITETTURA DEL MODELLO (API FUNZIONALE) ---
    # Definiamo i due ingressi necessari per i Transformer
    idx = layers.Input(shape=(128,), dtype="int32", name="input_ids")
    mask = layers.Input(shape=(128,), dtype="int32", name="attention_mask")

    # Applichiamo il nostro layer custom (Feature Extractor)
    embeddings = SimpleTransformer("distilbert-base-uncased")([idx, mask])

    # Aggiungiamo un "Capo" (Classifier Head) semplice:
    # Uno strato denso con 64 neuroni e l'uscita finale per le 4 classi (Softmax).
    x = layers.Dense(64, activation="relu")(embeddings)
    preds = layers.Dense(len(names), activation="softmax")(x)

    # Assembliamo il modello finale
    model = keras.Model(inputs=[idx, mask], outputs=preds)

    # Configurazione del training: Optimizer Adam e Loss per classificazione multi-classe
    model.compile(
        optimizer="adam", 
        loss="sparse_categorical_crossentropy", 
        metrics=["accuracy"]
    )

    # --- GESTIONE SBILANCIAMENTO ---
    # Calcoliamo dei pesi: le classi con pochi esempi (Sci/Tech) peseranno di più 
    # durante il calcolo dell'errore, costringendo il modello a impararle meglio.
    cw = class_weight.compute_class_weight('balanced', classes=np.unique(y_true), y=y_true)
    cw_dict = dict(enumerate(cw))

    # --- PREPARAZIONE DATI DI TRAINING ---
    # Trasformiamo i testi in tensori PyTorch pronti per il modello
    t_input = tokenizer(
        t_final, 
        padding="max_length", 
        truncation=True, 
        max_length=128, 
        return_tensors="pt"
    )

    # --- ADDESTRAMENTO ---
    # Nota: Anche se il backend è PyTorch, usiamo il comodissimo .fit() di Keras.
    model.fit(
        [t_input["input_ids"], t_input["attention_mask"]], 
        y_true, 
        epochs=1, 
        batch_size=32, 
        class_weight=cw_dict, 
        verbose=0 # Silenzioso perché Streamlit gestisce l'output
    )

    return model, tokenizer, names, y_true, t_input

# --- 3. ESECUZIONE E INTERFACCIA UTENTE ---

# Mostriamo un caricamento all'avvio
with st.spinner("Inizializzazione Intelligenza Artificiale (Caricamento Modelli PyTorch)..."):
    model, tokenizer, categories, y_true, t_input = load_and_train_model()

# Header principale
st.title("News Classification AI Dashboard")
st.markdown("""
Questa dashboard mostra la capacità di un'intelligenza artificiale di categorizzare notizie.
Il sistema utilizza un'architettura **Ibrida**:
- **Encoder:** DistilBERT (PyTorch) per comprendere il testo.
- **Classificatore:** Rete Densa (Keras 3) per decidere la categoria.
""")

# Layout a due colonne per i grafici
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Analisi Accuratezza")
    # Otteniamo le predizioni del modello su tutto il mini-dataset
    preds_prob = model.predict([t_input["input_ids"], t_input["attention_mask"]], verbose=0)
    y_pred = np.argmax(preds_prob, axis=1) # Scegliamo la classe con probabilità più alta

    # Creazione della Matrice di Confusione (dove il modello sbaglia?)
    fig, ax = plt.subplots(figsize=(6, 5))
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=categories, yticklabels=categories, cmap="Blues", ax=ax)
    ax.set_title("Matrice di Confusione")
    st.pyplot(fig)

with col2:
    st.subheader("Distribuzione Topic")
    # Conteggio di quante notizie sono state assegnate a ogni categoria
    unique, counts = np.unique(y_pred, return_counts=True)
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    ax2.pie(counts, labels=[categories[i] for i in unique], autopct='%1.1f%%', 
            startangle=140, colors=sns.color_palette("viridis"))
    st.pyplot(fig2)

# --- FASE 4: TEST INTERATTIVO (Inference) ---
st.divider()
st.subheader("Prova il Modello in Tempo Reale")
user_text = st.text_area("Incolla qui il testo di una notizia (inglese consigliato):", 
                         placeholder="Example: The local football team won the match in the final minutes...")

if user_text:
    # 1. TRASFORMAZIONE: Prepariamo il testo dell'utente come fatto nel training
    inputs = tokenizer(user_text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")

    # 2. INFERENZA: Chiediamo al modello di classificare
    prob = model.predict([inputs["input_ids"], inputs["attention_mask"]], verbose=0)[0]
    best_class_idx = np.argmax(prob)
    confidenza = prob[best_class_idx] * 100

    # 3. VISUALIZZAZIONE RISULTATI
    st.success(f"### Categoria Suggerita: **{categories[best_class_idx]}**")
    st.progress(confidenza / 100)
    st.write(f"**Livello di confidenza:** {confidenza:.2f}%")

    # Messaggio di cautela se la confidenza è bassa (Human-in-the-loop)
    if confidenza < 60:
        st.warning("**Confidenza Bassa:** Il sistema è incerto. Si suggerisce la validazione da parte di un giornalista umano.")

# Barra laterale con dettagli tecnici
st.sidebar.title("Info Sistema")
st.sidebar.info(f"""
- **Backend:** PyTorch {torch.__version__}
- **Framework:** Keras {keras.__version__}
- **Modello Base:** DistilBERT
- **Stato:** Operativo
""")


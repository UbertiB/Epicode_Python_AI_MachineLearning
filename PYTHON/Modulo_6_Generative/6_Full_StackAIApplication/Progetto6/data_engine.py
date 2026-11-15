"""
FASE 1 - DATA ENGINE

Prepara il dataset tabellare per il VAE e lo riporta ai valori originali dopo la generazione.
- Pulizia: righe duplicate, colonne vuote, zeri che in realtà sono valori mancanti
- Gestione dei valori nulli: mediana per le numeriche, moda per le categoriche
- Numeriche: MinMaxScaler (valori tra 0 e 1)
- Categoriche: One-Hot Encoding (una colonna 0/1 per ogni categoria)
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# -----------------------------------------------------------------------------
# 1. CONFIGURAZIONE
# -----------------------------------------------------------------------------
# Una colonna con pochi valori distinti (es. Outcome 0/1) la tratto come categorica,
# anche se contiene numeri.
MAX_VALORI_CATEGORICI = 10

# ZERO_COME_NULLO colonne il cui valore zero sta a indicare null
# Esempio nel dataset Pima Indians Diabetes lo zero nelle colonne glucose, boodpressure, ecc
# sta ad indicare un dato mancante:
# Se il dataset caricato non ha queste colonne, la regola viene ignorata.
ZERO_COME_NULLO = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]

# -----------------------------------------------------------------------------
# 2. CLASSE DATA ENGINE
# -----------------------------------------------------------------------------
class DataEngine:
    """
    Impara dal dataset reale come trasformarlo (fit) e poi applica la stessa trasformazione
    in avanti (transform) e all'indietro (inverse_transform).
    Il VAE lavora solo con la matrice numerica tra 0 e 1, mai con il DataFrame originale.
    """

    def __init__(self, max_valori_categorici: int = MAX_VALORI_CATEGORICI):
        self.max_valori_categorici = max_valori_categorici
        self.scaler = MinMaxScaler()  #scaler creato ma non addestrato (non conosce ancora nulla)
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")  #encoder creato ma non addestrato (non conosce ancora nulla)
        self.colonne = []             # ordine originale delle colonne
        self.col_numeriche = []
        self.col_categoriche = []
        self.col_intere = []          # numeriche da riportare a numeri interi (es. età)
        self.tipi_categorici = {}     # tipo originale delle categoriche (per ripristinarlo)
        self.mappe_categorie = {}     # testo usato dall'encoder -> valore originale (es. "False" -> False)
        self.valori_imputazione = {}  # mediana o moda usata per riempire i nulli
        self.riepilogo = {}           # informazioni da mostrare nella UI

    def _pulisci(self, df: pd.DataFrame) -> pd.DataFrame:
        """Rimuove colonne vuote e duplicati, converte gli zeri anomali in nulli."""
        df = df.dropna(axis=1, how="all").drop_duplicates().reset_index(drop=True)
        for col in ZERO_COME_NULLO:
            if col in df.columns:
                df[col] = df[col].replace(0, np.nan)
        return df

    def fit(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analizza il dataset reale, prepara scaler ed encoder.

        Returns:
            Il DataFrame pulito e senza nulli
        """
        righe_iniziali = len(df)
        df = self._pulisci(df)
        self.colonne = list(df.columns)

        # Classificazione delle colonne: 
        # 1) Categorica: testo - booleani - numerici con pochi valori (max_valori_categorici).
        # 2) Numerici: tutte le colonne numeriche tranne le numercihe con pochi valori (diventate categoriche)
        for col in self.colonne:
            pochi_valori = df[col].nunique() <= self.max_valori_categorici
            non_numerica = not pd.api.types.is_numeric_dtype(df[col])
            if non_numerica or pd.api.types.is_bool_dtype(df[col]) or pochi_valori: #stringa booleana o pochi valori
                self.col_categoriche.append(col)
                self.tipi_categorici[col] = df[col].dtype
            else:
                #le colonne intere le tengo separate dalle altre colonne numeriche.
                #questo perchè quando genero dati sintetici, le colonne intere non devono avere decimali.
                #esempio, la colonna "n. gravidanze" non deve contenere numeri con virgola
                self.col_numeriche.append(col)
                valori = df[col].dropna()
                if (valori == valori.round()).all(): # confronto i valori con i valori arrotondati a 0 decimali
                    self.col_intere.append(col)

        # Gestione nulli: 
        # - mediana per numeriche (più robusta agli outlier rispetto alla media)
        # - moda per categoriche
        nulli = df.isna().sum()
        for col in self.col_numeriche:
            self.valori_imputazione[col] = df[col].median()
        for col in self.col_categoriche:
            self.valori_imputazione[col] = df[col].mode().iloc[0]
        df = df.fillna(self.valori_imputazione)

        # Dizionario di traduzione per ogni colonna
        for col in self.col_categoriche:
            self.mappe_categorie[col] = {str(v): v for v in df[col].unique()}

        #applico lo scaler
        if self.col_numeriche:
            self.scaler.fit(df[self.col_numeriche])
        #applico l'encoder
        if self.col_categoriche:
            self.encoder.fit(df[self.col_categoriche].astype(str))

        self.riepilogo = {
            "righe_iniziali": righe_iniziali,
            "righe_dopo_pulizia": len(df),
            "colonne_numeriche": self.col_numeriche,
            "colonne_categoriche": self.col_categoriche,
            "nulli_imputati": {c: int(n) for c, n in nulli.items() if n > 0},
            "dimensione_vettore_vae": self.n_feature,
        }
        return df

    @property
    def n_feature(self) -> int:
        """Lunghezza del vettore in ingresso al VAE (numeriche + colonne one-hot)."""
        n_onehot = sum(len(c) for c in self.encoder.categories_) if self.col_categoriche else 0
        return len(self.col_numeriche) + n_onehot

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Prende il df pulito e lo trasforma in una matrice di soli numeri tra 0 e 1
           Lo scaler e il onhot fatto in fit ha imparato come trasformarli. Con transform li trasformo
           Questo perchè il VAE ha bisogno di dati 'standarizzati' tra loro
           Poi ritorno ai valori originali con inverse_transform"""
        parti = []
        if self.col_numeriche:
            parti.append(self.scaler.transform(df[self.col_numeriche]))
        if self.col_categoriche:
            parti.append(self.encoder.transform(df[self.col_categoriche].astype(str)))
        return np.hstack(parti).astype("float32")

    def inverse_transform(self, X: np.ndarray) -> pd.DataFrame:
        """Matrice generata dal VAE -> DataFrame con le colonne e le unità originali."""
        out = pd.DataFrame(index=range(len(X)))
        n_num = len(self.col_numeriche)

        if self.col_numeriche:
            # clip: il decoder usa la Sigmoid, ma per sicurezza restiamo nell'intervallo visto in training
            valori = self.scaler.inverse_transform(np.clip(X[:, :n_num], 0, 1))
            out[self.col_numeriche] = valori
            for col in self.col_intere:
                out[col] = out[col].round().astype(int)
            for col in set(self.col_numeriche) - set(self.col_intere):
                out[col] = out[col].round(3)

        if self.col_categoriche:
            # Per ogni gruppo one-hot l'encoder sceglie la categoria con il valore più alto (argmax)
            categorie = self.encoder.inverse_transform(X[:, n_num:])
            for i, col in enumerate(self.col_categoriche):
                originali = pd.Series(categorie[:, i]).map(self.mappe_categorie[col])
                out[col] = originali.astype(self.tipi_categorici[col])

        return out[self.colonne]

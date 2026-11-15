"""
FASE 3 - VALIDAZIONE DEI DATI SINTETICI

Dimostra che i dati generati rispettano le proprietà dei dati reali senza copiarli:
- Statistiche: media, deviazione standard, minimo e massimo per colonna
- Correlazione: matrici reali e sintetiche e loro differenza media
- Privacy check: record identici e distanza dal record reale più vicino (DCR)
"""

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# Numero massimo di record su cui calcolare le distanze del privacy check
MAX_CAMPIONE_DCR = 5000


# -----------------------------------------------------------------------------
# 1. STATISTICHE E CORRELAZIONI
# -----------------------------------------------------------------------------
def confronta_statistiche(reale: pd.DataFrame, sintetico: pd.DataFrame) -> pd.DataFrame:
    """Tabella comparativa reale vs sintetico per ogni colonna numerica."""
    righe = []
    for col in reale.select_dtypes("number").columns:
        r, s = reale[col], sintetico[col]
        righe.append({
            "colonna": col,
            "media_reale": r.mean(), "media_sintetica": s.mean(),
            "std_reale": r.std(), "std_sintetica": s.std(),
            "min_reale": r.min(), "min_sintetico": s.min(),
            "max_reale": r.max(), "max_sintetico": s.max(),
            # scarto della media in % della deviazione standard reale:
            # più leggibile di un valore assoluto quando le scale sono diverse
            "scarto_media_su_std_%": abs(r.mean() - s.mean()) / r.std() * 100 if r.std() else 0.0,
        })
    return pd.DataFrame(righe).round(3)


def confronta_correlazioni(reale: pd.DataFrame, sintetico: pd.DataFrame) -> dict:
    """Matrici di correlazione e differenza media assoluta (0 = identiche)."""
    corr_r = reale.select_dtypes("number").corr().round(3)
    corr_s = sintetico[corr_r.columns].corr().round(3)
    differenza = float(np.nanmean(np.abs(corr_r.values - corr_s.values)))
    return {"reale": corr_r, "sintetica": corr_s, "differenza_media": round(differenza, 4)}


# -----------------------------------------------------------------------------
# 2. PRIVACY CHECK
# -----------------------------------------------------------------------------
def privacy_check(reale: pd.DataFrame, sintetico: pd.DataFrame,
                  X_reale: np.ndarray, X_sintetico: np.ndarray) -> dict:
    """
    1) Copie esatte: righe sintetiche identiche (su tutte le colonne) a una riga reale.
    2) DCR (Distance to Closest Record): distanza di ogni record sintetico dal reale più vicino,
       calcolata nello spazio scalato 0-1. Il riferimento è la distanza tra record reali vicini:
       se molti sintetici sono più vicini ai reali di quanto i reali lo siano tra loro,
       il modello sta memorizzando (overfitting) invece di generalizzare.
    """
    copie_esatte = len(sintetico.merge(reale.drop_duplicates(), how="inner"))

    # Su dataset grandi (es. Credit Card, 284.000 righe) confrontare tutti con tutti è troppo lento:
    # l'indice contiene TUTTI i reali, ma le distanze si calcolano su un campione casuale.
    rng = np.random.default_rng(0)
    def campione(X):
        return X[rng.choice(len(X), MAX_CAMPIONE_DCR, replace=False)] if len(X) > MAX_CAMPIONE_DCR else X

    nn_model = NearestNeighbors(n_neighbors=2).fit(X_reale)
    dcr_sintetici = nn_model.kneighbors(campione(X_sintetico), n_neighbors=1)[0][:, 0]
    # Per i reali prendiamo il secondo vicino: il primo è il record stesso (distanza 0)
    dcr_reali = nn_model.kneighbors(campione(X_reale))[0][:, 1]
    soglia = np.percentile(dcr_reali, 5)

    return {
        "copie_esatte": int(copie_esatte),
        "dcr_mediana_sintetici": round(float(np.median(dcr_sintetici)), 4),
        "dcr_mediana_reali": round(float(np.median(dcr_reali)), 4),
        "soglia_vicinanza": round(float(soglia), 4),
        "quota_sintetici_troppo_vicini_%": round(float((dcr_sintetici < soglia).mean() * 100), 2),
    }

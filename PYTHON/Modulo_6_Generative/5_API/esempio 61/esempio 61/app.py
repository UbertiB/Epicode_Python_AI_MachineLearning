import torch # Libreria principale per il Deep Learning, utilizzata per gestire i tensori e il modello neurale
import torch.nn as nn # Sottomodulo per la definizione degli strati della rete neurale
import joblib # Utilizzata per caricare oggetti Python serializzati, come lo scaler per la normalizzazione dei dati
from fastapi import FastAPI # Framework web moderno e veloce per la creazione di API in Python
from pydantic import BaseModel # Per definire schemi di dati con validazione automatica
from typing import List # Per specificare il tipo di dati nelle liste dello schema Pydantic

# 1. Definizione dell'Architettura della Rete Neurale
# Questa classe definisce la struttura della rete neurale che utilizzeremo per le previsioni.
# È fondamentale che sia IDENTICA a quella usata durante la fase di addestramento (training).
class IrisNet(nn.Module):
    def __init__(self, input_size=4, hidden_size=16, num_classes=3):
        # Inizializziamo la classe base nn.Module
        super(IrisNet, self).__init__()
        # Definiamo una sequenza di strati (layers) che compongono la rete
        self.network = nn.Sequential(
            # Primo strato lineare: accetta 4 caratteristiche in ingresso (misure del fiore) e produce 16 uscite
            nn.Linear(input_size, hidden_size),
            # Funzione di attivazione ReLU: introduce non-linearità nel modello (imposta a zero i valori negativi)
            nn.ReLU(),
            # Secondo strato lineare: prende le 16 uscite e produce 3 punteggi (uno per ogni classe di Iris)
            nn.Linear(hidden_size, num_classes)
        )
    
    def forward(self, x):
        # Definisce come i dati fluiscono attraverso la rete durante l'inferenza
        return self.network(x)

# 2. Inizializzazione dell'Applicazione FastAPI e Caricamento degli Asset
# Creiamo l'istanza principale dell'API che gestirà le richieste HTTP
app = FastAPI(title="Iris AI Service 2026")

# Carichiamo lo scaler precedentemente salvato per garantire che i nuovi dati 
# siano normalizzati nello stesso modo di quelli usati per l'addestramento
scaler = joblib.load("scaler.pkl")

# Creiamo un'istanza del modello IrisNet
model = IrisNet()
# Carichiamo i pesi (parametri) ottimizzati che la rete ha "imparato" durante il training
model.load_state_dict(torch.load("iris_model.pth", weights_only=True))
# Impostiamo il modello in modalità 'eval' (valutazione). 
# Questo è fondamentale perché disabilita moduli come il Dropout, ottimizzando la stabilità delle previsioni.
model.eval()

# 3. Definizione dello Schema dei Dati di Input
# Utilizziamo Pydantic per definire come deve essere fatta una richiesta POST al nostro endpoint.
# Questo garantisce che chi usa l'API invii i dati nel formato corretto.
class IrisInput(BaseModel):
    # Ci aspettiamo una lista di 4 numeri in virgola mobile (es: [5.1, 3.5, 1.4, 0.2])
    features: List[float]

# 4. Endpoint Principale per la Predizione
# Definiamo una rotta che accetta richieste POST all'indirizzo '/predict'
@app.post("/predict")
async def predict(data: IrisInput):
    # Passaggio A: Recuperiamo le caratteristiche grezze dall'input ricevuto
    raw_features = [data.features]
    
    # Passaggio B: Applichiamo lo scaler ai dati. 
    # Le reti neurali lavorano meglio se i dati sono normalizzati (es. tra 0 e 1).
    scaled_features = scaler.transform(raw_features)
    
    # Passaggio C: Convertiamo i dati normalizzati in un Tensore di PyTorch, il formato letto dal modello
    input_tensor = torch.FloatTensor(scaled_features)

    # Passaggio D: Eseguiamo l'inferenza (la previsione vera e propria)
    # Usiamo 'torch.no_grad()' per dire a PyTorch di non calcolare i gradienti, 
    # riducendo drasticamente l'uso della memoria e del processore.
    with torch.no_grad():
        # Passiamo i dati alla rete neurale
        outputs = model(input_tensor)
        # La rete restituisce 3 punteggi. Prendiamo l'indice con il valore più alto (la classe più probabile).
        _, predicted = torch.max(outputs, 1)
        
    # Elenco delle classi corrispondenti agli indici 0, 1 e 2
    classes = ['Setosa', 'Versicolor', 'Virginica']
    
    # Restituiamo il risultato come JSON al client
    return {
        "prediction": int(predicted.item()), # L'indice numerico della classe
        "label": classes[predicted.item()],  # Il nome testuale della classe (es. 'Setosa')
        "status": "success"                  # Messaggio di conferma operazione
    }

# 5. Endpoint di Health Check
# Un semplice controllo per verificare se il server è attivo e se il modello è stato caricato.
@app.get("/health")
def health_check():
    return {"status": "online", "model_loaded": True}
''' 
Ricevo un testo in inglese, 
cerco un risultato già disponibile in Redis e, 
se manca, lo calcolo con DistilBert
'''
import hashlib
import json
import logging
import os
import asyncio
from contextlib import asynccontextmanager
from typing import Optional

# Importazione della libreria async per Redis.
# Usiamo 'redis.asyncio' per non bloccare il server FastAPI durante le chiamate al database.
import redis.asyncio as redis

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from transformers import pipeline

# Configurazione del sistema di logging standard di Python.
# Questo ci permette di vedere i messaggi di stato nella console del server.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurazione delle variabilio per la connessione a Redis.
# Queste variabili vengono lette dall'ambiente (passate da Docker Compose).
# Se non presenti, usiamo valori di default per lo sviluppo locale (localhost:6379).
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Variabili globali per mantenere lo stato dell'applicazione.
# 'sentiment_pipeline': conterrà il modello DistilBERT caricato in memoria.
# 'redis_client': gestirà la connessione persistente al database di cache.
sentiment_pipeline = None
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestore del ciclo di vita dell'applicazione (Lifespan Events).
    lifespan prepara risorse prima di accettare richieste
    
    In FastAPI, questo contesto viene eseguito una sola volta all'avvio ('yield' prima)
    e una volta alla chiusura ('yield' dopo).

    * prima yield: caricamento modello e creazione cliente Redis
    * durante yield: gestione delle richieste
    * dopo yield: chiusura client Redis
    
    Uso:
    1. All'avvio: Carichiamo il modello di IA (operazione pesante) e apriamo la connessione Redis.
    2. Durante l'esecuzione: L'app usa queste risorse globali. Le risorse convidise vale
    per processo, più worker possono significare più copie del modello
    3. Alla chiusura: Chiudiamo correttamente la connessione Redis per evitare leak di risorse.
    """

    # ** VARIABILI GLOBALI **

    global sentiment_pipeline, redis_client
    
    # --- FASE DI AVVIO ---
    logger.info("Avvio caricamento del modello DistilBERT...")
    
    # Carichiamo la pipeline di Hugging Face per la Sentiment Analysis.
    # Usiamo 'distilbert-base-uncased-finetuned-sst-2-english', un modello efficente e veloce.
    # Specificando 'framework="pt"', forziamo l'uso di PyTorch come backend.

    # ** CARICAMENTO MODELLO **
    try:
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            framework="pt"
        )
        logger.info("Modello caricato correttamente in memoria.")
    except Exception as e:
        # Se il modello non si carica, l'applicazione non può funzionare, quindi logghiamo l'errore.
        logger.error(f"Errore critico nel caricamento del modello: {e}")
        raise e

    # ** CREAZIONE CLIENT REDIS **

    logger.info(f"Tentativo di connessione a Redis su {REDIS_HOST}:{REDIS_PORT}...")
    # Creiamo il client Redis asincrono. 'decode_responses=True' ci fa ottenere stringhe invece di bytes.
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    
    # --- PUNTO DI ESECUZIONE DELL'APP ---
    # Tutto ciò che è prima di yield accade allo startup.
    # Tutto ciò che è dopo yield accade allo shutdown.

    # ** YIELD **

    try:
        # L'applicazione rimane in servizio.
        yield

    finally:
        # Pulizia delle risorse alla chiusura.
        logger.info("Chiusura connessione Redis...")

        if redis_client is not None:
            await redis_client.aclose()

        logger.info("Applicazione terminata.")

# Creazione dell'istanza FastAPI con il gestore lifespan definito sopra.

# ** CREAZIONE APPLICAZIONE **

app = FastAPI(title="Sentiment Analysis API", lifespan=lifespan)

# --- DEFINIZIONE MODELLI DATI (PYDANTIC) ---

class SentimentRequest(BaseModel):
    """
    Modello per validare i dati in ingresso nell'endpoint POST.
    Pydantic garantisce che il campo 'text' sia presente e sia una stringa non vuota.
    """
    text: str = Field(..., min_length=1, description="Il testo in lingua inglese da analizzare.")
    #text= nome del campo JSON; str= deve essere una stringa; ...= campo obbligatorio; 
    #min_lenth=1= almeno un carattere; description= documentazione

class SentimentResponse(BaseModel):
    """
    Modello per strutturare la risposta JSON verso il client.
    """
    label: str  # Es: "POSITIVE" o "NEGATIVE"
    score: float  # Un valore tra 0 e 1 che indica la confidenza del modello
    source: str = Field(..., ge=0, le=1, description="Origine del dato: 'cache' (Redis) o 'model' (calcolo live).")

# --- FUNZIONI DI UTILITÀ ---

def generate_cache_key(text: str) -> str:
    """
    Crea una chiave unica per identificare una richiesta.
    
    Poiché Redis usa chiavi testuali, facciamo l'hash MD5 del testo in input.
    Questo ci permette di avere chiavi di lunghezza fissa indipendentemente dalla lunghezza del testo.
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()

# --- ENDPOINT API ---

@app.post("/predict", response_model=SentimentResponse)
async def predict_sentiment(request: SentimentRequest):
    """
    Endpoint principale per l'analisi del sentimento.
    
    Flusso logico:
    1. Validazione input (gestita automaticamente da Pydantic).
    2. Controllo manuale lunghezza testo (per evitare sovraccarico).
    3. Calcolo Hash del testo.
    4. Verifica presenza in Cache (Redis).
    5. Se non in cache -> Esecuzione inferenza IA (Async).
    6. Salvataggio in cache e ritorno risposta.
    """
    text = request.text
    
    # Controllo esplicito della lunghezza per evitare Denial of Service con testi enormi.
    # DistilBERT gestisce max 512 token, noi tagliamo a 2000 caratteri per sicurezza.
    if len(text) > 2000: 
        raise HTTPException(status_code=400, detail="Testo troppo lungo (max 2000 caratteri).")
            
    # Generiamo la chiave per Redis
    cache_key = generate_cache_key(text)

    # 1. TENTATIVO DI LETTURA DALLA CACHE (HIT)
    if redis_client:
        try:
            # Cerchiamo la chiave in Redis. Operazione asincrona molto veloce (< 1ms).
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                # Se il dato esiste, lo deserializziamo da JSON e lo restituiamo subito.
                logger.info("Cache HIT: Risultato trovato in memoria.")
                data = json.loads(cached_result)
                return SentimentResponse(
                    label=data["label"],
                    score=data["score"],
                    source="cache"
                )
        except Exception as e:
            # Se Redis fallisce (es. timeout), non blocchiamo l'app ma procediamo col calcolo.
            logger.warning(f"Errore lettura Redis: {e}. Procedo con inferenza diretta.")

    # 2. ESECUZIONE INFERENZA (MISS)
    logger.info("Cache MISS: Avvio inferenza sul modello...")

    # La pipeline di Transformers è cpu-bound (blocca il thread principale).
    # Per non bloccare l'intero server asincrono, eseguiamo il calcolo in un thread separato
    # usando asyncio.to_thread.
    try:
        results = await asyncio.to_thread(sentiment_pipeline, text)
        # La pipeline restituisce una lista, es: [{'label': 'POSITIVE', 'score': 0.99}]
        top_result = results[0]
    except Exception as e:
         logger.error(f"Errore durante l'inferenza: {e}")
         raise HTTPException(status_code=500, detail="Errore interno del modello AI.")

    label = top_result["label"]
    score = top_result["score"]

    # 3. SALVATAGGIO IN CACHE
    # Salviamo il risultato calcolato in Redis per le future richieste identiche.
    if redis_client:
        try:
            # 'setex' salva il valore e imposta una scadenza (TTL) atomica.
            # Qui impostiamo 3600 secondi (1 ora) di durata della cache.
            await redis_client.setex(
                cache_key,
                3600,
                json.dumps({"label": label, "score": score})
            )
        except Exception as e:
            logger.warning(f"Impossibile salvare in cache: {e}")

    return SentimentResponse(label=label, score=score, source="model")

@app.get("/health")
async def health_check():
    """Endpoint leggero per verificare che il container sia attivo."""
    return {"status": "ok"}

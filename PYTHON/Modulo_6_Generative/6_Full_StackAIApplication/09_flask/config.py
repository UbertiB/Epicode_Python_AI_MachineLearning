import os

class Config:
    # Chiave segreta per la gestione delle sessioni e della sicurezza in Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default_secret_key_for_development'
    
    # Configurazione di Celery
    # Per installazioni enterprise, è consigliato l'utilizzo di Redis
    
    # Parametri per la retrocompatibilità
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'sqla+sqlite:///celery_broker.db'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'db+sqlite:///celery_broker.db'
    
    # Parametri moderni richiesti da Celery 5.x+
    broker_url = CELERY_BROKER_URL
    result_backend = CELERY_RESULT_BACKEND
    
    # Gestione delle connessioni al boot del worker
    broker_connection_retry_on_startup = True
    
    # Configurazione del server di inferenza locale (es. LM Studio)
    # LM Studio espone un'interfaccia compatibile con le API OpenAI
    LM_STUDIO_BASE_URL = os.environ.get('LM_STUDIO_BASE_URL') or "http://localhost:1234/v1"
    
    # Chiave fittizia richiesta dalla libreria client per ragioni di compatibilità
    LM_STUDIO_API_KEY = "lm-studio"
    
    # Identificativo del modello caricato nel server locale
    LLM_MODEL_NAME = "qwen3.5-35b-a3b"

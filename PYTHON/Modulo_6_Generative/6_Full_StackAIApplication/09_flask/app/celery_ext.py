from celery import Celery

def make_celery(app_name=__name__):
    """
    Inizializza un'istanza di Celery con i parametri predefiniti per SQLite.
    La configurazione definitiva viene iniettata successivamente durante l'avvio della factory Flask.
    """
    # Utilizzo di broker_url e result_backend per compatibilità con Celery 5.x
    return Celery(
        app_name,
        broker_url='sqla+sqlite:///celery_broker.db',
        result_backend='db+sqlite:///celery_broker.db',
        broker_connection_retry_on_startup=True
    )

# Inizializza l'oggetto Celery globale che verrà configurato in app/__init__.py
celery_app = make_celery()

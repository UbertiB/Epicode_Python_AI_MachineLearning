from flask import Flask
from config import Config
from app.celery_ext import celery_app

def create_app(config_class=Config):
    """
    Inizializza l'applicazione Flask tramite il pattern Application Factory.
    Questo approccio evita importazioni circolari e facilita la gestione di
    configurazioni diverse per sviluppo, test o produzione.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Configurazione di Celery tramite l'oggetto config di Flask.
    # Viene utilizzato config_from_object per mappare correttamente i parametri
    # (es. CELERY_BROKER_URL viene convertito internamente in broker_url).
    celery_app.config_from_object(app.config)
    
    # Aggiornamento esplicito per compatibilità con Celery 5.x+,
    # garantendo che il broker e il backend siano impostati correttamente.
    celery_app.conf.update(
        broker_url=app.config.get('CELERY_BROKER_URL'),
        result_backend=app.config.get('CELERY_RESULT_BACKEND'),
        broker_connection_retry_on_startup=True
    )
    
    # Log di debug per verificare le URL caricate all'avvio del worker.
    print(f"CELERY CONFIG LOADED: Broker: {celery_app.conf.broker_url}, Backend: {celery_app.conf.result_backend}")
    
    class ContextTask(celery_app.Task):
        """
        Wrapper per eseguire i task Celery all'interno dell'app context di Flask.
        Necessario se i task devono accedere a database, configurazioni o estensioni di Flask.
        """
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
                
    celery_app.Task = ContextTask
    
    # Registrazione dei Blueprints per la gestione delle rotte in moduli separati.
    from app.api.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app

Avvia il Server Web : python run.py

Avvia il Worker Celery in background celery -A run.celery_app worker --loglevel=info -P solo

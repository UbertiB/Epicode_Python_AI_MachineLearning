import os
from app import create_app
from app.celery_ext import celery_app

# Utilizzo del Factory Pattern per l'inizializzazione dell'app
app = create_app()

if __name__ == '__main__':
    print("="*60)
    print("SISTEMA AVVIATO: FLASK + LM STUDIO (Architettura Modulare)")
    print("="*60)
    print("Accesso tramite browser: http://127.0.0.1:5000")
    print("\nREQUISITI PER IL FUNZIONAMENTO:\n")
    print("1. [LM Studio]: Verificare che il modello sia caricato.")
    print("2. [LM Studio]: Server locale attivo sulla porta 1234.")
    print("3. [Celery]: Avviare il worker in un terminale dedicato: ")
    print("            celery -A run.celery_app worker --loglevel=info -P solo")
    print("")
    print("Nota per ambienti Windows: l'utilizzo del flag '-P solo' è richiesto.")
    print("="*60)
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

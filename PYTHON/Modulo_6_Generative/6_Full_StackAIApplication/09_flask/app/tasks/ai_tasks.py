import time
import torch
from app.celery_ext import celery_app

# Il decoratore @celery_app.task definisce la funzione come un task asincrono
# che può essere gestito dai worker di Celery.

@celery_app.task(bind=True)
def task_pytorch_pesante(self, testo_lungo):
    """
    Simula un'operazione di calcolo intensivo (es. calcolo di embedding)
    che richiede tempi di esecuzione non compatibili con una risposta HTTP sincrona.
    """
    print(f"[CELERY WORKER ID: {self.request.id}] Avvio elaborazione in background.")
    
    # Simulazione operazione PyTorch
    print("[PYTORCH] Inizializzazione tensori.")
    dimensione_simulata = 512
    input_tensor = torch.randint(low=0, high=30000, size=(1, dimensione_simulata))
    
    print(f"[PYTORCH] Input generato. Shape: {input_tensor.shape}")
    
    # Esecuzione di moltiplicazioni matriciali fittizie per simulare il carico CPU/GPU
    weights = torch.randn((dimensione_simulata, 1024))
    
    for i in range(5):
        _ = torch.matmul(input_tensor.float(), weights)
        print(f"[CELERY] Elaborazione batch {i+1}/5 completata.")
        time.sleep(1) # Latenza simulata
        
    risultato_finale = "Analisi completata con successo."
    
    print(f"[CELERY WORKER ID: {self.request.id}] Task terminato.")
    
    # Il risultato viene salvato nel backend configurato (es. SQLite/Redis)
    return {"risultato": risultato_finale, "status": "SUCCESS"}

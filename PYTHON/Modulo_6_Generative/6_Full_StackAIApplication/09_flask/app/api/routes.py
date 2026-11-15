from flask import Blueprint, Response, request, jsonify, render_template

# Disaccoppiamento dei service e dei task asincroni
from app.services.llm_service import LMStudioService
from app.tasks.ai_tasks import task_pytorch_pesante

# Definizione del blueprint per la gestione del modulo principale
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Restituisce l'interfaccia utente per il test dei moduli.
    """
    return render_template('index.html')


@main_bp.route('/api/analyze-async', methods=['POST'])
def start_heavy_task():
    """
    Gestisce l'invio di task onerosi a Celery per l'elaborazione in background.
    Restituisce immediatamente un ID task per permettere il monitoraggio asincrono.
    """
    dati_richiesta = request.get_json()
    testo = dati_richiesta.get('testo', 'Testo predefinito per analisi.')
    
    # Invio del task al worker Celery
    task = task_pytorch_pesante.delay(testo)
    
    return jsonify({
        "stato": "Richiesta acquisita",
        "task_id": task.id
    }), 202


@main_bp.route('/api/stream-chat', methods=['POST'])
def start_streaming():
    """
    Implementa lo streaming dei token tramite Server-Sent Events (SSE).
    La connessione rimane aperta mentre il modello genera il contenuto.
    """
    dati_richiesta = request.get_json()
    prompt = dati_richiesta.get('prompt', 'Fornisci una breve descrizione dei Large Language Models.')
    
    # Recupero del generatore dal service dedicato
    stream_generator = LMStudioService.stream_response(prompt)
    
    # Restituisce la risposta con il mimetype specifico per SSE
    return Response(
        stream_generator, 
        mimetype='text/event-stream'
    )

import json
from openai import OpenAI
from flask import current_app

class LMStudioService:
    """
    Service Layer per la gestione della comunicazione con il modello LLM.
    Mantiene la logica di business separata dalle interfacce di input/output.
    """
    
    @classmethod
    def get_client(cls):
        """
        Inizializza il client per le chiamate al server locale di LM Studio.
        """
        return OpenAI(
            base_url=current_app.config['LM_STUDIO_BASE_URL'],
            api_key=current_app.config['LM_STUDIO_API_KEY']
        )
        
    @classmethod
    def stream_response(cls, prompt):
        """
        Gestisce la generazione in streaming della risposta dal modello.
        Implementa un generatore Python che restituisce i dati nel formato 
        Server-Sent Events (SSE).
        """
        # Catturiamo l'oggetto applicativo reale per l'utilizzo nel thread dello stream
        app = current_app._get_current_object()
        
        def generate():
            with app.app_context():
                client = cls.get_client()
                model_name = app.config['LLM_MODEL_NAME']
                
                try:
                    # Chiamata asincrona con supporto allo streaming dei token
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "Sei un assistente specializzato in analisi dati e programmazione."},
                            {"role": "user", "content": prompt}
                        ],
                        stream=True
                    )
                    
                    for chunk in response:
                        # Estrazione del contenuto testuale dal frammento ricevuto
                        if chunk.choices[0].delta.content is not None:
                            testo = chunk.choices[0].delta.content
                            
                            # Formattazione per SSE: "data: <payload>\n\n"
                            payload = json.dumps({"token": testo})
                            yield f"data: {payload}\n\n"
                            
                    # Invio del segnale di fine stream
                    yield "data: [DONE]\n\n"
                    
                except Exception as e:
                    # Gestione delle eccezioni (es. problemi di connessione al server locale)
                    payload = json.dumps({"error": str(e)})
                    yield f"data: {payload}\n\n"
                    yield "data: [DONE]\n\n"
        
        return generate()

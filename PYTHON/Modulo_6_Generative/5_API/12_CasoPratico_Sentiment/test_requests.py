import requests
import time
import concurrent.futures

# Indirizzo base dell'API. In ambiente Docker locale è localhost:8000.
BASE_URL = "http://localhost:8000"
PREDICT_URL = f"{BASE_URL}/predict"

def test_health():
    """
    Verifica che il server sia attivo e risponda alle chiamate HTTP.
    
    È una buona pratica chiamare l'endpoint '/health' prima di eseguire qualsiasi test
    complesso, per assicurarsi che il container sia 'ready'.
    """
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("[OK] Health Check: Il server è attivo e funzionante.")
        else:
            print(f"[FAIL] Health Check: Il server ha risposto con codice {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Health Check: Impossibile connettersi al server ({e})")
        print("Suggerimento: Controlla se il container Docker è avviato.")

def send_request(text, expected_source=None, expected_status=200):
    """
    Funzione helper per inviare una richiesta POST e analizzare la risposta.
    
    Parametri:
    - text: Il testo da analizzare.
    - expected_source: 'cache' o 'model' (opzionale), per verificare l'origine del dato.
    - expected_status: Codice HTTP atteso (es. 200 per successo, 400 per errore client).
    """
    start_time = time.time()
    try:
        # Invio della richiesta POST con payload JSON
        response = requests.post(PREDICT_URL, json={"text": text})
        elapsed_time = time.time() - start_time
        
        # Verifica se lo status code corrisponde a quello atteso
        if response.status_code == expected_status:
            # CASO DI SUCCESSO (200 OK)
            if response.status_code == 200:
                data = response.json()
                source = data['source']
                # Stampiamo i dettagli della predizione e il tempo impiegato
                print(f"[OK] Input: '{text[:30]}...' -> Label: {data['label']} ({data['score']:.4f}) | Source: {source} | Time: {elapsed_time:.4f}s")
                
                # Controllo aggiuntivo sulla sorgente (Cache vs Model)
                if expected_source and source != expected_source:
                    print(f"    ATTENZIONE: Atteso {expected_source}, ricevuto invece {source}")
            
            # CASO DI ERRORE ATTESO (Es. 400 Bad Request)
            else:
                print(f"[OK] Input valido per il test: Il server ha rifiutato correttamente con codice {response.status_code}")
        
        # CASO DI ERRORE IMPREVISTO
        else:
            print(f"[FAIL] Input: '{text[:30]}...' -> Errore imprevisto {response.status_code}: {response.text}")
            if expected_status != 200:
                print(f"    ATTENZIONE: Ci aspettavamo un codice {expected_status}, ma ne abbiamo ricevuto un altro.")

    except Exception as e:
        print(f"[ERROR] Errore critico nell'invio della richiesta: {e}")

def test_caching():
    """
    Testa il meccanismo di caching di Redis.
    
    Invia due richieste identiche:
    1. La prima deve essere lenta (inferenza del modello) e avere source='model'.
    2. La seconda deve essere immediata (lettura da RAM) e avere source='cache'.
    """
    print("\n--- Test 1: Verifica del Caching ---")
    text = "This course is absolutely amazing and I learned a lot concerning Deep Learning!"
    
    print("1. Prima chiamata (dovrebbe essere processata dal modello - più lenta)")
    send_request(text, expected_source="model")
    
    print("2. Seconda chiamata (dovrebbe essere recuperata dalla cache - istantanea)")
    send_request(text, expected_source="cache")

def test_error_handling():
    """
    Testa la robustezza dell'API contro input non validi.
    
    Verifichiamo che il server risponda con codici di errore appropriati (4xx)
    invece di crashare (500).
    """
    print("\n--- Test 2: Gestione degli Errori ---")
    
    # Testo vuoto: Dovrebbe essere bloccato dalla validazione Pydantic (HTTP 422 - Unprocessable Entity)
    print("1. Invio di testo vuoto (Atteso errore 422)")
    send_request("", expected_status=422) 

    # Testo troppo lungo: Dovrebbe essere bloccato dal nostro controllo di lunghezza (HTTP 400 - Bad Request)
    print("2. Invio di testo eccessivamente lungo (Atteso errore 400)")
    long_text = "Analysis " * 500  # Crea una stringa molto lunga ripetendo la parola
    send_request(long_text, expected_status=400)

def test_concurrency():
    """
    Testa la capacità del server di gestire richieste simultanee.
    
    Simuliamo 5 utenti che interrogano l'API nello stesso istante.
    Grazie al `ThreadPoolExecutor`, le richieste partono in parallelo dal client.
    Lato server, verifichiamo che l'async non si blocchi e risponda velocemente a tutti.
    """
    print("\n--- Test 3: Concorrenza (5 richieste simultanee) ---")
    texts = [
        "I love Python programming.",
        "Deployment is hard but necessary.",
        "Docker is incredibly useful for isolation.",
        "Debugging can be fun sometimes.",
        "Redis makes applications lightning fast."
    ]
    
    start_time = time.time()
    # Eseguiamo le richieste in thread separati
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(send_request, texts)
    
    total_time = time.time() - start_time
    print(f"Tempo totale per completare tutte le richieste: {total_time:.4f}s")

if __name__ == "__main__":
    print("Avvio della Test Suite per Sentiment Analysis API...")
    print("Assicurati che il server Docker sia attivo su localhost:8000")
    
    test_health()
    test_caching()
    test_error_handling()
    test_concurrency()
    
    print("\nTutti i test sono stati completati.")

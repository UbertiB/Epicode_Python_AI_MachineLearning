

## Architettura del Sistema

Il progetto si compone di tre elementi principali:
1.  **API Server (FastAPI)**: Gestisce le richieste HTTP, carica il modello di Deep Learning e comunica con la cache.
2.  **Cache (Redis)**: Memorizza i risultati delle inferenze precedenti per evitare ricalcoli inutili su testi identici.
3.  **Docker Compose**: Coordina l'avvio e la rete interna tra i vari componenti.

---

## Prerequisiti

Prima di iniziare, assicurati di avere installato:
*   [Docker](https://www.docker.com/get-started) e Docker Compose.
*   [Python 3.11+](https://www.python.org/downloads/) (opzionale, solo per eseguire i test localmente).

---

## Come Avviare l'Applicazione

### 1. Avvio della Stack con Docker
Per avviare l'intera infrastruttura (API + Redis), apri il terminale nella cartella del progetto ed esegui:

```bash
docker-compose up --build
```

*   **--build**: Forza la ricostruzione dell'immagine se sono state effettuate modifiche al codice.
*   Il server sarà accessibile all'indirizzo: `http://localhost:8000`

### 2. Verifica dello Stato
Puoi verificare che il server sia attivo visitando `http://localhost:8000/health` nel browser o usando cURL:

```bash
curl http://localhost:8000/health
```

---

## Come Eseguire i Test

È incluso uno script di test per verificare il corretto funzionamento del caching, della concorrenza e della gestione degli errori.

### Installazione Dipendenze per i Test
Assicurati di avere la libreria `requests` installata nel tuo ambiente Python:

```bash
pip install requests
```

### Esecuzione della Test Suite
Con i container Docker in esecuzione, avvia lo script:

```bash
python test_requests.py
```

---

## Utilizzo dell'API (Esempi)

### Analisi del Sentimento (POST)
Invia una richiesta JSON all'endpoint `/predict`:

```bash
# Esempio con cURL
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "I really enjoy learning about artificial intelligence!"}'
```

### Risposta Attesa
Il server restituirà un oggetto JSON contenente la polarità del testo, lo score di confidenza e la sorgente del dato:

```json
{
  "label": "POSITIVE",
  "score": 0.9998,
  "source": "model"
}
```
*Se invii la stessa richiesta una seconda volta, la sorgente diventerà `"cache"`.*

---

## Manutenzione e Risorse

*   **Pesi del Modello**: Vengono salvati in un volume Docker (`hf_cache`) per evitare di riscaricarli ogni volta.
*   **Logs**: Puoi vedere i log in tempo reale tramite il terminale dove è attivo Docker Compose.

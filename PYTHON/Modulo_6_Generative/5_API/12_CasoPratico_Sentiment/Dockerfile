# --- DOCKERFILE ---
# Questo file descrive come costruire l'immagine del contenitore per la nostra applicazione.

# 1. Immagine Base
# Partiamo da un'immagine ufficiale di Python 3.11 molto leggera ('slim').
# Questo riduce la dimensione finale del container e i tempi di download.
FROM python:3.11-slim

# 2. Directory di Lavoro
# Impostiamo '/app' come cartella principale all'interno del container.
# Tutti i comandi successivi verranno eseguiti qui.
WORKDIR /app

# 3. Dipendenze di Sistema
# Aggiorniamo i pacchetti di sistema e installiamo strumenti di compilazione essenziali.
# 'build-essential' serve per compilare alcune librerie Python che hanno componenti in C.
# Puliamo subito la cache di apt per mantenere l'immagine piccola.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Dipendenze Python
# Copiamo prima solo il file dei requisiti.
# Questo sfrutta la cache di Docker: se 'requirements.txt' non cambia,
# Docker salterà il passaggio di installazione (molto lento) nelle build successive.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Codice Applicativo
# Copiamo il resto del codice sorgente (app.py) nel container.
COPY app.py .

# 6. Esposizione Porte
# Indichiamo che il container ascolterà sulla porta 8000.
# Nota: Questo è solo documentale, la pubblicazione vera avviene nel docker-compose.
EXPOSE 8000

# 7. Comando di Avvio
# Definiamo il comando che verrà eseguito quando il container parte.
# Usiamo 'uvicorn' per lanciare l'applicazione FastAPI.
# --host 0.0.0.0: Necessario per rendere il server accessibile dall'esterno del container.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

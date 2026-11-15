# Progetto 6 - Synthetic Data Sandbox (VAE Edition)

Un VAE impara le distribuzioni di un dataset sensibile e genera un dataset sintetico con le stesse proprietà statistiche, ma senza record reali. Un LLM risponde a domande sui dati sintetici scrivendo codice Pandas + Matplotlib, che il backend esegue e restituisce come grafico.

## Struttura dei file

| File | Fase | A cosa serve |
|---|---|---|
| `data_engine.py` | 1 | Pulizia, gestione nulli, MinMaxScaler, One-Hot Encoding e trasformazione inversa |
| `vae.py` | 2 | Encoder, reparameterization trick, decoder, loss MSE + KL, training e sampling |
| `validazione.py` | 3 | Statistiche, correlazioni, privacy check (copie esatte e distanza dal record più vicino) |
| `analista_llm.py` | 4 | System prompt, codice dall'LLM, controllo di sicurezza ed esecuzione isolata |
| `api.py` | 5 | Backend FastAPI: `/upload`, `/train`, `/generate`, `/synthetic-data`, `/report`, `/analyze` |
| `app.py` | 5 | Dashboard Streamlit: chiama solo il backend, nessuna logica di ML |
| `.env.example` | - | Configurazione dell'LLM (LM Studio oppure OpenAI) |

Flusso: `app.py` → HTTP → `api.py` → `data_engine` / `vae` / `validazione` / `analista_llm`

## Dataset

Scarica **Pima Indians Diabetes** da Kaggle (`uciml/pima-indians-diabetes-database`, file `diabetes.csv`, 768 righe, 9 colonne).

Cosa fa il preprocessing su questo dataset:
- lo zero in Glucose, BloodPressure, SkinThickness, Insulin e BMI è un valore mancante: viene trasformato in nullo e sostituito con la mediana
- `Outcome` (0/1) ha pochi valori distinti, quindi viene trattata come categorica e codificata One-Hot
- le altre colonne sono numeriche e vengono scalate tra 0 e 1

Funziona anche con altri CSV: le colonne di testo o con al massimo 10 valori distinti diventano categoriche.

### Secondo dataset: Credit Card Fraud Detection (`creditcard.csv`)

284.807 transazioni, 31 colonne: `Time`, `V1`-`V28` (già anonimizzate con PCA), `Amount` e `Class` (1 = frode, solo lo 0,17%). La copia nella cartella viene da GitHub e ha gli stessi conteggi dell'originale Kaggle.

Cosa cambia rispetto a Pima:
- **Training**: la UI propone da sola batch 512 e 20 epoche. Con i valori di Pima (batch 64, 300 epoche) il training durerebbe ore.
- **Privacy check**: le distanze sono calcolate su un campione di 5.000 record (l'indice contiene comunque tutti i reali), altrimenti richiederebbe minuti.
- **Pulizia**: 1.081 righe duplicate vengono rimosse (284.807 → 283.726).

Risultati dei test (20 epoche, 283.726 righe generate): differenza media delle correlazioni 0,015, deviazione standard sintetica pari a quella reale (mediana), zero copie esatte.

**Limite importante: il VAE non genera frodi.** Con lo 0,17% di casi positivi, il modello impara la classe dominante e ignora quella rara. Per un dataset sintetico utile all'analisi delle frodi servirebbe un VAE condizionale (CVAE) oppure l'addestramento con le frodi sovra-campionate. È un buon punto da discutere in presentazione: dimostra che le metriche medie (correlazioni, distribuzioni) possono essere ottime e nascondere la perdita della classe che interessa di più.

## Avvio in Windows

Servono **due terminali** PowerShell, entrambi con la `.venv` attiva e nella cartella del progetto.

```powershell
& 'F:\EPICODE\Epicode_Python_AI_MachineLearning\.venv\Scripts\Activate.ps1'
python -m pip install -r .\requirements.txt
copy .env.example .env
```

Terminale 1, backend (il primo avvio impiega 20-30 secondi per caricare PyTorch):
```powershell
python api.py
```
La documentazione interattiva delle API è su http://127.0.0.1:8001/docs

Se compare `WinError 10048` o `10013`, la porta è occupata o riservata da Windows: cambia `API_PORT` e `API_URL` nel file `.env` (es. 8002) mettendo lo stesso numero in entrambi.

Terminale 2, interfaccia:
```powershell
python -m streamlit run .\app.py
```

Per l'analista LLM: avvia il server di LM Studio e controlla che `LLM_MODEL` nel file `.env` corrisponda a un modello della lista. Per usare OpenAI, segui l'opzione B nel file `.env`.

## Prova guidata

1. **Dati**: trascina `diabetes.csv` e premi *Carica e preprocessa*. Controlla le colonne numeriche, quelle categoriche e i nulli imputati.
2. **Addestramento**: lascia i valori di default (8 dimensioni latenti, 300 epoche, beta 0.05) e avvia. Le curve di ricostruzione e KL devono scendere e stabilizzarsi.
3. **Generazione e validazione**: genera 768 righe e controlla:
   - statistiche: lo scarto della media dovrebbe restare sotto il 10-20% della deviazione standard
   - heatmap: le due matrici di correlazione devono avere la stessa struttura
   - istogrammi: forme simili per Glucose, BMI, Age
   - privacy: 0 record identici, quota "troppo vicini" intorno al 5% o meno
4. **Analista LLM**: chiedi ad esempio *"Qual è la correlazione tra BMI e Glucose? Fai uno scatter plot."* Apri l'espansore per vedere il codice generato.

## Endpoint e metodi HTTP

| Endpoint | Metodo | Cosa fa |
|---|---|---|
| `/health` | GET | Health check: `servizio` vale "ok" oppure "degradato" se l'LLM non è raggiungibile |
| `/upload` | POST | Carica e preprocessa il CSV |
| `/train` | POST | Avvia l'addestramento in background e risponde subito (202) |
| `/train/status` | GET | Avanzamento (epoca corrente) e storico delle loss |
| `/train/commento` | GET | Commento dell'LLM sui risultati del training |
| `/generate` | POST | Genera i dati sintetici e li salva nel backend |
| `/synthetic-data` | GET | Scarica l'ultimo dataset sintetico generato |
| `/real-data` | GET | Dataset reale pulito |
| `/report` | GET | Statistiche, correlazioni, privacy check |
| `/report/commento` | GET | Commento dell'LLM sul report di validazione |
| `/analyze` | POST | Domanda in linguaggio naturale all'analista LLM |

Regola seguita: **GET solo per leggere** (sicuro e idempotente: ripeterlo non cambia nulla), **POST per le azioni che modificano lo stato**. Per questo la generazione (azione) e il download (lettura) sono due endpoint distinti: aprire un link o aggiornare la pagina non può più sovrascrivere i dati sintetici per errore.

## Parametri del VAE

| Parametro | Effetto |
|---|---|
| Dimensione latente | Più alta = ricostruzione migliore, ma rischio di memorizzare i dati |
| Beta | Peso della KL. Con 1.0 il modello collassa e genera righe quasi identiche (posterior collapse). Con valori molto bassi (0.002) la varianza torna, ma medie e correlazioni si spostano. 0.05 è il compromesso trovato nei test |
| Epoche | Troppe possono portare a overfitting: controlla il privacy check |

### Due scelte motivate da test (da citare nella presentazione)

1. **Beta = 0.05 e non 1.** Sul dataset Pima, con beta 1 la KL scende a zero e la deviazione standard dei dati sintetici è circa il 6% di quella reale: tutte le righe sono quasi uguali.
2. **Rumore di ricostruzione in generazione.** Il decoder restituisce la media attesa per ogni punto latente. Aggiungendo il rumore gaussiano stimato a fine training (cioè campionando davvero da p(x|z)), la deviazione standard torna al 96-98% del reale e la differenza media delle correlazioni scende sotto 0.07.

## Sicurezza dell'esecuzione del codice LLM

Il codice generato passa due controlli:
1. **Analisi statica (AST)**: blocca import non consentiti, funzioni come `open`, `exec`, `eval`, accesso ad attributi interni e metodi che leggono o scrivono file.
2. **Processo separato con timeout di 20 secondi**: se il codice si blocca o va in errore, il server non ne risente.

È una protezione adeguata a un progetto didattico, **non una sandbox completa**. In produzione il codice andrebbe eseguito in un container isolato senza rete.

## Limiti noti

- Lo stato (dataset e modello) resta in memoria nel backend: un utente alla volta, e si perde al riavvio.
- Il training è asincrono ma gira in un thread dello stesso processo: un solo addestramento alla volta, e se il backend si riavvia il training in corso si perde. In produzione servirebbe una coda di job (es. Celery) con lo stato salvato su database.
- Il VAE con MSE tende a "lisciare" le code delle distribuzioni: i valori estremi risultano meno frequenti che nei dati reali.

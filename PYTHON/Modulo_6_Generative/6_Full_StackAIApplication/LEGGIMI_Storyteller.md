# Storyteller App

Un caso pratico di generazione testo e immagini. Scrivi un titolo, leggi i capitoli man mano che compaiono e sfoglia un libro illustrato. Il file Python riprende la struttura dell’esempio di analisi documenti, con sezioni numerate, client HTTP, funzioni separate e una `main()` per Streamlit.

## Quale file usare

| File | A cosa serve |
|---|---|
| `14_CasoPratico_Storyteller.py` | È il file da aprire in VS Code e da avviare con Streamlit. Contiene motori, worker e interfaccia. |
| `requirements.txt` | Elenca i tre pacchetti Python dell’app. Va nella stessa cartella del file `.py`. |
| `LEGGIMI_Storyteller.md` | È questa guida. Aprila in anteprima Markdown in VS Code. |
| `Libro_Storyteller.html` | Lo scarichi dalla pagina a libro concluso. Contiene testo e immagini e si apre con un browser. |

Il formato da scegliere per l’app è **`.py`**. Un notebook `.ipynb` è adatto a provare una funzione o un modello in celle separate. Qui il comando `streamlit run` avvia l’intera interfaccia a partire dallo script.

## Avvio in Windows

Estrai lo ZIP e apri in VS Code la cartella che contiene `requirements.txt`. Vai su **Terminale → Nuovo terminale**, scegli PowerShell e attiva il tuo ambiente virtuale. Se usi la `.venv` di EPICODE e il percorso è quello dei tuoi esercizi, puoi attivarla così.

```powershell
& 'F:\EPICODE\Epicode_Python_AI_MachineLearning\.venv\Scripts\Activate.ps1'
```

Nel terminale con `(.venv)`, esegui dalla cartella estratta.

```powershell
python -m pip install -r .\requirements.txt
python -m streamlit run .\14_CasoPratico_Storyteller.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Apri l’indirizzo stampato dal terminale, di solito [http://127.0.0.1:8501](http://127.0.0.1:8501). Lascia PowerShell aperto mentre usi l’app. Con **Ctrl+C** fermi Streamlit.

### Prima prova in modalità Demo locale

1. Lascia **Demo locale**, titolo *La mappa delle luci*, **Acquerello** e tre capitoli. Premi **Genera il libro**.
2. Osserva la prima pagina. La prosa appare a piccoli pezzi. La cornice dell’illustrazione mostra la fase del lavoro.
3. Sfoglia con **Successivo** e **Precedente**. Ricarica la scheda a libro completato per ritrovare la pagina aperta.
4. Prova **Rigenera questa illustrazione**. L’app crea una nuova edizione con una variante del capitolo selezionato. Puoi scegliere anche la risoluzione.
5. Premi **Scarica il libro HTML** e apri il file scaricato. L’indice porta ai capitoli e le immagini sono incorporate.
6. Torna all’officina e invia gli stessi parametri iniziali. Il messaggio di riuso indica che l’app ha ritrovato il lavoro.

La demo usa una trama campione e disegni procedurali creati in Pillow. Titolo, stile, seed, risoluzione e numero di capitoli influenzano la prova. I campi idea e genere sono riservati alla modalità **AI locale**.

### Modalità AI locale

| Componente | Dove gira | Cosa inserire in Storyteller |
|---|---|---|
| Narratore | LM Studio, porta predefinita `1234` | L’ID esatto di un modello chat che supporta streaming e JSON Schema. |
| Revisore delle immagini | LM Studio, stesso server | L’ID di un modello con capacità visiva. Se il narratore supporta anche le immagini, puoi provare lo stesso ID in entrambi i campi. |
| Illustratore | ComfyUI, porta predefinita `8188` | Il nome del checkpoint con CLIP e VAE integrati, compatibile con il workflow Stable Diffusion 1.5. |

Avvia **Local Server** in LM Studio e il server ComfyUI nella tua installazione. Metti il checkpoint nella cartella `ComfyUI/models/checkpoints` e verifica che ComfyUI lo elenchi. Copia gli identificatori dei modelli che intendi usare, scegli **AI locale** e compila i tre campi nella sidebar.

Con i server sul tuo PC e senza autenticazione, questi comandi PowerShell permettono di verificare ciò che espongono.

```powershell
(Invoke-RestMethod 'http://127.0.0.1:1234/v1/models').data.id
(Invoke-RestMethod 'http://127.0.0.1:1234/api/v1/models').models |
    Select-Object key, loaded_instances, capabilities
Invoke-RestMethod 'http://127.0.0.1:8188/models/checkpoints'
```

Il secondo comando usa l’API nativa di LM Studio e mostra anche quali modelli dichiarano capacità visive. Per configurazioni con autenticazione, il client legge il token dalla variabile `LM_STUDIO_API_TOKEN` del processo. Se un motore è su un’altra macchina, imposta il suo indirizzo effettivo nello stesso terminale prima di avviare Streamlit.

```powershell
$env:STORYTELLER_LM_URL = 'http://127.0.0.1:1234'
$env:STORYTELLER_COMFY_URL = 'http://127.0.0.1:8188'
python -m streamlit run .\14_CasoPratico_Storyteller.py --server.address 127.0.0.1 --browser.gatherUsageStats false
```

Con la tua Quadro P4000 partirei da **due capitoli, 512 × 384 e GPU condivisa**, verificando il checkpoint in ComfyUI prima di collegare tutti i motori. L’occupazione effettiva dipende dai modelli caricati e dall’offload. Questa configurazione è un punto di partenza, la compatibilità GPU va verificata sul tuo PC.

## Spiegazione del file Python

### 01. Configurazione e struttura dei dati

Gli import standard gestiscono file, code, thread, JSON e hash. `requests` chiama i server, Pillow legge e crea le immagini, Streamlit disegna la pagina.

- `Impostazioni` fotografa i parametri quando premi **Genera il libro**. I worker usano quella fotografia anche se poi tocchi un widget.
- `Libro` contiene titolo, sinossi, scheda visiva e lista dei capitoli. `Capitolo` contiene prosa, scena, stato del testo, stato dell’immagine e ID dell’asset.
- `cap-01`, `cap-02` e i successivi ancorano le immagini. Un risultato viene salvato nel capitolo associato al lavoro in coda, anche se nel frattempo stai leggendo un’altra pagina.
- `REVISIONE` fa parte delle chiavi della cache. Aumentala se cambi il workflow, le istruzioni o le regole di controllo.

### 02. Controlli e file

`campo_testo()` verifica tipo, lunghezza e presenza di un testo. `controlla_testo()` applica un filtro lessicale didattico al brief, alle scene e al testo cumulativo prima che venga mostrato. Il filtro intercetta i termini configurati e può produrre falsi positivi o lasciar passare casi che richiedono comprensione del contesto.

`normalizza_jpeg()` verifica che ComfyUI abbia restituito un’immagine leggibile delle dimensioni richieste e la converte in JPEG. La verifica semantica avviene separatamente con il revisore visivo. `scrivi_atomico()` scrive un temporaneo e poi lo sostituisce al file finale, così il lettore trova un file completo.

### 03. Chiamate ai due motori

| Funzione | Richiesta | Risultato |
|---|---|---|
| `json_strutturato()` | POST a `/v1/chat/completions` con JSON Schema | Scaletta o descrizione di una scena. |
| `capitolo_stream()` | POST allo stesso endpoint con `stream: true` | Pezzi di testo ricavati dagli eventi SSE. |
| `ComfyUIClient.genera()` | POST `/prompt`, GET `/history/{prompt_id}` e GET `/view` | Byte dell’immagine del lavoro richiesto. |
| `approva_immagine()` | POST `/api/v1/chat` con immagine JPEG in Base64 | Verdetto del modello visivo. |

Per il testo, una riga SSE inizia con `data:`. Il client legge `choices[0].delta.content`, accumula il testo e riconosce la fine dello stream. Il worker pubblica gli aggiornamenti in memoria a intervalli brevi. La pagina li visualizza al successivo aggiornamento del lettore.

Per l’immagine, `workflow_diffusione()` collega sette nodi. Il loader apre checkpoint, CLIP e VAE. I due `CLIPTextEncode` codificano i prompt positivo e negativo. Il latente vuoto stabilisce forma e dimensioni. `KSampler` usa seed, conditioning e passi di denoising. Il VAE porta il latente nei pixel. `PreviewImage` produce il file temporaneo che il client recupera usando il `prompt_id`.

Il revisore visivo riceve i byte solo dopo la verifica del formato. Un esito diverso da `CONSENTITA`, un errore o una risposta ambigua fanno trattenere l’illustrazione. Il file approvato entra nella cache dell’app. Le anteprime di ComfyUI sono gestite dalla sua cartella temporanea. La revisione è un filtro didattico a modello e può sbagliare.

### 04. Narrativa, estrazione del prompt e coerenza

1. `crea_piano()` chiede al narratore una scaletta JSON, la sinossi e una scheda dei personaggi. Python verifica quanti capitoli sono arrivati e assegna gli ID.
2. `prompt_capitolo()` combina l’evento del capitolo, la scheda visiva e la coda del testo precedente. Per esempio, se Lea ha appena attraversato il ponte, la pagina successiva sa da dove ripartire.
3. `estrai_scena()` legge la prosa terminata e ricava una singola inquadratura in inglese con soggetto, azione, luce e ambiente. Se la chiamata fallisce, l’app può usare lo spunto già presente nella scaletta e lo segnala nei dettagli del capitolo. Un blocco del filtro ferma la scena.
4. `prompt_immagine()` unisce la scena allo stesso modificatore di stile e agli stessi tratti di continuità. Nel demo Lea ricompare con il cappotto ocra. In AI locale il modello riceve quel tratto nel prompt insieme alla scena.

Il modello linguistico stima la probabilità del token successivo dato il contesto precedente. La temperatura influisce sulla scelta tra continuazioni possibili. Il nodo CLIP traduce il testo in un condizionamento numerico per la diffusione. Il modello usa quel condizionamento durante il denoising. Stile, descrizioni e seed aumentano la ripetibilità. La somiglianza tra personaggi nelle diverse immagini dipende anche dal checkpoint e dalla scena.

### 05. Latenza, worker, GPU e cache

`Officina` mantiene lo stato condiviso. Il worker **testo** scrive i capitoli in ordine per conservare la trama. Dopo aver ottenuto la scena, inserisce il capitolo nella coda delle immagini e passa al testo successivo. Il worker **immagini** preleva un solo lavoro alla volta. Le prime pagine e le rigenerazioni esplicite hanno precedenza nella coda.

`SlotGPU` coordina le chiamate quando i motori condividono la GPU. Dà priorità al testo quando si libera lo slot e concede un turno all’immagine dopo al massimo due richieste testuali consecutive in presenza di attesa. La chiamata già in esecuzione termina prima del cambio di turno. Il controllo della memoria dei pesi caricati appartiene ai server di inferenza.

Su risorse separate puoi impostare `STORYTELLER_SHARED_GPU=0` e riavviare per permettere la sovrapposizione delle chiamate. In un esempio ipotetico, tre testi da 6 secondi e tre immagini da 10 secondi richiedono 48 secondi in sequenza. Se i due worker possono sovrapporsi, la prima immagine parte al secondo 6, le altre finiscono al 26 e al 36. L’utente intanto può iniziare a leggere dai primi aggiornamenti del testo. Tempi reali e grado di sovrapposizione dipendono dai motori.

`avvia()` usa l’hash della ricetta completa per riconoscere richieste uguali, comprese quelle contemporanee. Titolo, genere, stile, seed e modelli contribuiscono alla chiave. Anche le singole immagini approvate hanno una chiave. Dieci richieste identiche nello stesso processo possono così condividere un solo libro. Una variante crea un nuovo ID di libro e un nuovo seed per il capitolo scelto, mantenendo i riferimenti degli altri.

Questa versione usa **una coda locale, sei libri attivi al massimo e batch di una immagine**. Il prefetch è lineare. Un’estensione a bivi darebbe un ID anche al ramo e accoderebbe per primo quello più probabile. Una versione distribuita avrebbe bisogno di una coda condivisa e di worker che condividano la cache. Per misurare il costo, comincia da risoluzione, secondi del worker e tasso di riuso. Passare da 512 × 384 a 768 × 576 moltiplica i pixel per 2,25. L’effetto sui tempi si misura sul tuo hardware.

### 06. Esportazione

`esporta_html()` crea un libro con copertina, indice, ancore di capitolo e immagini JPEG incorporate in Base64. Il file si apre anche dopo aver chiuso Streamlit. Per ottenere una copia PDF puoi usare **Stampa → Salva come PDF** nel browser. I paragrafi vengono trasformati in HTML con escaping, così un carattere di markup nel testo viene mostrato come testo.

### 07. Interfaccia e memoria

`main()` configura la pagina e il form nella sidebar. `st.cache_resource` crea una sola officina per processo. I worker scrivono lo stato sotto lock, mentre Streamlit legge una copia coerente.

`st.fragment(run_every=0.55)` aggiorna solo il lettore durante la generazione. `mostra_capitolo()` affianca prosa e immagine e usa una cornice 4:3 mentre l’illustrazione è in coda. `st.session_state` tiene i byte già letti per la sessione corrente.

Ricaricando la scheda, Streamlit crea una nuova sessione. Per riaprire il libro l’app combina `?storia=…&cap=…` nell’URL con il manifesto JSON e i JPEG nella cartella `storyteller_data`. Quella cartella contiene i libri locali e deve restare accanto all’app oppure nel percorso impostato con `STORYTELLER_DATA_DIR`. Se fermi il processo durante un lavoro, i capitoli completati sono recuperabili e il lavoro interrotto viene segnalato.

Per un audiolibro illustrato potresti aggiungere un terzo worker TTS che prende il testo completo, salva un audio con lo stesso ID del capitolo e lo mostra con `st.audio()`. Qui l’audio è un’estensione descritta.

## Se una prova si ferma

| Messaggio o situazione | Cosa controllare |
|---|---|
| `No module named streamlit` | Controlla `(.venv)` e lancia `python -m pip install -r .\requirements.txt` da quella cartella. |
| `missing ScriptRunContext` avviando il file | Usa `python -m streamlit run .\14_CasoPratico_Storyteller.py` in PowerShell. |
| JSON narrativo illeggibile | Verifica l’ID e il supporto JSON Schema del modello narrativo. Controlla la console LM Studio. |
| Workflow senza anteprima | Verifica il nome del checkpoint e gli errori nella console ComfyUI. Parti da 512 × 384. |
| Illustrazione trattenuta | Verifica che il modello visivo accetti immagini su `/api/v1/chat` e guarda il messaggio del capitolo. |
| Timeout di ComfyUI | Controlla il lavoro indicato nella coda di ComfyUI prima di rilanciare. Il timeout riguarda l’attesa del client. |

## Fonti

- [Streamlit, aggiornare solo una parte della pagina con fragment](https://docs.streamlit.io/develop/api-reference/execution-flow/st.fragment)
- [Streamlit, thread di lavoro e session state](https://docs.streamlit.io/develop/concepts/design/multithreading) e [durata dello stato di sessione](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state)
- [LM Studio, Chat Completions](https://lmstudio.ai/docs/developer/openai-compat/chat-completions), [JSON strutturato](https://lmstudio.ai/docs/developer/openai-compat/structured-output) e [chat con immagini](https://lmstudio.ai/docs/developer/rest/chat)
- [ComfyUI, installazione Windows](https://docs.comfy.org/installation/comfyui_portable_windows), [rotte HTTP](https://docs.comfy.org/development/comfyui-server/comms_routes) e [CLIP Text Encode](https://docs.comfy.org/built-in-nodes/ClipTextEncode)

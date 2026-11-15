"""Caso pratico Streamlit. Una storia illustrata in cui ogni scena ha il suo capitolo."""

import base64
import hashlib
import html
import io
import itertools
import json
import logging
import os
import queue
import random
import re
import tempfile
import threading
import time
import uuid
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from pathlib import Path

import requests
import streamlit as st
from PIL import Image, ImageDraw


# -----------------------------------------------------------------------------
# 01. CONFIGURAZIONE E STRUTTURA DEI DATI
# -----------------------------------------------------------------------------

# I server si configurano nel terminale. La sidebar riceve gli ID dei modelli.
LM_STUDIO_URL = os.getenv("STORYTELLER_LM_URL", "http://127.0.0.1:1234").rstrip("/")
if LM_STUDIO_URL.endswith("/v1"):
    LM_STUDIO_URL = LM_STUDIO_URL[:-3]
COMFYUI_URL = os.getenv("STORYTELLER_COMFY_URL", "http://127.0.0.1:8188").rstrip("/")
DATA_DIR = Path(os.getenv("STORYTELLER_DATA_DIR", str(Path(__file__).with_name("storyteller_data"))))
GPU_CONDIVISA = os.getenv("STORYTELLER_SHARED_GPU", "1") != "0"

# Cambia revisione se cambi prompt, workflow o regole di controllo.
REVISIONE = 1
MAX_LIBRI_ATTIVI = 6
MAX_BYTE_IMMAGINE = 12 * 1024 * 1024
STILI = {
    "Acquerello": "watercolor children's book illustration, soft washes, paper grain, muted jewel tones",
    "Carta ritagliata": "layered paper cutout illustration, tactile paper, clean shapes, warm ink palette",
    "Cyberpunk": "painterly cyberpunk storybook illustration, teal and amber neon, atmospheric night",
}
GENERI = ("Avventura", "Mistero", "Fiaba", "Fantascienza")
REGOLA = "Scrivi per un pubblico di tutte le età, con una trama adatta a un libro illustrato."
NEGATIVO = "text, typography, watermark, logo, explicit nudity, graphic violence, gore"
STATI_PENDENTI = {"in coda", "in corso", "in revisione"}
LOG = logging.getLogger("storyteller")


@dataclass(frozen=True)
class Impostazioni:
    """Una fotografia immutabile dei parametri al momento del clic."""

    titolo: str
    idea: str
    genere: str
    stile: str
    numero_capitoli: int
    seed: int
    dimensione: int
    passi: int
    demo: bool
    llm: str = ""
    visione: str = ""
    checkpoint: str = ""


@dataclass
class Capitolo:
    """Testo, prompt e asset sono associati dallo stesso identificatore."""

    id: str
    titolo: str
    evento: str
    spunto: str
    testo: str = ""
    scena: str = ""
    stato_testo: str = "in attesa"
    stato_immagine: str = "in attesa"
    asset: str = ""
    errore: str = ""
    nota: str = ""
    variante: int = 0
    dimensione: int = 512
    secondi: float = 0.0


@dataclass
class Libro:
    id: str
    chiave: str
    config: Impostazioni
    titolo: str
    sinossi: str = ""
    scheda: str = ""
    scrittura: str = "in coda"
    errore: str = ""
    capitoli: list[Capitolo] = field(default_factory=list)

    @property
    def attivo(self) -> bool:
        return self.scrittura in STATI_PENDENTI or any(
            capitolo.stato_immagine in STATI_PENDENTI for capitolo in self.capitoli
        )


# -----------------------------------------------------------------------------
# 02. CONTROLLO DEGLI INPUT, DEL TESTO E DEGLI ASSET
# -----------------------------------------------------------------------------

class ErroreMotore(RuntimeError):
    """Errore leggibile da mostrare nello stato del libro o del capitolo."""


class ContenutoBloccato(ErroreMotore):
    pass


# È un esempio didattico di filtro lessicale. L'AI visiva ha una verifica separata.
TERMINI_BLOCCATI = re.compile(
    r"\b(?:pornograf\w*|pedopornograf\w*|stupr\w*|dismembrament\w*|"
    r"pornograph\w*|sexual assault|graphic dismemberment|gore)\b",
    re.IGNORECASE,
)


def controlla_testo(testo: str) -> None:
    """Controlla il testo cumulativo anche se una parola arriva in più eventi SSE."""
    normalizzato = " ".join(testo.split())
    if TERMINI_BLOCCATI.search(normalizzato):
        raise ContenutoBloccato("Il filtro testuale ha fermato il contenuto. Riformula l’idea per tutte le età.")


def campo_testo(valore: object, limite: int) -> str:
    if not isinstance(valore, str) or not valore.strip() or len(valore) > limite:
        raise ErroreMotore("Il modello ha restituito un campo testuale vuoto o fuori limite.")
    testo = valore.strip()
    controlla_testo(testo)
    return testo


def impronta(dati: object) -> str:
    """SHA-256 stabile per deduplicare richieste identiche e nominare gli asset."""
    serializzato = json.dumps(dati, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(serializzato.encode("utf-8")).hexdigest()


def scrivi_atomico(percorso: Path, dati: bytes) -> None:
    """Pubblica un file intero dopo aver completato la scrittura temporanea."""
    with tempfile.NamedTemporaryFile(dir=percorso.parent, delete=False) as temporaneo:
        nome = Path(temporaneo.name)
        try:
            temporaneo.write(dati)
        except OSError:
            temporaneo.close()
            nome.unlink(missing_ok=True)
            raise
    try:
        nome.replace(percorso)
    finally:
        nome.unlink(missing_ok=True)


def dimensioni(larghezza: int) -> tuple[int, int]:
    """Rapporto 4:3. Le due dimensioni sono multipli di 64 per il workflow SD."""
    return larghezza, larghezza * 3 // 4


def normalizza_jpeg(dati: bytes, larghezza: int) -> bytes:
    """Verifica il contenitore e uniforma l'asset a JPEG per UI, cache ed export."""
    try:
        with Image.open(io.BytesIO(dati)) as immagine:
            if immagine.size != dimensioni(larghezza):
                raise ErroreMotore("ComfyUI ha restituito una dimensione diversa da quella richiesta.")
            uscita = io.BytesIO()
            immagine.convert("RGB").save(uscita, "JPEG", quality=90, optimize=True)
            return uscita.getvalue()
    except (OSError, Image.DecompressionBombError) as errore:
        raise ErroreMotore("Il motore grafico ha restituito un file immagine illeggibile.") from errore


# -----------------------------------------------------------------------------
# 03. CLIENT HTTP PER LM STUDIO E COMFYUI
# -----------------------------------------------------------------------------

def sessione_http(token: str = "") -> requests.Session:
    sessione = requests.Session()
    # Un server locale può essere raggiunto direttamente anche con un proxy aziendale impostato.
    sessione.trust_env = False
    if token:
        sessione.headers["Authorization"] = f"Bearer {token}"
    return sessione


def verifica_http(risposta: requests.Response, servizio: str) -> None:
    if risposta.ok and not risposta.is_redirect:
        return
    dettaglio = ""
    try:
        errore = risposta.json().get("error", {})
        if isinstance(errore, dict):
            dettaglio = str(errore.get("message", ""))[:260]
    except (ValueError, AttributeError):
        pass
    raise ErroreMotore(f"{servizio} ha risposto HTTP {risposta.status_code}. {dettaglio}".strip())


def schema_oggetto(proprieta: dict) -> dict:
    return {
        "type": "object",
        "properties": proprieta,
        "required": list(proprieta),
        "additionalProperties": False,
    }


class LMStudioClient:
    """Il client si occupa di HTTP. Il worker decide cosa salvare e pubblicare."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = os.getenv("LM_STUDIO_API_TOKEN", "")

    def json_strutturato(
        self, modello: str, sistema: str, utente: str, nome: str, schema: dict,
        limite: int, seed: int,
    ) -> dict:
        payload = {
            "model": modello,
            "messages": [{"role": "system", "content": sistema}, {"role": "user", "content": utente}],
            "temperature": 0.2,
            "seed": seed,
            "max_tokens": limite,
            "stream": False,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": nome, "strict": True, "schema": schema},
            },
        }
        with sessione_http(self.token) as sessione:
            risposta = sessione.post(
                f"{self.base_url}/v1/chat/completions", json=payload, timeout=(5, 180),
                allow_redirects=False,
            )
            verifica_http(risposta, "LM Studio")
            try:
                dati = json.loads(risposta.json()["choices"][0]["message"]["content"])
                if not isinstance(dati, dict):
                    raise ValueError("È atteso un oggetto JSON.")
                return dati
            except (ValueError, TypeError, KeyError, IndexError) as errore:
                raise ErroreMotore("JSON narrativo illeggibile. Controlla che il modello supporti JSON Schema.") from errore

    def capitolo_stream(self, modello: str, prompt: str, seed: int):
        """Estrae i delta testuali SSE. I delta di ragionamento restano fuori dal libro."""
        payload = {
            "model": modello,
            "messages": [
                {"role": "system", "content": f"Sei uno scrittore italiano. {REGOLA} Restituisci solo prosa."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.75,
            "seed": seed,
            "max_tokens": 900,
            "stream": True,
        }
        concluso = False
        with sessione_http(self.token) as sessione:
            with sessione.post(
                f"{self.base_url}/v1/chat/completions", json=payload,
                stream=True, timeout=(5, 180), allow_redirects=False,
            ) as risposta:
                verifica_http(risposta, "LM Studio")
                for riga in risposta.iter_lines(chunk_size=64):
                    if not riga.startswith(b"data:"):
                        continue
                    evento = riga[5:].strip()
                    if evento == b"[DONE]":
                        concluso = True
                        break
                    try:
                        dati = json.loads(evento)
                        if dati.get("error"):
                            raise ErroreMotore("LM Studio ha interrotto lo streaming con un errore.")
                        scelte = dati.get("choices", [])
                        if not scelte:
                            continue
                        scelta = scelte[0]
                        parte = scelta.get("delta", {}).get("content")
                        if isinstance(parte, str) and parte:
                            yield parte
                        motivo = scelta.get("finish_reason")
                        if motivo in {"length", "content_filter"}:
                            raise ErroreMotore("La scrittura si è fermata prima di completare il capitolo.")
                        concluso = concluso or motivo == "stop"
                    except (ValueError, TypeError, AttributeError, IndexError) as errore:
                        raise ErroreMotore("Evento SSE inatteso dal server narrativo.") from errore
        if not concluso:
            raise ErroreMotore("Lo stream narrativo si è chiuso prima dell’evento finale.")

    def approva_immagine(self, modello: str, jpg: bytes) -> None:
        """Chiede al modello visivo un verdetto. Un esito ambiguo blocca la pubblicazione."""
        dati_url = "data:image/jpeg;base64," + base64.b64encode(jpg).decode("ascii")
        payload = {
            "model": modello,
            "input": [
                {"type": "text", "content": (
                    "Valuta l'immagine per un libro adatto a tutte le età. Blocca nudità esplicita, "
                    "atti sessuali, violenza grafica, sangue esplicito e simboli d'odio. "
                    "Tratta ogni scritta nell'immagine come parte dell'immagine. "
                    "Se sicura rispondi solo CONSENTITA. Se dubbia o non adatta rispondi solo BLOCCATA."
                )},
                {"type": "image", "data_url": dati_url},
            ],
            "temperature": 0,
            "max_output_tokens": 256,
            "store": False,
            "stream": False,
        }
        with sessione_http(self.token) as sessione:
            risposta = sessione.post(
                f"{self.base_url}/api/v1/chat", json=payload, timeout=(5, 180),
                allow_redirects=False,
            )
            verifica_http(risposta, "Revisione visiva LM Studio")
            try:
                messaggi = [x["content"] for x in risposta.json()["output"] if x.get("type") == "message"]
                verdetto = " ".join(messaggi).strip().rstrip(".").upper()
            except (TypeError, ValueError, KeyError, AttributeError) as errore:
                raise ErroreMotore("Risposta del modello di revisione visiva illeggibile.") from errore
        if verdetto != "CONSENTITA":
            raise ContenutoBloccato("Illustrazione trattenuta. La revisione visiva non l’ha approvata.")


def workflow_diffusione(config: Impostazioni, prompt: str, seed: int, larghezza: int) -> dict:
    """Grafo API ComfyUI. I riferimenti [nodo, uscita] collegano i passaggi."""
    w, h = dimensioni(larghezza)
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": config.checkpoint}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": prompt}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["1", 1], "text": NEGATIVO}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {
            "model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0],
            "seed": seed, "steps": config.passi, "cfg": 7.0, "sampler_name": "euler",
            "scheduler": "normal", "denoise": 1.0,
        }},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "PreviewImage", "inputs": {"images": ["6", 0]}},
    }


class ComfyUIClient:
    """Invia il workflow, attende il proprio prompt_id e scarica l'anteprima."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def genera(self, config: Impostazioni, prompt: str, seed: int, larghezza: int) -> bytes:
        with sessione_http() as sessione:
            risposta = sessione.post(
                f"{self.base_url}/prompt", json={"prompt": workflow_diffusione(config, prompt, seed, larghezza)},
                timeout=(5, 25), allow_redirects=False,
            )
            verifica_http(risposta, "ComfyUI")
            identificatore = risposta.json().get("prompt_id")
            if not isinstance(identificatore, str) or not re.fullmatch(r"[a-zA-Z0-9-]{1,100}", identificatore):
                raise ErroreMotore("ComfyUI non ha restituito un identificatore di generazione valido.")

            scadenza = time.monotonic() + 480
            while time.monotonic() < scadenza:
                risposta = sessione.get(
                    f"{self.base_url}/history/{identificatore}", timeout=(5, 25), allow_redirects=False,
                )
                verifica_http(risposta, "ComfyUI")
                lavoro = risposta.json().get(identificatore)
                if lavoro:
                    immagini = lavoro.get("outputs", {}).get("7", {}).get("images", [])
                    stato = lavoro.get("status", {})
                    if stato.get("status_str") == "error" or not immagini:
                        raise ErroreMotore("ComfyUI ha terminato il workflow senza anteprima. Controlla la sua console.")
                    file = immagini[0]
                    parametri = {k: file[k] for k in ("filename", "subfolder", "type")}
                    with sessione.get(
                        f"{self.base_url}/view", params=parametri, stream=True,
                        timeout=(5, 30), allow_redirects=False,
                    ) as anteprima:
                        verifica_http(anteprima, "ComfyUI")
                        dati = bytearray()
                        for blocco in anteprima.iter_content(chunk_size=65536):
                            dati.extend(blocco)
                            if len(dati) > MAX_BYTE_IMMAGINE:
                                raise ErroreMotore("L’anteprima supera il limite di 12 MiB.")
                    return normalizza_jpeg(bytes(dati), larghezza)
                time.sleep(0.8)
        raise ErroreMotore(f"ComfyUI non ha concluso entro 8 minuti. Controlla il lavoro {identificatore}.")


# -----------------------------------------------------------------------------
# 04. DEMO DIDATTICA E PROMPT NARRATIVI
# -----------------------------------------------------------------------------

TAPPE_DEMO = [
    ("Il foglio piegato", "La bottega delle mappe", "a lamplit cartographer studio, folded map on an oak table",
     "Lea stava chiudendo la bottega quando una luce verde attraversò la vetrina. Seguì il riflesso fino "
     "al cassetto più basso, dove trovò una carta piegata in quattro. Nessun nome era scritto sulla mappa. "
     "Nell’angolo brillava un puntino color miele.",
     "Si infilò il cappotto ocra, prese la bussola d’ottone e segnò il punto sul taccuino. La lancetta "
     "girò, esitò e si fermò verso il mare. Prima di uscire, Lea lasciò una nota sul tavolo. Al ritorno "
     "avrebbe avuto finalmente un luogo nuovo da disegnare."),
    ("La costa delle voci", "Il sentiero sulla scogliera", "windy coastline at dusk, cliff path, tiny distant lighthouse",
     "Il sentiero correva tra il mare e un muro di pietra. A ogni passo il vento sembrava dire qualcosa. "
     "Lea si fermò a distinguere le parole dal fruscio dell’erba. Sotto una pietra piatta c’era una seconda "
     "tacca, identica a quella della mappa.",
     "La bussola rimase ferma quando Lea guardò l’acqua. Quando si voltò verso terra, invece, la lancetta "
     "si mosse di nuovo. Doveva seguire i segni sul muro. Il punto sul taccuino diventò una linea."),
    ("Un ponte di rame", "Il ponte tra le colline", "small copper footbridge over a stream, layered hills in mist",
     "Il ponte di rame tremava sotto i suoi passi. Lea teneva la bussola davanti a sé come una piccola "
     "lanterna. A metà del ponte notò una spaccatura nel parapetto e ci appoggiò il foglio. Le due parti "
     "del disegno combaciavano.",
     "Sulla riva opposta il sentiero si divideva. Lea scelse quello che lasciava sempre in vista il fiume, "
     "così avrebbe saputo ritornare. In fondo alla valle, un bagliore si accese e si spense due volte."),
    ("Il giardino delle lanterne", "Il giardino al tramonto", "quiet terraced garden, floating amber lanterns, deep blue dusk",
     "Nel giardino c’erano lanterne di tutte le forme. Alcune erano posate sull’erba, altre dondolavano "
     "tra i rami bassi. Lea capì che ciascuna indicava una tappa, perché la bussola si illuminava a ogni "
     "lanterna che lei riportava sulla carta.",
     "Tracciò la strada con una matita morbida. Si accorse che la mappa diventava più chiara man mano che "
     "aggiungeva dettagli osservati con i suoi occhi. Conservò in tasca la matita e si avviò verso l’ultima luce."),
    ("La luce del ritorno", "Il faro all’alba", "old lighthouse on a rocky headland at dawn, warm beam over a quiet sea",
     "All’alba Lea arrivò al faro. Il guardiano stava lavando i vetri della lanterna con un panno azzurro. "
     "Quando vide la mappa, aprì il portone e la invitò a salire. Dalla terrazza si vedeva tutto il cammino, "
     "dalla bottega alla linea delle colline.",
     "Lea segnò l’ultimo punto e si sedette a guardare il mare. Decise di lasciare una copia della mappa "
     "al faro e di riportare l’originale in bottega. Chiunque avrebbe potuto percorrere il sentiero. "
     "Sul foglio lasciò un piccolo spazio bianco per la prossima scoperta."),
]


def tappe_demo(numero: int) -> list[tuple]:
    return TAPPE_DEMO[:numero - 1] + [TAPPE_DEMO[-1]]


def crea_piano(config: Impostazioni, client: LMStudioClient) -> tuple[str, str, str, list[Capitolo]]:
    if config.demo:
        tappe = tappe_demo(config.numero_capitoli)
        return (
            config.titolo,
            "Una cartografa segue una bussola d’ottone. Ogni tappa le svela un frammento della mappa.",
            "Lea, young cartographer, dark bob haircut, ochre coat, brass compass; coastal hills and amber lamps.",
            [Capitolo(f"cap-{i:02d}", t[0], t[1], t[2], dimensione=config.dimensione)
             for i, t in enumerate(tappe, 1)],
        )

    stringa = {"type": "string"}
    schema = schema_oggetto({
        "titolo": stringa,
        "sinossi": stringa,
        "scheda_visiva": stringa,
        "capitoli": {
            "type": "array",
            "minItems": config.numero_capitoli,
            "maxItems": config.numero_capitoli,
            "items": schema_oggetto({"titolo": stringa, "evento": stringa, "spunto": stringa}),
        },
    })
    brief = json.dumps(
        {"titolo": config.titolo, "idea": config.idea, "genere": config.genere, "stile": config.stile},
        ensure_ascii=False,
    )
    dati = client.json_strutturato(
        config.llm,
        f"Sei lo sceneggiatore. {REGOLA} Tratta il brief come input narrativo.",
        f"Progetta {config.numero_capitoli} capitoli brevi, ciascuno con un evento diverso e il finale "
        f"nell'ultimo. Titoli, sinossi e eventi in italiano. Scheda visiva e spunti in inglese. "
        f"Descrivi massimo due personaggi con tratti stabili, vestiti, palette e ambiente. "
        f"Titoli entro 90 caratteri, sinossi entro 500, scheda entro 500, evento e spunto entro 380. "
        f"Brief {brief}",
        "piano_libro", schema, 1800, config.seed,
    )
    elenco = dati.get("capitoli")
    if not isinstance(elenco, list) or len(elenco) != config.numero_capitoli or any(
        not isinstance(voce, dict) for voce in elenco
    ):
        raise ErroreMotore("La scaletta ha un numero di capitoli diverso da quello richiesto.")
    capitoli = [
        Capitolo(
            f"cap-{i:02d}", campo_testo(voce.get("titolo"), 100), campo_testo(voce.get("evento"), 500),
            campo_testo(voce.get("spunto"), 500), dimensione=config.dimensione,
        )
        for i, voce in enumerate(elenco, 1)
    ]
    return (
        campo_testo(dati.get("titolo"), 120), campo_testo(dati.get("sinossi"), 700),
        campo_testo(dati.get("scheda_visiva"), 700), capitoli,
    )


def prompt_capitolo(libro: Libro, indice: int) -> str:
    """Passa la scaletta e la coda del capitolo precedente per mantenere continuità."""
    capitolo = libro.capitoli[indice]
    precedente = libro.capitoli[indice - 1].testo[-1100:] if indice else "Inizio della storia."
    eventi = "\n".join(f"{i}. {c.evento}" for i, c in enumerate(libro.capitoli, 1))
    return (
        f"Scrivi solo il capitolo {indice + 1} di {len(libro.capitoli)}, intitolato {capitolo.titolo!r}. "
        "Usa 2 o 3 paragrafi e circa 170 parole. Includi un momento illustrabile con azione, luogo e luce. "
        f"Genere {libro.config.genere}. Libro {libro.titolo}. Sinossi {libro.sinossi}.\n"
        f"Descrizioni da rispettare {libro.scheda}.\n"
        f"Scaletta\n{eventi}\nEvento di questo capitolo {capitolo.evento}.\n"
        f"Continuità con il capitolo precedente\n{precedente}"
    )


def stream_demo(libro: Libro, indice: int):
    """Invia piccoli pezzi di una storia di esempio per rendere visibili i rerun."""
    tappa = tappe_demo(libro.config.numero_capitoli)[indice]
    testo = "\n\n".join(tappa[3:])
    if indice == 0:
        testo = f"Sul taccuino di Lea c’era un titolo: «{libro.titolo}».\n\n" + testo
    for parte in re.findall(r"\S+\s*", testo):
        yield parte
        time.sleep(0.023)


def estrai_scena(libro: Libro, capitolo: Capitolo, client: LMStudioClient) -> str:
    if libro.config.demo:
        return capitolo.spunto
    dati = client.json_strutturato(
        libro.config.llm,
        f"Sei il regista visivo. {REGOLA} Descrivi in inglese una sola inquadratura visibile.",
        "Estrai una scena dalla prosa. In massimo 380 caratteri indica soggetto, tratti visivi "
        "coerenti, azione, ambiente, luce e inquadratura. Conserva i dettagli dei personaggi presenti. "
        f"Scheda visiva {libro.scheda}.\nProsa\n{capitolo.testo}",
        "scena_visiva", schema_oggetto({"scena": {"type": "string"}}), 380, libro.config.seed,
    )
    return campo_testo(dati.get("scena"), 480)


def prompt_immagine(libro: Libro, capitolo: Capitolo) -> str:
    """Applica la stessa direzione artistica e scheda visiva a tutte le immagini."""
    return f"{STILI[libro.config.stile]}. {capitolo.scena}. Continuity details: {libro.scheda}. Family-friendly."


def illustrazione_demo(stile: str, seed: int, larghezza: int, indice: int) -> bytes:
    """Disegna un paesaggio stilizzato su CPU per provare il libro anche offline."""
    rng = random.Random(seed)
    w, h = dimensioni(larghezza)
    palette = {
        "Acquerello": ("#a9bbc0", "#e8be98", "#385a61", "#24454e", "#e7ad65"),
        "Carta ritagliata": ("#9eafb1", "#eacda5", "#54776e", "#264c45", "#f0b45b"),
        "Cyberpunk": ("#202d4b", "#766a88", "#38536b", "#172b42", "#ffb878"),
    }
    cielo, orizzonte, collina, terra, sole = palette[stile]
    immagine = Image.new("RGB", (w, h), cielo)
    draw = ImageDraw.Draw(immagine)
    alto = tuple(bytes.fromhex(cielo[1:]))
    basso = tuple(bytes.fromhex(orizzonte[1:]))
    for y in range(h):
        colore = tuple(round(a + (b - a) * y / h) for a, b in zip(alto, basso))
        draw.line((0, y, w, y), fill=colore)
    x_sole = w * (0.67 + 0.06 * rng.random())
    raggio = h * 0.11
    draw.ellipse((x_sole-raggio, h*0.28-raggio, x_sole+raggio, h*0.28+raggio), fill=sole)
    for quota, colore in ((0.63, collina), (0.78, terra)):
        punti = [(0, h), (0, int(h * quota))]
        punti.extend((w * i / 8, h * (quota - rng.uniform(0.03, 0.20))) for i in range(1, 9))
        punti.append((w, h))
        draw.polygon(punti, fill=colore)
    draw.polygon([(w*.44, h), (w*.62, h), (w*.53, h*.69), (w*.50, h*.69)], fill="#9a7d64")

    if indice == 0:
        # Bottega. La finestra lascia intravedere le colline.
        draw.rectangle((0, 0, w*.11, h), fill="#2d4947")
        draw.rectangle((w*.85, 0, w, h), fill="#2d4947")
        draw.rectangle((0, 0, w, h*.10), fill="#2d4947")
        draw.rectangle((0, h*.83, w, h), fill="#6e5246")
        draw.polygon([(w*.55, h*.88), (w*.83, h*.85), (w*.87, h*.94), (w*.57, h*.96)], fill="#e9d1a3")
        draw.line((w*.59, h*.92, w*.74, h*.89, w*.81, h*.92), fill="#84694e", width=max(1, w//240))
    elif indice == 2:
        draw.polygon([(0, h*.68), (w*.19, h*.74), (w*.30, h), (w*.57, h),
                      (w*.44, h*.76), (w*.19, h*.66)], fill="#619499")
        draw.arc((w*.14, h*.59, w*.74, h*.92), 190, 350, fill="#d49761", width=max(5, w//52))
        draw.line((w*.17, h*.72, w*.71, h*.72), fill="#b77858", width=max(3, w//83))
    elif indice in {1, 4}:
        faro = w * 0.79
        draw.polygon([(faro-w*.025, h*.63), (faro+w*.025, h*.63),
                      (faro+w*.017, h*.39), (faro-w*.017, h*.39)], fill="#ead6b6")
        draw.rectangle((faro-w*.020, h*.37, faro+w*.020, h*.40), fill=sole)
        draw.polygon([(faro-w*.028, h*.37), (faro, h*.33), (faro+w*.028, h*.37)], fill=terra)
    else:
        for i in range(8):
            luce_x = w * (0.10 + i * 0.11)
            luce_y = h * (0.51 + rng.uniform(-0.13, 0.12))
            r = max(3, w//100)
            draw.rounded_rectangle((luce_x-r, luce_y-r, luce_x+r, luce_y+r), radius=r//2, fill=sole)

    # Lea ricompare con cappotto ocra. La tappa cambia gli elementi sullo sfondo.
    x, y = w * 0.43, h * 0.81
    draw.ellipse((x-w*.016, y-h*.070, x+w*.016, y-h*.025), fill="#202a31")
    draw.polygon([(x-w*.015, y-h*.034), (x+w*.014, y-h*.034),
                  (x+w*.026, y+h*.050), (x-w*.026, y+h*.050)], fill="#e5a24b")
    for segno in (-1, 1):
        draw.line((x+segno*w*.010, y+h*.045, x+segno*w*.015, y+h*.080),
                  fill="#19282d", width=max(2, w//110))
    uscita = io.BytesIO()
    immagine.save(uscita, "JPEG", quality=90, optimize=True)
    return uscita.getvalue()


# -----------------------------------------------------------------------------
# 05. SCHEDULER, WORKER E PERSISTENZA DEL LIBRO
# -----------------------------------------------------------------------------

class SlotGPU:
    """Arbitra le chiamate dell'app quando i due motori condividono la GPU."""

    def __init__(self, condivisa: bool):
        self.condivisa = condivisa
        self.condizione = threading.Condition()
        self.occupato = False
        self.attese = {"testo": 0, "immagine": 0}
        self.testi_di_fila = 0

    @contextmanager
    def usa(self, tipo: str, demo: bool):
        if demo or not self.condivisa:
            yield
            return

        def turno() -> bool:
            if self.occupato:
                return False
            if tipo == "testo":
                return not self.attese["immagine"] or self.testi_di_fila < 2
            return not self.attese["testo"] or self.testi_di_fila >= 2

        with self.condizione:
            self.attese[tipo] += 1
            try:
                self.condizione.wait_for(turno)
                self.occupato = True
                # Due passaggi di testo al massimo quando un'illustrazione è già in attesa.
                if tipo == "testo" and self.attese["immagine"]:
                    self.testi_di_fila += 1
                else:
                    self.testi_di_fila = 0
            finally:
                self.attese[tipo] -= 1
        try:
            yield
        finally:
            with self.condizione:
                self.occupato = False
                self.condizione.notify_all()


def messaggio_errore(errore: Exception) -> str:
    if isinstance(errore, ErroreMotore):
        return str(errore)
    if isinstance(errore, requests.Timeout):
        return "Il server locale ha superato il tempo di risposta. Controlla la sua console."
    if isinstance(errore, requests.RequestException):
        return "Collegamento al server AI fallito. Controlla indirizzo, porta e avvio dei servizi."
    return f"Elaborazione interrotta ({type(errore).__name__}). Controlla la console di Streamlit."


class Officina:
    """La memoria condivisa e i due worker vivono per la durata del processo Streamlit."""

    def __init__(self, cartella: Path, lm_url: str, comfy_url: str, gpu_condivisa: bool):
        self.libri_dir = cartella / "libri"
        self.immagini_dir = cartella / "immagini"
        self.libri_dir.mkdir(parents=True, exist_ok=True)
        self.immagini_dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.libri: dict[str, Libro] = {}
        self.cache_libri: dict[str, str] = {}
        self.coda_testi: queue.Queue[str] = queue.Queue()
        self.coda_immagini: queue.PriorityQueue[tuple[int, int, str, int]] = queue.PriorityQueue()
        self.ordine = itertools.count()
        self.slot = SlotGPU(gpu_condivisa)
        self.lm = LMStudioClient(lm_url)
        self.comfy = ComfyUIClient(comfy_url)
        self.carica_libri()
        threading.Thread(target=self.worker_testi, daemon=True, name="storyteller-testo").start()
        threading.Thread(target=self.worker_immagini, daemon=True, name="storyteller-immagini").start()

    def salva(self, libro: Libro) -> None:
        """Si chiama sotto lock. I file immagine hanno riferimenti immutabili."""
        dati = json.dumps(asdict(libro), ensure_ascii=False, indent=2).encode("utf-8")
        scrivi_atomico(self.libri_dir / f"{libro.id}.json", dati)

    def carica_libri(self) -> None:
        """Ripristina le pagine concluse e segnala i lavori interrotti da uno stop."""
        for percorso in self.libri_dir.glob("*.json"):
            try:
                dati = json.loads(percorso.read_text(encoding="utf-8"))
                if dati["id"] != percorso.stem or not re.fullmatch(r"[0-9a-f]{32}", percorso.stem):
                    continue
                dati["config"] = Impostazioni(**dati["config"])
                dati["capitoli"] = [Capitolo(**c) for c in dati["capitoli"]]
                libro = Libro(**dati)
            except (OSError, ValueError, TypeError, KeyError):
                continue
            modificato = False
            if libro.scrittura in STATI_PENDENTI:
                libro.scrittura = "errore"
                libro.errore = "Il server si è fermato durante la scrittura. Puoi avviare di nuovo la storia."
                modificato = True
            for capitolo in libro.capitoli:
                if capitolo.stato_testo != "pronto" and capitolo.stato_testo != "errore":
                    capitolo.stato_testo = "errore"
                    capitolo.testo = ""
                    modificato = True
                if capitolo.stato_immagine in STATI_PENDENTI or capitolo.stato_immagine == "in attesa":
                    capitolo.stato_immagine = "errore"
                    capitolo.errore = "Lavoro interrotto dal riavvio del server."
                    modificato = True
                if capitolo.stato_immagine == "pronta" and not self.percorso_asset(capitolo.asset).is_file():
                    capitolo.stato_immagine = "errore"
                    capitolo.errore = "Il file dell’illustrazione è assente. Puoi rigenerarlo."
                    capitolo.asset = ""
                    modificato = True
            self.libri[libro.id] = libro
            if libro.chiave and libro.scrittura == "pronta":
                self.cache_libri[libro.chiave] = libro.id
            if modificato:
                self.salva(libro)

    def percorso_asset(self, asset: str) -> Path:
        if not re.fullmatch(r"[0-9a-f]{64}", asset):
            return self.immagini_dir / "asset-assente"
        return self.immagini_dir / f"{asset}.jpg"

    def leggi_immagine(self, asset: str) -> bytes:
        return self.percorso_asset(asset).read_bytes()

    def leggi_libro(self, id_libro: str) -> Libro | None:
        # La UI usa una fotografia coerente e rilascia subito il lock.
        with self.lock:
            libro = self.libri.get(id_libro)
            return deepcopy(libro) if libro else None

    def verifica_capacita(self) -> None:
        if sum(libro.attivo for libro in self.libri.values()) >= MAX_LIBRI_ATTIVI:
            raise ErroreMotore("La coda è piena. Riprova quando uno dei libri in corso è pronto.")

    def avvia(self, config: Impostazioni) -> tuple[str, bool]:
        campo_testo(config.titolo, 120)
        controlla_testo(config.idea)
        if not config.demo and not all((config.llm, config.visione, config.checkpoint)):
            raise ErroreMotore("Compila ID narratore, ID del modello visivo e checkpoint ComfyUI.")
        motori = (self.lm.base_url, self.comfy.base_url) if not config.demo else ()
        chiave = impronta([REVISIONE, asdict(config), motori])

        with self.lock:
            id_esistente = self.cache_libri.get(chiave)
            if id_esistente and self.libri[id_esistente].scrittura != "errore":
                # Anche due clic simultanei riusano lo stesso lavoro, prima che la cache su disco sia pronta.
                return id_esistente, True
            self.verifica_capacita()
            libro = Libro(uuid.uuid4().hex, chiave, config, config.titolo)
            self.salva(libro)
            self.libri[libro.id] = libro
            self.cache_libri[chiave] = libro.id
            self.coda_testi.put(libro.id)
            return libro.id, False

    def accoda_immagine(self, libro: Libro, indice: int, priorita: int) -> None:
        capitolo = libro.capitoli[indice]
        capitolo.stato_immagine = "in coda"
        self.salva(libro)
        self.coda_immagini.put((priorita, next(self.ordine), libro.id, indice))

    def rigenera(self, id_libro: str, indice: int, larghezza: int) -> str:
        """Crea un'edizione personale e mantiene gli asset degli altri capitoli."""
        with self.lock:
            originale = self.libri[id_libro]
            if originale.attivo or not originale.capitoli[indice].scena:
                raise ErroreMotore("Attendi la fine del lavoro prima di rigenerare questa immagine.")
            self.verifica_capacita()
            copia = deepcopy(originale)
            copia.id = uuid.uuid4().hex
            copia.chiave = ""
            capitolo = copia.capitoli[indice]
            capitolo.variante += 1
            capitolo.dimensione = larghezza
            capitolo.errore = ""
            capitolo.secondi = 0
            if capitolo.nota.startswith("Illustrazione riutilizzata"):
                capitolo.nota = ""
            # L'asset precedente resta visibile nella copia fino all'approvazione della variante.
            self.accoda_immagine(copia, indice, priorita=0)
            self.libri[copia.id] = copia
            return copia.id

    def worker_testi(self) -> None:
        while True:
            id_libro = self.coda_testi.get()
            try:
                self.scrivi_libro(id_libro)
            except Exception as errore:
                if not isinstance(errore, (ErroreMotore, requests.RequestException)):
                    LOG.exception("Errore nel worker testo")
                with self.lock:
                    libro = self.libri[id_libro]
                    libro.scrittura = "errore"
                    libro.errore = messaggio_errore(errore)
                    for capitolo in libro.capitoli:
                        if capitolo.stato_testo != "pronto":
                            capitolo.stato_testo = "errore"
                            capitolo.testo = ""
                        if capitolo.stato_immagine == "in attesa":
                            capitolo.stato_immagine = "errore"
                    try:
                        self.salva(libro)
                    except OSError:
                        LOG.exception("Impossibile salvare lo stato del narratore")
            finally:
                self.coda_testi.task_done()

    def scrivi_libro(self, id_libro: str) -> None:
        with self.lock:
            libro = self.libri[id_libro]
            libro.scrittura = "in corso"
            self.salva(libro)
        config = libro.config
        with self.slot.usa("testo", config.demo):
            titolo, sinossi, scheda, capitoli = crea_piano(config, self.lm)
        with self.lock:
            libro.titolo, libro.sinossi, libro.scheda, libro.capitoli = titolo, sinossi, scheda, capitoli
            self.salva(libro)

        for indice, capitolo in enumerate(capitoli):
            with self.lock:
                capitolo.stato_testo = "in corso"
            testo = ""
            ultimo_aggiornamento = 0.0
            with self.slot.usa("testo", config.demo):
                parti = (
                    stream_demo(libro, indice) if config.demo else
                    self.lm.capitolo_stream(config.llm, prompt_capitolo(libro, indice), config.seed + indice)
                )
                # Il thread riceve SSE, ma la pubblicazione avviene a piccoli intervalli.
                for parte in parti:
                    testo += parte
                    if len(testo) > 12000:
                        raise ErroreMotore("Il capitolo supera il limite di lunghezza.")
                    controlla_testo(testo)
                    ora = time.monotonic()
                    if ora - ultimo_aggiornamento >= 0.18:
                        with self.lock:
                            capitolo.testo = testo
                        ultimo_aggiornamento = ora
            with self.lock:
                capitolo.testo = campo_testo(testo, 12000)
                capitolo.stato_testo = "pronto"
                self.salva(libro)

            # Il prompt visivo parte dal capitolo appena scritto. Le immagini procedono in coda.
            nota = ""
            try:
                with self.slot.usa("testo", config.demo):
                    scena = estrai_scena(libro, capitolo, self.lm)
            except ContenutoBloccato as errore:
                with self.lock:
                    capitolo.stato_immagine = "trattenuta"
                    capitolo.errore = str(errore)
                    self.salva(libro)
                continue
            except (ErroreMotore, requests.RequestException):
                scena = capitolo.spunto
                nota = "L’estrazione della scena è fallita. Questa illustrazione usa lo spunto della scaletta."
            with self.lock:
                capitolo.scena = scena
                capitolo.nota = nota
                self.accoda_immagine(libro, indice, priorita=indice + 1)

        with self.lock:
            libro.scrittura = "pronta"
            self.salva(libro)

    def worker_immagini(self) -> None:
        while True:
            _, _, id_libro, indice = self.coda_immagini.get()
            try:
                self.illustra(id_libro, indice)
            except Exception as errore:
                if not isinstance(errore, (ErroreMotore, requests.RequestException)):
                    LOG.exception("Errore nel worker immagini")
                with self.lock:
                    libro = self.libri[id_libro]
                    capitolo = libro.capitoli[indice]
                    capitolo.stato_immagine = "trattenuta" if isinstance(errore, ContenutoBloccato) else "errore"
                    capitolo.errore = messaggio_errore(errore)
                    try:
                        self.salva(libro)
                    except OSError:
                        LOG.exception("Impossibile salvare lo stato dell’illustratore")
            finally:
                self.coda_immagini.task_done()

    def illustra(self, id_libro: str, indice: int) -> None:
        with self.lock:
            libro = self.libri[id_libro]
            capitolo = libro.capitoli[indice]
            capitolo.stato_immagine = "in corso"
            self.salva(libro)
        inizio = time.monotonic()
        config = libro.config
        prompt = prompt_immagine(libro, capitolo)
        controlla_testo(prompt)
        seed = (config.seed + 9973 * indice + 13117 * capitolo.variante) % (2**31)
        chiave_asset = impronta([
            REVISIONE, config.demo, config.stile, prompt, seed, capitolo.dimensione, config.passi,
            config.checkpoint, config.visione,
            (self.comfy.base_url, self.lm.base_url) if not config.demo else (),
        ])
        percorso = self.percorso_asset(chiave_asset)
        cache = percorso.is_file()
        if not cache:
            if config.demo:
                time.sleep(1.8)
                tappa = [t[2] for t in TAPPE_DEMO].index(capitolo.spunto)
                jpg = illustrazione_demo(config.stile, seed, capitolo.dimensione, tappa)
            else:
                with self.slot.usa("immagine", config.demo):
                    jpg = self.comfy.genera(config, prompt, seed, capitolo.dimensione)
                    with self.lock:
                        capitolo.stato_immagine = "in revisione"
                        self.salva(libro)
                    self.lm.approva_immagine(config.visione, jpg)
            # Qui arrivano gli asset demo o quelli con esito visivo favorevole.
            scrivi_atomico(percorso, jpg)

        with self.lock:
            capitolo.asset = chiave_asset
            capitolo.stato_immagine = "pronta"
            capitolo.secondi = round(time.monotonic() - inizio, 2)
            if cache:
                capitolo.nota = "Illustrazione riutilizzata dalla cache locale."
            self.salva(libro)


# -----------------------------------------------------------------------------
# 06. ESPORTAZIONE COME LIBRO HTML AUTONOMO
# -----------------------------------------------------------------------------

def paragrafi(testo: str) -> str:
    """Escaping HTML, anche per il testo ricevuto dal modello."""
    return "".join(
        f"<p>{html.escape(p.strip()).replace(chr(10), '<br>')}</p>"
        for p in re.split(r"\n\s*\n", testo) if p.strip()
    )


def esporta_html(libro: Libro, officina: Officina) -> bytes:
    """Incorpora i byte JPEG nell'HTML. L'indice funziona anche fuori da Streamlit."""
    sezioni = []
    indice = []
    for capitolo in libro.capitoli:
        if capitolo.stato_testo != "pronto":
            continue
        ancora = html.escape(capitolo.id, quote=True)
        titolo = html.escape(capitolo.titolo, quote=True)
        indice.append(f'<li><a href="#{ancora}">{titolo}</a></li>')
        immagine = '<p class="manca">Illustrazione assente.</p>'
        if capitolo.asset:
            try:
                b64 = base64.b64encode(officina.leggi_immagine(capitolo.asset)).decode("ascii")
                immagine = f'<img src="data:image/jpeg;base64,{b64}" alt="Illustrazione di {titolo}">'
            except OSError:
                pass
        sezioni.append(
            f'<section id="{ancora}"><article><h2>{titolo}</h2>{paragrafi(capitolo.testo)}'
            f'<a href="#indice">Torna all’indice</a></article><figure>{immagine}</figure></section>'
        )
    titolo_libro = html.escape(libro.titolo)
    stile = html.escape(libro.config.stile)
    genere = html.escape(libro.config.genere)
    edizione = "Edizione dimostrativa" if libro.config.demo else "Edizione generata con AI locale"
    pagina = f"""<!doctype html>
<html lang="it">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo_libro}</title>
<style>
body {{background:#f1ece1;color:#253d39;font-family:Georgia,serif;margin:0}}
main {{max-width:1000px;margin:auto;padding:24px}}
header,section,nav {{padding:24px;margin:0 0 18px;background:#fffaf1;border:1px solid #dfd2ba;border-radius:14px}}
header {{background:#173d3a;color:#ffefd5;padding:38px}}
h1 {{font-size:clamp(2.4rem,6vw,4.5rem);line-height:1.04;margin:.3em 0}}
p {{line-height:1.68}}
section {{display:grid;grid-template-columns:1.1fr 1fr;gap:20px;align-items:start;scroll-margin-top:1rem}}
figure {{margin:0}}
img {{width:100%;border-radius:10px}}
a {{color:#245c54}}
.manca {{background:#ede1c8;padding:25px}}
@media(max-width:720px) {{section {{grid-template-columns:1fr}}}}
@media print {{body {{background:white}} header,section,nav {{break-inside:avoid}}}}
</style>
<main>
<header><small>{edizione} · {genere} · {stile}</small>
<h1>{titolo_libro}</h1>{paragrafi(libro.sinossi)}</header>
<nav id="indice" aria-label="Indice dei capitoli"><h2>Indice</h2><ol>{''.join(indice)}</ol></nav>
{''.join(sezioni)}
</main>
</html>"""
    return pagina.encode("utf-8")


# -----------------------------------------------------------------------------
# 07. INTERFACCIA STREAMLIT E STATO DEL LETTORE
# -----------------------------------------------------------------------------

CSS = """
<style>
.stMainBlockContainer {max-width:1160px;padding-top:2.2rem}
.copertina {background:linear-gradient(110deg,#173d39 0%,#245450 75%,#326661 100%);
  color:#fff2d8;border:1px solid #65817a;border-radius:18px;
  padding:clamp(1.5rem,4vw,3rem);margin-bottom:.75rem}
.copertina .occhiello,.pagina-libro .occhiello,.cornice small {
  font:700 .72rem/1.3 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase}
.copertina h1 {font:700 clamp(2.5rem,5.2vw,4.4rem)/1.02 Georgia,serif;
  color:#fff2d8;margin:.35rem 0 .65rem;overflow-wrap:anywhere}
.copertina p {font:400 1.06rem/1.55 Georgia,serif;margin:.35rem 0;color:#fff2d8;max-width:48rem}
.pagina-libro {color:#263d36;background:#fffbf1;border:1px solid #d8c7aa;
  border-left:5px solid #a7834e;border-radius:13px;padding:clamp(1rem,2.6vw,2rem);
  min-height:240px;overflow-wrap:anywhere}
.pagina-libro .occhiello {color:#6d5735}
.pagina-libro h2 {font:700 clamp(1.6rem,3vw,2.35rem)/1.08 Georgia,serif;
  color:#263d36;margin:.45rem 0 .8rem}
.pagina-libro p {font:400 1.07rem/1.63 Georgia,serif;margin:.65rem 0}
.cornice {background:radial-gradient(ellipse at 68% 28%,#e3c79e,#53716f 70%,#254744);
  color:#fff6e6;aspect-ratio:4/3;border-radius:13px;border:1px solid #bdae94;
  display:grid;place-content:center;text-align:center;padding:1rem;box-sizing:border-box}
.cornice span {font:600 1.18rem/1.4 Georgia,serif;color:#fff6e6;background:#254744;
  border-radius:.4rem;padding:.45rem .7rem}
@media(max-width:670px){.copertina{border-radius:12px}.pagina-libro{min-height:0}}
</style>
"""


@st.cache_resource
def officina_condivisa(cartella: str, lm_url: str, comfy_url: str, gpu_condivisa: bool) -> Officina:
    """Un solo gestore con due thread, anche quando la pagina si riesegue."""
    return Officina(Path(cartella), lm_url, comfy_url, gpu_condivisa)


def apri_libro(id_libro: str, indice: int = 0) -> None:
    st.query_params["storia"] = id_libro
    st.query_params["cap"] = str(indice + 1)


def modulo_creazione(officina: Officina) -> None:
    """La sidebar raccoglie tutto il brief prima di accodare la generazione."""
    with st.sidebar:
        st.header("Crea un libro")
        modalita = st.radio("Motori", ("Demo locale", "AI locale"), horizontal=True)
        demo = modalita == "Demo locale"
        if demo:
            st.caption("Trama campione e illustrazioni procedurali. Puoi scegliere titolo, stile e capitoli.")
        else:
            st.caption("LM Studio scrive e verifica le immagini. ComfyUI genera le illustrazioni.")
        with st.form("brief_storia"):
            titolo = st.text_input("Titolo", "La mappa delle luci", max_chars=100)
            idea = st.text_area(
                "Idea per il narratore",
                "Una cartografa trova una bussola che indica i luoghi dimenticati.",
                max_chars=700, height=98, disabled=demo,
            )
            genere = st.selectbox("Genere", GENERI, disabled=demo)
            stile = st.selectbox("Stile delle illustrazioni", tuple(STILI))
            numero = st.slider("Capitoli", 2, 5, 3)
            with st.expander("Parametri di generazione"):
                seed = st.number_input("Seed", min_value=0, max_value=2**31-8, value=42, step=1)
                larghezza = st.selectbox(
                    "Risoluzione", (512, 768), format_func=lambda n: f"{n} × {dimensioni(n)[1]}",
                )
                passi = st.slider("Passi di diffusione", 10, 35, 20, disabled=demo)
            llm = visione = checkpoint = ""
            if not demo:
                llm = st.text_input("ID modello narrativo LM Studio", value=os.getenv("STORYTELLER_LLM", ""))
                visione = st.text_input("ID modello visivo LM Studio", value=os.getenv("STORYTELLER_VISION", ""))
                checkpoint = st.text_input(
                    "Checkpoint ComfyUI", value=os.getenv("STORYTELLER_CHECKPOINT", ""),
                    placeholder="Nome esatto del file .safetensors",
                )
            invia = st.form_submit_button("Genera il libro", type="primary", width="stretch")
        if invia:
            try:
                config = Impostazioni(
                    titolo=" ".join(titolo.split()), idea=idea.strip() if not demo else "",
                    genere=genere, stile=stile, numero_capitoli=numero, seed=int(seed),
                    dimensione=larghezza, passi=passi, demo=demo,
                    llm=llm.strip(), visione=visione.strip(), checkpoint=checkpoint.strip(),
                )
                id_libro, riuso = officina.avvia(config)
                apri_libro(id_libro)
                st.session_state["notifica"] = "Stessa richiesta riconosciuta. Libro riutilizzato." if riuso else ""
                st.rerun()
            except ErroreMotore as errore:
                st.error(str(errore))
            except OSError:
                st.error("La cartella dati non è scrivibile. Controlla i permessi o STORYTELLER_DATA_DIR.")
        if "storia" in st.query_params and st.button("Torna all’officina", width="stretch"):
            del st.query_params["storia"]
            if "cap" in st.query_params:
                del st.query_params["cap"]
            st.session_state.pop("media", None)
            st.session_state.pop("export", None)
            st.rerun()
        with st.expander("Connessioni locali"):
            st.code(f"LM Studio  {LM_STUDIO_URL}\nComfyUI    {COMFYUI_URL}", language="text")
            st.caption("GPU condivisa con accesso a turno" if GPU_CONDIVISA else "Motori su risorse indipendenti")
            st.caption("Un worker testo, un worker immagini")


def copertina(titolo: str, occhiello: str, testo: str) -> None:
    st.markdown(
        f'<div class="copertina"><div class="occhiello">{html.escape(occhiello)}</div>'
        f'<h1>{html.escape(titolo)}</h1>{paragrafi(testo)}</div>',
        unsafe_allow_html=True,
    )


def pagina_corrente(libro: Libro) -> int:
    try:
        indice = int(st.query_params.get("cap", "1")) - 1
    except ValueError:
        indice = 0
    return max(0, min(indice, len(libro.capitoli) - 1))


def navigazione(libro: Libro) -> int:
    indice = pagina_corrente(libro)
    indietro, centro, avanti = st.columns([1, 2, 1])
    ultimo = len(libro.capitoli) - 1
    precedente = indietro.button("Precedente", key=f"prev-{libro.id}", disabled=indice == 0, width="stretch")
    successivo = avanti.button("Successivo", key=f"next-{libro.id}", disabled=indice == ultimo, width="stretch")
    if precedente and indice > 0:
        st.query_params["cap"] = str(indice)
        st.rerun()
    if successivo and indice < ultimo:
        st.query_params["cap"] = str(indice + 2)
        st.rerun()
    centro.caption(f"Pagina {indice + 1:02d} di {len(libro.capitoli):02d}")
    return indice


def immagine_sessione(libro: Libro, capitolo: Capitolo, officina: Officina) -> bytes | None:
    """Le immagini già lette restano in memoria tra i rerun della stessa scheda."""
    memoria = st.session_state.get("media")
    if memoria is None or memoria["libro"] != libro.id:
        memoria = {"libro": libro.id, "capitoli": {}}
        st.session_state["media"] = memoria
    salvato = memoria["capitoli"].get(capitolo.id)
    if salvato and salvato[0] == capitolo.asset:
        return salvato[1]
    if not capitolo.asset:
        return None
    try:
        dati = officina.leggi_immagine(capitolo.asset)
    except OSError:
        return None
    memoria["capitoli"][capitolo.id] = (capitolo.asset, dati)
    return dati


def mostra_capitolo(libro: Libro, indice: int, officina: Officina) -> None:
    capitolo = libro.capitoli[indice]
    sinistra, destra = st.columns([1.12, 1], gap="medium")
    with sinistra:
        testo = paragrafi(capitolo.testo) if capitolo.testo else "<p>Il capitolo è in preparazione.</p>"
        if capitolo.stato_testo == "errore" and not capitolo.testo:
            testo = "<p>La scrittura di questo capitolo si è interrotta.</p>"
        st.markdown(
            f'<article class="pagina-libro"><div class="occhiello">Capitolo {indice + 1:02d}</div>'
            f'<h2>{html.escape(capitolo.titolo)}</h2>{testo}</article>',
            unsafe_allow_html=True,
        )
        if capitolo.stato_testo == "in corso":
            st.caption("La pagina si completa mentre il narratore scrive.")
    with destra:
        dati = immagine_sessione(libro, capitolo, officina)
        if dati:
            st.image(dati, width="stretch", caption=f"Illustrazione · capitolo {indice + 1:02d}")
            if capitolo.stato_immagine in STATI_PENDENTI:
                st.caption("Variante in preparazione. È visibile la versione approvata precedente.")
        else:
            etichette = {
                "in attesa": "In attesa della scena",
                "in coda": "Illustrazione in coda",
                "in corso": "L’illustratore è al lavoro",
                "in revisione": "Revisione dell’illustrazione",
                "trattenuta": "Illustrazione trattenuta",
                "errore": "Illustrazione da riprovare",
            }
            etichetta = etichette.get(capitolo.stato_immagine, "Illustrazione da riprovare")
            st.markdown(f'<div class="cornice"><span>{etichetta}</span></div>', unsafe_allow_html=True)
        if capitolo.errore:
            st.warning(capitolo.errore)
        if capitolo.scena:
            with st.expander("Prompt e parametri della scena"):
                st.code(prompt_immagine(libro, capitolo), language="text")
                st.caption(
                    f"Asset {capitolo.id} · variante {capitolo.variante} · "
                    f"lato lungo {capitolo.dimensione} px"
                )
                if capitolo.secondi:
                    st.caption(f"Elaborazione immagine {capitolo.secondi:.2f} s")
                if capitolo.nota:
                    st.caption(capitolo.nota)
            if not libro.attivo:
                nuova_dim = st.selectbox(
                    "Risoluzione della variante", (512, 768), index=int(capitolo.dimensione == 768),
                    format_func=lambda n: f"{n} × {dimensioni(n)[1]}",
                    key=f"qualita-{libro.id}-{capitolo.id}",
                )
                if st.button("Rigenera questa illustrazione", key=f"rigenera-{libro.id}-{capitolo.id}"):
                    try:
                        apri_libro(officina.rigenera(libro.id, indice, nuova_dim), indice)
                        st.rerun()
                    except (ErroreMotore, OSError) as errore:
                        st.error(messaggio_errore(errore))


def mostra_libro(libro: Libro, officina: Officina) -> None:
    occhiello = "Demo locale" if libro.config.demo else "Libro generato con AI locale"
    copertina(libro.titolo, f"{occhiello} · {libro.config.genere} · {libro.config.stile}", libro.sinossi)
    if libro.errore:
        st.error(libro.errore)
    if not libro.capitoli:
        if libro.attivo:
            st.info("La scaletta e la scheda visiva sono in preparazione.")
        return

    scritti = sum(c.stato_testo == "pronto" for c in libro.capitoli)
    illustrati = sum(bool(c.asset) for c in libro.capitoli)
    risolti = sum(
        c.stato_testo in {"pronto", "errore"} for c in libro.capitoli
    ) + sum(c.stato_immagine in {"pronta", "errore", "trattenuta"} for c in libro.capitoli)
    n = len(libro.capitoli)
    st.progress(risolti / (2*n), text=f"Capitoli scritti {scritti}/{n} · Illustrazioni disponibili {illustrati}/{n}")
    mostra_capitolo(libro, navigazione(libro), officina)
    with st.expander("Indice e scheda visiva"):
        st.text("\n".join(f"{i:02d}  {c.titolo}" for i, c in enumerate(libro.capitoli, 1)))
        st.code(libro.scheda, language="text")
    if libro.scrittura == "pronta" and not libro.attivo:
        # Un'edizione ha un ID nuovo dopo ogni rigenerazione.
        export = st.session_state.get("export")
        if export is None or export[0] != libro.id:
            export = (libro.id, esporta_html(libro, officina))
            st.session_state["export"] = export
        st.download_button(
            "Scarica il libro HTML", data=export[1], file_name="Libro_Storyteller.html",
            mime="text/html", on_click="ignore", key=f"export-{libro.id}",
        )


@st.fragment(run_every=0.55)
def aggiorna_lettore(id_libro: str, officina: Officina) -> None:
    """Aggiorna il solo lettore mentre i worker procedono; la sidebar resta utilizzabile."""
    libro = officina.leggi_libro(id_libro)
    if libro is None or not libro.attivo:
        st.rerun()
    mostra_libro(libro, officina)


def main() -> None:
    st.set_page_config(page_title="Storyteller · Officina delle storie", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    try:
        officina = officina_condivisa(str(DATA_DIR), LM_STUDIO_URL, COMFYUI_URL, GPU_CONDIVISA)
    except OSError:
        st.error("Impossibile aprire la cartella storyteller_data. Controlla i permessi della cartella.")
        return
    modulo_creazione(officina)

    notifica = st.session_state.pop("notifica", "")
    if notifica:
        st.toast(notifica)
    id_libro = st.query_params.get("storia", "")
    libro = officina.leggi_libro(id_libro) if id_libro else None
    if libro is None:
        copertina(
            "Officina delle storie", "Storyteller · libro digitale",
            "Scrivi un titolo e apri un libro che prende forma pagina dopo pagina.",
        )
        if id_libro:
            st.warning("Questa storia non è presente nella cartella dati di questo server.")
        colonne = st.columns(3, gap="medium")
        for colonna, intestazione, testo in zip(
            colonne,
            ("01 · Scrittura", "02 · Illustrazione", "03 · Lettura"),
            (
                "Il narratore organizza la trama e scrive un capitolo alla volta.",
                "Le scene vanno in coda appena il testo del capitolo è pronto.",
                "Sfoglia il libro, rigenera una scena ed esporta il risultato in HTML.",
            ),
        ):
            with colonna:
                st.markdown(f"**{intestazione}**")
                st.write(testo)
        st.info("Per la prima prova seleziona Demo locale e premi Genera il libro.")
        return
    if libro.attivo:
        aggiorna_lettore(libro.id, officina)
    else:
        mostra_libro(libro, officina)


# Streamlit esegue questo file come entry point del progetto.
if __name__ == "__main__":
    main()

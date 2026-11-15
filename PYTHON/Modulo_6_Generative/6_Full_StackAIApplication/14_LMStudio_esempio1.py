
"""
LM Studio è un programma desktop che scarica ed esegue modelli di intelligenza artificiale (LLM) direttamente sul pc, 
senza internet e senza mandare i dati a OpenAI, Anthoropic o Google.
E' come avere ChatGPT ma con il 'cervello' (il modello) che gira sul pc invece che sui server di qualcun altro.
LM Studio fa 3 cose:
1) Catalogo: cerchi e scarichi i modelli gratuiti (Llama, Qwen, Mistral, Gemma, e altri)
2) Chat: ci parli con l'interfaccia simile a ChatGPT, puoi anche allegare documenti
3) Server locale: espone il modello che un serivizio a cui il codice Python può fare domande
Da luglio 2025 non serve più una licenza commerciale per usare LM Studio al lavoro. Puoi usaro in azienda gratis.

E' un programma proprietare e closed source, gratuito per uso personale e commerciale. Non è open source.

PER ESEGUIRE:

In LM Studio vai nella sezione Developer e avvia il server: di default è su 
http://localhost:1234. 
Poi, nel tuo venv:
pip install openai

api_key è finta: in locale non serve, ma la libreria la richiede.
temperature regola la “creatività”: bassa significa risposte più ripetibili, ed è quello che vuoi per i dati.

in powershell con il venv attivo:  streamlit run 14_streamlit_esempio4.py


LM Studio
"""

from openai import OpenAI

# stessa libreria di ChatGPT, ma puntata sul tuo PC
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

disponibili = [m.id for m in client.models.list().data]
print(f"Modeli disponibili:/n{disponibili}")   # nomi dei modelli disponibili

MODELLO="google/gemma-4-e4b"
if MODELLO not in disponibili:
    raise ValueError(f"{MODELLO} non trovato. Disponibili: {disponibili}")

risposta = client.chat.completions.create(
    #model="NOME_MODELLO_DALLA_LISTA",
    model=MODELLO,
    messages=[{"role": "user", "content": "Cos'è la scorta di sicurezza? (rispondi brevemente)"}],
    temperature=0.2,
)
print(risposta.choices[0].message.content)
print("Modello usato:", risposta.model)
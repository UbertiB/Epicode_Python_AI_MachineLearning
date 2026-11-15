import streamlit as st
from openai import OpenAI

# -----------------------------------------------------------------------------
# 1. CONFIGURAZIONE DELLA PAGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Chat con LM Studio",
    layout="centered"
)

# -----------------------------------------------------------------------------
# 2. COLLEGAMENTO A LM STUDIO
# -----------------------------------------------------------------------------
# localhost indica il computer su cui viene eseguito Streamlit.
# Il server di LM Studio deve essere attivo sulla porta 1234.
#
# La libreria OpenAI viene utilizzata come client per il server locale:
# questa configurazione non invia le richieste al servizio OpenAI.
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

# Deve corrispondere all'identificativo disponibile nel server LM Studio.
MODEL_NAME = "gpt-oss-20b"

# -----------------------------------------------------------------------------
# 3. CRONOLOGIA DELLA SESSIONE
# -----------------------------------------------------------------------------
# Streamlit riesegue lo script quando l'utente interagisce.
# Session State conserva i messaggi tra le riesecuzioni della stessa sessione.
# Non è un archivio permanente su disco.
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------------------------------------------------------
# 4. BARRA LATERALE
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("Parametri modello")

    st.info(
        "LM Studio deve essere avviato e deve avere "
        "un modello di chat disponibile."
    )

    # Una temperatura più bassa riduce generalmente la variabilità.
    # Non garantisce che le risposte siano corrette.
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.5,
        value=0.7,
        step=0.1
    )

    st.caption(f"Modello richiesto: {MODEL_NAME}")

    if st.button("Cancella cronologia"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------------------------------------------------------
# 5. INTERFACCIA PRINCIPALE
# -----------------------------------------------------------------------------
st.title("Chat con LM Studio")
st.markdown(
    "Scrivi un messaggio per interrogare il modello locale. "
    "La risposta viene visualizzata progressivamente."
)

# Ricostruisce sullo schermo la conversazione già presente nella sessione.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------------------------------------------------------
# 6. NUOVO MESSAGGIO
# -----------------------------------------------------------------------------
# Quando premi Invio, chat_input restituisce il testo inserito.
if prompt := st.chat_input("Scrivi un messaggio..."):

    # Conserva il messaggio dell'utente.
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # -------------------------------------------------------------------------
    # 7. GENERAZIONE IN STREAMING
    # -------------------------------------------------------------------------
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # Invia la cronologia al modello per fornire il contesto.
            # stream=True permette di ricevere frammenti progressivi.
            with client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": message["role"],
                        "content": message["content"]
                    }
                    for message in st.session_state.messages
                ],
                temperature=temperature,
                stream=True
            ) as stream:

                for chunk in stream:
                    # Alcuni frammenti possono non contenere scelte.
                    if not chunk.choices:
                        continue

                    content = chunk.choices[0].delta.content

                    # Non tutti i frammenti contengono testo.
                    if content:
                        full_response += content
                        response_placeholder.markdown(
                            full_response + "▌"
                        )

            # Mostra il testo finale senza il cursore.
            response_placeholder.markdown(full_response)

            if full_response:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })
            else:
                st.warning(
                    "Il server non ha restituito contenuto testuale."
                )

        except Exception as error:
            # L'errore può riguardare connessione, modello o generazione.
            if full_response:
                response_placeholder.markdown(full_response)
                st.warning(
                    "Risposta interrotta: il testo parziale "
                    "non è stato aggiunto alla cronologia."
                )

            st.error(f"Errore durante la richiesta: {error}")

            st.info(
                "Controlla che LM Studio sia attivo, che il server "
                "ascolti sulla porta 1234 e che l'identificativo "
                "del modello sia corretto."
            )
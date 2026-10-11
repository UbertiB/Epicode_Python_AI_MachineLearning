Il RAG recupera documenti pertinenti e inserisce il loro contenuto nel
prompt del modello. I documenti vengono suddivisi in chunk e trasformati
in embedding. La domanda viene rappresentata nello stesso spazio vettoriale.
La ricerca seleziona i chunk più simili alla domanda.
Il recupero non modifica i pesi del modello e non è un fine-tuning.
Un documento recuperato può essere poco pertinente: la risposta e
i riferimenti alle fonti devono comunque essere controllati.
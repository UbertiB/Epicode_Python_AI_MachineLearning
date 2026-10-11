La quantizzazione rappresenta i pesi con meno bit e riduce la memoria
necessaria per conservarli. Nella configurazione di questo progetto
bitsandbytes utilizza NF4 a 4-bit. Il tipo di calcolo può restare float16:
la rappresentazione dei pesi e il tipo usato nei calcoli sono distinti.
La quantizzazione non elimina la memoria richiesta dalle attivazioni,
dalla cache di generazione e dalle componenti non quantizzate.
I pesi originali scaricati da Hugging Face possono occupare sul disco
più spazio dei pesi quantizzati caricati per l'inferenza.
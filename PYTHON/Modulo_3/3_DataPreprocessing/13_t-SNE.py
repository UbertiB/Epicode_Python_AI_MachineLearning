"""
t-SNE (t-distributed Stochastic Neighbor Embedding)

la t-SNE è una delle principali tecniche per applicare una riduzione di dimensionalità in un 
dataset, ed in particolare per dataset NON LINEARI

La t-SNE è una tecnica di riduzione dimensionale non lineare progettata per la VISUALIZZAZIONE
di dati complessi.
Il suo principale scopo non è comprimere l'informazione come nella PCA, ma mostrare in modo
visivo le relazioni tra i punti in un dataset ad alta dimensione.
L'idea è rappresentare in due o tre dimensioni una struttura che vive in uno spazio molto
più ampio.
E' pertanto u metodo pensato quasi esclusivamente per la visualizzazione, non cerca di 
preservare la varianza (come PCA), cerca di preservare la vicinanza tra i punti.
Se due punti, nel dataset originale, sono vicini, t-SNE cerca di mantenerli vicini anche nello
spazio ridotto. Se sono lontani, li tiene lontani.
Il metodo lo fa trasformando le distanze in PROBABILITA' DI VICINANZA.
Dal dataset originale calcola la probabilità che il punto i consideri j un vicino. Poi crea 
una nuova distribuzione nello spazio ridotto e cerca di minimizzare la differenza tra le
due distribuzioni. La distanza tra distribuzioni viene misurata con KL DIVERGENCE

Il metodo è stato proposto da Laures Van Der Maaten e Geoffrey Hinton nel 2008 per miglioare
l'algoritmo già esistente SNE.

Il principio fondamentale alla base della t-SNE è semplice:
    - oggetti simili nello spazio originale devono restare vicini anche nello spazio ridotto
    - oggetti dissimili devono apparire distanti nella mappa rappresentazione finale
Questo crea un rappresentazione che riflette la struttura locale del dataset, anzichè la sua 
forma globale.
Il risultato finale è una mappa, in 2D o 3D, in cui i punti vicini corrispondono a osservazioni
simili.
In pratica, la t-SNE traduce la complessità matematica dei dati in forme visivamente 
interpretabili

La PCA è un metodo lineare che cerca di spiegare la varianza massima dei dati attraverso 
poche componenti principali.
La t-SNE, invece, è non lineare e si concentra nel preservare la vicinanza tra i punti,
non la varianza complessiva.
Questo la rende molto più adatta a dati con strutture o curve complesse.
Mentre la PCA evidenzia le direzioni principali di massima varianza nei dati, la t-SNE 
ricostruisce la forma locale delle relazioni.
Il risultato è che la PCA mostra tendenze globali, mentra la t-SNE rivela cluster bene separati
e interpretabili visivamente.

Funzionamento
Nel primo passo, t-SNE assegna a ogni coppia di punti una probabilità basata sulla loro distanza.
Viene usata una distribuzione gaussiana centrata su ciascun punto:
i vicini stretti hanno probabilità alte, i lontani hanno probabilità molto basse.
In questo modo, le relazioni locali diventano più importanti di quelle globali.
Il parametro perplexity controlla quanto 'vicino' o 'lontano' guardare per stimare queste
probabilità
E' come scegliere quanto dettaglio vogliamo osservare nella nostra rappresentazione.
Una volta definita la similarità nello spazio originale, la t-SNE costruisce una distribuzione 
analoga ello spazio 2D o 3D.
Questa volta, però, utilizza una distibuzione t di Student, che ha code più ampie rispetto
alla gaussina.
Questo acorgimento evita il "crowding" cioè l'ammassamento dei punti al centro della mappa.
Grazie alla distribuzione t, i cluester risultano più separati e visbili.
Questo rende la mappa finale più interpretabile dal punto di vista visivo.
Grazie alla distribuzione t, i cluster risultano ben separati e visibili, rendendo la mappa 
finale più interpretabile dal punto di vista grafico e visivo.

Dopo aver costruito le due distribuzioni, la t-SNE misura quanto esse siano diverse.
L'obiettivo dell'algoritmo è minimizzare la divergenza di Kullback-Leibler (KL) tra la 
gistribuzione originale e quella ridotta Kullback-Leibler (KL) .
Questa misura quantifica la perdita di informazione nel passaggio tra gli spazi.
Durante l'ottimizzazione, i punti "si muovono" nel piano 2D finchè non trovano una disposizione
coerente con le similarità originali.
Il risultato è una rappresentazione che preserva le relazioni locali in modo intuitivo e coerente.

PARAMETRI PERPLEXITY & LEARNING RATE
la t-SNE ha due parametri che possono portare a soluzioni completamente diverse.

Il parametro PERPLEXITY nella t-SNE controlla l'equilibrio tra la visione locale e quella 
globale dei dati: valori bassi enfatizzano le piccole strutture, mentre valori alti
tendono a fondere i cluster in gruppi più ampi.
In pratica, la perplexity rappresenta il numero medio di vicini che ogni punto considera nel
calcolo delle similarità, influenzando profondamente la forma finale della mappa.
La perplessità sta nel scegliere il numero medio di vicino di ogni punto.
Una scelta troppo bassa può frammentare i cluster, mentre una troppo alta può nascondere
dettagli importanti: per questo si consiglia di sperimentare valori compresi tra
5 e 50 
t-SNE costriuisce, per ogni punto, una distribuzione di probabilità sui suoi vicini. Se due
punti sono vicini nello spazio originale, probabilità alta; se due punti sono lontani, 
probabilità bassa. La perplexity controlla quanto larga è questa distribuzione. In pratica
regola la scale del 'quartiere locale'. Valori bassi: avrò una struttura molto lacale; 
valori alti: la struttura diventa più globale.
Non fidarti mai di una sola t-SNE, bisogna testare sempre più valori di perplexity, se i 
cluster rimangono simili allora struttura reale, se i cluster cambiano molto allora il 
dataset non ha cluster forti.

La LEARGINIG RATE, invece controlla la velocità con cui i punti si spostano durante
l'ottimizzazione iterativa che va a minimizzare la divergenza di Kullback-Leibler.
La t-SNE cerca una configurazione dei punti (nello spazio 2D o 3D) che minimizzi una funzione
di errore. Per farlo usa un metod iterativo che sposta i punti un po' per volta. Quindi i 
punti si muovono durante l'allenamento dell'algoritmo. La velocità controllata dal
learning rate, è semplicemente quanto grande è lo spostamento ad ogni iterazione.
Se LR è troppo basso, la convergenza sarà lenta e i punti potranno bloccarsi in
configurazioni errate; se è troppo alto, i punti rischiano di muoversi in modo instabile 
e caotico, non andando più a rappresentare la forma a livello locale.
In sintesi, questi due parametri (perplexity, learning rate) determinano quanti finemente 
t-SNE osserva le relazioni tra i dati e quanto rapidamente impara a rappresentarle, influenzando
in modo decisivo la qualità della visualizzazione finale.

La rappresentazione grafica finale, mostra i punti come se fossero 'galassie di dati'.
Punti vicini rappresentano osservazioni simili, mentre gruppi distinti suggeriscono la 
presenza di cluster.
E' importante ricordare che la distanza tra cluster non è quantitivamente significativa.
La t-SNE va letta come una mappa qualitativa delle relazioni, non come un'analisi metrica.
Tuttavia, la chiarezza visiva che offre è spesso insostituibile nella prima fase di
data analysis, quella esplorativa.

La t-SNE è un algoritmo stocastico, quindi risultati diversi possono emergere anche con gli 
stessi dati.
La scelta dei parametri e l'inizializzazione casuale influiscono molto sulla mappa finale.
E' consigliabile eseguire più run e confrontare i risultati per verificare la stabilità 
dei pattern.
Anche piccole differnze nei dati, possono modificare l'aspetto dei cluster.
Questo non significa che l'algoritmo sia impreciso, ma che va interpretato con cautela.
La complessità temporale e spaziale è O(m2)

t-SNE vs Kernel PCA
La t-SNE produce mappe più intuitive e visivamente chiare, ma richiede molti calcoli
e una parametrizzazione sempre attenta.
La KPCA è più stabile e ripetibile, ma non sempre riesce a catturare la complessità dei dati 
reali.
In prativa, si può usare la KPCA per ridurre la dimensionalità iniziale e poi applicare la
t-SNE per visualizzare i risultati.
Questo approccio combinato offre un ottimo equilibrio tra efficienza e interpretabilità, 
proprio per il discorso che la t-SNE ha una complessità computazionale molto elevata, legandola
a KPCA si riduce notevolmente il costo computazionale.
Le due tecniche, quindi, non sono alternative, ma spesso utilizzate in modo complementare.

Vantaggi
- E' una delle tecniche più potenti per visualizzare struttura complesse e non lineari
- Rivela cluster nascosti, relazioni locali e pattern che sono difficilmente rilevabili 
  con altri motodi.
- Riesce a fare mappe bidimensionali facili da interpretare
- La visione grafica immediata e intuitiva del comportamento dei dati.
Svantaggi
- Computazionalmente molto costosa (sia in tempo che momoria)
- Sensibile a parametri iniziali
- Non fornisce una trasformazione stabile
- I cluster visivi non sempre corrispondono a veri gruppi statistici.

t-SNE è ampiamente usata in ambiti come riconoscimento di immagini, analisi di testo, 
bioinformatica e deep learning.
Serve per visualizzare embedding di parole, rappresentazioni latenti o risultati di 
clustering.
Nel ml viene spesso usata per diagnosticare modelli o verificare separazioni tra classi.
In biologia, permette di identificare gruppi di cellule o geni con comportamento simile.
In tutti i casi, aiuta a trasformare dati complessi in intuizioni visive.



"""
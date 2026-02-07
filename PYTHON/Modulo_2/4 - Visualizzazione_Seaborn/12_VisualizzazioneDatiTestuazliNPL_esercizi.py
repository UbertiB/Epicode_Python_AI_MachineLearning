from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import nltk

# Esercizio 1
# Creare un grafico delle frequenze delle parole in un testo a scelta, eliminando stopword e ordinando 
# le parole per frequenza.

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import nltk

# Scarica stopwords se non l'hai già fatto
#nltk.download('stopwords')

text = """
Python is a powerful programming language. Python is used in data science, web development, machine learning, 
and AI. It is versatile, easy to learn, and widely adopted by professionals.
"""
text = """
Python è un meraviglioso linguaggio di programmazione. Python è utilizzato in data science, costruzioni web, machine learning, 
e AI. è versatile e facile da imparare, e spesso utilizzato professionalmente.
"""
# Tokenizzazione senza usare punkt
tokens = wordpunct_tokenize(text.lower())
print(f"Tokens: \n{tokens}")
#stop_words = set(stopwords.words('english'))
stop_words = set(stopwords.words('italian'))
print(f"\nStop_words: \n{stop_words}")  #visualizzo le stopwords per validarle
words = [w for w in tokens if w.isalpha() and w not in stop_words]  #tolgo le stopwords

freq = Counter(words)
most_common = freq.most_common(10) #estraggo solo le 10 parole più frequenti

plt.figure(figsize=(8,5))
plt.bar([w[0] for w in most_common], [w[1] for w in most_common], color="skyblue")
plt.title("Frequenze parole più comuni")
plt.ylabel("Frequenza")
plt.show()

# Esercizio 2
# Costruire una heatmap di co-occorrenza tra parole, evidenziando i legami più forti.

import pandas as pd
import seaborn as sns
import numpy as np

unique_words = list(set(words)) #tramite il set trasformo in parole uniche
co_matrix = np.zeros((len(unique_words), len(unique_words)))

for i, w1 in enumerate(unique_words):
    for j, w2 in enumerate(unique_words):
        co_matrix[i,j] = sum(1 for k in range(len(words)-1) if (words[k]==w1 and words[k+1]==w2))

co_df = pd.DataFrame(co_matrix, index=unique_words, columns=unique_words)

plt.figure(figsize=(8,6))
sns.heatmap(co_df, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("Heatmap co-occorrenza parole")
plt.show()

# Esercizio 3
# Applicare PCA o t-SNE a un set di embedding e visualizzare i risultati con Seaborn.

from sklearn.decomposition import PCA
import seaborn as sns

# Embedding sintetici (5 parole x 4 dimensioni)
embeddings = np.random.rand(len(unique_words), 4)
pca = PCA(n_components=2)
pca_result = pca.fit_transform(embeddings)

df_pca = pd.DataFrame(pca_result, columns=["PC1", "PC2"])
df_pca["word"] = unique_words

plt.figure(figsize=(8,6))
sns.scatterplot(data=df_pca, x="PC1", y="PC2")
for i, row in df_pca.iterrows():
    plt.text(row["PC1"]+0.01, row["PC2"]+0.01, row["word"])
plt.title("PCA embeddings parole")
plt.show()

# Esercizio 4
# Analizzare il sentiment di un dataset di recensioni e rappresentarne la distribuzione per categoria.

from textblob import TextBlob

reviews = pd.DataFrame({
    "text": ["I love this product", "Terrible service", "Great quality", "Not worth the price", "Excellent!"],
    "category": ["positive", "negative", "positive", "negative", "positive"]
})

reviews["sentiment"] = reviews["text"].apply(lambda x: TextBlob(x).sentiment.polarity)

plt.figure(figsize=(8,5))
sns.boxplot(x="category", y="sentiment", data=reviews, palette="Pastel1")
plt.title("Distribuzione sentiment per categoria")
plt.show()

# Esercizio 5
# Eseguire un semplice topic modeling con LDA e visualizzare le parole chiave di ciascun topic.

from gensim import corpora, models

documents = [text.lower().split()]
dictionary = corpora.Dictionary(documents)
corpus = [dictionary.doc2bow(doc) for doc in documents]

lda = models.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=10)
for i, topic in lda.print_topics(num_words=5):
    print(f"Topic {i}: {topic}")

# Esercizio 6
# Calcolare e visualizzare la similarità tra documenti tramite heatmap o clustering gerarchico.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

docs = [
    "I love data science",
    "Data science is great",
    "I hate spam emails",
    "Spam emails are annoying"
]

vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(docs)
sim_matrix = cosine_similarity(tfidf)

plt.figure(figsize=(6,5))
sns.heatmap(sim_matrix, annot=True, cmap="coolwarm", xticklabels=range(1,len(docs)+1), yticklabels=range(1,len(docs)+1))
plt.title("Similarità tra documenti")
plt.show()
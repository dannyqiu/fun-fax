import numpy as np
import spacy
from collections import defaultdict

class Thesaurus:

    def __init__(self, nlp=None):
        self.nlp = nlp
        if self.nlp is None:
            self.nlp = spacy.load('en_core_web_lg')
        self.vocab = [w for w in self.nlp.vocab if w.is_lower and w.prob >= -15 and w.vector.any()]
        self.vocab_vectors = np.array([w.vector for w in self.vocab])

    def most_similar(self, word: str, top=10):
        word_vector = self.nlp.vocab[word].vector
        # word does not appear in our vocabulary, doesn't make sense to give any similar words
        if not np.any(word_vector):
            return [word]
        return self.most_similar_by_embedding(word_vector, top)

    def most_similar_by_embedding(self, word_vector, top=10):
        sim = np.inner(word_vector, self.vocab_vectors)
        by_similarity = [self.vocab[i] for i in np.argsort(-sim)]
        top_similar = by_similarity[:top]
        return [w.lower_ for w in top_similar]

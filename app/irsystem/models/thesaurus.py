import os
import numpy as np
import pickle
import spacy
from collections import defaultdict

from app import app

PICKLE_DIR = os.path.abspath(os.path.join(app.instance_path, "..", "pkl"))

class Thesaurus:

    def __init__(self):
        try:
            with open(os.path.join(PICKLE_DIR, "thesaurus.vocab.pkl"), 'rb') as f:
                self.vocab = pickle.load(f)
            with open(os.path.join(PICKLE_DIR, "thesaurus.vocab_vectors.pkl"), 'rb') as f:
                self.vocab_vectors = pickle.load(f)
        except Exception as e:
            print("No pickle file, recomputing...", e)
            nlp = spacy.load('en_core_web_lg')
            nlp_vocab = [w for w in nlp.vocab if w.is_lower and w.prob >= -15 and w.vector.any()]
            self.vocab = [w.lower_ for w in nlp_vocab]
            self.vocab_vectors = np.array([w.vector for w in nlp_vocab])
            with open(os.path.join(PICKLE_DIR, "thesaurus.vocab.pkl"), 'wb') as f:
                pickle.dump(self.vocab, f)
            with open(os.path.join(PICKLE_DIR, "thesaurus.vocab_vectors.pkl"), 'wb') as f:
                pickle.dump(self.vocab_vectors, f)
        self.vocab_index = {w: i for i, w in enumerate(self.vocab)}

    def most_similar(self, word, top=10):
        # word does not appear in our vocabulary, doesn't make sense to give any similar words
        if word not in self.vocab_index:
            return [word]
        word_vector = self.vocab_vectors[self.vocab_index[word]]
        sim = self.vocab_vectors.dot(word_vector)
        by_similarity = [self.vocab[i] for i in np.argsort(-sim)]
        top_similar = by_similarity[:top]
        return top_similar

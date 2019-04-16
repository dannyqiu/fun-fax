import spacy

class Thesaurus:

    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.vocab = [w for w in self.nlp.vocab if w.is_lower and w.prob >= -15 and w.vector.any()]

    def most_similar(self, word, top=10):
        word = self.nlp.vocab[word]
        by_similarity = sorted(self.vocab, key=lambda w: word.similarity(w), reverse=True)
        top_similar = by_similarity[:top]
        return [w.lower_ for w in top_similar]

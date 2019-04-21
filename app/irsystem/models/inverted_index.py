import nltk
from collections import defaultdict
from nltk.stem.snowball import EnglishStemmer  # Assuming we're working with English

nltk.download('punkt')
nltk.download('stopwords')
DEFAULT_STOPWORDS = nltk.corpus.stopwords.words('english')

class InvertedIndex:
    """ Inverted index datastructure """

    def __init__(self, tokenizer=nltk.word_tokenize, stemmer=EnglishStemmer(), stopwords=DEFAULT_STOPWORDS):
        """
        tokenizer   -- NLTK compatible tokenizer function
        stemmer     -- NLTK compatible stemmer
        stopwords   -- list of ignored words
        """
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        if stopwords:
            self.stopwords = set(stopwords)
        else:
            self.stopwords = set()

        self.index = defaultdict(list)

    def lookup(self, word):
        """
        Lookup a word in the index
        """
        word = word.lower()
        if self.stemmer:
            word = self.stemmer.stem(word)

        return self.index[word]

    def add(self, uuid, document):
        """
        Add a document string to the index
        """
        tokens = [t.lower() for t in self.tokenizer(document)]
        tokens = set(tokens).difference(self.stopwords)
        for token in tokens:
            if self.stemmer:
                token = self.stemmer.stem(token)

            self.index[token].append(uuid)

import re
import spacy
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from . import FUN_FACT_TITLE_CSV, TIL_TITLE_CSV, YSK_TITLE_CSV, REQUIRED_COLUMNS

class WeightedEmbeddingSearch:

    def __init__(self):
        print("Loading data csv")
        fun_fact_title_data = pd.read_csv(FUN_FACT_TITLE_CSV).dropna(subset=REQUIRED_COLUMNS)
        til_title_data = pd.read_csv(TIL_TITLE_CSV).dropna(subset=REQUIRED_COLUMNS)
        ysk_title_data = pd.read_csv(YSK_TITLE_CSV).dropna(subset=REQUIRED_COLUMNS)

        title_data = pd.concat([
            fun_fact_title_data,
            til_title_data,
            ysk_title_data,
        ], join='inner').reset_index(drop=True)

        print("Computing tf-idf matrix")
        self.vectorizer = TfidfVectorizer(stop_words='english', dtype=np.float32)
        tfidf_matrix = self.vectorizer.fit_transform(title_data["title"])

        print("Loading spacy")
        nlp = spacy.load('en_core_web_lg')

        print("Computing weighted embeddings")
        features = self.vectorizer.get_feature_names()
        self.f_vectors = np.array([nlp.vocab[f].vector for f in features])
        self.weighted_embeddings = tfidf_matrix.dot(self.f_vectors)
        assert self.weighted_embeddings.shape == (len(title_data.index), 300)

        print("Compressing pandas dataframe into index")
        self.index = list(title_data.itertuples())

        print("Done loading {} rows".format(len(title_data.index)))

    def search(self, query, top=10):
        query_tfidf = self.vectorizer.transform([query])
        query_weighted = query_tfidf.dot(self.f_vectors)
        rankings = self.weighted_embeddings.dot(query_weighted.flatten())
        rel = np.argsort(-rankings)[:top]
        results = [
            {
                "type": "submission",
                "title": self.index[d].title,
                "subreddit": self.index[d].subreddit,
                "permalink": self.index[d].permalink,
                "score": self.index[d].score,
            }
            for d in rel
        ]
        return results

import re
import spacy
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

from . import FUN_FACT_TITLE_CSV, TIL_TITLE_CSV, YSK_TITLE_CSV, REQUIRED_COLUMNS, BANNED_SUBREDDITS, TOKENIZATION_REGEX

EPS = 1e-6

class WeightedEmbeddingSearch:

    def __init__(self):
        print("Loading data csv")
        fun_fact_title_data = pd.read_csv(FUN_FACT_TITLE_CSV, usecols=REQUIRED_COLUMNS).dropna()
        til_title_data = pd.read_csv(TIL_TITLE_CSV, usecols=REQUIRED_COLUMNS).dropna()
        ysk_title_data = pd.read_csv(YSK_TITLE_CSV, usecols=REQUIRED_COLUMNS).dropna()

        title_data = pd.concat([
            fun_fact_title_data,
            til_title_data,
            ysk_title_data,
        ], join='inner').reset_index(drop=True)

        print("Computing tf-idf matrix")
        self.vectorizer = TfidfVectorizer(stop_words='english', dtype=np.float32)
        tfidf_matrix = self.vectorizer.fit_transform(title_data["title"])

        print("Loading spacy")
        self.nlp = spacy.load('en_core_web_lg')

        print("Computing weighted embeddings")
        features = self.vectorizer.get_feature_names()
        self.f_vectors = np.array([self.nlp.vocab[f].vector for f in features])
        weighted_embeddings = tfidf_matrix.dot(self.f_vectors)
        assert weighted_embeddings.shape == (len(title_data.index), 300)
        self.n_weighted_embeddings = weighted_embeddings / (np.linalg.norm(weighted_embeddings, axis=1)[:, np.newaxis] + EPS)

        print("Compressing pandas dataframe into index")
        self.index = list(title_data.itertuples())

        print("Done loading {} rows".format(len(title_data.index)))

    def _compute_query_embedding(self, query):
        query_tfidf = self.vectorizer.transform([query])
        if query_tfidf.count_nonzero() > 0:
            query_weighted = query_tfidf.dot(self.f_vectors).flatten()
        # average word embeddings if query words don't exist in our corpus (tfidf matrix)
        else:
            # query was all stopwords, so we'll have to manually tokenize
            tokens = TOKENIZATION_REGEX.findall(query.lower())
            query_weighted = np.average([self.nlp.vocab[t].vector for t in tokens], axis=0).flatten()
        return query_weighted

    def search(self, query, top=10):
        query_weighted = self._compute_query_embedding(query)
        # if we have no embeddings for the given query, we're out of luck
        if np.count_nonzero(query_weighted) == 0:
            return []

        n_query_weighted = query_weighted / (np.linalg.norm(query_weighted) + EPS)
        rankings = self.n_weighted_embeddings.dot(n_query_weighted)
        rankings_idx = np.argsort(-rankings)[:top]
        return self._format_results(rankings_idx)

    def _format_results(self, doc_ids: List[int]):
        results = [
            {
                "type": "submission",
                "title": self.index[d].title,
                "subreddit": self.index[d].subreddit,
                "permalink": self.index[d].permalink,
                "score": self.index[d].score,
            }
            for d in doc_ids
        ]
        return results

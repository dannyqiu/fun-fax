import os
import re
import spacy
import pickle
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from . import FUN_FACT_TITLE_CSV, TIL_TITLE_CSV, YSK_TITLE_CSV, REQUIRED_COLUMNS

EPS = 1e-6

from app import app

PICKLE_DIR = os.path.abspath(os.path.join(app.instance_path, "..", "pkl"))

class WeightedEmbeddingSearch:

    def __init__(self):
        print("Loading data csv")
        fun_fact_title_data = pd.read_csv(FUN_FACT_TITLE_CSV, usecols=REQUIRED_COLUMNS).dropna(subset=REQUIRED_COLUMNS)
        til_title_data = pd.read_csv(TIL_TITLE_CSV, usecols=REQUIRED_COLUMNS).dropna(subset=REQUIRED_COLUMNS)
        ysk_title_data = pd.read_csv(YSK_TITLE_CSV, usecols=REQUIRED_COLUMNS).dropna(subset=REQUIRED_COLUMNS)

        title_data = pd.concat([
            fun_fact_title_data,
            til_title_data,
            ysk_title_data,
        ], join='inner').reset_index(drop=True)

        try:
            with open(os.path.join(PICKLE_DIR, "weighted_embedding.vectorizer.pkl"), 'rb') as f:
                self.vectorizer = pickle.load(f)
            with open(os.path.join(PICKLE_DIR, "weighted_embedding.f_vectors.npy"), 'rb') as f:
                self.f_vectors = np.load(f)
            with open(os.path.join(PICKLE_DIR, "weighted_embedding.n_weighted_embeddings.npz"), 'rb') as f:
                self.n_weighted_embeddings = np.load(f)["n_weighted_embeddings"]
        except Exception as e:
            print("No pickle file, recomputing...", e)
            print("Computing tf-idf matrix")
            self.vectorizer = TfidfVectorizer(stop_words='english', dtype=np.float32)
            tfidf_matrix = self.vectorizer.fit_transform(title_data["title"])

            print("Loading spacy")
            nlp = spacy.load('en_core_web_lg')

            print("Computing weighted embeddings")
            features = self.vectorizer.get_feature_names()
            self.f_vectors = np.array([nlp.vocab[f].vector for f in features])
            weighted_embeddings = tfidf_matrix.dot(self.f_vectors)
            assert weighted_embeddings.shape == (len(title_data.index), 300)
            self.n_weighted_embeddings = weighted_embeddings / (np.linalg.norm(weighted_embeddings, axis=1)[:, np.newaxis] + EPS)

            with open(os.path.join(PICKLE_DIR, "weighted_embedding.vectorizer.pkl"), 'wb') as f:
                pickle.dump(self.vectorizer, f)
            with open(os.path.join(PICKLE_DIR, "weighted_embedding.f_vectors.npy"), 'wb') as f:
                np.save(f, self.f_vectors)
            with open(os.path.join(PICKLE_DIR, "weighted_embedding.n_weighted_embeddings.npz"), 'wb') as f:
                np.savez_compressed(f, n_weighted_embeddings=self.n_weighted_embeddings)

        print("Compressing pandas dataframe into index")
        self.index = list(title_data.itertuples())

        print("Done loading {} rows".format(len(title_data.index)))

    def search(self, query, top=10):
        query_tfidf = self.vectorizer.transform([query])
        if query_tfidf.count_nonzero() > 0:
            query_weighted = query_tfidf.dot(self.f_vectors).flatten()

        # if we have no embeddings for the given query, we're out of luck
        else:
            return []

        n_query_weighted = query_weighted / (np.linalg.norm(query_weighted) + EPS)
        rankings = self.n_weighted_embeddings.dot(n_query_weighted)
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

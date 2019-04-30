import re
import spacy
import numpy as np
import pandas as pd
import random
import scipy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import SpectralClustering
from enum import Enum
from typing import List

from . import FUN_FACT_TITLE_CSV, TIL_TITLE_CSV, YSK_TITLE_CSV
from . import REQUIRED_COLUMNS, OPTIONAL_COLUMNS, BANNED_SUBREDDITS, TOKENIZATION_REGEX
from ..utils import normalize_range, encode_numpy_array

EPS = 1e-6
ENTROPY_FACTOR = 0.125

class WeightedEmbeddingClusteringSearch:

    def __init__(self):
        print("Loading data csv")
        usecols = set(REQUIRED_COLUMNS + OPTIONAL_COLUMNS)
        fun_fact_title_data = pd.read_csv(FUN_FACT_TITLE_CSV, usecols=usecols).dropna(subset=REQUIRED_COLUMNS)
        til_title_data = pd.read_csv(TIL_TITLE_CSV, usecols=usecols).dropna(subset=REQUIRED_COLUMNS)
        ysk_title_data = pd.read_csv(YSK_TITLE_CSV, usecols=usecols).dropna(subset=REQUIRED_COLUMNS)

        title_data = pd.concat([
            fun_fact_title_data,
            til_title_data,
            ysk_title_data,
        ], join='inner')
        title_data = title_data[~title_data['subreddit'].isin(BANNED_SUBREDDITS)]
        # most documents with a significant number of hashtags are spam
        title_data = title_data[~title_data['title'].astype(str).apply(lambda t: t.count('#') > 4)]
        title_data = title_data.reset_index(drop=True)

        print("Computing tf-idf matrix")
        self.vectorizer = TfidfVectorizer(stop_words='english', dtype=np.float32)
        tfidf_matrix = self.vectorizer.fit_transform(title_data["title"])

        print("Loading spacy")
        self.nlp = spacy.load('en_core_web_lg', disable=["parser", "tagger", "ner"])

        print("Computing weighted embeddings")
        features = self.vectorizer.get_feature_names()
        self.f_vectors = np.array([self.nlp.vocab[f].vector for f in features])
        self.weighted_embeddings = tfidf_matrix.dot(self.f_vectors)
        assert self.weighted_embeddings.shape == (len(title_data.index), 300)
        self.n_weighted_embeddings = self.weighted_embeddings / (np.linalg.norm(self.weighted_embeddings, axis=1)[:, np.newaxis] + EPS)

        print("Computing documents entropy")
        self.entropy = self._compute_entropy(tfidf_matrix)

        print("Computing documents date distribution")
        dates = title_data['created_utc'].astype(np.int).to_numpy()
        old_dates_dist = scipy.stats.norm(np.min(dates), np.sqrt(np.var(dates) * 2))
        self.p_old_dates = normalize_range(old_dates_dist.pdf(dates))
        new_dates_dist = scipy.stats.norm(np.max(dates), np.sqrt(np.var(dates) * 2))
        self.p_new_dates = normalize_range(new_dates_dist.pdf(dates))

        print("Compressing pandas dataframe into index")
        self.index = list(title_data.itertuples())
        self.scores = title_data['score'].astype(np.int).to_numpy()

        print("Done loading {} rows".format(len(title_data.index)))

    def _compute_entropy(self, tfidf):
        sparse_logs = tfidf.copy()
        sparse_logs.data = np.log(sparse_logs.data)
        entropy = -(tfidf.multiply(sparse_logs)).sum(axis=1)
        entropy = np.minimum(2, np.log(np.asarray(entropy).flatten() + 1))
        return entropy

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

    def _group_documents(self, rankings, sort_method: str):
        upper_zscore = np.sum(scipy.stats.zscore(rankings) > 3.5)
        lower_zscore = np.sum(scipy.stats.zscore(rankings) < -3.5)
        scale = np.std(rankings) * abs(1 / scipy.stats.skew(rankings))
        TOP_HITS_KMEANS = max(15, min(200, int((upper_zscore + lower_zscore) * scale)))

        rankings_idx = np.argsort(-rankings)[:TOP_HITS_KMEANS]
        ranked_rankings = rankings[rankings_idx]
        ranked_scores = self.scores[rankings_idx]
        top_ranked_em = self.n_weighted_embeddings[rankings_idx]
        clustering = SpectralClustering(n_clusters=10, random_state=0).fit(top_ranked_em)

        _, best_similarity_idx = np.unique(clustering.labels_, return_index=True)
        if sort_method == "popularity":
            min_allowed_similarity = np.min(rankings[rankings_idx[best_similarity_idx]])
            # gives the highest Reddit score doc in each cluster that is above the similarity threshold
            best_score_idx = np.array([
                np.argsort(-np.where((clustering.labels_ == c) & (ranked_rankings >= min_allowed_similarity), ranked_scores, np.nan))[0]
                for c in range(10)
            ])
            best_score_doc_id = rankings_idx[best_score_idx]
            return best_score_doc_id[np.argsort(-self.scores[best_score_doc_id])]
        else:
            # gives the highest similarity doc in each cluster since top_ranked_em is ordered
            best_similarity_doc_id = rankings_idx[best_similarity_idx]
            return best_similarity_doc_id[np.argsort(-rankings[best_similarity_doc_id])]

    def _compute_rocchio(self, query_embedding, doc_ids: List[int]):
        alpha = 0.2
        beta = 0.7
        gamma = 0.1
        def _rocchio_helper(selected_id):
            new_em = alpha * query_embedding
            new_em += beta * self.weighted_embeddings[selected_id]
            new_em -= gamma * np.average(self.weighted_embeddings[doc_ids[doc_ids != selected_id]], axis=0)
            return new_em
        return np.array([_rocchio_helper(i) for i in doc_ids])

    def _search_helper(self, query_embedding, category, sort_method: str, recency_sort: str, top: int):
        n_query_embedding = query_embedding / (np.linalg.norm(query_embedding) + EPS)
        rankings = (1 - ENTROPY_FACTOR) * self.n_weighted_embeddings.dot(n_query_embedding) + ENTROPY_FACTOR * self.entropy
        if category:
            category_embedding = self.nlp.vocab[category].vector
            assert np.count_nonzero(category_embedding) > 0
            n_category_embedding = category_embedding / np.linalg.norm(category_embedding)
            rankings *= self.n_weighted_embeddings.dot(n_category_embedding)
        if recency_sort is not None:
            if recency_sort == "new":
                rankings *= self.p_new_dates
            elif recency_sort == "old":
                rankings *= self.p_old_dates
        doc_ids = self._group_documents(rankings, sort_method)
        rocchios = self._compute_rocchio(query_embedding, doc_ids)
        return self._format_results(doc_ids, rocchios)

    def search(self, query, category, sort_method: str="relevancy", recency_sort: str=None, top: int=10):
        query_weighted = self._compute_query_embedding(query)
        # if we have no embeddings for the given query, we're out of luck
        if np.count_nonzero(query_weighted) == 0:
            return []
        return self._search_helper(query_weighted, category, sort_method, recency_sort, top)

    def see_more(self, query_embedding, category, sort_method: str="relevancy", recency_sort: str=None, top: int=10):
        return self._search_helper(query_embedding, category, sort_method, recency_sort, top)

    def random(self, category):
        sample_docs = [d.title for d in random.sample(self.index, k=1)]
        sample_tfidf_matrix = self.vectorizer.transform(sample_docs)
        features = self.vectorizer.get_feature_names()
        words = set()
        for r, c in zip(*sample_tfidf_matrix.nonzero()):
            if sample_tfidf_matrix[r, c] > np.random.random() or not words:
                words.add(features[c])
        return self.search(" ".join(words), category, sort_method="popularity")

    def _format_results(self, doc_ids: List[int], rocchios):
        results = [
            {
                "type": "submission",
                "title": self.index[d].title,
                "subreddit": self.index[d].subreddit,
                "permalink": self.index[d].permalink,
                "score": self.index[d].score,
                "num_comments": self.index[d].num_comments,
                "created_utc": self.index[d].created_utc,
                "thumbnail": self.index[d].thumbnail,
                "see_more_query_vector": encode_numpy_array(r),
            }
            for d, r in zip(doc_ids, rocchios)
        ]
        return results

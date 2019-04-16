import os
import re
import spacy
import pandas as pd
from typing import Set

from app import app
from .inverted_index import InvertedIndex
from .thesaurus import Thesaurus

DATA_DIR = os.path.abspath(os.path.join(app.instance_path, "..", "data"))
MAX_SEARCH_TERMS = 8

class BooleanSearch:

    def __init__(self):
        print("Loading thesaurus")
        self.thesaurus = Thesaurus()
        regex = re.compile("[a-zA-Z]+")
        self.inv_idx = InvertedIndex(tokenizer=lambda d: regex.findall(d), stemmer=None, stopwords=[])
        self.index = {}

        print("Loading fun fact csv")
        fun_fact_title_data = pd.read_csv(os.path.join(DATA_DIR, "fun_fact_title.csv"))
        # til_title_data = pd.read_csv(os.path.join(DATA_DIR, "til_title.csv"))
        # ysk_title_data = pd.read_csv(os.path.join(DATA_DIR, "ysk_title.csv"))

        print("Adding to index")
        for row in fun_fact_title_data.itertuples():
            self.inv_idx.add(row.id, row.title)
            self.index[row.id] = row

        print("Done")

    def _rank_results(self, doc_nums, top=10):
        ranked = sorted(doc_nums, key=lambda d: self.index[d].score, reverse=True)
        return ranked[:top]

    def _boolean_search_with_synonyms(self, query_terms) -> Set[int]:
        doc_nums = None
        for word in query_terms:
            synonyms = self.thesaurus.most_similar(word)
            synonyms = list(filter(lambda w: w != word, synonyms))
            syn_docs = set()
            for syn in synonyms:
                docs = self.inv_idx.lookup(syn)
                syn_docs.union(docs)
            if doc_nums is None:
                doc_nums = syn_docs
            else:
                doc_nums = doc_nums.intersection(syn_docs)
        return doc_nums

    def _boolean_search(self, query_terms) -> Set[int]:
        doc_nums = None
        for word in query_terms:
            docs = set(self.inv_idx.lookup(word))
            if doc_nums is None:
                doc_nums = docs
            else:
                doc_nums = doc_nums.intersection(docs)
        return doc_nums

    def search(self, query, top=10):
        query_terms = query.lower().split()[:MAX_SEARCH_TERMS]
        doc_nums = self._boolean_search(query_terms)
        if len(doc_nums) < top:
            doc_nums = doc_nums.union(self._boolean_search_with_synonyms(query_terms))
        rel = self._rank_results(doc_nums)[:top]
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


class DummySearch:

    def search(self, query):
        results = [
            {
                "type": "submission",
                "title": "Fun fact: Did you know that you inputted {} into the search box?".format(query),
                "subreddit": "fun-fax-testing",
                "permalink": "/",
                "score": 999999,
            },
            {
                "type": "submission",
                "title": "Fun fact about the Vatican",
                "subreddit": "funny",
                "permalink": "https://reddit.com/r/funny/comments/16z5sr/fun_fact_about_the_vatican/",
                "score": 0.999,
            },
            {
                "type": "submission",
                "title": "TIL Corey Feldman already made a movie about killing Bin Laden",
                "subreddit": "todayilearned",
                "permalink": "https://reddit.com/r/todayilearned/comments/h2l9w/til_corey_feldman_already_made_a_movie_about/",
                "score": 0.459,
            },
            {
                "type": "comment",
                "title": "Shaq hit almost 12,000 baskets in his career. Exactly 1 of them was a 3-pointer.",
                "subreddit": "askreddit",
                "permalink": "https://www.reddit.com/r/AskReddit/comments/4lmm61/what_is_a_fun_fact_that_always_blows_peoples_minds/d3os740/",
                "score": 0.589,
            },
            {
                "type": "submission",
                "title": "YSK Useful Tips For A Rainy Day",
                "subreddit": "YouShouldKnow",
                "permalink": "https://reddit.com/r/YouShouldKnow/comments/16zf8g/ysk_useful_tips_for_a_rainy_day/",
                "score": 0.123,
            },
        ]
        return results

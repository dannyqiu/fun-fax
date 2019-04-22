import re
import pandas as pd
from typing import List, Set

from ..inverted_index import InvertedIndex
from ..thesaurus import Thesaurus
from . import FUN_FACT_TITLE_CSV, REQUIRED_COLUMNS

MAX_SEARCH_TERMS = 8

class BooleanSearch:

    def __init__(self):
        print("Loading thesaurus")
        self.thesaurus = Thesaurus()
        regex = re.compile("[a-zA-Z]+")
        self.inv_idx = InvertedIndex(tokenizer=lambda d: regex.findall(d), stemmer=None, stopwords=[])
        self.index = {}

        print("Loading fun fact csv")
        fun_fact_title_data = pd.read_csv(FUN_FACT_TITLE_CSV).dropna(subset=REQUIRED_COLUMNS)

        print("Adding to index")
        for row in fun_fact_title_data.itertuples():
            self.inv_idx.add(row.id, row.title)
            self.index[row.id] = row

        print("Done loading {} rows".format(len(fun_fact_title_data.index)))

    def _rank_results(self, doc_nums, top=10) -> List[int]:
        ranked = sorted(doc_nums, key=lambda d: self.index[d].score, reverse=True)
        return ranked[:top]

    def _boolean_search_with_synonyms(self, query_terms) -> Set[int]:
        doc_nums = None
        for word in query_terms:
            synonyms = self.thesaurus.most_similar(word)
            #synonyms = list(filter(lambda w: w != word, synonyms))
            syn_docs = set()
            for syn in synonyms:
                docs = self.inv_idx.lookup(syn)
                syn_docs = syn_docs.union(docs)
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
        rel = self._rank_results(doc_nums)[:top]
        if len(doc_nums) < top:
            syn_doc_nums = self._boolean_search_with_synonyms(query_terms)
            syn_doc_nums = syn_doc_nums.difference(doc_nums)
            syn_rel = self._rank_results(syn_doc_nums)[:top - len(doc_nums)]
            rel += syn_rel
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

from .search_base import SearchBase
import math

class BM25(SearchBase):
    def __init__(self, documents, k1=1.5, b=0.75):
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.N = len(documents)
        self.index = {}
        self.doc_len = []
        self._build_index()
        self.avgld = sum(self.doc_len) / self.N
        self.idf = self._compute_idf()

    def _build_index(self):
        for doc_id, doc in enumerate(self.documents):
            tokens = self.tokenizer(doc)
            self.doc_len.append(len(tokens))
            for term in tokens:
                if term not in self.index:
                    self.index[term] = {doc_id: 0}
                if doc_id not in self.index[term]:
                    self.index[term][doc_id] = 0
                self.index[term][doc_id] += 1

    def _compute_idf(self):
        idf = {}
        for term, postings in self.index.items():
            df = len(postings)
            idf[term] = math.log((self.N - df + 0.5) / (df + 0.5))
        return idf

    def _term_score(self, term, doc_id):
        f = self.index[term][doc_id]
        norm = (1 - self.b + self.b * (self.doc_len[doc_id]))
        tf = (f * (self.k1 + 1)) / (f + self.k1 * norm)
        idf = self.idf[term]
        return tf * idf

    def score(self, query_term, doc_id):
        score = 0.0
        for term in query_term:
            if term not in self.index:
                continue
            if doc_id not in self.index[term]:
                continue
            score += self._term_score(term, doc_id)
        return score

    def search(self, query, top_k=5):
        query_term = self.tokenizer(query)
        condidates = set()
        for term in query_term:
            if term not in self.index:
                continue
            condidates.update(self.index[term].keys())
        results = []
        for doc_id in condidates:
            score = self.score(query_term, doc_id)
            results.append((doc_id, score))
        results.sort(key= lambda x: x[1], reverse=True)
        return results[:top_k]

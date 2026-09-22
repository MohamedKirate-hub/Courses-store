from sentence_transformers import SentenceTransformer, util
from .search_base import SearchBase
import numpy as np

class SentenceSearch(SearchBase):

    def __int__(self, documents, model_name="all-MiniLM-L6-v2"):
        self.documents = documents
        self.model = SentenceTransformer(model_name)
        self.docs_embd = self.model.encode(documents, convert_to_tensor=True)

    def search(self, query, top_k=5):
        query_embd = self.encode([query], convert_to_tensor=True)
        similarity = util.cos_sim(query_embd, self.docs_embd)[0]
        scores = similarity.cpu().numpy()
        top_indeces = np.argsort(-scores)[:top_k]
        result = []
        for doc_id in top_indeces:
            result.append(
                int(doc_id), float(scores[doc_id])
            )
        return result

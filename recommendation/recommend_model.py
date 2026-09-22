from account_auth.models import User
from course.models import Course
import math

class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.N = len(documents)
        self.doc_len = []
        self.index = {}
        self._build_index()
        self.avgdl = sum(self.doc_len) / self.N
        self.idf = {}
        self._compute_idf()

    def tokenizer(self, text):
        return text.lower().split()

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
        for term, postings in self.index.items():
            df = len(postings)
            self.idf[term] = math.log((self.N - df + 0.5) / (df + 0.5))

    def _term_score(self, term, doc_id):
        f = self.index[term][doc_id]
        norm = 1 - self.b + self.b * (self.doc_len[doc_id] / self.avgdl)
        tf = (f * self.k1 + 1) / (f + self.k1 * norm)
        idf = self.idf[term]
        return tf * idf

    def score(self, query, doc_id):
        query_term = self.tokenizer(query)
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
        condidate = set()
        for term in query_term:
            if term not in self.index:
                continue
            condidate.update(self.index[term].keys())

        results = []
        for doc_id in condidate:
            score = self.score(query, doc_id)
            results.append((doc_id, score))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]


class RecommendationSystem:
    def __init__(self, user: User):
        self.__user = user

    def get_coure_data(self, course: Course):
        topics = " ".join(topic.name for topic in course.topics.all())
        return " ".join(
            [
                course.title or "",
                course.description or "",
                course.language or "",
                topics
            ]
        )

    def get_user_data(self):
        data = []
        for favorite in self.__user.favorites.all():
            data.append(
                self.get_coure_data(favorite.course)
            )

        for enrolled in self.__user.enrollments.all():
            data.append(
                self.get_coure_data(enrolled.course)
            )

        return " ".join(data)

    def recommendation(self):
        courses = Course.objects.all().exclude(author=self.__user)

        courses_data = [
            self.get_coure_data(course)
            for course in courses
        ]

        user_data = self.get_user_data()

        bm25 = BM25(courses_data)
        results = bm25.search(user_data, top_k=10)
        recommedations = []
        for doc_id, score in results:
            recommedations.append((courses[doc_id], score))
        return recommedations

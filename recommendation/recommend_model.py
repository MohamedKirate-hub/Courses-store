from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from account_auth.models import User
from course.models import Course

class RecommendationSystem:
    def __init__(self, user: User):
        self.__user = user

    def get_coure_data(self, course: Course):
        topics = " ".join(topic.name for topic in course.topics.all())
        return " ".join(
            course.title or "",
            course.description or "",
            course.language or "",
            topics
        )

    def get_user_data(self):
        data = []
        for favorite in self.__user.favorites.all():
            data.append(
                self.get_coure_data(favorite.course)
            )

        for enrolled in self.__user.enrollements.all():
            data.append(
                self.get_coure_data(enrolled.course)
            )

        return " ".join(data)

    def recommendation(self):
        courses = Course.objects.all()

        courses_data = [
            self.get_coure_data(course)
            for course in courses
        ]

        user_data = self.get_user_data()

        vectorizer = TfidfVectorizer(stop_words='english')
        courses_vector = vectorizer.fit_transform(courses_data)
        user_vector = vectorizer.transform(user_data)

        similarity = cosine_similarity(user_vector, courses_vector)[0]
        recommend = sorted(
            zip(courses, similarity),
            key=lambda x: x[1],
            reverse=True
        )
        return recommend

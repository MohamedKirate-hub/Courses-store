from sklearn.feature_extraction.text import TfidfVectorizer
from account_auth.models import User
from course.models import Course

class RecommendationSystem:
    def __init__(self, user: User):
        self.__user = user
        self.__user_data = ""
        self.__data = []

    def get_data(self):
        courses = Course.objects.filter(user=self.__user)
        for course in courses:
            data = (course.title + " " + course.description
                    + " " + course.language + " "
                    + " ".join(topic.name for topic in course.topics.all()))
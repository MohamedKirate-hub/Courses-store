from django.urls import path
from . import views

urlpatterns = [
    path('course-detail/<str:pk>', views.course_view, name='course-detail'),
    path('entrolle/<str:pk>', views.enrolle_course_view, name='enrolle-course'),
    path('learning/', views.learning_view, name='learning'),
    path('unenrolled-course/<str:pk>', views.unenrolle_course_view, name='unenrolled-course'),
    path('checkout/', views.enroll_courses, name='checkout'),
]
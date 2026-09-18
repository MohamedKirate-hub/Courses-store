from django.urls import path
from . import views

urlpatterns = [
    path('course-detail/<str:pk>', views.course_view, name='course-detail'),
    path('entrolle/<str:pk>', views.enrolle_course_view, name='enrolle-course'),
    path('learning/', views.learning_view, name='learning'),
    path('unenrolled-course/<str:pk>', views.unenrolle_course_view, name='unenrolled-course'),
    path('checkout/', views.enroll_courses, name='checkout'),
    path('create-section/<str:pk>', views.create_section, name='create-section'),
    path('section/<str:pk>/delete', views.delete_section, name='section-delete'),
    path('section/<str:pk>/update', views.update_section, name='section-update'),
    path('lecture/<str:pk>/create', views.create_lecteur, name='lecture-create'),
    path( 'lecture/<int:pk>/', views.lecture_detail, name='lecture-detail'),
    path('feedback/<str:pk>/delete', views.delete_feedback, name='delete-feedback'),
    path('feedback/<str:pk>/update', views.update_feedback, name='update-feedback'),
]
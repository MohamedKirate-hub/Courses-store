from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.profile_view, name='profile'),
    path('profile/<str:pk>/edit', views.update_profile_view, name='edit-profile')
]
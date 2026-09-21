from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('create-course', views.create_course_view, name='create-course'),
    path('update-course/<str:pk>', views.update_course_view, name='update-course'),
    path('delete-course/<str:pk>', views.delete_course_view, name='delete-course'),
    path('cart', views.cart_view, name='cart'),
    path('add-cart/<str:pk>', views.add_to_cart_view, name='add-cart'),
    path('delete-item-cart/<str:pk>', views.delete_at_cart, name='delete-item-cart'),
    path('add-favorite/<str:pk>', views.add_to_favorite_view, name='add-favorite'),
    path('delete-favorite/<str:pk>', views.delete_favorite, name='delete-favorite'),
    path('favorite/', views.favorites_view, name='favorite'),
    path('move-cart/<str:pk>', views.move_to_favorite, name='move-cart'),
    path('admin/import-courses/', views.import_courses_view, name='import-courses')
]
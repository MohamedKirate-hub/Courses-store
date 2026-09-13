from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account_auth.urls')),
    path('', include('item.urls')),
    path('course/', include('course.urls')),
]

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from custom_admin.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),
    path('account/', include('account_auth.urls')),
    path('course/', include('course.urls')),
    path('profile/', include('user_profile.urls')),
    path('', include('item.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # This connects to your api/urls.py
]

# 🔥 THIS IS THE MAGIC LINE FOR IMAGES
# It tells Django: "If someone asks for /media/, look in the MEDIA_ROOT folder"
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
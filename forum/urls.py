from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('tinymce/', include('tinymce.urls')),
    #path('hitcount/', include('hitcount.urls', namespace='hitcount')),
    path('event/', include('event.urls')),
    path('user/', include('user.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
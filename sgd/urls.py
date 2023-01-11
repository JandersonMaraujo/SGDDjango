from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



import sgdweb


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('gerenciamento/', admin.site.urls),
    path('web/', include('sgdweb.urls')),
    path('api/', include('sgdapi.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

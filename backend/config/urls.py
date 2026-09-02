from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [path('api/', include('apps.slides.urls')), path('api/', include('apps.analysis.urls')), path('api/', include('apps.annotations.urls')), path('api/', include('apps.scanner.urls')), path('api/', include('apps.health.urls'))] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

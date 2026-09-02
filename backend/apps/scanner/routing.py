from django.urls import path
from .consumers import ScannerConsumer
websocket_urlpatterns=[path('ws/scanner/',ScannerConsumer.as_asgi())]

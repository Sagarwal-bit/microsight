from django.urls import path
from .views import event,jobs
urlpatterns=[path('scanner/events/',event),path('scanner/jobs/',jobs)]

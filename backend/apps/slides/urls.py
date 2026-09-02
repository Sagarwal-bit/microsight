from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SlideViewSet, tile, metrics_view
router=DefaultRouter(); router.register('slides', SlideViewSet, basename='slide')
urlpatterns=[path('',include(router.urls)),path('slides/<uuid:slide_id>/tiles/<int:level>/<int:x>/<int:y>/',tile),path('metrics/',metrics_view)]

from rest_framework.routers import DefaultRouter
from .views import AnnotationViewSet
router=DefaultRouter(); router.register('annotations',AnnotationViewSet)
urlpatterns=router.urls

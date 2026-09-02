from django.urls import path
from .views import run_analysis,heatmap,objects,quality_check
urlpatterns=[path('slides/<uuid:slide_id>/analyze/',run_analysis),path('slides/<uuid:slide_id>/heatmap/',heatmap),path('slides/<uuid:slide_id>/objects/',objects),path('slides/<uuid:slide_id>/quality-check/',quality_check)]

from django.db import models
from apps.slides.models import Slide
class AnalysisRegion(models.Model):
    slide=models.ForeignKey(Slide,on_delete=models.CASCADE,related_name='regions'); x=models.PositiveIntegerField(); y=models.PositiveIntegerField(); width=models.PositiveIntegerField(); height=models.PositiveIntegerField(); score=models.FloatField(); analysis_type=models.CharField(max_length=48,default='BaselineCV'); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: indexes=[models.Index(fields=['slide','-score'])]
class DetectedObject(models.Model):
    slide=models.ForeignKey(Slide,on_delete=models.CASCADE,related_name='detected_objects'); x=models.PositiveIntegerField(); y=models.PositiveIntegerField(); width=models.PositiveIntegerField(); height=models.PositiveIntegerField(); area=models.FloatField(); score=models.FloatField(); method=models.CharField(max_length=48,default='BaselineCV')

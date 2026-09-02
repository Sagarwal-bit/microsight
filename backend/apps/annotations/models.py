from django.db import models
from apps.slides.models import Slide
class Annotation(models.Model):
    TYPES=[('POINT','Point'),('RECTANGLE','Rectangle'),('NOTE','Note')]
    slide=models.ForeignKey(Slide,on_delete=models.CASCADE,related_name='annotations'); type=models.CharField(max_length=16,choices=TYPES); x=models.FloatField(); y=models.FloatField(); width=models.FloatField(default=0); height=models.FloatField(default=0); text=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

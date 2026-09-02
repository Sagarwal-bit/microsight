import uuid
from django.db import models

class Slide(models.Model):
    class Status(models.TextChoices): UPLOADED='UPLOADED'; PROCESSING='PROCESSING'; READY='READY'; FAILED='FAILED'; ANALYZING='ANALYZING'; ANALYZED='ANALYZED'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    original_filename = models.CharField(max_length=255)
    image = models.ImageField(upload_to='originals/')
    width = models.PositiveIntegerField(default=0); height = models.PositiveIntegerField(default=0)
    image_format = models.CharField(max_length=20, blank=True); file_size = models.PositiveBigIntegerField(default=0)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.UPLOADED, db_index=True)
    pyramid_levels = models.PositiveSmallIntegerField(default=0); created_at = models.DateTimeField(auto_now_add=True); updated_at = models.DateTimeField(auto_now=True)
    class Meta: indexes = [models.Index(fields=['status', 'created_at'])]

class ProcessingJob(models.Model):
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE, related_name='jobs')
    kind = models.CharField(max_length=32); status = models.CharField(max_length=16); duration_ms = models.FloatField(null=True); created_at = models.DateTimeField(auto_now_add=True)

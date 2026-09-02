import uuid
from django.db import models
class ScannerJob(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False); slide_id=models.UUIDField(null=True); status=models.CharField(max_length=24,default='IDLE',db_index=True); progress=models.FloatField(default=0); current_x=models.IntegerField(default=0); current_y=models.IntegerField(default=0); retries=models.PositiveIntegerField(default=0); error=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
class ScannerEvent(models.Model):
    event_id=models.UUIDField(default=uuid.uuid4,editable=False,unique=True); timestamp=models.DateTimeField(auto_now_add=True); type=models.CharField(max_length=48); job=models.ForeignKey(ScannerJob,on_delete=models.CASCADE,related_name='events'); payload=models.JSONField(default=dict)

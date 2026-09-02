from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ScannerJob,ScannerEvent
class EventSerializer(serializers.Serializer):
    event_type=serializers.ChoiceField(choices=['SCANNER_CONNECTED','SCAN_STARTED','MOVE_STARTED','MOVE_COMPLETED','FOCUS_STARTED','FOCUS_COMPLETED','CAPTURE_STARTED','CAPTURE_COMPLETED','TILE_SAVED','TILE_FAILED','RETRY_STARTED','SCAN_PAUSED','SCAN_RESUMED','SCAN_COMPLETED','SCAN_FAILED'])
    job_id=serializers.UUIDField(); payload=serializers.DictField(required=False,default=dict)
@api_view(['POST'])
def event(request):
    s=EventSerializer(data=request.data); s.is_valid(raise_exception=True); d=s.validated_data
    job,_=ScannerJob.objects.get_or_create(id=d['job_id']); p=d['payload']; typ=d['event_type']
    job.status='COMPLETED' if typ=='SCAN_COMPLETED' else ('ERROR' if typ=='SCAN_FAILED' else typ); job.progress=float(p.get('progress',job.progress)); job.current_x=int(p.get('x',job.current_x)); job.current_y=int(p.get('y',job.current_y)); job.retries=int(p.get('retries',job.retries)); job.error=str(p.get('error',job.error)); job.save()
    e=ScannerEvent.objects.create(job=job,type=typ,payload=p); data={'event_id':str(e.event_id),'type':typ,'job_id':str(job.id),'payload':p}
    async_to_sync(get_channel_layer().group_send)('scanner',{'type':'scanner.event','data':data}); return Response(data,status=201)
@api_view(['GET'])
def jobs(request): return Response(list(ScannerJob.objects.order_by('-updated_at').values()))

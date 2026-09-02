import time
from pathlib import Path
from django.http import FileResponse, Http404
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Slide
from .serializers import SlideSerializer, SlideUploadSerializer
from .services import build_pyramid, tile_path, record_tile, metrics

class SlideViewSet(viewsets.ModelViewSet):
    queryset=Slide.objects.all().order_by('-created_at')
    def get_serializer_class(self): return SlideUploadSerializer if self.action == 'create' else SlideSerializer
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data); serializer.is_valid(raise_exception=True); slide=serializer.save(); build_pyramid(slide); return Response(SlideSerializer(slide).data, status=201)
    @action(detail=True, methods=['post'], url_path='process')
    def process(self, request, pk=None): build_pyramid(self.get_object()); return Response(SlideSerializer(self.get_object()).data)

@api_view(['GET'])
def tile(request, slide_id, level, x, y):
    started=time.perf_counter()
    try: slide=Slide.objects.get(pk=slide_id, status__in=[Slide.Status.READY, Slide.Status.ANALYZED])
    except Slide.DoesNotExist: raise Http404('Slide is not ready.')
    if level < 0 or level >= slide.pyramid_levels or x < 0 or y < 0: raise Http404('Invalid tile coordinates.')
    path=tile_path(slide, level, x, y)
    if not path.is_file(): raise Http404('Tile does not exist.')
    key=f'tile:{slide_id}:{level}:{x}:{y}'; cached=cache.get(key); hit=cached is not None
    if cached is None:
        cached=path.read_bytes(); cache.set(key, cached, 300)
    record_tile(hit, (time.perf_counter()-started)*1000)
    response=Response(cached, content_type='image/jpeg'); response['Cache-Control']='public, max-age=300'; return response
@api_view(['GET'])
def metrics_view(request): return Response(metrics())

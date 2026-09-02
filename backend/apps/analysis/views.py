from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.slides.models import Slide
from .models import AnalysisRegion,DetectedObject
from .services import analyze,quality
from PIL import Image
@api_view(['POST'])
def run_analysis(request, slide_id):
    slide=get_object_or_404(Slide,pk=slide_id); analyze(slide); return Response({'status':'ANALYZED','engine':'BaselineCV','disclaimer':'Experimental demonstration analysis; not medical diagnosis.'})
@api_view(['GET'])
def heatmap(request,slide_id):
    return Response({'analysis_type':'BaselineCV','disclaimer':'Experimental analysis flags only.','regions':list(AnalysisRegion.objects.filter(slide_id=slide_id).order_by('-score').values('id','x','y','width','height','score','analysis_type'))})
@api_view(['GET'])
def objects(request,slide_id): return Response(list(DetectedObject.objects.filter(slide_id=slide_id).values('id','x','y','width','height','area','score','method')))
@api_view(['POST'])
def quality_check(request,slide_id):
    slide=get_object_or_404(Slide,pk=slide_id)
    with Image.open(slide.image.path) as image: return Response(quality(image))

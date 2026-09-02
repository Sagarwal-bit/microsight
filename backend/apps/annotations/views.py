from rest_framework import serializers,viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Annotation
class AnnotationSerializer(serializers.ModelSerializer):
    class Meta: model=Annotation; fields='__all__'; read_only_fields=['slide']
    def validate(self,d):
        if d.get('type',getattr(self.instance,'type',None))=='RECTANGLE' and (d.get('width',0)<=0 or d.get('height',0)<=0): raise serializers.ValidationError('Rectangle annotations need positive width and height.')
        return d
class AnnotationViewSet(viewsets.ModelViewSet):
    queryset=Annotation.objects.all(); serializer_class=AnnotationSerializer
    @action(detail=False,methods=['get','post'],url_path='slides/(?P<slide_id>[^/.]+)/annotations')
    def by_slide(self,request,slide_id=None):
        if request.method=='GET': return Response(AnnotationSerializer(Annotation.objects.filter(slide_id=slide_id),many=True).data)
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); s.save(slide_id=slide_id); return Response(s.data,status=201)

from rest_framework import serializers
from .models import Slide
from .services import validate_image
class SlideSerializer(serializers.ModelSerializer):
    class Meta: model = Slide; fields = ['id','name','original_filename','width','height','image_format','file_size','status','pyramid_levels','created_at','updated_at']; read_only_fields = fields
class SlideUploadSerializer(serializers.ModelSerializer):
    class Meta: model=Slide; fields=['name','image']
    def validate_image(self, value): validate_image(value); return value
    def create(self, data):
        image=data['image']; size, fmt=validate_image(image)
        return Slide.objects.create(name=data.get('name') or image.name, original_filename=image.name, image=image, width=size[0], height=size[1], image_format=fmt, file_size=image.size)

from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk', read_only=True)
    image_name = serializers.CharField(source='name', allow_null=False)
    description = serializers.CharField(allow_null=False)

    class Meta:
        model = Image
        fields = ('id', 'image_name', 'description', 'horizontal_image', 'vertical_image',
                  'horizontal_small_image', 'gallery')



from django.db import IntegrityError

from rest_framework.serializers import ValidationError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import ImageSerializer
from .models import Image as ImageModel
from .constants import STANDARD_SIZE
from .resources import validate_new_image, push_to_s3, async_upload_image


class ImageViewSet(viewsets.ModelViewSet):

    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        # make a log of the method call with request data and unique id as information tag
        response = {
            'message': '',
            'success': False,
        }
        data = request.data
        image = request.data.get('image')
        try:
            is_valid = validate_new_image(image)
            if not is_valid:
                response['message'] = 'Invalid image size'
                response['error'] = '%s %s' % ('Provide valid size', STANDARD_SIZE)
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            image_url = push_to_s3(image)
            data['horizontal_image'] = image_url
            serializer = ImageSerializer(data=data)
            if not serializer.is_valid():
                response['errors'] = serializer.errors
                raise ValidationError(response)
            obj = ImageModel(**serializer.validated_data)
            obj.save()
            async_upload_image.apply_async(args=(image, obj))
            response['success'] = True
            response['message'] = 'Image Uploaded successfully'
            response['data'] = serializer.data
            return Response(response, status=status.HTTP_201_CREATED)

        except IntegrityError as i_err:
            # make a log in the logging system with critical tag
            response['message'] = 'Unable to save Data'
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValidationError as v_err:
            # log the data in the logging system
            return Response(v_err.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exc:
            # log in the logging system marking as critical tag
            response['message'] = 'Some error occured'
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        response = {
            'message': '',
            'success': False,
        }
        # make a log of the method call with request data and unique id as information tag
        data = request.data
        pk = kwargs.get('pk')
        try:

            image = data.get('image')
            obj = ImageModel.objects.filter(pk=pk).first()
            if not obj:
                response['message'] = "Validation error/ Provide valid id to update"
                raise ValidationError(response)
            if image:
                is_valid = validate_new_image(image)
                if not is_valid:
                    response['message'] = 'Invalid Image'
                    response['error'] = '%s %s' % ('Provide valid size', STANDARD_SIZE)
                    raise ValidationError(response)
                image_url = push_to_s3(image)
                data['horizontal_image'] = image_url

                async_upload_image.apply_async(args=(image, obj))
            serializer = ImageSerializer(instance=obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
            response['message'] = 'Updated Successfully'
            response['success'] = True
            return Response(response, status=status.HTTP_200_OK)

        except IntegrityError as i_err:
            # make a log in the logging system with critical tag
            response['message'] = 'Unable to Update Data'
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValidationError as v_err:
            # log the data in the logging system
            return Response(v_err.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exc:
            # log in the logging system marking as critical tag
            response['message'] = 'Some error occured'
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        response = {
            'message': '',
            'data': [],
            'success': False
        }
        pk = kwargs.get('pk', None)
        # make a log of the method call with request data and unique id as information tag
        if not pk:
            return Response('Provide id to get data', status=status.HTTP_200_OK)
        instance_obj = ImageModel.objects.filter(pk=pk).first()
        serializer = ImageSerializer(instance=instance_obj)
        response['data'] = serializer.data
        if response['data']:
            response['message'] = 'Data retrievied Successfully'
            response['success'] = True
        return Response(response, status=status.HTTP_200_OK)


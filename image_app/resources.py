
"""

This file contains all the resources and helper functions required for the application

"""
import ssl
import io

from django.conf import settings
from .serializers import ImageSerializer
from Image.utils.cloud_storage import S3Upload
from .constants import S3_MESSAGE
from celery import shared_task
from .constants import IMAGE_CONFIGURATION, STANDARD_PIXEL
import PIL
from PIL import Image

# This restores the same behavior as before.
ssl._create_default_https_context = ssl._create_unverified_context


def validate_new_image(image=None):
    """
    This method validates the size of the image in size '1024 x 1024' using pillow
    :param image:django in-memory content object
    :return: boolean True on success
    """
    try:
        im = Image.open(image)
        width, height = im.size
        if width == height and height == STANDARD_PIXEL:
            return True

    except AssertionError as asser_err:
        # log the error in the critical
        pass
    return False


def resize_image(image, name, base_width, base_height):
    """
    method resized the image in the given height and width
    :param image:
    :param base_width:
    :param base_height:
    :return:
    """

    dimension = (base_width, base_height)
    new_img = image.resize(dimension, PIL.Image.ANTIALIAS)
    new_img.save(name)
    new_img.name = name
    return new_img


def create_new_images(image):
    """

    :param image:
    :return: list of 3 different type of images
    """
    images = []
    ext = image.name.split('.')[-1]
    for k, v in IMAGE_CONFIGURATION.items():
        temp = Image.open(image)
        temp = resize_image(temp, k+'.'+ext, v.get('width'), v.get('height'))
        images.append(temp)
    return images


@shared_task(typing=False)
def async_upload_image(image, obj):
    """
    this method is celery linked which runs on async to create 3 different image of different dimensions
    and then push it to s3 and update it to the obj.
    :param obj:
    :param image:
    :return:
    """
    # initate a logger for the task with info tag

    images = create_new_images(image)
    results = []
    # can optimize here by pushing all 3 at once to s3
    for image in images:
        url = push_to_s3(image)
        results.append(url)
    data = {
        'vertical_image': results[0],
        'horizontal_small_image': results[1],
        'gallery': results[2]
    }
    serializer = ImageSerializer(instance=obj, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()


def push_to_s3(image):
    """
    this method helps in pushing the image to the s3 and get the url back from s3
    :param image:
    :return: dict containing two keys url and success
    """
    ext = image.name.split('.')[-1]         # -1 represents to take the last set
    accepted_img_type = ', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)
    if ext in accepted_img_type:
        s3 = S3Upload()
        s3_response = s3.upload(image)
        if s3_response['success']:
            s3_image_url = s3_response['data']
        else:
            raise Exception('Error occured while S3 upload')
    else:
        raise Exception(S3_MESSAGE.get('IMAGE_FORMAT'))
    return s3_image_url


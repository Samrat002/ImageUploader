"""
    This file contains list of all the constant used across the Application
"""
from django.conf import settings
STANDARD_PIXEL = 1024
STANDARD_SIZE = '1024 x 1024'
HORIZONTAL_IMAGE_HEIGHT = 755
HORIZONTAL_IMAGE_WIDTH = 450
VERTICAL_IMAGE_HEIGHT = 365
VERTICAL_IMAGE_WIDTH = 450
HORIZONTAL_SMALL_IMAGE_HEIGHT = 380
HORIZONTAL_SMALL_IMAGE_WIDTH = 212
GALLERY_HEIGHT = 380
GALLERY_WIDTH = 380
IMAGE_CONFIGURATION = {
    'horizontal_image': {
        'height': HORIZONTAL_IMAGE_HEIGHT,
        'width': HORIZONTAL_IMAGE_WIDTH
    },
    'vertical_image': {
        'height': VERTICAL_IMAGE_HEIGHT,
        'width': VERTICAL_IMAGE_WIDTH
    },
    'horizontal_small_image': {
        'height': HORIZONTAL_SMALL_IMAGE_HEIGHT,
        'width': HORIZONTAL_SMALL_IMAGE_WIDTH},
    'gallery': {
        'height': GALLERY_HEIGHT,
        'width': GALLERY_WIDTH
    }

}


S3_MESSAGE = {
    'IMAGE_FORMAT': 'only %s image format accepted' % str(settings.ALLOWED_IMAGE_EXTENSIONS)
}
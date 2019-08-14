
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _


def nameFile(instance, filename):
    return '/'.join(['images', str(instance.name), filename])


class Image(models.Model):
    name = models.CharField(_('Name of Image'), null=False, max_length=100)
    description = models.CharField(_('Description of Image'), max_length=1024)
    horizontal_image = models.URLField(_('Horizontal Image'), blank=True)
    vertical_image = models.URLField(_('Vertical Image'), blank=True)
    horizontal_small_image = models.URLField(_('Horizontal Small Image'), blank=True)
    gallery = models.URLField(_('Gallery'), blank=True)
    created_on = models.DateTimeField(_('Added On'), auto_now_add=True, db_index=True)
    modified_on = models.DateTimeField(_('Modified On'), auto_now=True, db_index=True)

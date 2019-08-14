
from .views import ImageViewSet

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'image', ImageViewSet, 'Image')

urlpatterns = router.urls
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

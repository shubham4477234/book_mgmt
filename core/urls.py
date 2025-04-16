from rest_framework.routers import DefaultRouter
from .views import BookViewSet, StudentViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'students', StudentViewSet)

urlpatterns = router.urls

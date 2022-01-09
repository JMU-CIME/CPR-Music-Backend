from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from teleband.users.api.views import UserViewSet
from teleband.courses.api.views import EnrollmentViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("enrollments", EnrollmentViewSet)


app_name = "api"
urlpatterns = router.urls

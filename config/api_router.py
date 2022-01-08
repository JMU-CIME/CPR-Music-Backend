from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from teleband.users.api.views import UserViewSet
from teleband.courses.api.views import CourseViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("courses", CourseViewSet, basename="Course")


app_name = "api"
urlpatterns = router.urls

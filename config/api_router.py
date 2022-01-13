from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from teleband.users.api.views import UserViewSet
from teleband.courses.api.views import EnrollmentViewSet, CourseViewSet
from teleband.assignments.api.views import AssignmentViewSet

if settings.DEBUG:
    router = DefaultRouter()
    nested_cls = routers.NestedDefaultRouter
else:
    router = SimpleRouter()
    nested_cls = routers.NestedSimpleRouter

router.register("users", UserViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("courses", CourseViewSet)
# router.register("assignments", AssignmentViewSet)
# router.register("courses/<slug:slug>/assignments", AssignmentViewSet)

courses_router = nested_cls(router, "courses", lookup="course_slug")
courses_router.register("assignments", AssignmentViewSet) #option basename omitted
# courses_router.register("activities", ActivityViewSet) #option basename omitted

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("", include(courses_router.urls)),
]

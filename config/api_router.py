from django.conf import settings
from django.urls import include, path

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

from teleband.users.api.views import UserViewSet
from teleband.courses.api.views import EnrollmentViewSet, CourseViewSet
from teleband.assignments.api.views import AssignmentViewSet, ActivityViewSet
from teleband.submissions.api.views import SubmissionViewSet, AttachmentViewSet
from teleband.musics.api.views import PieceViewSet
from teleband.instruments.api.views import InstrumentViewSet

if settings.DEBUG:
    router = DefaultRouter()
    nested_cls = routers.NestedDefaultRouter
else:
    router = SimpleRouter()
    nested_cls = routers.NestedSimpleRouter

router.register("users", UserViewSet)
router.register("enrollments", EnrollmentViewSet)
router.register("courses", CourseViewSet)
router.register("pieces", PieceViewSet)
router.register("instruments", InstrumentViewSet)

courses_router = nested_cls(router, "courses", lookup="course_slug")
courses_router.register("assignments", AssignmentViewSet)  # option basename omitted
courses_router.register("activities", ActivityViewSet)  # option basename omitted

assignments_router = nested_cls(courses_router, "assignments", lookup="assignment")
assignments_router.register("submissions", SubmissionViewSet)

attachments_router = nested_cls(assignments_router, "submissions", lookup="submission")
attachments_router.register("attachments", AttachmentViewSet)

app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("", include(courses_router.urls)),
    path("", include(assignments_router.urls)),
    path("", include(attachments_router.urls)),
]

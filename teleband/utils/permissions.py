import logging
from rest_framework import permissions

from teleband.courses.models import Enrollment

logger = logging.getLogger(__name__)


class IsTeacher(permissions.BasePermission):
    """
    Global permission check to only access if user is a
    teacher in the course.
    Assumes the viewset is nested under the courses router
    and therefore has course slug in view.kwargs or from
    the CourseViewSet itself
    """

    def has_permission(self, request, view):
        try:
            # if "course_slug_slug" in view.kwargs:
            e = Enrollment.objects.get(
                course__slug=view.kwargs["course_slug_slug"], user=request.user
            )
            # else:
            #     e = Enrollment.objects.get(course=view.get_object(), user=request.user)
            return e.role.name == "Teacher"
        except Enrollment.DoesNotExist:
            logger.info(
                "No Enrollment for {} in {}".format(
                    request.user, view.kwargs["course_slug_slug"]
                )
            )
        return False

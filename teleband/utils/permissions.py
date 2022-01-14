from rest_framework import permissions

from teleband.courses.models import Enrollment


class IsTeacher(permissions.BasePermission):
    """
    Global permission check to only access if user is a 
    teacher in the course.
    Assumes the viewset is nested under the courses router
    and therefore has course slug in view.kwargs
    """

    def has_permission(self, request, view):
        try:
            e = Enrollment.objects.get(
                course__slug=view.kwargs["course_slug_slug"],
                user=request.user
            )
            return e.role.name == "Teacher"
        except Enrollment.DoesNotExist:
            logger.info("No Enrollment for {} in {}".format(request.user, view.kwargs["course_slug_slug"]))
        return False


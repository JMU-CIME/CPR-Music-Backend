import pytest
from django.test import RequestFactory

from teleband.assignments.api.views import AssignmentViewSet
from teleband.courses.models import Enrollment

pytestmark = pytest.mark.django_db


class TestAssignmentViewSet:
    def test_get_queryset_student(self, enrollment: Enrollment, rf: RequestFactory):
        view = AssignmentViewSet()

        enrollment.role.name = "Student"
        enrollment.role.save()

        request = rf.get("/fake-url/")
        request.user = enrollment.user

        view.request = request
        setattr(view, "kwargs", {"course_slug_slug": enrollment.course.slug})

        queryset = view.get_queryset()
        # actually there is nothing in the queryset, need
        # to populate it with some assignments for this student
        # and some other students to actually check this

        # Make sure every assignment is assigned to me and only me
        for assignment in queryset:
            assert enrollment.user == assignment.enrollment.user

from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(VersionAdmin):
    list_display = ("id", "name", "slug", "owner")
    list_filter = ("owner",)
    raw_id_fields = ("users",)
    search_fields = ("name",)
    readonly_fields = ("slug",)


@admin.register(Enrollment)
class EnrollmentAdmin(VersionAdmin):
    list_display = ("id", "user", "course", "instrument", "role")
    list_filter = ("user", "course", "instrument", "role")

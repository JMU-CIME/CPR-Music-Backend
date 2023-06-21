from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Course, Enrollment


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0

@admin.register(Course)
class CourseAdmin(VersionAdmin):
    list_display = ("id", "name", "slug", "owner")
    list_filter = ("owner",)
    raw_id_fields = ("users",)
    search_fields = ("name",)
    readonly_fields = ("slug",)
    inlines = [EnrollmentInline]


@admin.register(Enrollment)
class EnrollmentAdmin(VersionAdmin):
    list_display = ("id", "user", "course", "instrument", "role")
    list_filter = ("course", "instrument", "role")
    search_fields = ("user__username", "course__name")

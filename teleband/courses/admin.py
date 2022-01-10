from django.contrib import admin

from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "owner")
    list_filter = ("owner",)
    raw_id_fields = ("users",)
    search_fields = ("name",)
    readonly_fields = ("slug",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "course", "instrument", "role")
    list_filter = ("user", "course", "instrument", "role")

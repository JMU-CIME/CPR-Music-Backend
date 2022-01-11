from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import ActivityCategory, ActivityType, Activity, Assignment


@admin.register(ActivityCategory)
class ActivityCategoryAdmin(VersionAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(ActivityType)
class ActivityTypeAdmin(VersionAdmin):
    list_display = ("id", "name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Activity)
class ActivityAdmin(VersionAdmin):
    list_display = ("id", "activity_type", "part", "body")
    list_filter = ("activity_type", "part")


@admin.register(Assignment)
class AssignmentAdmin(VersionAdmin):
    list_display = ("id", "activity", "user", "deadline", "instrument")
    list_filter = ("activity", "user", "deadline", "instrument")

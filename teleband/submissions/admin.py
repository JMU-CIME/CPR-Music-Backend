from django.contrib import admin
from reversion.admin import VersionAdmin

from .models import Submission, SubmissionAttachment, Grade


@admin.register(Submission)
class SubmissionAdmin(VersionAdmin):
    list_display = ("id", "assignment", "submitted", "content")
    list_filter = ("assignment", "submitted")


@admin.register(SubmissionAttachment)
class SubmissionAttachmentAdmin(VersionAdmin):
    list_display = ("id", "submission", "file")
    list_filter = ("submission",)


@admin.register(Grade)
class GradeAdmin(VersionAdmin):
    list_display = (
        "id",
        "student_submission",
        "own_submission",
        "grader",
        "rhythm",
        "tone",
        "expression",
    )
    list_filter = ("student_submission", "own_submission", "grader")

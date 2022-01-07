from django.contrib import admin

from .models import Submission, SubmissionAttachment


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "assignment", "submitted", "content")
    list_filter = ("assignment", "submitted")


@admin.register(SubmissionAttachment)
class SubmissionAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "submission", "file")
    list_filter = ("submission",)

from django.db import models
from django.conf import settings

from teleband.assignments.models import Assignment


class Submission(models.Model):

    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT)
    submitted = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assignment} ({self.submitted})"


class SubmissionAttachment(models.Model):

    submission = models.ForeignKey(Submission, on_delete=models.PROTECT)
    file = models.URLField()

    class Meta:
        verbose_name = "Submission Attachment"
        verbose_name_plural = "Submission Attachments"

    def __str__(self):
        return f"{self.submission}: {self.file}"


class Grade(models.Model):

    submission = models.ForeignKey(Submission, on_delete=models.PROTECT)
    grader = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="grades", on_delete=models.PROTECT
    )
    rhythm = models.FloatField(null=True, blank=True)
    tone = models.FloatField(null=True, blank=True)
    expression = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

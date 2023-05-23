from django.db import models
from django.conf import settings

from teleband.assignments.models import Assignment


class Grade(models.Model):

    # submission = models.ForeignKey(Submission, related_name="grades", on_delete=models.PROTECT)
    grader = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="grades", on_delete=models.PROTECT
    )
    rhythm = models.FloatField(null=True, blank=True)
    tone = models.FloatField(null=True, blank=True)
    expression = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Submission(models.Model):
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="student_submission",
    )
    self_grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="own_submission",
    )
    assignment = models.ForeignKey(Assignment, on_delete=models.PROTECT, related_name="submissions")
    index = models.PositiveIntegerField(default=0)
    submitted = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assignment} ({self.submitted})"


class SubmissionAttachment(models.Model):

    submission = models.ForeignKey(
        Submission, related_name="attachments", on_delete=models.PROTECT
    )
    file = models.FileField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Submission Attachment"
        verbose_name_plural = "Submission Attachments"
        ordering = ["-submitted"]

    def __str__(self):
        return f"{self.submission}: {self.file}"

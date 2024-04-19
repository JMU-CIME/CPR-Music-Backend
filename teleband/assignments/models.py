from django.db import models
from django.conf import settings

from teleband.courses.models import Course, Enrollment
from teleband.instruments.models import Instrument
from teleband.musics.models import PartType, Part, Piece


class ActivityCategory(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Activity Category"
        verbose_name_plural = "Activity Categories"

    def __str__(self):
        return self.name


class ActivityType(models.Model):

    name = models.CharField(unique=True, max_length=255)
    category = models.ForeignKey(ActivityCategory, on_delete=models.PROTECT)
    

    class Meta:
        verbose_name = "Activity Type"
        verbose_name_plural = "Activity Types"

    def __str__(self):
        return f"{self.name}"


class Activity(models.Model):

    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    part_type = models.ForeignKey(PartType, null=True, on_delete=models.PROTECT)
    body = models.TextField()
    number_of_submissions = models.PositiveIntegerField(default=1)
    activity_type_name = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.activity_type}: {self.part_type}"


class PiecePlan(models.Model):

    name = models.CharField(max_length=255)
    activities = models.ManyToManyField(Activity, through="PlannedActivity")
    piece = models.ForeignKey(Piece, on_delete=models.PROTECT)
    type = models.CharField(max_length=255, null=True, blank=True)

    def assign(self, enrollment, instrument, deadline=None):
        assignments = []
        piece = self.piece
        for activity in self.activities.all():
            part = Part.for_activity(activity, piece)
            assignments.append(Assignment.objects.create(
                activity=activity,
                enrollment=enrollment,
                part=part,
                instrument=instrument,
                piece_plan=self,
                deadline=deadline,
                piece=self.piece,
            ))
        return assignments

    def __str__(self):
        if self.type:
            return f"{self.name}: {self.piece.name} ({self.type})"
        else:
            return f"{self.name}: {self.piece.name} "


class Assignment(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.PROTECT)
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    deadline = models.DateField(null=True, blank=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    piece_plan = models.ForeignKey(PiecePlan, on_delete=models.PROTECT, null=True, blank=True)
    piece = models.ForeignKey(Piece, on_delete=models.PROTECT, null=True, blank=True)
    group = models.ForeignKey("AssignmentGroup", on_delete=models.PROTECT, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # FIXME: do this with https://docs.djangoproject.com/en/5.0/ref/models/options/#unique-together instead.
        # nevermind, this may be deprecated
        constraints = [
            models.UniqueConstraint(fields=["activity", "enrollment", "piece"], name="unique_assignment")
        ]

    def __str__(self):
        return f"[{self.enrollment.user.username}] {self.activity.id} {self.piece}"
    

class AssignmentGroup(models.Model):

    type = models.CharField(max_length=255, null=True, blank=True)
    

class PlannedActivity(models.Model):

    piece_plan = models.ForeignKey(PiecePlan, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ["piece_plan", "activity"]
        ordering = ["piece_plan__name", "order"]
        verbose_name_plural = "Planned Activities"

    def __str__(self):
        return f"{self.piece_plan.name}: {self.activity}"


class Curriculum(models.Model):

    name = models.CharField(max_length=255)
    ordered = models.BooleanField(default=False)
    piece_plans = models.ManyToManyField(PiecePlan, through="CurriculumEntry")
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Curriculum"
        verbose_name_plural = "Curricula"

    def __str__(self):
        return f"{self.name}: {self.course.name}"

class CurriculumEntry(models.Model):

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    piece_plan = models.ForeignKey(PiecePlan, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ["curriculum", "piece_plan"]
        ordering = ["order"]

    def __str__(self):
        return f"{self.curriculum.name}: {self.piece_plan.name}"


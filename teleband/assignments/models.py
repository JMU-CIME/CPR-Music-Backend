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
        return f"{self.name}: {self.category}"


class Activity(models.Model):

    activity_type = models.ForeignKey(ActivityType, on_delete=models.PROTECT)
    part_type = models.ForeignKey(PartType, null=True, on_delete=models.PROTECT)
    body = models.TextField()
    number_of_submissions = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.activity_type}: {self.part_type}"


class PiecePlan(models.Model):

    name = models.CharField(max_length=255)
    activities = models.ManyToManyField(Activity, through="PlannedActivity")
    piece = models.ForeignKey(Piece, on_delete=models.PROTECT)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Piece Plan"


class Assignment(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.PROTECT)
    part = models.ForeignKey(Part, on_delete=models.PROTECT)
    deadline = models.DateField(null=True, blank=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    piece_plan = models.ForeignKey(PiecePlan, null=True, blank=True, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.enrollment.user.username}] {self.activity} {self.part.piece}"
    
class PlannedActivity(models.Model):

    piece_plan = models.ForeignKey(PiecePlan, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ["piece_plan", "activity"]
        ordering = ["order"]
        verbose_name = "Planned Activity"
        verbose_name_plural = "Planned Activities"

    def __str__(self):
        return f"{self.piece_plan.name}: {self.activity}"


class Curriculum(models.Model):

    name = models.CharField(max_length=255)
    ordered = models.BooleanField(default=False)
    piece_plans = models.ManyToManyField(PiecePlan, through="CurriculumEntry")
    course = models.ForeignKey(Course, on_delete=models.PROTECT)


class CurriculumEntry(models.Model):

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    piece_plan = models.ForeignKey(PiecePlan, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ["curriculum", "piece_plan"]
        ordering = ["order"]
        verbose_name = "Curriculum Entry"
        verbose_name_plural = "Curriculum Entries"

    def __str__(self):
        return f"{self.curriculum.name}: {self.piece_plan.name}"


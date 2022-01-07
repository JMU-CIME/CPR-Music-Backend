from django.db import models
from django.conf import settings

from teleband.instruments.models import Instrument
from teleband.musics.models import PartTransposition


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
    part = models.ForeignKey(PartTransposition, on_delete=models.PROTECT)
    body = models.TextField()

    class Meta:
        verbose_name = "Activity"
        verbose_name_plural = "Activities"

    def __str__(self):
        return f"{self.activity_type}: {self.part}"


class Assignment(models.Model):

    activity = models.ForeignKey(Activity, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    deadline = models.DateField(null=True, blank=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)

    def __str__(self):
        return f"[{self.user.username}] {self.activity}"

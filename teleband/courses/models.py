from django.db import models
from django.conf import settings

from teleband.instruments.models import Instrument
from teleband.users.models import Role


class Course(models.Model):

    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="courses", on_delete=models.PROTECT
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Enrollment")

    def __str__(self):
        return self.name


class Enrollment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.user.username} -> {self.course.name}"

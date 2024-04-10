from django.db import models
from django.conf import settings

from teleband.instruments.models import Instrument
from teleband.users.models import Role
from teleband.utils.fields import generate_slug_from_name


class Course(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="courses", on_delete=models.PROTECT
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Enrollment")
    start_date = models.DateField()
    end_date = models.DateField()
    can_edit_instruments = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            generate_slug_from_name(self, Course)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Enrollment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, null=True, on_delete=models.PROTECT)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    class Meta:
        unique_together = ["user", "course"]

    def __str__(self):
        return f"{self.user.username}, {self.role.name} in {self.course.name}"

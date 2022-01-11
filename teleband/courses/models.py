from django.db import models
from django.conf import settings

from teleband.instruments.models import Instrument
from teleband.users.models import Role


import itertools
from django.utils.text import slugify


def generate_slug_from_name(instance, model_cls):
    # based on https://simpleit.rocks/python/django/generating-slugs-automatically-in-django-easy-solid-approaches/
    max_length = instance._meta.get_field("slug").max_length
    value = instance.name
    slug_candidate = slug_original = slugify(value, allow_unicode=True)
    for i in itertools.count(1):
        if not model_cls.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = "{}-{}".format(slug_original, i)

    instance.slug = slug_candidate


class Course(models.Model):

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="courses", on_delete=models.PROTECT
    )
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Enrollment")
    start_date = models.DateField()
    end_date = models.DateField()

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

    def __str__(self):
        return f"{self.user.username} -> {self.course.name}"

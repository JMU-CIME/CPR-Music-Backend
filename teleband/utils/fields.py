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

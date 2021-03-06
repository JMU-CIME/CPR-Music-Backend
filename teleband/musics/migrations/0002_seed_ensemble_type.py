# Generated by Django 3.2.11 on 2022-01-09 19:31

from django.db import migrations


def update_site_forward(apps, schema_editor):
    """Set site domain and name."""
    EnsembleType = apps.get_model("musics", "EnsembleType")
    for name in ["Band", "Orchestra"]:
        EnsembleType.objects.update_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("musics", "0001_initial"),
    ]

    operations = [migrations.RunPython(update_site_forward, migrations.RunPython.noop)]

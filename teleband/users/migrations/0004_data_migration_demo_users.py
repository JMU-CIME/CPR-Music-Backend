# Generated by Django 3.2.11 on 2022-01-14 02:19

from django.db import migrations
from django.contrib.auth.hashers import make_password


def demo_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    User.objects.update_or_create(
        email="michael@tele.band",
        username="demomike",
        name="Michael Stewart",
        password=make_password("michael"),
    )
    User.objects.update_or_create(
        email="dave@tele.band",
        username="demodave",
        name="Dave Stringham",
        password=make_password("dave"),
    )
    User.objects.update_or_create(
        email="alden@tele.band",
        username="demoalden",
        name="Alden Snell",
        password=make_password("alden"),
    )


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_data_migration_student_teacher"),
    ]

    operations = [migrations.RunPython(demo_users, migrations.RunPython.noop)]

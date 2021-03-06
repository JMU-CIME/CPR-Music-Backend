# Generated by Django 3.2.11 on 2022-01-08 02:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("submissions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Grade",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rhythm", models.FloatField(blank=True, null=True)),
                ("tone", models.FloatField(blank=True, null=True)),
                ("expression", models.FloatField(blank=True, null=True)),
                (
                    "grader",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="grades",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="submissions.submission",
                    ),
                ),
            ],
        ),
    ]

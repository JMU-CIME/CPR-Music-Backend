# Generated by Django 3.2.11 on 2022-01-08 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
        ("assignments", "0005_auto_20220108_1517"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assignment",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="courses.course"
            ),
        ),
    ]

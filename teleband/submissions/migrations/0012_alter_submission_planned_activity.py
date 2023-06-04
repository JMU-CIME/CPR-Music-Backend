# Generated by Django 3.2.11 on 2023-06-04 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0025_auto_20230604_1328'),
        ('submissions', '0011_create_submission_plannedactivity_references'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='planned_activity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='assignments.plannedactivity'),
        ),
    ]
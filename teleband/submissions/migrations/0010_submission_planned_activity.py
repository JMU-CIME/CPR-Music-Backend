# Generated by Django 3.2.11 on 2023-06-02 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0023_auto_20230602_1258'),
        ('submissions', '0009_submission_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='planned_activity',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='assignments.plannedactivity'),
        ),
    ]
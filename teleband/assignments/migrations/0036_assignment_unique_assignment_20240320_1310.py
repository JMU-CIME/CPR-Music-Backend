from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0035_dedupe_assignments'),
    ]

    operations = [
        # migrations.RunPython(remove_dupes, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name='assignment',
            constraint=models.UniqueConstraint(fields=('activity', 'enrollment', 'piece'), name='unique_assignment'),
        ),
    ]

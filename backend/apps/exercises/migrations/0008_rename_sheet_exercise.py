from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("exercises", "0007_alter_uploadedfile_file_type"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Sheet",
            new_name="Exercise",
        ),
        migrations.RunSQL(
            "alter sequence exercises_sheet_id_seq rename to exercises_exercise_id_seq;",
            "alter sequence exercises_exercise_id_seq rename to exercises_sheet_id_seq;",
        ),
        migrations.RunSQL(
            "alter sequence exercises_sheet_tags_id_seq rename to exercises_exercise_tags_id_seq;",
            "alter sequence exercises_exercise_tags_id_seq rename to exercises_sheet_tags_id_seq ;",
        ),
    ]

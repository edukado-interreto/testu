import django.contrib.auth.validators
from django.db import migrations, models


def fill_username(apps, schema_editor):
    User = apps.get_model("core", "User")
    for row in User.objects.all():
        row.username = row.email
        row.save(update_fields=["username"])


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_user_username"),
    ]

    operations = [
        migrations.RunPython(fill_username, reverse_code=migrations.RunPython.noop),
    ]

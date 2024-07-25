# Generated by Django 4.2.6 on 2024-07-09 12:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workflows", "0007_alter_workflow_core_alter_workflow_is_update"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workflow",
            name="status",
            field=models.CharField(
                choices=[
                    ("running", "Running"),
                    ("approval", "Waiting for approva"),
                    ("completed", "Completed"),
                    ("error", "Error"),
                ],
                default="running",
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="workflow",
            name="workflow_type",
            field=models.CharField(
                choices=[
                    ("HEP_CREATE", "HEP create"),
                    ("HEP_UPDATE", "HEP update"),
                    ("AUTHOR_CREATE", "Author create"),
                    ("AUTHOR_UPDATE", "Author update"),
                ],
                default="HEP_CREATE",
                max_length=30,
            ),
        ),
    ]
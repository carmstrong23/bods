# Generated by Django 3.2.16 on 2023-07-18 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("otc", "0008_auto_20230622_1657"),
    ]

    operations = [
        migrations.CreateModel(
            name="InactiveService",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("registration_number", models.CharField(max_length=20, unique=True)),
                ("registration_status", models.CharField(blank=True, max_length=20)),
                ("effective_date", models.DateField(null=True)),
            ],
        ),
    ]

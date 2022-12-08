# Generated by Django 3.2.13 on 2022-11-30 16:50

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("organisation", "0057_add_unique_together_contraint"),
        ("fares_validator", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="faresvalidation",
            name="dataset_id",
        ),
        migrations.AddField(
            model_name="faresvalidation",
            name="revision",
            field=models.ForeignKey(
                default=1,
                help_text="The revision that validation occurred in.",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="fares_validations",
                to="organisation.datasetrevision",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="faresvalidation",
            name="category",
            field=models.CharField(
                help_text="The category of the observation.", max_length=1024
            ),
        ),
        migrations.AlterField(
            model_name="faresvalidation",
            name="error",
            field=models.CharField(
                help_text="The detailed error of the observation.", max_length=2000
            ),
        ),
        migrations.AlterField(
            model_name="faresvalidation",
            name="error_line_no",
            field=models.IntegerField(help_text="The line number of the observation."),
        ),
        migrations.AlterField(
            model_name="faresvalidation",
            name="file_name",
            field=models.CharField(
                help_text="The name of the file the observation occurs in.",
                max_length=256,
            ),
        ),
        migrations.AlterField(
            model_name="faresvalidation",
            name="important_note",
            field=models.CharField(
                default="Data containing this warning will be rejected by BODS after January 2023. Please contact your ticket machine supplier",
                help_text="The Important Note error of the observation.",
                max_length=2000,
            ),
        ),
        migrations.AlterField(
            model_name="faresvalidation",
            name="reference",
            field=models.CharField(
                default="Please see BODS Fares Validator Guidance v0.2",
                help_text="The reference of the observation",
                max_length=1024,
            ),
        ),
        migrations.AlterField(
            model_name="faresvalidation",
            name="type_of_observation",
            field=models.CharField(help_text="Type Of Observation", max_length=1024),
        ),
        migrations.CreateModel(
            name="FaresValidationResult",
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
                ("count", models.IntegerField(help_text="Number of fare violations.")),
                (
                    "report_file_name",
                    models.CharField(
                        help_text="The name of the report file.", max_length=256
                    ),
                ),
                (
                    "created",
                    django_extensions.db.fields.CreationDateTimeField(
                        auto_now_add=True, verbose_name="created"
                    ),
                ),
                (
                    "organisation",
                    models.ForeignKey(
                        help_text="Bus portal organisation.",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organisation.organisation",
                    ),
                ),
                (
                    "revision",
                    models.OneToOneField(
                        help_text="The revision being validated.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fares_validation_result",
                        to="organisation.datasetrevision",
                    ),
                ),
            ],
        ),
    ]

import os
from typing import Final

from celery import Celery
from celery.schedules import crontab
from django.apps import AppConfig, apps
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "config.settings.local"
    )  # pragma: no cover

app = Celery("transit_odp")

PIPELINE_TASKS: Final = "transit_odp.pipelines.tasks."
TIMETABLE_TASKS: Final = "transit_odp.timetables.tasks."
AVL_TASKS: Final = "transit_odp.avl.tasks."
FARES_TASKS: Final = "transit_odp.fares.tasks."
ADMIN_TASKS: Final = "transit_odp.site_admin.tasks."


class CeleryAppConfig(AppConfig):
    name = "transit_odp.taskapp"
    verbose_name = "Celery Config"

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        # - namespace='CELERY' means all celery-related configuration keys
        #   should have a `CELERY_` prefix.
        app.config_from_object("django.conf:settings", namespace="CELERY")
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        app.conf.beat_schedule = {
            "monitor_feeds": {
                "task": TIMETABLE_TASKS + "task_update_remote_timetables",
                "schedule": crontab(minute=0, hour=4),
            },
            "monitor_feeds_afternoon": {
                "task": TIMETABLE_TASKS + "task_update_remote_timetables",
                "schedule": crontab(minute=0, hour=16),
            },
            "retry_unavailable_feeds": {
                "task": TIMETABLE_TASKS + "task_retry_unavailable_timetables",
                "schedule": crontab(minute=0),
            },
            "deactivate_txc_2.1_datasets": {
                "task": TIMETABLE_TASKS + "task_deactivate_txc_2_1",
                "schedule": crontab(minute=0, hour=2),
            },
            "monitor_fares_dataset": {
                "task": FARES_TASKS + "task_update_remote_fares",
                "schedule": crontab(minute=0, hour=4),
            },
            "monitor_fares_dataset_afternoon": {
                "task": FARES_TASKS + "task_update_remote_fares",
                "schedule": crontab(minute=0, hour=16),
            },
            "retry_unavailable_fares_datasets": {
                "task": FARES_TASKS + "task_retry_unavailable_fares",
                "schedule": crontab(minute=0),
            },
            # scheduled 1 hour after task_set_expired_feeds to ensure archive
            # excluded newly expired datasets
            "create_bulk_data_archive": {
                "task": PIPELINE_TASKS + "task_create_bulk_data_archive",
                "schedule": crontab(minute=0, hour=6),
            },
            # scheduled 1 hour after task_set_expired_feeds to ensure archive
            # excluded newly expired datasets
            "create_change_data_archive": {
                "task": PIPELINE_TASKS + "task_create_change_data_archive",
                "schedule": crontab(minute=0, hour=6),
            },
            # scheduled at 1am and this task should be the first that runs
            # before other tasks
            "run_naptan_etl": {
                "task": PIPELINE_TASKS + "task_run_naptan_etl",
                "schedule": crontab(minute=0, hour=1),
            },
            "dqs_monitor": {
                "task": PIPELINE_TASKS + "task_dqs_monitor",
                "schedule": 60.0,
            },
            "monitor_avl_feeds": {
                "task": AVL_TASKS + "task_monitor_avl_feeds",
                "schedule": 30.0,
            },
            "create_siri_zip": {
                "task": AVL_TASKS + "task_create_sirivm_zipfile",
                "schedule": 10.0,
            },
            "create_gtfsrt_zip": {
                "task": AVL_TASKS + "task_create_gtfsrt_zipfile",
                "schedule": 10.0,
            },
            "timetable_upgrade_task": {
                "task": TIMETABLE_TASKS + "task_reprocess_file_based_datasets",
                "schedule": crontab(minute=0, hour="0, 2, 4, 18, 20, 22"),
            },
            "log_stuck_tasks": {
                "task": TIMETABLE_TASKS + "task_log_stuck_revisions",
                "schedule": crontab(minute=0, hour=18),
            },
            "create_daily_api_stats": {
                "task": ADMIN_TASKS + "task_create_daily_api_stats",
                "schedule": crontab(minute=10, hour=0),
            },
            "save_operational_stats": {
                "task": ADMIN_TASKS + "task_save_operational_stats",
                "schedule": crontab(minute=0, hour=23),
            },
            "save_operational_exports": {
                "task": ADMIN_TASKS + "task_create_operational_exports_archive",
                "schedule": 1.0 * 60.0 * 60.0,
            },
        }

        if hasattr(settings, "RAVEN_CONFIG"):
            # Celery signal registration
            # Since raven is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            # @formatter:off
            from raven import Client as RavenClient
            from raven.contrib.celery import (
                register_logger_signal as raven_register_logger_signal,
            )
            from raven.contrib.celery import register_signal as raven_register_signal

            # @formatter:on

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG["dsn"])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)

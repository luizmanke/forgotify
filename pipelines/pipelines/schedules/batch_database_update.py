from dagster import DefaultScheduleStatus, ScheduleDefinition

from pipelines.jobs.batch_database_update import batch_database_update as job


batch_database_update = ScheduleDefinition(
    job=job,
    cron_schedule="*/5 * * * *",
    default_status=DefaultScheduleStatus.RUNNING
)

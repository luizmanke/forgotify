from dagster import job, op
from dagster import DefaultScheduleStatus, ScheduleDefinition


@op
def get_number():
    return 200


@job
def pipeline():
    get_number()


pipeline_schedule = ScheduleDefinition(
    job=pipeline,
    cron_schedule="*/5 * * * *",
    default_status=DefaultScheduleStatus.RUNNING
)

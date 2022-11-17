from dagster import repository

from pipelines.jobs.batch_database_update import batch_database_update as batch_database_update_job
from pipelines.schedules.batch_database_update import batch_database_update as batch_database_update_schedule


jobs_list = [
    batch_database_update_job
]

schedules_list = [
    batch_database_update_schedule
]


@repository
def pipelines():
    return [
        *jobs_list,
        *schedules_list
    ]

from dagster import job, op

from batch_database_update.main import run


@op
def run_batch_database_update():
    run()


@job
def batch_database_update():
    run_batch_database_update()

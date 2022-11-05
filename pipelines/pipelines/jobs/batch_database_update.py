from dagster import job, op


@op
def get_number():
    return 200


@job
def batch_database_update():
    get_number()

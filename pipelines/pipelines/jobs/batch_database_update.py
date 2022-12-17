from dagster import job, op
from dagster import In, Nothing

from batch_database_update import main


@op
def update_artists():
    main.update_artists()


@op(ins={"depends_on": In(Nothing)})
def update_tracks():
    main.update_tracks()


@job
def batch_database_update():
    update_artists_success = update_artists()
    update_tracks(depends_on=update_artists_success)

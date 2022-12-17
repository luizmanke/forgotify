from dagster import job, op

from batch_database_update import main


@op
def update_artists() -> bool:
    main.update_artists()
    return True


@op
def update_tracks(previous_state: bool) -> bool:
    main.update_tracks()
    return True


@job
def batch_database_update():

    update_artists_state = update_artists()
    update_tracks(update_artists_state)

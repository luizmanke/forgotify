"""Create tracks table

Revision ID: 1fd33fc239d2
Revises: c3234d2b1d35
Create Date: 2022-12-03 20:50:17.451116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1fd33fc239d2"
down_revision = "c3234d2b1d35"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "artists_to_tracks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("artist_id", sa.String(), nullable=False),
        sa.Column("track_id", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_table(
        "tracks",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("popularity", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )


def downgrade() -> None:
    op.drop_table("tracks")
    op.drop_table("artists_to_tracks")

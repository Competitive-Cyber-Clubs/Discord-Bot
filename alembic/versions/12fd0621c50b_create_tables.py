"""create tables

Revision ID: 12fd0621c50b
Revises: 
Create Date: 2022-11-24 14:18:50.903819

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "12fd0621c50b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'schools',
        sa.Column('school', sa.TEXT, unique=True, nullable=False),
        sa.Column('region', sa.TEXT, nullable=False),
        sa.Column('color', sa.INTEGER, nullable=False),
        sa.Column('id', sa.BIGINT, nullable=False),
        sa.Column('added_by', sa.TEXT, nullable=False),
        sa.Column('added_by_id', sa.BIGINT, nullable=False),
        sa.PrimaryKeyConstraint('school')
    )
    op.create_table(
        'bot_admins',
        sa.Column('id', sa.BIGINT, unique=True, nullable=False),
        sa.Column('name', sa.TEXT, nullable=False),
        sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table(
        'admin_channels',
        sa.Column('id', sa.BIGINT, unique=True, nullable=False),
        sa.Column('guild_id', sa.BIGINT, nullable=False),
        sa.Column('log', sa.Boolean, default=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'regions',
        sa.Column('name', sa.TEXT, unique=True, nullable=False),
        sa.Column('id', sa.BIGINT, nullable=False),
        sa.PrimaryKeyConstraint('name')
    )
    op.create_table(
        'errors',
        sa.Column('id', sa.BIGINT, unique=True, nullable=False),
        sa.Column('command', sa.TEXT, nullable=False),
        sa.Column('message', sa.TEXT, nullable=False),
        sa.Column('error', sa.TEXT, nullable=False),
        sa.Column('time', sa.TIMESTAMP, nullable=False),
        sa.Column('ack', sa.Boolean, nullable=False, default=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'keys',
        sa.Column('key', sa.TEXT, unique=True, nullable=False),
        sa.Column('value', sa.TEXT, nullable=False),
    )
    op.create_table(
        'messages',
        sa.Column('name', sa.TEXT, unique=True, nullable=False),
        sa.Column('message', sa.TEXT, nullable=False),
        sa.PrimaryKeyConstraint('name')
    )
    op.create_table(
        'reports',
        sa.Column('id', sa.BIGINT, unique=True, nullable=False),
        sa.Column('name', sa.TEXT, nullable=False),
        sa.Column('name_id', sa.BIGINT, nullable=False),
        sa.Column('message', sa.TEXT, nullable=False),
        sa.Column('time', sa.TIMESTAMP, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('schools')
    op.drop_table('bot_admins')
    op.drop_table('admin_channels')
    op.drop_table('regions')
    op.drop_table('errors')
    op.drop_table('keys')
    op.drop_table('messages')
    op.drop_table('reports')

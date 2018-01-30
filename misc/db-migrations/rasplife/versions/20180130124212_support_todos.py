"""support todos

Revision ID: 317b581bde90
Revises: e75eab5b81d9
Create Date: 2018-01-30 12:42:12.152934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '317b581bde90'
down_revision = 'e75eab5b81d9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'todo',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('date', sa.Date),
        sa.Column('created_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('updated_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('deleted_at', sa.Integer, server_default=sa.text('0'))
    )

    op.create_table(
        'todo_item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('todo_id', sa.Integer, nullable=False),
        sa.Column('content', sa.String),
        sa.Column('status', sa.Integer, server_default=sa.text('0')),
        sa.Column('created_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('updated_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('deleted_at', sa.Integer, server_default=sa.text('0'))
    )

    op.create_index('idx_todo_user_id', 'todo', ['user_id'])
    op.create_index('idx_todo_date', 'todo', ['date'])
    op.create_index('idx_todo_item_todo_id', 'todo_item', ['todo_id'])


def downgrade():
    op.drop_table('todo')
    op.drop_table('todo_item')

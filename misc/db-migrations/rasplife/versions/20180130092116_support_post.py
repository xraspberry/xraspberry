"""support post

Revision ID: e75eab5b81d9
Revises: b675d4882d82
Create Date: 2018-01-30 09:21:16.417942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e75eab5b81d9'
down_revision = 'b675d4882d82'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'post',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('title', sa.String),
        sa.Column('content', sa.String),
        sa.Column('update_count', sa.Integer, server_default=sa.text('1')),
        sa.Column('read_count', sa.Integer, server_default=sa.text('0')),
        sa.Column('created_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('updated_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('deleted_at', sa.Integer, server_default=sa.text('0'))
    )

    op.create_index('idx_post_user_id', 'post', ['user_id'])
    op.create_index('idx_post_title', 'post', ['title'])


def downgrade():
    op.drop_table('post')

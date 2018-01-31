"""add diary

Revision ID: 3aa82b7aaa86
Revises: 317b581bde90
Create Date: 2018-01-31 10:23:04.424144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa82b7aaa86'
down_revision = '317b581bde90'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column('post_type', sa.Integer, server_default=sa.text("0")))
    op.create_index('idx_post_post_type', 'post', ['post_type'])


def downgrade():
    op.drop_column('post', 'post_type')

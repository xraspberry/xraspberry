"""init db

Revision ID: b675d4882d82
Revises: 
Create Date: 2018-01-24 16:34:11.605451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b675d4882d82'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('nickname', sa.String),
        sa.Column('sex', sa.Integer),
        sa.Column('birth', sa.DateTime),
        sa.Column('birth_place', sa.String),
        sa.Column('phone', sa.ARRAY(sa.String)),
        sa.Column('email', sa.ARRAY(sa.String)),
        sa.Column('password_hash', sa.String),
        sa.Column('role', sa.Integer),
        sa.Column('created_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('updated_at', sa.Integer, server_default=sa.text('extract(epoch from now())::int')),
        sa.Column('deleted_at', sa.Integer, server_default=sa.text('0'))
    )

    op.create_index('idx_user_username', 'user', ['username'], unique=True)


def downgrade():
    op.drop_table('user')

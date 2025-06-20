"""Create tables

Revision ID: 6d78d455feff
Revises: 
Create Date: 2025-05-27 08:03:30.345500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d78d455feff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('budget_history',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.String(length=100), nullable=False),
    sa.Column('request_data', sa.JSON(), nullable=False),
    sa.Column('response_data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('description_history',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.String(length=100), nullable=False),
    sa.Column('request_data', sa.JSON(), nullable=False),
    sa.Column('response_data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('examples',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('translation_history',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.String(length=100), nullable=False),
    sa.Column('source_text', sa.Text(), nullable=False),
    sa.Column('translated_text', sa.Text(), nullable=False),
    sa.Column('source_language', sa.String(length=10), nullable=False),
    sa.Column('target_language', sa.String(length=10), nullable=False),
    sa.Column('source_language_label', sa.String(length=100), nullable=False),
    sa.Column('target_language_label', sa.String(length=100), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('trip_history',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.String(length=100), nullable=False),
    sa.Column('request_data', sa.JSON(), nullable=False),
    sa.Column('response_data', sa.JSON(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fullName', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('passport_number', sa.String(length=50), nullable=True),
    sa.Column('travel_preferences', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('api_hits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('endpoint', sa.String(length=255), nullable=False),
    sa.Column('method', sa.String(length=10), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('user_agent', sa.Text(), nullable=True),
    sa.Column('status_code', sa.Integer(), nullable=True),
    sa.Column('response_time', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('app_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(length=100), nullable=False),
    sa.Column('value', sa.Text(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['updated_by'], ['admins.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('app_config')
    op.drop_table('api_hits')
    op.drop_table('users')
    op.drop_table('trip_history')
    op.drop_table('translation_history')
    op.drop_table('examples')
    op.drop_table('description_history')
    op.drop_table('budget_history')
    op.drop_table('admins')
    # ### end Alembic commands ###

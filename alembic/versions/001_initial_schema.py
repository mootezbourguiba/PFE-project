"""Initial schema: Create User table

Revision ID: 001
Revises: 
Create Date: 2026-07-15 22:45:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create the initial database schema.
    
    This migration creates the User table and the alembic_version table
    for tracking migration versions.
    """
    # Create user enum type
    user_role_enum = sa.Enum('administrator', 'maintenance_engineer', 'drone_operator', name='userrole')
    user_role_enum.create(op.get_bind())
    
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', user_role_enum, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # Create indexes
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)


def downgrade() -> None:
    """
    Rollback the initial database schema.
    
    This migration drops the User table and the user role enum.
    """
    # Drop indexes
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    
    # Drop user table
    op.drop_table('user')
    
    # Drop user role enum
    sa.Enum(name='userrole').drop(op.get_bind())

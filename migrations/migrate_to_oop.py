"""Migrate to OOP structure

Revision ID: migrate_to_oop
Revises: bf99e8100b85
Create Date: 2024-03-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'migrate_to_oop'
down_revision = 'bf99e8100b85'
branch_labels = None
depends_on = None

def upgrade():
    # Add created_at and updated_at to existing tables if they don't exist
    tables = ['user', 'product', 'cart', 'order']
    
    for table in tables:
        # Check if the column exists before adding it
        with op.batch_alter_table(table) as batch_op:
            try:
                batch_op.add_column(sa.Column('updated_at', sa.DateTime))
            except Exception:
                pass  # Column might already exist

def downgrade():
    # Remove added columns if needed
    tables = ['user', 'product', 'cart', 'order']
    
    for table in tables:
        with op.batch_alter_table(table) as batch_op:
            try:
                batch_op.drop_column('updated_at')
            except Exception:
                pass  # Column might not exist 
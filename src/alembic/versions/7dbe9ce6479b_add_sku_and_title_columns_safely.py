"""Add sku and title columns safely

Revision ID: 7dbe9ce6479b
Revises: 9cac49144ad4
Create Date: 2025-10-24 12:23:03.627479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dbe9ce6479b'
down_revision = '9cac49144ad4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add columns as nullable first
    op.add_column('product_models', sa.Column('sku', sa.String(), nullable=True))
    op.add_column('product_models', sa.Column('title', sa.String(), nullable=True))
    
    # Update existing records with default values based on code
    op.execute("""
        UPDATE product_models 
        SET title = CASE 
            WHEN code IS NOT NULL THEN REPLACE(REPLACE(code, '_', ' '), 'IPHONE', 'iPhone')
            ELSE 'Untitled Product'
        END
        WHERE title IS NULL
    """)
    
    # Now make title NOT NULL since all records have values
    op.alter_column('product_models', 'title', nullable=False)
    
    # Add unique constraint for sku
    op.create_unique_constraint('uq_product_models_sku', 'product_models', ['sku'])


def downgrade() -> None:
    # Remove constraints and columns
    op.drop_constraint('uq_product_models_sku', 'product_models', type_='unique')
    op.drop_column('product_models', 'title')
    op.drop_column('product_models', 'sku')
"""change_family_labels_to_json

Revision ID: 597d978496b6
Revises: d7c796b8849f
Create Date: 2026-01-30 23:21:25.697449

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '597d978496b6'
down_revision = 'd7c796b8849f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Step 1: Add a temporary column for the JSON data
    op.execute("ALTER TABLE families ADD COLUMN labels_temp JSON")
    
    # Step 2: Convert the array data to JSON in the temp column
    op.execute("""
        UPDATE families 
        SET labels_temp = CASE 
            WHEN labels IS NOT NULL AND array_length(labels, 1) > 0 
            THEN labels[1]::json 
            ELSE NULL 
        END
    """)
    
    # Step 3: Drop the old column
    op.execute("ALTER TABLE families DROP COLUMN labels")
    
    # Step 4: Rename the temp column to labels
    op.execute("ALTER TABLE families RENAME COLUMN labels_temp TO labels")


def downgrade() -> None:
    # Step 1: Add a temporary array column
    op.execute("ALTER TABLE families ADD COLUMN labels_temp VARCHAR[]")
    
    # Step 2: Convert JSON back to array
    op.execute("""
        UPDATE families 
        SET labels_temp = CASE 
            WHEN labels IS NOT NULL 
            THEN ARRAY[labels::text] 
            ELSE NULL 
        END
    """)
    
    # Step 3: Drop the JSON column
    op.execute("ALTER TABLE families DROP COLUMN labels")
    
    # Step 4: Rename temp column to labels
    op.execute("ALTER TABLE families RENAME COLUMN labels_temp TO labels")
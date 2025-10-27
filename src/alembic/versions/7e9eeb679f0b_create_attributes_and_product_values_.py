"""create attributes and product values model

Revision ID: 7e9eeb679f0b
Revises: 7dbe9ce6479b
Create Date: 2025-10-27 18:21:52.751705

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7e9eeb679f0b'
down_revision = '7dbe9ce6479b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create PostgreSQL enum types first
    attributetype_enum = postgresql.ENUM('TEXT', 'TEXTAREA', 'NUMBER', 'BOOLEAN', 'SIMPLE_SELECT', 'MULTI_SELECT', 'DATE', 'PRICE', 'IMAGE', name='attributetype')
    attributetype_enum.create(op.get_bind())
    
    backendtype_enum = postgresql.ENUM('STRING', 'FLOAT', 'BOOLEAN', 'OPTION', 'OPTIONS', 'DATE', 'JSON', name='backendtype')
    backendtype_enum.create(op.get_bind())
    
    # Now we can alter the columns to use these enum types
    op.alter_column('attribute_options', 'sort_order',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_nullable=True)
    op.drop_constraint('attribute_options_attribute_id_fkey', 'attribute_options', type_='foreignkey')
    op.create_foreign_key(None, 'attribute_options', 'attributes', ['attribute_id'], ['id'], ondelete='CASCADE')
    
    op.alter_column('attributes', 'type',
               existing_type=sa.VARCHAR(),
               type_=attributetype_enum,
               existing_nullable=False,
               postgresql_using='type::attributetype')
               
    op.alter_column('attributes', 'backend_type',
               existing_type=sa.VARCHAR(),
               type_=backendtype_enum,
               existing_nullable=False,
               postgresql_using='backend_type::backendtype')
    
    op.drop_constraint('product_models_family_variant_id_fkey', 'product_models', type_='foreignkey')
    op.drop_constraint('product_models_parent_id_fkey', 'product_models', type_='foreignkey')


def downgrade() -> None:
    # Recreate foreign keys
    op.create_foreign_key('product_models_parent_id_fkey', 'product_models', 'product_models', ['parent_id'], ['id'])
    op.create_foreign_key('product_models_family_variant_id_fkey', 'product_models', 'family_variants', ['family_variant_id'], ['id'])
    
    # Alter columns back to VARCHAR
    op.alter_column('attributes', 'backend_type',
               existing_type=sa.Enum('STRING', 'FLOAT', 'BOOLEAN', 'OPTION', 'OPTIONS', 'DATE', 'JSON', name='backendtype'),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.alter_column('attributes', 'type',
               existing_type=sa.Enum('TEXT', 'TEXTAREA', 'NUMBER', 'BOOLEAN', 'SIMPLE_SELECT', 'MULTI_SELECT', 'DATE', 'PRICE', 'IMAGE', name='attributetype'),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    
    # Drop foreign key and recreate with original constraint
    op.drop_constraint(None, 'attribute_options', type_='foreignkey')
    op.create_foreign_key('attribute_options_attribute_id_fkey', 'attribute_options', 'attributes', ['attribute_id'], ['id'])
    op.alter_column('attribute_options', 'sort_order',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    
    # Drop the enum types
    op.execute('DROP TYPE IF EXISTS attributetype')
    op.execute('DROP TYPE IF EXISTS backendtype')
"""empty message

Revision ID: a7aefe10dae2
Revises: f8c039212bf7
Create Date: 2018-09-26 19:56:29.270689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7aefe10dae2'
down_revision = 'f8c039212bf7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('itemedited',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('edited_timestamp', sa.DateTime(), nullable=True),
    sa.Column('name', sa.Boolean(), nullable=True),
    sa.Column('brand', sa.Boolean(), nullable=True),
    sa.Column('category', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_itemedited_edited_timestamp'), 'itemedited', ['edited_timestamp'], unique=False)
    op.create_table('variantedited',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('variant_id', sa.Integer(), nullable=True),
    sa.Column('edited_timestamp', sa.DateTime(), nullable=True),
    sa.Column('var_name', sa.Boolean(), nullable=True),
    sa.Column('sp', sa.Boolean(), nullable=True),
    sa.Column('cp', sa.Boolean(), nullable=True),
    sa.Column('quantity', sa.Boolean(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['variant_id'], ['variant.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_variantedited_edited_timestamp'), 'variantedited', ['edited_timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_variantedited_edited_timestamp'), table_name='variantedited')
    op.drop_table('variantedited')
    op.drop_index(op.f('ix_itemedited_edited_timestamp'), table_name='itemedited')
    op.drop_table('itemedited')
    # ### end Alembic commands ###
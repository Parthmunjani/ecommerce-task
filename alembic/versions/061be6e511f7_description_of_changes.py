"""Description of changes

Revision ID: 061be6e511f7
Revises: fdd0638e1d8c
Create Date: 2023-07-28 16:12:44.599718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '061be6e511f7'
down_revision = 'fdd0638e1d8c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('product', sa.Column('modified_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'modified_at')
    op.drop_column('product', 'created_at')
    # ### end Alembic commands ###
"""empty message

Revision ID: f5c92818a7ee
Revises: 46b63427fffb
Create Date: 2020-10-06 16:37:30.580479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5c92818a7ee'
down_revision = '46b63427fffb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('orders', sa.Column('items', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'items')
    op.drop_column('orders', 'date')
    # ### end Alembic commands ###

"""book summary column

Revision ID: 7555e67fb93c
Revises: e8d9c91087da
Create Date: 2020-02-23 07:12:27.639076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7555e67fb93c'
down_revision = 'e8d9c91087da'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('book', sa.Column('summary', sa.Text(), nullable=True))
    op.create_index(op.f('ix_book_author'), 'book', ['author'], unique=False)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_author'), table_name='book')
    op.drop_column('book', 'summary')
    # ### end Alembic commands ###

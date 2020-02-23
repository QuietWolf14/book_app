"""BookList table

Revision ID: 3934aa3532e9
Revises: 7555e67fb93c
Create Date: 2020-02-23 16:41:17.341167

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3934aa3532e9'
down_revision = '7555e67fb93c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book_list',
    sa.Column('list_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('isbn', sa.Integer(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('list_id', 'isbn')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_list')
    # ### end Alembic commands ###
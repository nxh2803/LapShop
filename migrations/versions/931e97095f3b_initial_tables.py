"""initial tables

Revision ID: 931e97095f3b
Revises: aece6c44a9ae
Create Date: 2023-07-02 18:57:33.160001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '931e97095f3b'
down_revision = 'aece6c44a9ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('invoice', sa.Column('user_id', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('invoice', 'user_id')
    # ### end Alembic commands ###

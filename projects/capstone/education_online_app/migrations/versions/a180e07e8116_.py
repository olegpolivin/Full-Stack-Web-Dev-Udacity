"""empty message

Revision ID: a180e07e8116
Revises: 550a47b40ef4
Create Date: 2020-10-07 07:36:01.741228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a180e07e8116'
down_revision = '550a47b40ef4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'migrate_check')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('migrate_check', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
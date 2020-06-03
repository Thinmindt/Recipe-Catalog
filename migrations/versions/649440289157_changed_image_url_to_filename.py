"""Changed Image url to filename

Revision ID: 649440289157
Revises: 1b4fff37c257
Create Date: 2020-06-03 11:19:51.767065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '649440289157'
down_revision = '1b4fff37c257'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('filename', sa.Text(), nullable=False))
    op.drop_column('image', 'url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('url', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('image', 'filename')
    # ### end Alembic commands ###

"""Added recipe categories relationship

Revision ID: 9a3273596e94
Revises: 270a904b25a7
Create Date: 2020-07-22 14:07:16.205043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a3273596e94'
down_revision = '270a904b25a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('id_recipe_category', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'recipe', 'category', ['id_recipe_category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    op.drop_column('recipe', 'id_recipe_category')
    # ### end Alembic commands ###

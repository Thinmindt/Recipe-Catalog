"""Add Recipe and User

Revision ID: 6842d0563733
Revises: 
Create Date: 2020-05-14 13:22:48.130990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6842d0563733'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=True),
    sa.Column('type', sa.String(length=8), nullable=True),
    sa.Column('web_link', sa.Text(), nullable=True),
    sa.Column('book_title', sa.String(length=120), nullable=True),
    sa.Column('book_page', sa.Integer(), nullable=True),
    sa.Column('book_image_path', sa.String(length=256), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipe_book_title'), 'recipe', ['book_title'], unique=False)
    op.create_index(op.f('ix_recipe_title'), 'recipe', ['title'], unique=True)
    op.create_index(op.f('ix_recipe_type'), 'recipe', ['type'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_recipe_type'), table_name='recipe')
    op.drop_index(op.f('ix_recipe_title'), table_name='recipe')
    op.drop_index(op.f('ix_recipe_book_title'), table_name='recipe')
    op.drop_table('recipe')
    # ### end Alembic commands ###
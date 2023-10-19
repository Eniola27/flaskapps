"""empty message

Revision ID: 71402e86dfba
Revises: da19d695f47b
Create Date: 2023-10-19 18:35:39.927448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '71402e86dfba'
down_revision = 'da19d695f47b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medication', schema=None) as batch_op:
        batch_op.alter_column('taken_at',
               existing_type=mysql.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('medication', schema=None) as batch_op:
        batch_op.alter_column('taken_at',
               existing_type=sa.Date(),
               type_=mysql.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###

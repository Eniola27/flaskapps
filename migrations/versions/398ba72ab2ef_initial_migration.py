"""initial migration

Revision ID: 398ba72ab2ef
Revises: 
Create Date: 2023-10-20 16:51:51.137258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '398ba72ab2ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('admin_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_username', sa.String(length=80), nullable=True),
    sa.Column('admin_pwd', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('admin_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_username', sa.String(length=100), nullable=False),
    sa.Column('user_email', sa.String(length=120), nullable=True),
    sa.Column('user_pwd', sa.String(length=120), nullable=False),
    sa.Column('user_dob', sa.Date(), nullable=False),
    sa.Column('user_height', sa.Integer(), nullable=True),
    sa.Column('user_weight', sa.Integer(), nullable=True),
    sa.Column('user_pix', sa.String(length=120), nullable=True),
    sa.Column('user_datejoined', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('cycle_entry',
    sa.Column('entry_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cyc_user_id', sa.Integer(), nullable=False),
    sa.Column('cycle_length', sa.Integer(), server_default='7', nullable=False),
    sa.Column('period_length', sa.Integer(), server_default='28', nullable=False),
    sa.Column('lastperioddate', sa.Date(), nullable=False),
    sa.Column('note', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['cyc_user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('entry_id')
    )
    op.create_table('family_planning',
    sa.Column('familyplan_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('planning_type', sa.String(length=255), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('familyplan_id')
    )
    op.create_table('symptoms_tracking',
    sa.Column('symptom_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('symptom_type', sa.String(length=70), nullable=True),
    sa.Column('Severity', sa.Integer(), nullable=True),
    sa.Column('recorded_at', sa.Date(), nullable=True),
    sa.Column('sys_user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sys_user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('symptom_id')
    )
    op.create_table('medication',
    sa.Column('med_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('symptom_id', sa.Integer(), nullable=False),
    sa.Column('med_name', sa.String(length=50), nullable=True),
    sa.Column('dosage', sa.String(length=50), nullable=True),
    sa.Column('taken_at', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['symptom_id'], ['symptoms_tracking.symptom_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('med_id')
    )
    op.create_table('mood_table',
    sa.Column('mood_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mood_entry_id', sa.Integer(), nullable=False),
    sa.Column('date_recorded', sa.Date(), nullable=True),
    sa.Column('mood_swing', sa.Enum('1', '0'), nullable=True),
    sa.Column('mood_name', sa.String(length=100), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('symptom_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['mood_entry_id'], ['cycle_entry.entry_id'], ),
    sa.ForeignKeyConstraint(['symptom_id'], ['symptoms_tracking.symptom_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('mood_id')
    )
    op.create_table('ovulation',
    sa.Column('ovulation_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('next_period_start_date', sa.DateTime(), nullable=True),
    sa.Column('ovul_entry_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ovul_entry_id'], ['cycle_entry.entry_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('ovulation_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ovulation')
    op.drop_table('mood_table')
    op.drop_table('medication')
    op.drop_table('symptoms_tracking')
    op.drop_table('family_planning')
    op.drop_table('cycle_entry')
    op.drop_table('user')
    op.drop_table('admin')
    # ### end Alembic commands ###

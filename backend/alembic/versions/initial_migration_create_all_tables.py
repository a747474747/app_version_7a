"""Initial migration - Create all tables

Revision ID: 001_initial
Revises:
Create Date: 2025-11-22 16:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create user_profiles table
    op.create_table('user_profiles',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.Column('clerk_id', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('display_name', sa.String(length=200), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('organization_id', sa.String(length=255), nullable=True),
        sa.Column('organization_name', sa.String(length=255), nullable=True),
        sa.Column('afsl_number', sa.String(length=50), nullable=True),
        sa.Column('aflp_number', sa.String(length=50), nullable=True),
        sa.Column('certification_expiry', sa.String(length=10), nullable=True),
        sa.Column('permissions', sa.JSON(), nullable=True),
        sa.Column('preferences', sa.JSON(), nullable=True),
        sa.Column('last_login_at', sa.String(length=25), nullable=True),
        sa.Column('created_by_clerk_id', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('clerk_id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_profiles_clerk_id'), 'user_profiles', ['clerk_id'], unique=False)
    op.create_index(op.f('ix_user_profiles_email'), 'user_profiles', ['email'], unique=False)
    op.create_index(op.f('ix_user_profiles_organization_id'), 'user_profiles', ['organization_id'], unique=False)

    # Create strategies table
    op.create_table('strategies',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.Column('strategy_id', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('domain', sa.String(length=50), nullable=False),
        sa.Column('target_metric', sa.String(length=50), nullable=False),
        sa.Column('constraints', sa.JSON(), nullable=True),
        sa.Column('parameters', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_template', sa.Boolean(), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('created_by_clerk_id', sa.String(length=255), nullable=False),
        sa.Column('updated_by_clerk_id', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('strategy_id')
    )

    # Create scenarios table
    op.create_table('scenarios',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.Column('scenario_id', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('user_profile_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('version', sa.String(length=20), nullable=False),
        sa.Column('calculation_state', sa.JSON(), nullable=True),
        sa.Column('assumption_set', sa.JSON(), nullable=True),
        sa.Column('strategy_config', sa.JSON(), nullable=True),
        sa.Column('mode', sa.String(length=100), nullable=False),
        sa.Column('projection_output', sa.JSON(), nullable=True),
        sa.Column('last_calculated_at', sa.String(length=25), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('created_by_clerk_id', sa.String(length=255), nullable=False),
        sa.Column('updated_by_clerk_id', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['user_profile_id'], ['user_profiles.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scenario_id')
    )
    op.create_index(op.f('ix_scenarios_user_profile_id'), 'scenarios', ['user_profile_id'], unique=False)

    # Create advice_outcomes table
    op.create_table('advice_outcomes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), onupdate=sa.text('now()'), nullable=False),
        sa.Column('advice_outcome_id', sa.String(length=255), nullable=False),
        sa.Column('scenario_id', sa.Integer(), nullable=False),
        sa.Column('best_interest_duty_passed', sa.String(length=10), nullable=False),
        sa.Column('compliance_warnings', sa.JSON(), nullable=True),
        sa.Column('regulatory_citations', sa.JSON(), nullable=True),
        sa.Column('risk_warnings', sa.JSON(), nullable=True),
        sa.Column('suitability_score', sa.Float(), nullable=True),
        sa.Column('approved_strategies', sa.JSON(), nullable=True),
        sa.Column('rejected_strategies', sa.JSON(), nullable=True),
        sa.Column('assessment_details', sa.JSON(), nullable=True),
        sa.Column('assessed_by_clerk_id', sa.String(length=255), nullable=False),
        sa.Column('assessment_version', sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(['scenario_id'], ['scenarios.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('advice_outcome_id')
    )
    op.create_index(op.f('ix_advice_outcomes_scenario_id'), 'advice_outcomes', ['scenario_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order to handle foreign keys
    op.drop_table('advice_outcomes')
    op.drop_table('scenarios')
    op.drop_table('strategies')
    op.drop_table('user_profiles')

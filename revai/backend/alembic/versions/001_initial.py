"""initial

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Organizations
    op.create_table('organizations',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('crm_type', sa.String(), nullable=False),
        sa.Column('hubspot_access_token', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Users
    op.create_table('users',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_org_id'), 'users', ['org_id'], unique=False)

    # Prospects
    op.create_table('prospects',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('domain', sa.String(), nullable=False),
        sa.Column('contact_name', sa.String(), nullable=False),
        sa.Column('contact_email', sa.String(), nullable=False),
        sa.Column('contact_linkedin', sa.String(), nullable=True),
        sa.Column('icp_score', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('fit_signals', postgresql.JSONB(astext_type=sa.Text()), server_default='[]', nullable=False),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_prospects_org_id'), 'prospects', ['org_id'], unique=False)

    # Sequences
    op.create_table('sequences',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('prospect_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('steps', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('current_step', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['prospect_id'], ['prospects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sequences_prospect_id'), 'sequences', ['prospect_id'], unique=False)

    # Deals
    op.create_table('deals',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('crm_deal_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('value', sa.Numeric(), nullable=False),
        sa.Column('stage', sa.String(), nullable=False),
        sa.Column('close_date', sa.Date(), nullable=True),
        sa.Column('health_score', sa.Integer(), nullable=False),
        sa.Column('risk_signals', postgresql.JSONB(astext_type=sa.Text()), server_default='[]', nullable=False),
        sa.Column('last_contact_date', sa.Date(), nullable=True),
        sa.Column('assigned_to', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deals_crm_deal_id'), 'deals', ['crm_deal_id'], unique=False)
    op.create_index(op.f('ix_deals_org_id'), 'deals', ['org_id'], unique=False)

    # Deal Alerts
    op.create_table('deal_alerts',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('deal_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('alert_type', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('recovery_play', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['deal_id'], ['deals.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deal_alerts_deal_id'), 'deal_alerts', ['deal_id'], unique=False)

    # Accounts
    op.create_table('accounts',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('company_name', sa.String(), nullable=False),
        sa.Column('mrr', sa.Numeric(), nullable=False),
        sa.Column('contract_end_date', sa.Date(), nullable=True),
        sa.Column('churn_score', sa.Integer(), nullable=False),
        sa.Column('churn_reason', sa.Text(), nullable=True),
        sa.Column('usage_data', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.Column('intervention_status', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_org_id'), 'accounts', ['org_id'], unique=False)

    # Battlecards
    op.create_table('battlecards',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('competitor_name', sa.String(), nullable=False),
        sa.Column('strengths', sa.Text(), nullable=False),
        sa.Column('weaknesses', sa.Text(), nullable=False),
        sa.Column('positioning', sa.Text(), nullable=False),
        sa.Column('objection_handlers', postgresql.JSONB(astext_type=sa.Text()), server_default='[]', nullable=False),
        sa.Column('last_updated', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_battlecards_org_id'), 'battlecards', ['org_id'], unique=False)

    # Agent Logs
    op.create_table('agent_logs',
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('org_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('agent_type', sa.String(), nullable=False),
        sa.Column('action', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_logs_org_id'), 'agent_logs', ['org_id'], unique=False)


def downgrade() -> None:
    op.drop_table('agent_logs')
    op.drop_table('battlecards')
    op.drop_table('accounts')
    op.drop_table('deal_alerts')
    op.drop_table('deals')
    op.drop_table('sequences')
    op.drop_table('prospects')
    op.drop_table('users')
    op.drop_table('organizations')
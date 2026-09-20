# -*- coding: utf-8 -*-
"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'business_plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('frequency', sa.Enum('monthly', 'quarterly', 'yearly', name='planfrequency'), nullable=False),
        sa.Column('status', sa.Enum('draft', 'active', 'archived', name='planstatus'), nullable=False, server_default='draft'),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('company_size', sa.String(50), nullable=True),
        sa.Column('revenue_range', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_business_plans_id'), 'business_plans', ['id'], unique=False)

    op.create_table(
        'executive_summaries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('key_highlights', sa.JSON(), nullable=True),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('plan_id')
    )

    op.create_table(
        'financial_projections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('period', sa.String(20), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('quarter', sa.Integer(), nullable=True),
        sa.Column('month', sa.Integer(), nullable=True),
        sa.Column('revenue', sa.Float(), nullable=False, server_default='0'),
        sa.Column('cogs', sa.Float(), nullable=False, server_default='0'),
        sa.Column('gross_profit', sa.Float(), nullable=False, server_default='0'),
        sa.Column('operating_expenses', sa.Float(), nullable=False, server_default='0'),
        sa.Column('ebitda', sa.Float(), nullable=False, server_default='0'),
        sa.Column('depreciation', sa.Float(), nullable=False, server_default='0'),
        sa.Column('interest', sa.Float(), nullable=False, server_default='0'),
        sa.Column('tax', sa.Float(), nullable=False, server_default='0'),
        sa.Column('net_income', sa.Float(), nullable=False, server_default='0'),
        sa.Column('cash_flow_operating', sa.Float(), nullable=False, server_default='0'),
        sa.Column('cash_flow_investing', sa.Float(), nullable=False, server_default='0'),
        sa.Column('cash_flow_financing', sa.Float(), nullable=False, server_default='0'),
        sa.Column('net_cash_flow', sa.Float(), nullable=False, server_default='0'),
        sa.Column('cash_balance', sa.Float(), nullable=False, server_default='0'),
        sa.Column('assets_current', sa.Float(), nullable=False, server_default='0'),
        sa.Column('assets_fixed', sa.Float(), nullable=False, server_default='0'),
        sa.Column('total_assets', sa.Float(), nullable=False, server_default='0'),
        sa.Column('liabilities_current', sa.Float(), nullable=False, server_default='0'),
        sa.Column('liabilities_longterm', sa.Float(), nullable=False, server_default='0'),
        sa.Column('total_liabilities', sa.Float(), nullable=False, server_default='0'),
        sa.Column('equity', sa.Float(), nullable=False, server_default='0'),
        sa.Column('assumptions', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_financial_projections_id'), 'financial_projections', ['id'], unique=False)

    op.create_table(
        'market_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('tam', sa.Float(), nullable=True),
        sa.Column('sam', sa.Float(), nullable=True),
        sa.Column('som', sa.Float(), nullable=True),
        sa.Column('market_growth_rate', sa.Float(), nullable=True),
        sa.Column('key_trends', sa.JSON(), nullable=True),
        sa.Column('target_segments', sa.JSON(), nullable=True),
        sa.Column('industry_benchmarks', sa.JSON(), nullable=True),
        sa.Column('macro_indicators', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('plan_id')
    )

    op.create_table(
        'competitor_analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('competitors', sa.JSON(), nullable=True),
        sa.Column('competitive_matrix', sa.JSON(), nullable=True),
        sa.Column('positioning_map', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('plan_id')
    )

    op.create_table(
        'strategies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('swot', sa.JSON(), nullable=True),
        sa.Column('pestle', sa.JSON(), nullable=True),
        sa.Column('gtm_strategy', sa.JSON(), nullable=True),
        sa.Column('value_proposition', sa.Text(), nullable=True),
        sa.Column('pricing_strategy', sa.Text(), nullable=True),
        sa.Column('channel_strategy', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('plan_id')
    )

    op.create_table(
        'okrs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('objective', sa.String(500), nullable=False),
        sa.Column('key_results', sa.JSON(), nullable=False),
        sa.Column('owner', sa.String(100), nullable=True),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='not_started'),
        sa.Column('progress', sa.Float(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_okrs_id'), 'okrs', ['id'], unique=False)

    op.create_table(
        'execution_trackers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('milestone', sa.String(255), nullable=False),
        sa.Column('target_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('actual_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('variance_days', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('alert_sent', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_execution_trackers_id'), 'execution_trackers', ['id'], unique=False)

    op.create_table(
        'plan_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('snapshot', sa.JSON(), nullable=False),
        sa.Column('change_summary', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['business_plans.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plan_versions_id'), 'plan_versions', ['id'], unique=False)

def downgrade() -> None:
    op.drop_table('plan_versions')
    op.drop_table('execution_trackers')
    op.drop_table('okrs')
    op.drop_table('strategies')
    op.drop_table('competitor_analyses')
    op.drop_table('market_analyses')
    op.drop_table('financial_projections')
    op.drop_table('executive_summaries')
    op.drop_table('business_plans')
    
    # Note: SQLite stores enums as VARCHAR, no types to drop
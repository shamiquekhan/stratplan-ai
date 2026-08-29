from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum
from datetime import datetime


class PlanFrequency(str, enum.Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class PlanStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class BusinessPlan(Base):
    __tablename__ = "business_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    frequency = Column(SQLEnum(PlanFrequency), nullable=False)
    status = Column(SQLEnum(PlanStatus), default=PlanStatus.DRAFT)
    industry = Column(String(100), nullable=True)
    company_size = Column(String(50), nullable=True)
    revenue_range = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    executive_summary = relationship("ExecutiveSummary", back_populates="plan", uselist=False, cascade="all, delete-orphan")
    financial_projections = relationship("FinancialProjection", back_populates="plan", cascade="all, delete-orphan")
    market_analysis = relationship("MarketAnalysis", back_populates="plan", uselist=False, cascade="all, delete-orphan")
    competitor_analysis = relationship("CompetitorAnalysis", back_populates="plan", uselist=False, cascade="all, delete-orphan")
    strategy = relationship("Strategy", back_populates="plan", uselist=False, cascade="all, delete-orphan")
    okrs = relationship("OKR", back_populates="plan", cascade="all, delete-orphan")
    execution_tracker = relationship("ExecutionTracker", back_populates="plan", cascade="all, delete-orphan")
    versions = relationship("PlanVersion", back_populates="plan", cascade="all, delete-orphan")


class ExecutiveSummary(Base):
    __tablename__ = "executive_summaries"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"), unique=True)
    content = Column(Text, nullable=False)
    key_highlights = Column(JSON, nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    plan = relationship("BusinessPlan", back_populates="executive_summary")


class FinancialProjection(Base):
    __tablename__ = "financial_projections"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"))
    period = Column(String(20), nullable=False)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=True)
    month = Column(Integer, nullable=True)

    revenue = Column(Float, default=0)
    cogs = Column(Float, default=0)
    gross_profit = Column(Float, default=0)
    operating_expenses = Column(Float, default=0)
    ebitda = Column(Float, default=0)
    depreciation = Column(Float, default=0)
    interest = Column(Float, default=0)
    tax = Column(Float, default=0)
    net_income = Column(Float, default=0)

    cash_flow_operating = Column(Float, default=0)
    cash_flow_investing = Column(Float, default=0)
    cash_flow_financing = Column(Float, default=0)
    net_cash_flow = Column(Float, default=0)
    cash_balance = Column(Float, default=0)

    assets_current = Column(Float, default=0)
    assets_fixed = Column(Float, default=0)
    total_assets = Column(Float, default=0)
    liabilities_current = Column(Float, default=0)
    liabilities_longterm = Column(Float, default=0)
    total_liabilities = Column(Float, default=0)
    equity = Column(Float, default=0)

    assumptions = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plan = relationship("BusinessPlan", back_populates="financial_projections")


class MarketAnalysis(Base):
    __tablename__ = "market_analyses"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"), unique=True)
    tam = Column(Float, nullable=True)
    sam = Column(Float, nullable=True)
    som = Column(Float, nullable=True)
    market_growth_rate = Column(Float, nullable=True)
    key_trends = Column(JSON, nullable=True)
    target_segments = Column(JSON, nullable=True)
    industry_benchmarks = Column(JSON, nullable=True)
    macro_indicators = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan = relationship("BusinessPlan", back_populates="market_analysis")


class CompetitorAnalysis(Base):
    __tablename__ = "competitor_analyses"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"), unique=True)
    competitors = Column(JSON, nullable=True)
    competitive_matrix = Column(JSON, nullable=True)
    positioning_map = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan = relationship("BusinessPlan", back_populates="competitor_analysis")


class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"), unique=True)
    swot = Column(JSON, nullable=True)
    pestle = Column(JSON, nullable=True)
    gtm_strategy = Column(JSON, nullable=True)
    value_proposition = Column(Text, nullable=True)
    pricing_strategy = Column(Text, nullable=True)
    channel_strategy = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan = relationship("BusinessPlan", back_populates="strategy")


class OKR(Base):
    __tablename__ = "okrs"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"))
    objective = Column(String(500), nullable=False)
    key_results = Column(JSON, nullable=False)
    owner = Column(String(100), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="not_started")
    progress = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan = relationship("BusinessPlan", back_populates="okrs")


class ExecutionTracker(Base):
    __tablename__ = "execution_trackers"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"))
    milestone = Column(String(255), nullable=False)
    target_date = Column(DateTime(timezone=True), nullable=False)
    actual_date = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(50), default="pending")
    variance_days = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    alert_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    plan = relationship("BusinessPlan", back_populates="execution_tracker")


class PlanVersion(Base):
    __tablename__ = "plan_versions"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("business_plans.id", ondelete="CASCADE"))
    version_number = Column(Integer, nullable=False)
    snapshot = Column(JSON, nullable=False)
    change_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    plan = relationship("BusinessPlan", back_populates="versions")
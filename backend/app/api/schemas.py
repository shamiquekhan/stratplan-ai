from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class PlanFrequency(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class PlanStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class BusinessPlanBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    frequency: PlanFrequency
    industry: Optional[str] = None
    company_size: Optional[str] = None
    revenue_range: Optional[str] = None


class BusinessPlanCreate(BusinessPlanBase):
    pass


class BusinessPlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[PlanFrequency] = None
    status: Optional[PlanStatus] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    revenue_range: Optional[str] = None


class BusinessPlanResponse(BusinessPlanBase):
    id: int
    status: PlanStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExecutiveSummaryBase(BaseModel):
    content: str
    key_highlights: Optional[List[str]] = None


class ExecutiveSummaryResponse(ExecutiveSummaryBase):
    id: int
    plan_id: int
    generated_at: datetime

    class Config:
        from_attributes = True


class FinancialProjectionBase(BaseModel):
    period: str
    year: int
    quarter: Optional[int] = None
    month: Optional[int] = None
    revenue: float = 0
    cogs: float = 0
    gross_profit: float = 0
    operating_expenses: float = 0
    ebitda: float = 0
    depreciation: float = 0
    interest: float = 0
    tax: float = 0
    net_income: float = 0
    cash_flow_operating: float = 0
    cash_flow_investing: float = 0
    cash_flow_financing: float = 0
    net_cash_flow: float = 0
    cash_balance: float = 0
    assets_current: float = 0
    assets_fixed: float = 0
    total_assets: float = 0
    liabilities_current: float = 0
    liabilities_longterm: float = 0
    total_liabilities: float = 0
    equity: float = 0
    assumptions: Optional[Dict[str, Any]] = None


class FinancialProjectionResponse(FinancialProjectionBase):
    id: int
    plan_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MarketAnalysisBase(BaseModel):
    tam: Optional[float] = None
    sam: Optional[float] = None
    som: Optional[float] = None
    market_growth_rate: Optional[float] = None
    key_trends: Optional[List[str]] = None
    target_segments: Optional[List[Dict[str, Any]]] = None
    industry_benchmarks: Optional[Dict[str, Any]] = None
    macro_indicators: Optional[Dict[str, Any]] = None


class MarketAnalysisResponse(MarketAnalysisBase):
    id: int
    plan_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CompetitorAnalysisBase(BaseModel):
    competitors: Optional[List[Dict[str, Any]]] = None
    competitive_matrix: Optional[Dict[str, Any]] = None
    positioning_map: Optional[Dict[str, Any]] = None


class CompetitorAnalysisResponse(CompetitorAnalysisBase):
    id: int
    plan_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StrategyBase(BaseModel):
    swot: Optional[Dict[str, List[str]]] = None
    pestle: Optional[Dict[str, List[str]]] = None
    gtm_strategy: Optional[Dict[str, Any]] = None
    value_proposition: Optional[str] = None
    pricing_strategy: Optional[str] = None
    channel_strategy: Optional[List[Dict[str, Any]]] = None


class StrategyResponse(StrategyBase):
    id: int
    plan_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OKRBase(BaseModel):
    objective: str
    key_results: List[Dict[str, Any]]
    owner: Optional[str] = None
    due_date: Optional[datetime] = None
    status: str = "not_started"
    progress: float = 0


class OKRCreate(OKRBase):
    pass


class OKRResponse(OKRBase):
    id: int
    plan_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExecutionTrackerBase(BaseModel):
    milestone: str
    target_date: datetime
    actual_date: Optional[datetime] = None
    status: str = "pending"
    variance_days: int = 0
    notes: Optional[str] = None


class ExecutionTrackerCreate(ExecutionTrackerBase):
    pass


class ExecutionTrackerResponse(ExecutionTrackerBase):
    id: int
    plan_id: int
    alert_sent: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PlanVersionBase(BaseModel):
    version_number: int
    snapshot: Dict[str, Any]
    change_summary: Optional[str] = None


class PlanVersionResponse(PlanVersionBase):
    id: int
    plan_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GeneratePlanRequest(BaseModel):
    # plan_id lives in the URL; keep optional for older clients that also send it in the body
    plan_id: Optional[int] = None
    user_inputs: Dict[str, Any] = {}


class ExportRequest(BaseModel):
    plan_id: Optional[int] = None
    format: str = Field(..., pattern="^(pdf|docx|xlsx)$")
    sections: Optional[List[str]] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    ollama_connected: bool
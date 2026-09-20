from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json
import os

from app.core.database import get_db
from app.core.config import settings
from app.db.models import BusinessPlan, PlanFrequency, PlanStatus, PlanVersion
from app.api.schemas import (
    BusinessPlanCreate, BusinessPlanUpdate, BusinessPlanResponse,
    GeneratePlanRequest, ExportRequest, ExecutiveSummaryResponse,
    FinancialProjectionResponse, MarketAnalysisResponse,
    CompetitorAnalysisResponse, StrategyResponse,
    OKRResponse, ExecutionTrackerResponse, PlanVersionResponse,
    HealthResponse
)
from app.orchestrator.graph import orchestrator
from app.services.export_service import PDFExporter, DOCXExporter, XLSXExporter


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    ollama_connected = False
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get("http://localhost:11434/api/tags")
            ollama_connected = resp.status_code == 200
    except:
        pass
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        ollama_connected=ollama_connected
    )


@router.post("/plans", response_model=BusinessPlanResponse, status_code=201)
async def create_plan(plan: BusinessPlanCreate, db: Session = Depends(get_db)):
    db_plan = BusinessPlan(
        name=plan.name,
        description=plan.description,
        frequency=plan.frequency,
        industry=plan.industry,
        company_size=plan.company_size,
        revenue_range=plan.revenue_range,
        status=PlanStatus.DRAFT
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.get("/plans", response_model=List[BusinessPlanResponse])
async def list_plans(
    skip: int = 0,
    limit: int = 100,
    status: Optional[PlanStatus] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BusinessPlan)
    if status:
        query = query.filter(BusinessPlan.status == status)
    plans = query.order_by(BusinessPlan.updated_at.desc()).offset(skip).limit(limit).all()
    return plans


@router.get("/plans/{plan_id}")
async def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(BusinessPlan).filter(BusinessPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Return complete plan data
    return await _build_plan_data(db, plan)


@router.patch("/plans/{plan_id}", response_model=BusinessPlanResponse)
async def update_plan(plan_id: int, plan_update: BusinessPlanUpdate, db: Session = Depends(get_db)):
    plan = db.query(BusinessPlan).filter(BusinessPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    update_data = plan_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/plans/{plan_id}", status_code=204)
async def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(BusinessPlan).filter(BusinessPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(plan)
    db.commit()


@router.post("/plans/{plan_id}/generate")
async def generate_plan(plan_id: int, request: GeneratePlanRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    plan = db.query(BusinessPlan).filter(BusinessPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    plan_dict = {
        "id": plan.id,
        "name": plan.name,
        "description": plan.description,
        "frequency": plan.frequency.value,
        "industry": plan.industry,
        "company_size": plan.company_size,
        "revenue_range": plan.revenue_range
    }
    
    try:
        result = await orchestrator.generate_plan(plan_dict, request.user_inputs, thread_id=f"plan_{plan_id}")
        
        # Save generated content to database
        await _save_generated_plan(db, plan, result)
        
        # Build and return complete plan data
        plan_data = await _build_plan_data(db, plan)
        return plan_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


async def _save_generated_plan(db: Session, plan: BusinessPlan, result: dict):
    # Save executive summary
    if result.get("generated_plan"):
        from app.db.models import ExecutiveSummary
        summary = db.query(ExecutiveSummary).filter(ExecutiveSummary.plan_id == plan.id).first()
        if not summary:
            summary = ExecutiveSummary(plan_id=plan.id)
            db.add(summary)
        summary.content = result["generated_plan"]
        summary.key_highlights = []  # Could extract from result
    
    # Save financial projections
    if result.get("financial_projections"):
        from app.db.models import FinancialProjection
        fin = result["financial_projections"]
        assumptions = fin.get("assumptions", {})
        
        for pnl_row in fin.get("pnl", []):
            fp = FinancialProjection(
                plan_id=plan.id,
                period=pnl_row.get("period", ""),
                year=2024,  # Parse from period
                revenue=pnl_row.get("revenue", 0),
                cogs=pnl_row.get("cogs", 0),
                gross_profit=pnl_row.get("gross_profit", 0),
                operating_expenses=pnl_row.get("operating_expenses", 0),
                ebitda=pnl_row.get("ebitda", 0),
                depreciation=pnl_row.get("depreciation", 0),
                interest=pnl_row.get("interest", 0),
                tax=pnl_row.get("tax", 0),
                net_income=pnl_row.get("net_income", 0),
                assumptions=assumptions
            )
            db.add(fp)
    
    # Save market analysis
    if result.get("market_analysis"):
        from app.db.models import MarketAnalysis
        market = result["market_analysis"]
        ma = db.query(MarketAnalysis).filter(MarketAnalysis.plan_id == plan.id).first()
        if not ma:
            ma = MarketAnalysis(plan_id=plan.id)
            db.add(ma)
        ma.tam = market.get("tam")
        ma.sam = market.get("sam")
        ma.som = market.get("som")
        ma.market_growth_rate = market.get("market_growth_rate")
        ma.key_trends = market.get("key_trends")
        ma.target_segments = market.get("target_segments")
        ma.industry_benchmarks = market.get("industry_benchmarks")
        ma.macro_indicators = market.get("macro_indicators")
    
    # Save competitor analysis
    if result.get("competitor_analysis"):
        from app.db.models import CompetitorAnalysis
        comp = result["competitor_analysis"]
        ca = db.query(CompetitorAnalysis).filter(CompetitorAnalysis.plan_id == plan.id).first()
        if not ca:
            ca = CompetitorAnalysis(plan_id=plan.id)
            db.add(ca)
        ca.competitors = comp.get("competitors")
        ca.competitive_matrix = comp.get("competitive_matrix")
        ca.positioning_map = comp.get("positioning_map")
    
    # Save strategy
    if result.get("strategy"):
        from app.db.models import Strategy
        strat = result["strategy"]
        s = db.query(Strategy).filter(Strategy.plan_id == plan.id).first()
        if not s:
            s = Strategy(plan_id=plan.id)
            db.add(s)
        s.swot = strat.get("swot")
        s.pestle = strat.get("pestle")
        s.gtm_strategy = strat.get("gtm_strategy")
        s.value_proposition = strat.get("gtm_strategy", {}).get("value_proposition")
        s.pricing_strategy = strat.get("gtm_strategy", {}).get("pricing_strategy")
        s.channel_strategy = strat.get("gtm_strategy", {}).get("channels")
    
    # Save OKRs
    if result.get("strategy", {}).get("okrs"):
        from app.db.models import OKR
        for okr_data in result["strategy"]["okrs"]:
            okr = OKR(
                plan_id=plan.id,
                objective=okr_data.get("objective", ""),
                key_results=okr_data.get("key_results", []),
                owner=okr_data.get("owner"),
                status="not_started",
                progress=0
            )
            db.add(okr)
    
    # Save execution tracker
    if result.get("execution_tracker"):
        from app.db.models import ExecutionTracker
        for et_data in result["execution_tracker"]:
            target_date = et_data.get("target_date")
            if isinstance(target_date, str):
                try:
                    target_date = datetime.fromisoformat(target_date.replace("Z", "+00:00"))
                except:
                    target_date = datetime.utcnow() + timedelta(days=30)
            
            et = ExecutionTracker(
                plan_id=plan.id,
                milestone=et_data.get("milestone", ""),
                target_date=target_date,
                status=et_data.get("status", "pending"),
                variance_days=et_data.get("variance_days", 0),
                notes=et_data.get("notes")
            )
            db.add(et)
    
    # Save version snapshot
    if result.get("version_snapshot"):
        from app.db.models import PlanVersion
        vs = result["version_snapshot"]
        pv = PlanVersion(
            plan_id=plan.id,
            version_number=vs.get("version_number", 1),
            snapshot=vs.get("snapshot", {}),
            change_summary=vs.get("change_summary", "Initial generation")
        )
        db.add(pv)
    
    plan.status = PlanStatus.ACTIVE
    plan.updated_at = datetime.utcnow()
    db.commit()


@router.post("/plans/{plan_id}/export")
async def export_plan(plan_id: int, request: ExportRequest, db: Session = Depends(get_db)):
    plan = db.query(BusinessPlan).filter(BusinessPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Build complete plan data
    plan_data = await _build_plan_data(db, plan)
    
    os.makedirs(settings.EXPORT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{plan.name.replace(' ', '_')}_{timestamp}.{request.format}"
    output_path = os.path.join(settings.EXPORT_DIR, filename)
    
    if request.format == "pdf":
        exporter = PDFExporter()
        exporter.export(plan_data, output_path)
    elif request.format == "docx":
        exporter = DOCXExporter()
        exporter.export(plan_data, output_path)
    elif request.format == "xlsx":
        exporter = XLSXExporter()
        exporter.export(plan_data, output_path)
    else:
        raise HTTPException(status_code=400, detail="Invalid format")
    
    return {"download_url": f"/api/v1/exports/{filename}", "filename": filename}


@router.get("/exports/{filename}")
async def download_export(filename: str):
    from fastapi.responses import FileResponse
    file_path = os.path.join(settings.EXPORT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, filename=filename)


@router.get("/plans/{plan_id}/versions", response_model=List[PlanVersionResponse])
async def get_plan_versions(plan_id: int, db: Session = Depends(get_db)):
    versions = db.query(PlanVersion).filter(PlanVersion.plan_id == plan_id).order_by(PlanVersion.version_number.desc()).all()
    return versions


async def _build_plan_data(db: Session, plan: BusinessPlan) -> dict:
    from app.db.models import ExecutiveSummary, FinancialProjection, MarketAnalysis, CompetitorAnalysis, Strategy, OKR, ExecutionTracker, PlanVersion
    
    summary = db.query(ExecutiveSummary).filter(ExecutiveSummary.plan_id == plan.id).first()
    financials = db.query(FinancialProjection).filter(FinancialProjection.plan_id == plan.id).all()
    market = db.query(MarketAnalysis).filter(MarketAnalysis.plan_id == plan.id).first()
    competitor = db.query(CompetitorAnalysis).filter(CompetitorAnalysis.plan_id == plan.id).first()
    strategy = db.query(Strategy).filter(Strategy.plan_id == plan.id).first()
    okrs = db.query(OKR).filter(OKR.plan_id == plan.id).all()
    execution = db.query(ExecutionTracker).filter(ExecutionTracker.plan_id == plan.id).all()
    versions = db.query(PlanVersion).filter(PlanVersion.plan_id == plan.id).order_by(PlanVersion.version_number.desc()).all()
    
    return {
        "plan": {
            "id": plan.id,
            "name": plan.name,
            "description": plan.description,
            "frequency": plan.frequency.value,
            "industry": plan.industry,
            "company_size": plan.company_size,
            "revenue_range": plan.revenue_range,
            "status": plan.status.value,
            "created_at": plan.created_at.isoformat() if plan.created_at else None
        },
        "generated_plan": summary.content if summary else "",
        "financial_projections": {
            "assumptions": financials[0].assumptions if financials else {},
            "pnl": [
                {
                    "period": f.period,
                    "revenue": f.revenue,
                    "cogs": f.cogs,
                    "gross_profit": f.gross_profit,
                    "operating_expenses": f.operating_expenses,
                    "ebitda": f.ebitda,
                    "depreciation": f.depreciation,
                    "interest": f.interest,
                    "tax": f.tax,
                    "net_income": f.net_income
                } for f in financials
            ],
            "key_metrics": {}
        },
        "market_analysis": {
            "tam": market.tam if market else 0,
            "sam": market.sam if market else 0,
            "som": market.som if market else 0,
            "market_growth_rate": market.market_growth_rate if market else 0,
            "key_trends": market.key_trends if market else [],
            "target_segments": market.target_segments if market else [],
            "industry_benchmarks": market.industry_benchmarks if market else {},
            "macro_indicators": market.macro_indicators if market else {}
        },
        "competitor_analysis": {
            "competitors": competitor.competitors if competitor else [],
            "competitive_matrix": competitor.competitive_matrix if competitor else {},
            "positioning_map": competitor.positioning_map if competitor else {}
        },
        "strategy": {
            "swot": strategy.swot if strategy else {},
            "pestle": strategy.pestle if strategy else {},
            "gtm_strategy": strategy.gtm_strategy if strategy else {},
            "okrs": [
                {
                    "objective": o.objective,
                    "key_results": o.key_results,
                    "owner": o.owner,
                    "timeline": "Q1-Q4"
                } for o in okrs
            ],
            "milestones": [
                {
                    "milestone": e.milestone,
                    "target_date": e.target_date.isoformat() if e.target_date else None,
                    "dependencies": [],
                    "success_criteria": e.notes
                } for e in execution
            ]
        }
    }
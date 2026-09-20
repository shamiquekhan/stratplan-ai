import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base, init_db
from app.db.models import (
    BusinessPlan, PlanFrequency, PlanStatus,
    ExecutiveSummary, FinancialProjection, MarketAnalysis,
    CompetitorAnalysis, Strategy, OKR, ExecutionTracker, PlanVersion
)
from app.services.financial_engine import FinancialEngine

def seed_database():
    print("Seeding demo database...")
    init_db()
    db: Session = SessionLocal()

    try:
        # Check if demo plan already exists
        existing = db.query(BusinessPlan).filter(BusinessPlan.name == "Q4 SaaS Growth Plan").first()
        if existing:
            db.delete(existing)
            db.commit()

        # 1. Create Business Plan
        plan = BusinessPlan(
            name="Q4 SaaS Growth Plan",
            description="High-growth B2B SaaS expansion plan focusing on product-led growth and enterprise sales.",
            frequency=PlanFrequency.QUARTERLY,
            status=PlanStatus.ACTIVE,
            industry="SaaS",
            company_size="$100k-1M",
            revenue_range="$100k-1M"
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        print(f"Created plan ID: {plan.id}")

        # 2. Executive Summary
        summary = ExecutiveSummary(
            plan_id=plan.id,
            content="### Executive Summary\n\nThis Q4 SaaS Growth Plan outlines our strategic roadmap to scale annual recurring revenue (ARR) from $500k to $2.5M. By leveraging product-led growth (PLG) for SMBs and a targeted outbound motion for mid-market accounts, we project reaching cash flow break-even by Month 8.\n\n#### Key Highlights:\n- **Revenue Target:** 30% MoM growth rate.\n- **Gross Margins:** Maintaining industry-leading 72% gross margins.\n- **Capital Efficiency:** Controlled operating expense ratio with runway exceeding 24 months.",
            key_highlights=["30% MoM growth target", "Cash flow break-even by Month 8", "Enterprise expansion via outbound sales"]
        )
        db.add(summary)

        # 3. Financial Projections
        fin_engine = FinancialEngine()
        assumptions = {
            "revenue_growth_rate": 0.30,
            "gross_margin": 0.72,
            "operating_expense_ratio": 0.50,
            "tax_rate": 0.21,
            "interest_rate": 0.05,
            "depreciation_rate": 0.10,
            "working_capital_days": 30,
            "capex_percentage_of_revenue": 0.05,
            "churn_rate": 0.03,
            "cac": 850
        }
        projections = fin_engine.build_projections(assumptions, starting_revenue=50000, months=12)
        
        for i, pnl_row in enumerate(projections["pnl"]):
            m_num = i + 1
            fp = FinancialProjection(
                plan_id=plan.id,
                period=pnl_row["period"],
                year=2026 + ((m_num - 1) // 12),
                quarter=((m_num - 1) // 3) + 1,
                month=m_num,
                revenue=pnl_row["revenue"],
                cogs=pnl_row["cogs"],
                gross_profit=pnl_row["gross_profit"],
                operating_expenses=pnl_row["operating_expenses"],
                ebitda=pnl_row["ebitda"],
                depreciation=pnl_row["depreciation"],
                interest=pnl_row["interest"],
                tax=pnl_row["tax"],
                net_income=pnl_row["net_income"],
                cash_flow_operating=projections["cash_flow"][i]["operating"],
                cash_flow_investing=projections["cash_flow"][i]["investing"],
                cash_flow_financing=projections["cash_flow"][i]["financing"],
                net_cash_flow=projections["cash_flow"][i]["net_cash_flow"],
                cash_balance=projections["cash_flow"][i]["cash_balance"],
                assumptions=assumptions
            )
            db.add(fp)

        # 4. Market Analysis
        market = MarketAnalysis(
            plan_id=plan.id,
            tam=15000000000.0,
            sam=2500000000.0,
            som=150000000.0,
            market_growth_rate=0.22,
            key_trends=[
                "AI-driven automation in business workflows",
                "Shift towards PLG with enterprise upgrade paths",
                "Increased focus on security and compliance (SOC2, GDPR)"
            ],
            target_segments=[
                {"segment": "Mid-Market B2B SaaS", "size": "50-500 employees", "need": "Workflow optimization"},
                {"segment": "Enterprise Operations", "size": "500+ employees", "need": "Custom integrations & security"}
            ],
            industry_benchmarks={"avg_growth_rate": 0.35, "avg_gross_margin": 0.70, "avg_cac_payback": 12},
            macro_indicators={"interest_rate": 0.05, "inflation_rate": 0.028}
        )
        db.add(market)

        # 5. Competitor Analysis
        competitor = CompetitorAnalysis(
            plan_id=plan.id,
            competitors=[
                {"name": "CompetitorA", "url": "https://comp1.com", "pricing": "$99/mo", "strengths": "Brand recognition", "weaknesses": "Legacy UI", "funding_stage": "series_b"},
                {"name": "CompetitorB", "url": "https://comp2.com", "pricing": "$149/mo", "strengths": "Feature rich", "weaknesses": "Complex onboarding", "funding_stage": "seed"}
            ],
            competitive_matrix={
                "features": ["Ease of Use", "AI Integration", "Pricing", "Support"],
                "us": [True, True, "Affordable", "24/7"],
                "competitor_a": [False, True, "High", "Standard"],
                "competitor_b": [True, False, "Medium", "Email only"]
            },
            positioning_map={"x_axis": "Price", "y_axis": "Complexity", "our_position": {"x": 0.4, "y": 0.3}}
        )
        db.add(competitor)

        # 6. Strategy
        strategy = Strategy(
            plan_id=plan.id,
            swot={
                "strengths": ["Proprietary AI engine", "Low churn rate", "Agile development team"],
                "weaknesses": ["Brand awareness", "Limited enterprise sales team"],
                "opportunities": ["Global expansion", "Partnership ecosystem"],
                "threats": ["Aggressive pricing by incumbents", "Data privacy regulations"]
            },
            pestle={
                "political": "Favorable tech tax credits",
                "economic": "Stable B2B software spending",
                "social": "Remote work adoption driving tool demand",
                "technological": "Rapid advancements in LLMs",
                "legal": "Stricter data residency requirements",
                "environmental": "Cloud carbon footprint awareness"
            },
            gtm_strategy={
                "channels": ["Content & SEO", "Outbound Sales", "Product-Led Growth"],
                "value_proposition": "Automate business operations with AI intelligence and zero setup friction.",
                "pricing_strategy": "Tiered subscription: Starter ($49/mo), Pro ($199/mo), Enterprise (Custom)"
            },
            value_proposition="Automate business operations with AI intelligence and zero setup friction.",
            pricing_strategy="Tiered subscription: Starter ($49/mo), Pro ($199/mo), Enterprise (Custom)",
            channel_strategy=["Content & SEO", "Outbound Sales", "Product-Led Growth"]
        )
        db.add(strategy)

        # 7. OKRs
        okrs_data = [
            {
                "objective": "Achieve 30% Month-over-Month Revenue Growth",
                "owner": "CEO",
                "key_results": [
                    {"metric": "Monthly Recurring Revenue", "target": "$150k", "current": "$50k", "unit": "USD"},
                    {"metric": "Conversion Rate (Free to Paid)", "target": "8%", "current": "4%", "unit": "%"}
                ]
            },
            {
                "objective": "Enhance Product-Led Growth & Onboarding",
                "owner": "Head of Product",
                "key_results": [
                    {"metric": "Time to First Value", "target": "< 5 mins", "current": "15 mins", "unit": "mins"},
                    {"metric": "D30 Retention", "target": "45%", "current": "30%", "unit": "%"}
                ]
            }
        ]
        for od in okrs_data:
            okr = OKR(
                plan_id=plan.id,
                objective=od["objective"],
                key_results=od["key_results"],
                owner=od["owner"],
                status="in_progress",
                progress=40
            )
            db.add(okr)

        # 8. Execution Tracker
        from datetime import datetime
        tasks_data = [
            {"milestone": "Launch Self-Serve Onboarding Flow", "target_date": datetime(2026, 10, 15), "status": "in_progress", "notes": "High priority"},
            {"milestone": "Hire First Account Executive", "target_date": datetime(2026, 10, 30), "status": "pending", "notes": "Recruiting underway"},
            {"milestone": "Complete SOC2 Type II Audit", "target_date": datetime(2026, 11, 30), "status": "pending", "notes": "Auditor scheduled"},
            {"milestone": "Launch Q4 Paid Acquisition Campaign", "target_date": datetime(2026, 10, 5), "status": "completed", "notes": "Completed on time"}
        ]
        for td in tasks_data:
            task = ExecutionTracker(
                plan_id=plan.id,
                milestone=td["milestone"],
                target_date=td["target_date"],
                status=td["status"],
                notes=td["notes"]
            )
            db.add(task)

        db.commit()
        print("Demo database seeded successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

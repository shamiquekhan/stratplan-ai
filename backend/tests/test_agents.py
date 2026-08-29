import pytest
from app.agents.financial_agent import FinancialAgent
from app.agents.market_research import MarketResearchAgent
from app.agents.strategy_agent import StrategyAgent
from app.services.financial_engine import FinancialEngine


class TestFinancialEngine:
    def test_build_projections_basic(self):
        engine = FinancialEngine()
        assumptions = {
            "revenue_growth_rate": 0.20,
            "gross_margin": 0.65,
            "operating_expense_ratio": 0.45,
            "tax_rate": 0.21,
            "interest_rate": 0.05,
            "depreciation_rate": 0.10,
            "working_capital_days": 30,
            "capex_percentage_of_revenue": 0.05,
        }
        
        result = engine.build_projections(assumptions, starting_revenue=100000, months=12)
        
        assert "pnl" in result
        assert "cash_flow" in result
        assert "balance_sheet" in result
        assert "key_metrics" in result
        assert len(result["pnl"]) == 12
        assert len(result["cash_flow"]) == 12
        assert len(result["balance_sheet"]) == 12
        
        # Check first month
        assert result["pnl"][0]["revenue"] == 100000
        assert result["pnl"][0]["gross_profit"] == 65000
        
        # Check growth
        assert result["pnl"][-1]["revenue"] > result["pnl"][0]["revenue"]
        
        # Check key metrics
        assert "runway_months" in result["key_metrics"]
        assert "break_even_month" in result["key_metrics"]
    
    def test_sensitivity_analysis(self):
        engine = FinancialEngine()
        assumptions = {
            "revenue_growth_rate": 0.20,
            "gross_margin": 0.65,
            "operating_expense_ratio": 0.45,
        }
        
        result = engine.sensitivity_analysis(assumptions, 100000)
        
        assert "base" in result
        assert "optimistic" in result
        assert "pessimistic" in result
        
        # Optimistic should have higher revenue
        assert result["optimistic"]["final_revenue"] > result["base"]["final_revenue"]
        assert result["pessimistic"]["final_revenue"] < result["base"]["final_revenue"]


class TestFinancialAgent:
    @pytest.mark.asyncio
    async def test_generate_assumptions(self):
        agent = FinancialAgent()
        plan = {"industry": "SaaS", "frequency": "quarterly"}
        user_inputs = {"stage": "growth", "current_revenue": 50000, "business_model": "subscription"}
        benchmarks = {"avg_growth_rate": 0.30, "avg_margin": 0.70}
        macro = {"interest_rate": 0.05, "inflation_rate": 0.03}
        
        assumptions = await agent._generate_assumptions(plan, user_inputs, benchmarks, macro)
        
        assert "revenue_growth_rate" in assumptions
        assert "gross_margin" in assumptions
        assert "operating_expense_ratio" in assumptions
        assert assumptions["tax_rate"] == 0.21
        assert assumptions["interest_rate"] == 0.05
        
        # Growth stage should have high growth
        assert assumptions["revenue_growth_rate"] >= 0.30
        assert assumptions["gross_margin"] >= 0.65
        assert assumptions["operating_expense_ratio"] <= 0.45


class TestMarketResearchAgent:
    @pytest.mark.asyncio
    async def test_default_market(self):
        agent = MarketResearchAgent()
        plan = {"industry": "SaaS"}
        user_inputs = {"geography": "US"}
        
        result = agent._get_default_market(plan)
        
        assert "tam" in result
        assert "sam" in result
        assert "som" in result
        assert result["tam"] > result["sam"] > result["som"]
        assert "key_trends" in result
        assert "industry_benchmarks" in result


class TestStrategyAgent:
    @pytest.mark.asyncio
    async def test_default_strategy(self):
        agent = StrategyAgent()
        plan = {"industry": "SaaS"}
        
        result = agent._get_default_strategy(plan)
        
        assert "swot" in result
        assert "pestle" in result
        assert "gtm_strategy" in result
        assert "okrs" in result
        assert "milestones" in result
        assert "risk_assessment" in result
        
        # Check SWOT structure
        for quadrant in ["strengths", "weaknesses", "opportunities", "threats"]:
            assert quadrant in result["swot"]
            assert isinstance(result["swot"][quadrant], list)
            assert len(result["swot"][quadrant]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
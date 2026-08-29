from typing import Dict, Any
from app.agents.base import BaseAgent
from app.services.financial_engine import FinancialEngine
import json
import re


class FinancialAgent(BaseAgent):
    def __init__(self, llm=None):
        super().__init__(llm)
        self.engine = FinancialEngine()
    
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("plan", {})
        user_inputs = state.get("user_inputs", {})
        
        benchmarks = state.get("industry_benchmarks", {})
        macro_data = state.get("macro_indicators", {})
        
        try:
            if self._mock_mode:
                assumptions = self._get_default_assumptions(plan, user_inputs, benchmarks, macro_data)
            else:
                # Use LLM to determine assumptions based on context
                assumptions = await self._generate_assumptions(plan, user_inputs, benchmarks, macro_data)
            
            # Build projections using financial engine
            starting_revenue = user_inputs.get("current_revenue", 0)
            financial_data = self.engine.build_projections(assumptions, starting_revenue)
            
            # Add sensitivity analysis
            financial_data["sensitivity"] = self.engine.sensitivity_analysis(assumptions, starting_revenue)
        except Exception as e:
            # Fallback to defaults if LLM fails
            assumptions = self._get_default_assumptions(plan, user_inputs, benchmarks, macro_data)
            starting_revenue = user_inputs.get("current_revenue", 0)
            financial_data = self.engine.build_projections(assumptions, starting_revenue)
            financial_data["sensitivity"] = self.engine.sensitivity_analysis(assumptions, starting_revenue)
        
        return {
            **state,
            "financial_projections": financial_data,
            "current_agent": "financial"
        }
    
    async def _generate_assumptions(
        self, 
        plan: Dict, 
        user_inputs: Dict, 
        benchmarks: Dict, 
        macro: Dict
    ) -> Dict[str, float]:
        """Use LLM to generate realistic assumptions, then validate with engine defaults"""
        
        prompt = self._get_assumptions_prompt(plan, user_inputs, benchmarks, macro)
        
        try:
            response = await self.llm.ainvoke(prompt)
            content = response.content if response.content else "{}"
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                llm_assumptions = json.loads(json_match.group())
            else:
                llm_assumptions = {}
        except Exception:
            llm_assumptions = {}
        
        # Merge with defaults, preferring LLM values
        defaults = self._get_default_assumptions(plan, user_inputs, benchmarks, macro)
        for key, default_val in defaults.items():
            if key not in llm_assumptions or llm_assumptions[key] is None:
                llm_assumptions[key] = default_val
        
        return llm_assumptions
    
    def _get_default_assumptions(
        self, 
        plan: Dict, 
        user_inputs: Dict, 
        benchmarks: Dict, 
        macro: Dict
    ) -> Dict[str, float]:
        stage = user_inputs.get("stage", "early")
        industry = plan.get("industry", "general")
        
        # Stage-based defaults
        stage_defaults = {
            "early": {"revenue_growth_rate": 0.25, "gross_margin": 0.55, "operating_expense_ratio": 0.70},
            "mvp": {"revenue_growth_rate": 0.35, "gross_margin": 0.60, "operating_expense_ratio": 0.60},
            "traction": {"revenue_growth_rate": 0.40, "gross_margin": 0.65, "operating_expense_ratio": 0.50},
            "growth": {"revenue_growth_rate": 0.30, "gross_margin": 0.70, "operating_expense_ratio": 0.40},
            "scale": {"revenue_growth_rate": 0.20, "gross_margin": 0.75, "operating_expense_ratio": 0.35},
        }
        
        s = stage_defaults.get(stage, stage_defaults["early"])
        
        # Adjust for macro
        fed_funds = macro.get("interest_rate", 0.05)
        inflation = macro.get("inflation_rate", 0.03)
        
        return {
            "revenue_growth_rate": s["revenue_growth_rate"],
            "gross_margin": s["gross_margin"],
            "operating_expense_ratio": s["operating_expense_ratio"],
            "tax_rate": 0.21,
            "interest_rate": fed_funds,
            "depreciation_rate": 0.10,
            "working_capital_days": 30,
            "capex_percentage_of_revenue": 0.05,
            "churn_rate": 0.05,
            "cac": 1000,
        }
    
    def _get_assumptions_prompt(self, plan: Dict, user_inputs: Dict, benchmarks: Dict, macro: Dict) -> str:
        return f"""You are a CFO determining key financial assumptions for a {plan.get('frequency', 'quarterly')} business plan.

Business Context:
- Industry: {plan.get('industry', 'general business')}
- Stage: {user_inputs.get('stage', 'early')}
- Current Revenue: ${user_inputs.get('current_revenue', 0):,.0f}
- Business Model: {user_inputs.get('business_model', 'subscription')}

Industry Benchmarks: {json.dumps(benchmarks, indent=2) if benchmarks else "Not available"}
Macro Indicators: {json.dumps(macro, indent=2) if macro else "Not available"}

Generate a JSON object with ONLY these keys (use realistic values):
{{
  "revenue_growth_rate": 0.0,
  "gross_margin": 0.0,
  "operating_expense_ratio": 0.0,
  "tax_rate": 0.21,
  "interest_rate": 0.05,
  "depreciation_rate": 0.10,
  "working_capital_days": 30,
  "capex_percentage_of_revenue": 0.05,
  "churn_rate": 0.05,
  "cac": 1000
}}

Rules:
1. Early stage = higher growth, lower margins, higher OpEx
2. Growth stage = high growth, improving margins, controlled OpEx
3. Scale stage = moderate growth, high margins, efficient OpEx
4. Adjust interest_rate based on macro fed_funds_rate
5. SaaS: lower churn (3-5%), higher gross margin (70-80%)
6. E-commerce: higher churn, lower gross margin (30-50%)
7. Services: lower gross margin (50-60%), lower CAC
Return ONLY valid JSON.
"""
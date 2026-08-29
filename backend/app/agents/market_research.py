from typing import Dict, Any
from app.agents.base import BaseAgent
import json
import re


class MarketResearchAgent(BaseAgent):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("plan", {})
        user_inputs = state.get("user_inputs", {})
        
        # Get external data if available
        fred_data = state.get("fred_data", {})
        alpha_vantage_data = state.get("alpha_vantage_data", {})
        
        if self._mock_mode:
            market_data = self._get_default_market(plan)
        else:
            try:
                prompt = self._get_market_prompt(plan, user_inputs, fred_data, alpha_vantage_data)
                response = await self.llm.ainvoke(prompt)
                content = response.content if response.content else "{}"
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    market_data = json.loads(json_match.group())
                else:
                    market_data = self._get_default_market(plan)
            except Exception:
                market_data = self._get_default_market(plan)
        
        return {
            **state,
            "market_analysis": market_data,
            "current_agent": "market_research"
        }
    
    def _get_market_prompt(self, plan: Dict, user_inputs: Dict, fred: Dict, alpha: Dict) -> str:
        industry = plan.get("industry", "general business")
        geography = user_inputs.get("geography", "US")
        
        return f"""You are a market research analyst. Create a comprehensive market analysis for a business in the {industry} industry, targeting {geography}.

Plan Context:
- Industry: {industry}
- Geography: {geography}
- Business Stage: {user_inputs.get('stage', 'early')}
- Target Customer: {user_inputs.get('target_customer', 'Not specified')}

Macro Data (FRED): {json.dumps(fred, indent=2) if fred else "Not available"}
Industry Data (Alpha Vantage): {json.dumps(alpha, indent=2) if alpha else "Not available"}

Generate a JSON object with this exact structure:
{{
  "tam": 0,
  "sam": 0,
  "som": 0,
  "market_growth_rate": 0.0,
  "key_trends": ["trend 1", "trend 2", "trend 3"],
  "target_segments": [
    {{"segment": "Segment name", "size": 0, "growth_rate": 0.0, "characteristics": ["char1", "char2"]}}
  ],
  "industry_benchmarks": {{
    "avg_revenue_per_employee": 0,
    "avg_gross_margin": 0.0,
    "avg_operating_margin": 0.0,
    "typical_cac": 0,
    "typical_ltv": 0
  }},
  "macro_indicators": {{
    "gdp_growth": 0.0,
    "inflation_rate": 0.0,
    "interest_rate": 0.0,
    "unemployment_rate": 0.0,
    "consumer_confidence": 0.0
  }},
  "market_drivers": ["driver 1", "driver 2"],
  "market_barriers": ["barrier 1", "barrier 2"]
}}

Rules:
1. TAM/SAM/SOM must be realistic for the industry and geography
2. Use macro data to ground growth rates
3. Key trends should be specific to the industry
4. Target segments should be distinct and actionable
5. Return ONLY valid JSON, no markdown formatting
"""
    
    def _get_default_market(self, plan: Dict) -> Dict:
        industry = plan.get("industry", "SaaS")
        base_tam = {"SaaS": 5000000000, "FinTech": 3000000000, "HealthTech": 2000000000, "E-commerce": 8000000000}.get(industry, 1000000000)
        
        return {
            "tam": base_tam,
            "sam": base_tam // 10,
            "som": base_tam // 100,
            "market_growth_rate": 0.15,
            "key_trends": ["AI/ML integration", "Vertical specialization", "PLG motion", "Usage-based pricing"],
            "target_segments": [
                {"segment": "SMB (50-500 employees)", "size": base_tam // 50, "growth_rate": 0.18, "characteristics": ["Budget-conscious", "Need simplicity", "Fast decision cycles"]},
                {"segment": "Mid-market (500-2000)", "size": base_tam // 20, "growth_rate": 0.12, "characteristics": ["Integration needs", "Security requirements", "Longer sales cycles"]}
            ],
            "industry_benchmarks": {
                "avg_revenue_per_employee": 250000,
                "avg_gross_margin": 0.75,
                "avg_operating_margin": 0.20,
                "typical_cac": 800,
                "typical_ltv": 12000
            },
            "macro_indicators": {
                "gdp_growth": 0.025,
                "inflation_rate": 0.03,
                "interest_rate": 0.05,
                "unemployment_rate": 0.04,
                "consumer_confidence": 102
            },
            "market_drivers": ["Digital transformation", "Remote work adoption", "API economy growth"],
            "market_barriers": ["High switching costs", "Data privacy regulations", "Talent shortage"]
        }
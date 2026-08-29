from typing import Dict, Any
from app.agents.base import BaseAgent
import json
import re


class StrategyAgent(BaseAgent):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("plan", {})
        user_inputs = state.get("user_inputs", {})
        
        # Use outputs from previous agents
        market = state.get("market_analysis", {})
        competitor = state.get("competitor_analysis", {})
        financial = state.get("financial_projections", {})
        
        if self._mock_mode:
            strategy_data = self._get_default_strategy(plan)
        else:
            try:
                prompt = self._get_strategy_prompt(plan, user_inputs, market, competitor, financial)
                response = await self.llm.ainvoke(prompt)
                content = response.content if response.content else "{}"
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    strategy_data = json.loads(json_match.group())
                else:
                    strategy_data = self._get_default_strategy(plan)
            except Exception:
                strategy_data = self._get_default_strategy(plan)
        
        return {
            **state,
            "strategy": strategy_data,
            "current_agent": "strategy"
        }
    
    def _get_strategy_prompt(self, plan: Dict, user_inputs: Dict, market: Dict, competitor: Dict, financial: Dict) -> str:
        industry = plan.get("industry", "general business")
        frequency = plan.get("frequency", "quarterly")
        
        return f"""You are a Chief Strategy Officer. Create a comprehensive strategy for a {frequency} business plan in the {industry} industry.

Context from Other Agents:
- Market Analysis: {json.dumps(market, indent=2) if market else "Not available"}
- Competitor Analysis: {json.dumps(competitor, indent=2) if competitor else "Not available"}
- Financial Projections: {json.dumps(financial.get('assumptions', {}), indent=2) if financial else "Not available"}

User Inputs:
- Business Model: {user_inputs.get('business_model', 'Not specified')}
- GTM Preference: {user_inputs.get('gtm_preference', 'Not specified')}
- Funding Status: {user_inputs.get('funding_status', 'bootstrapped')}

Generate a JSON object with this exact structure:
{{
  "swot": {{
    "strengths": ["strength1", "strength2", "strength3"],
    "weaknesses": ["weakness1", "weakness2"],
    "opportunities": ["opportunity1", "opportunity2", "opportunity3"],
    "threats": ["threat1", "threat2"]
  }},
  "pestle": {{
    "political": ["factor1", "factor2"],
    "economic": ["factor1", "factor2"],
    "social": ["factor1", "factor2"],
    "technological": ["factor1", "factor2"],
    "legal": ["factor1", "factor2"],
    "environmental": ["factor1", "factor2"]
  }},
  "gtm_strategy": {{
    "value_proposition": "Clear value prop statement",
    "target_customer": "Primary ICP description",
    "pricing_strategy": "Strategy description",
    "channels": [
      {{"channel": "Channel name", "priority": "high|medium|low", "budget_allocation": 0.0, "expected_cac": 0, "timeline": "Q1"}}
    ],
    "launch_sequence": [
      {{"phase": "Phase 1", "activities": ["activity1", "activity2"], "timeline": "Month 1-3"}}
    ],
    "partnerships": ["partner1", "partner2"]
  }},
  "okrs": [
    {{
      "objective": "Objective statement",
      "key_results": [
        {{"metric": "Metric name", "target": 0, "current": 0, "unit": "%|$|count"}}
      ],
      "owner": "Role",
      "timeline": "Q1-Q4"
    }}
  ],
  "milestones": [
    {{"milestone": "Milestone name", "target_date": "YYYY-MM-DD", "dependencies": ["dep1"], "success_criteria": "Criteria"}}
  ],
  "risk_assessment": [
    {{"risk": "Risk description", "likelihood": "high|medium|low", "impact": "high|medium|low", "mitigation": "Mitigation strategy"}}
  ]
}}

Rules:
1. SWOT must be specific to the business, not generic
2. PESTLE factors should reference actual macro trends
3. GTM channels should match budget and stage
4. OKRs must be measurable and time-bound
5. Milestones should be achievable and sequenced
6. Risks should have concrete mitigations
7. Return ONLY valid JSON, no markdown formatting
"""
    
    def _get_default_strategy(self, plan: Dict) -> Dict:
        industry = plan.get("industry", "SaaS")
        stage = "early"  # Could extract from user_inputs
        return {
            "swot": {
                "strengths": [
                    f"Modern {industry} architecture with API-first design",
                    "Superior user experience and fast onboarding (< 5 min)",
                    "Flexible pricing that scales with customer growth",
                    "Strong founding team with domain expertise"
                ],
                "weaknesses": [
                    "Limited brand recognition in early market",
                    "Small team constrains parallel feature development",
                    "No enterprise sales motion yet",
                    "Dependent on third-party integrations for key features"
                ],
                "opportunities": [
                    "Growing demand for AI-enhanced workflow automation",
                    "Vertical expansion into adjacent markets (FinTech, HealthTech)",
                    "Partnership channel with system integrators",
                    "International expansion to EU/APAC markets"
                ],
                "threats": [
                    "Well-funded competitors adding similar features",
                    "Economic downturn reducing B2B software budgets",
                    "Platform risk from major cloud providers",
                    "Talent acquisition challenges in competitive market"
                ]
            },
            "pestle": {
                "political": [
                    "Increased government scrutiny on data sovereignty",
                    "Procurement policy changes favoring domestic vendors"
                ],
                "economic": [
                    "Rising interest rates increase cost of capital for startups",
                    "Enterprise software spend growing despite macro headwinds"
                ],
                "social": [
                    "Remote/hybrid work driving collaboration tool adoption",
                    "Generational shift toward self-serve purchasing"
                ],
                "technological": [
                    "LLM commoditization enabling AI features at low cost",
                    "API standardization reducing integration friction"
                ],
                "legal": [
                    "GDPR/CCPA compliance as baseline requirement",
                    "SOC 2 Type II becoming table stakes for enterprise"
                ],
                "environmental": [
                    "Carbon-neutral cloud hosting as differentiator",
                    "Green software practices attracting ESG-focused buyers"
                ]
            },
            "gtm_strategy": {
                "value_proposition": f"The only {industry} platform combining enterprise-grade power with consumer-grade simplicity — deploy in minutes, scale without limits",
                "target_customer": "Growth-stage B2B companies (50-500 employees) seeking to modernize operations without enterprise complexity",
                "pricing_strategy": "Three-tier value-based pricing with usage-based overages; free trial + freemium tier for PLG motion",
                "channels": [
                    {"channel": "Content & SEO", "priority": "high", "budget_allocation": 0.35, "expected_cac": 300, "timeline": "Q1-Q4"},
                    {"channel": "Product-Led Growth", "priority": "high", "budget_allocation": 0.25, "expected_cac": 150, "timeline": "Q1-Q4"},
                    {"channel": "Strategic Partnerships", "priority": "high", "budget_allocation": 0.20, "expected_cac": 400, "timeline": "Q2-Q4"},
                    {"channel": "Paid Search", "priority": "medium", "budget_allocation": 0.15, "expected_cac": 800, "timeline": "Q2-Q4"},
                    {"channel": "Outbound Sales", "priority": "medium", "budget_allocation": 0.05, "expected_cac": 2500, "timeline": "Q3-Q4"}
                ],
                "launch_sequence": [
                    {"phase": "Foundation", "activities": ["Website redesign", "Content engine", "Free tier launch", "Analytics setup"], "timeline": "Month 1-2"},
                    {"phase": "Growth", "activities": ["Partner program", "Paid campaigns", "Case studies", "Webinar series"], "timeline": "Month 3-6"},
                    {"phase": "Scale", "activities": ["Enterprise sales hire", "ABM campaigns", "International SEO", "Customer marketing"], "timeline": "Month 7-12"}
                ],
                "partnerships": ["Zapier/Make", "HubSpot/Salesforce", "Cloud marketplaces (AWS/Azure/GCP)", "System integrators", "Industry consultants"]
            },
            "okrs": [
                {
                    "objective": "Achieve Product-Market Fit",
                    "key_results": [
                        {"metric": "NPS", "target": 50, "current": 0, "unit": "score"},
                        {"metric": "Monthly Churn", "target": 3, "current": 15, "unit": "%"},
                        {"metric": "Activation Rate (Day 7)", "target": 60, "current": 25, "unit": "%"},
                        {"metric": "Organic Signups/Month", "target": 500, "current": 50, "unit": "count"}
                    ],
                    "owner": "Product",
                    "timeline": "Q1-Q2"
                },
                {
                    "objective": "Build Scalable Go-to-Market Engine",
                    "key_results": [
                        {"metric": "CAC Payback Period", "target": 8, "current": 24, "unit": "months"},
                        {"metric": "Pipeline from Partnerships", "target": 30, "current": 0, "unit": "%"},
                        {"metric": "Content-Driven Organic Traffic", "target": 50000, "current": 2000, "unit": "visits/mo"},
                        {"metric": "Sales Cycle (SMB)", "target": 30, "current": 60, "unit": "days"}
                    ],
                    "owner": "Marketing/Growth",
                    "timeline": "Q2-Q4"
                },
                {
                    "objective": "Prepare for Series A",
                    "key_results": [
                        {"metric": "ARR", "target": 500000, "current": 50000, "unit": "$"},
                        {"metric": "Net Revenue Retention", "target": 110, "current": 85, "unit": "%"},
                        {"metric": "Team Size", "target": 15, "current": 5, "unit": "count"},
                        {"metric": "Runway", "target": 18, "current": 10, "unit": "months"}
                    ],
                    "owner": "CEO/Founder",
                    "timeline": "Q3-Q4"
                }
            ],
            "milestones": [
                {"milestone": "MVP Launch + Free Tier", "target_date": "2024-02-01", "dependencies": [], "success_criteria": "100 active free users, < 5 min time-to-value"},
                {"milestone": "Product-Market Fit Signals", "target_date": "2024-05-01", "dependencies": ["MVP Launch + Free Tier"], "success_criteria": "NPS > 40, Churn < 5%, 20+ paying customers"},
                {"milestone": "Partner Program Live", "target_date": "2024-07-01", "dependencies": ["Product-Market Fit Signals"], "success_criteria": "5 certified partners, 20% pipeline from partners"},
                {"milestone": "Series A Fundraise", "target_date": "2024-11-01", "dependencies": ["Partner Program Live"], "success_criteria": "$500k ARR, 3x YoY growth, 18mo runway"},
                {"milestone": "Enterprise Features GA", "target_date": "2025-02-01", "dependencies": ["Series A Fundraise"], "success_criteria": "SSO, SCIM, Audit logs, SLA — 3 enterprise pilots"}
            ],
            "risk_assessment": [
                {"risk": "Major competitor launches AI-native competing product", "likelihood": "high", "impact": "high", "mitigation": "Accelerate AI roadmap; build proprietary data moat; deepen vertical specialization"},
                {"risk": "Economic recession extends sales cycles, reduces budgets", "likelihood": "medium", "impact": "high", "mitigation": "Emphasize ROI/cost-savings messaging; extend free tier; pursue annual prepaid discounts"},
                {"risk": "Key engineering talent poached by Big Tech", "likelihood": "medium", "impact": "medium", "mitigation": "Equity refresh grants; interesting technical challenges; remote-first culture"},
                {"risk": "Platform dependency risk (cloud provider API changes)", "likelihood": "low", "impact": "high", "mitigation": "Multi-cloud architecture; abstract provider APIs; maintain exit options"}
            ]
        }
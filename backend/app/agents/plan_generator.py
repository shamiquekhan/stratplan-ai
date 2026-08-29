from typing import Dict, Any
from app.agents.base import BaseAgent


class PlanGeneratorAgent(BaseAgent):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("plan", {})
        user_inputs = state.get("user_inputs", {})
        
        if self._mock_mode:
            generated_plan = self._get_mock_plan(plan, user_inputs)
        else:
            try:
                prompt = self._get_generation_prompt(plan, user_inputs)
                response = await self.llm.ainvoke(prompt)
                generated_plan = response.content if response.content else "Plan generation failed"
            except Exception as e:
                generated_plan = f"Error generating plan: {str(e)}"
        
        return {
            **state,
            "generated_plan": generated_plan,
            "current_agent": "plan_generator"
        }
    
    def _get_generation_prompt(self, plan: Dict, user_inputs: Dict) -> str:
        frequency = plan.get("frequency", "quarterly")
        industry = plan.get("industry", "general business")
        company_size = plan.get("company_size", "SME")
        
        return f"""You are an expert business strategist. Create a comprehensive {frequency} business plan for a {company_size} in the {industry} industry.

Plan Details:
- Name: {plan.get('name', 'Untitled Plan')}
- Description: {plan.get('description', 'No description provided')}
- Frequency: {frequency}
- Industry: {industry}
- Company Size: {company_size}
- Revenue Range: {plan.get('revenue_range', 'Not specified')}

User Inputs: {user_inputs}

Generate a structured business plan with the following sections:
1. Executive Summary
2. Market Analysis (TAM/SAM/SOM, trends, target segments)
3. Competitive Analysis (key competitors, positioning)
4. Strategy (SWOT, PESTLE, GTM, value proposition)
5. Financial Projections (3-statement model assumptions)
6. OKRs & Milestones
7. Risk Assessment

Be specific, data-driven, and actionable. Use professional business language.
"""
    
    def _get_mock_plan(self, plan: Dict, user_inputs: Dict) -> str:
        return f"""# {plan.get('name', 'Business Plan')} - Executive Summary

## Company Overview
{plan.get('name', 'Our Company')} is a {plan.get('company_size', 'SME')} in the {plan.get('industry', 'technology')} industry, operating on a {plan.get('frequency', 'quarterly')} planning cycle.

## Mission & Vision
To deliver innovative {user_inputs.get('business_model', 'subscription')} solutions that empower {user_inputs.get('target_customer', 'B2B customers')} to achieve their goals through cutting-edge technology and exceptional service.

## Market Opportunity
Addressing a significant market gap in {plan.get('industry', 'the industry')}, we target {user_inputs.get('target_customer', 'SMBs')} with a differentiated approach focused on {user_inputs.get('differentiation', 'superior user experience and competitive pricing')}.

## Financial Highlights
- Current Revenue: ${user_inputs.get('current_revenue', 0):,.0f}
- Projected 3-Year Revenue Growth: 150-200%
- Target Gross Margin: 70%+
- Break-even: Month 18-24

## Key Strategies
1. **Product-Led Growth**: Self-serve onboarding and viral features
2. **Content & SEO**: Thought leadership to drive organic acquisition
3. **Strategic Partnerships**: Integration with complementary platforms
4. **Customer Success**: Dedicated support for enterprise accounts

## Funding & Milestones
- Status: {user_inputs.get('funding_status', 'Bootstrapped')}
- Next Milestone: Product-Market Fit (Month 6)
- Series A Target: $100k ARR with 3x YoY growth

## Risk Factors
- Competition from established players
- Economic uncertainty affecting B2B spend
- Technology disruption in AI/ML space

*Generated in MOCK_MODE for testing purposes*
"""
from typing import Dict, Any
from app.agents.base import BaseAgent
import json
import re


class CompetitorAgent(BaseAgent):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("plan", {})
        user_inputs = state.get("user_inputs", {})
        
        # Get scraped competitor data if available
        scraped_data = state.get("competitor_scraped_data", {})
        
        if self._mock_mode:
            competitor_data = self._get_default_competitors(plan)
        else:
            try:
                prompt = self._get_competitor_prompt(plan, user_inputs, scraped_data)
                response = await self.llm.ainvoke(prompt)
                content = response.content if response.content else "{}"
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    competitor_data = json.loads(json_match.group())
                else:
                    competitor_data = self._get_default_competitors(plan)
            except Exception:
                competitor_data = self._get_default_competitors(plan)
        
        return {
            **state,
            "competitor_analysis": competitor_data,
            "current_agent": "competitor"
        }
    
    def _get_competitor_prompt(self, plan: Dict, user_inputs: Dict, scraped: Dict) -> str:
        industry = plan.get("industry", "general business")
        
        return f"""You are a competitive intelligence analyst. Analyze competitors for a business in the {industry} industry.

User Inputs:
- Known Competitors: {user_inputs.get('competitors', 'Not specified')}
- Business Differentiation: {user_inputs.get('differentiation', 'Not specified')}

Scraped Data: {json.dumps(scraped, indent=2) if scraped else "Not available"}

Generate a JSON object with this exact structure:
{{
  "competitors": [
    {{
      "name": "Competitor Name",
      "website": "https://example.com",
      "description": "Brief description",
      "pricing_model": "subscription|freemium|per_use|license",
      "pricing_tiers": [
        {{"name": "Basic", "price": 0, "features": ["feat1", "feat2"]}}
      ],
      "key_features": ["feature1", "feature2", "feature3"],
      "tech_stack": ["React", "Node.js", "PostgreSQL"],
      "positioning": "Value proposition statement",
      "target_segment": "Target customer segment",
      "strengths": ["strength1", "strength2"],
      "weaknesses": ["weakness1", "weakness2"],
      "funding_stage": "seed|series_a|series_b|public|bootstrapped",
      "employee_count": 0,
      "estimated_revenue": 0
    }}
  ],
  "competitive_matrix": {{
    "criteria": ["Price", "Features", "Ease of Use", "Support", "Integrations"],
    "scores": {{
      "Our Company": [4, 5, 4, 4, 3],
      "Competitor 1": [3, 4, 3, 3, 4],
      "Competitor 2": [5, 3, 5, 2, 5]
    }}
  }},
  "positioning_map": {{
    "x_axis": "Price",
    "y_axis": "Features",
    "positions": {{
      "Our Company": [0.6, 0.8],
      "Competitor 1": [0.3, 0.5],
      "Competitor 2": [0.9, 0.4]
    }}
  }},
  "competitive_advantages": ["advantage1", "advantage2"],
  "threats": ["threat1", "threat2"]
}}

Rules:
1. Include 3-5 competitors if possible
2. Use scraped data to ground pricing and features
3. Competitive matrix criteria should be industry-relevant
4. Positioning map should use meaningful axes
5. Be objective - highlight both strengths and weaknesses
6. Return ONLY valid JSON, no markdown formatting
"""
    
    def _get_default_competitors(self, plan: Dict) -> Dict:
        industry = plan.get("industry", "SaaS")
        return {
            "competitors": [
                {
                    "name": "Competitor A",
                    "website": "https://competitor-a.com",
                    "description": f"Leading {industry} platform for enterprise",
                    "pricing_model": "subscription",
                    "pricing_tiers": [
                        {"name": "Starter", "price": 49, "features": ["Core features", "Email support"]},
                        {"name": "Professional", "price": 149, "features": ["Advanced analytics", "Priority support", "API access"]},
                        {"name": "Enterprise", "price": 499, "features": ["Custom integrations", "Dedicated CSM", "SLA guarantee"]}
                    ],
                    "key_features": ["Advanced reporting", "Team collaboration", "Third-party integrations", "Custom workflows", "SSO/SAML"],
                    "tech_stack": ["React", "Node.js", "PostgreSQL", "Kubernetes"],
                    "positioning": "Complete platform for scaling teams",
                    "target_segment": "Mid-market to Enterprise",
                    "strengths": ["Market leader", "Extensive integrations", "Strong brand"],
                    "weaknesses": ["High price", "Complex onboarding", "Rigid pricing"],
                    "funding_stage": "series_c",
                    "employee_count": 450,
                    "estimated_revenue": 85000000
                },
                {
                    "name": "Competitor B",
                    "website": "https://competitor-b.com",
                    "description": f"Modern {industry} tool for startups",
                    "pricing_model": "freemium",
                    "pricing_tiers": [
                        {"name": "Free", "price": 0, "features": ["Up to 5 users", "Basic features"]},
                        {"name": "Pro", "price": 29, "features": ["Unlimited users", "Advanced features", "Integrations"]}
                    ],
                    "key_features": ["Real-time collaboration", "Mobile app", "Automation", "Templates"],
                    "tech_stack": ["Vue.js", "Go", "PostgreSQL", "Redis"],
                    "positioning": "Fast, simple, affordable",
                    "target_segment": "Startups and SMBs",
                    "strengths": ["Free tier", "Easy setup", "Modern UX"],
                    "weaknesses": ["Limited enterprise features", "No phone support", "Fewer integrations"],
                    "funding_stage": "series_a",
                    "employee_count": 80,
                    "estimated_revenue": 8000000
                },
                {
                    "name": "Competitor C",
                    "website": "https://competitor-c.com",
                    "description": f"Specialized {industry} solution for vertical markets",
                    "pricing_model": "per_use",
                    "pricing_tiers": [
                        {"name": "Pay-per-use", "price": 0.10, "features": ["Per transaction pricing", "Volume discounts"]}
                    ],
                    "key_features": ["Industry-specific workflows", "Compliance built-in", "White-label options"],
                    "tech_stack": ["Angular", "Java", "Oracle", "AWS"],
                    "positioning": "Vertical expertise, compliance-first",
                    "target_segment": "Regulated industries (FinTech, HealthTech)",
                    "strengths": ["Deep vertical expertise", "Compliance certifications", "High retention"],
                    "weaknesses": ["Niche focus", "Legacy tech stack", "Slow innovation"],
                    "funding_stage": "bootstrapped",
                    "employee_count": 120,
                    "estimated_revenue": 25000000
                }
            ],
            "competitive_matrix": {
                "criteria": ["Price", "Features", "Ease of Use", "Support", "Integrations", "Scalability"],
                "scores": {
                    "Our Company": [5, 4, 5, 4, 4, 4],
                    "Competitor A": [2, 5, 3, 4, 5, 5],
                    "Competitor B": [4, 3, 5, 3, 3, 3],
                    "Competitor C": [3, 4, 2, 5, 2, 4]
                }
            },
            "positioning_map": {
                "x_axis": "Price (Low to High)",
                "y_axis": "Feature Breadth (Narrow to Broad)",
                "positions": {
                    "Our Company": [0.7, 0.75],
                    "Competitor A": [0.9, 0.9],
                    "Competitor B": [0.2, 0.4],
                    "Competitor C": [0.5, 0.6]
                }
            },
            "competitive_advantages": ["Best price-to-value ratio", "Superior UX/onboarding", "Flexible pricing", "Modern tech stack"],
            "threats": ["Competitor A's market dominance", "Competitor B's free tier", "New AI-native entrants"]
        }
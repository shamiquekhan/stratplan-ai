from typing import Dict, Any
from app.agents.base import BaseAgent
from datetime import datetime, timedelta


class ExecutionAgent(BaseAgent):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        plan = state.get("plan", {})
        strategy = state.get("strategy", {})
        
        try:
            # Create execution tracker from milestones
            milestones = strategy.get("milestones", [])
            execution_tracker = self._create_execution_tracker(milestones)
            
            # Create initial version snapshot
            version_snapshot = self._create_version_snapshot(state)
        except Exception:
            execution_tracker = []
            version_snapshot = {"version_number": 1, "snapshot": {}, "change_summary": "Initial plan generation", "created_at": datetime.now().isoformat()}
        
        return {
            **state,
            "execution_tracker": execution_tracker,
            "version_snapshot": version_snapshot,
            "current_agent": "execution"
        }
    
    def _create_execution_tracker(self, milestones: list) -> list:
        tracker = []
        for i, ms in enumerate(milestones):
            target_str = ms.get("target_date", "")
            try:
                target = datetime.fromisoformat(target_str.replace("Z", "+00:00"))
            except:
                target = datetime.now() + timedelta(days=30 * (i + 1))
            
            tracker.append({
                "milestone": ms.get("milestone", f"Milestone {i+1}"),
                "target_date": target,
                "status": "pending",
                "variance_days": 0,
                "notes": ms.get("success_criteria", ""),
                "dependencies": ms.get("dependencies", [])
            })
        return tracker
    
    def _create_version_snapshot(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "version_number": 1,
            "snapshot": {
                "plan": state.get("plan", {}),
                "generated_plan": state.get("generated_plan", ""),
                "financial_projections": state.get("financial_projections", {}),
                "market_analysis": state.get("market_analysis", {}),
                "competitor_analysis": state.get("competitor_analysis", {}),
                "strategy": state.get("strategy", {}),
                "execution_tracker": state.get("execution_tracker", []),
            },
            "change_summary": "Initial plan generation",
            "created_at": datetime.now().isoformat()
        }
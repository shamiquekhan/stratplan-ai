from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import asyncio

from app.agents.plan_generator import PlanGeneratorAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.market_research import MarketResearchAgent
from app.agents.competitor_agent import CompetitorAgent
from app.agents.strategy_agent import StrategyAgent
from app.agents.execution_agent import ExecutionAgent
from app.services.data_collectors import collect_market_data, collect_competitor_data


class PlanState(TypedDict):
    plan: Dict[str, Any]
    user_inputs: Dict[str, Any]
    generated_plan: str
    financial_projections: Dict[str, Any]
    market_analysis: Dict[str, Any]
    competitor_analysis: Dict[str, Any]
    strategy: Dict[str, Any]
    execution_tracker: list
    version_snapshot: Dict[str, Any]
    industry_benchmarks: Dict[str, Any]
    macro_indicators: Dict[str, Any]
    fred_data: Dict[str, Any]
    alpha_vantage_data: Dict[str, Any]
    competitor_scraped_data: Dict[str, Any]
    current_agent: str
    error: str


class PlanOrchestrator:
    def __init__(self):
        self.plan_generator = PlanGeneratorAgent()
        self.financial_agent = FinancialAgent()
        self.market_agent = MarketResearchAgent()
        self.competitor_agent = CompetitorAgent()
        self.strategy_agent = StrategyAgent()
        self.execution_agent = ExecutionAgent()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(PlanState)
        
        workflow.add_node("collect_data", self._collect_data)
        workflow.add_node("plan_generator", self._run_plan_generator)
        workflow.add_node("financial_agent", self._run_financial_agent)
        workflow.add_node("market_research", self._run_market_research)
        workflow.add_node("competitor_agent", self._run_competitor_agent)
        workflow.add_node("strategy_agent", self._run_strategy_agent)
        workflow.add_node("execution_agent", self._run_execution_agent)
        workflow.add_node("save_plan", self._save_plan)
        
        workflow.set_entry_point("collect_data")
        workflow.add_edge("collect_data", "plan_generator")
        workflow.add_edge("plan_generator", "financial_agent")
        workflow.add_edge("financial_agent", "market_research")
        workflow.add_edge("market_research", "competitor_agent")
        workflow.add_edge("competitor_agent", "strategy_agent")
        workflow.add_edge("strategy_agent", "execution_agent")
        workflow.add_edge("execution_agent", "save_plan")
        workflow.add_edge("save_plan", END)
        
        return workflow.compile(checkpointer=MemorySaver())
    
    async def _collect_data(self, state: PlanState) -> PlanState:
        plan = state.get("plan", {})
        industry = plan.get("industry", "")
        user_inputs = state.get("user_inputs", {})
        competitors = user_inputs.get("competitors", "")
        
        try:
            market_data = await asyncio.wait_for(collect_market_data(industry), timeout=30.0)
            state["industry_benchmarks"] = market_data.get("benchmarks", {})
            state["macro_indicators"] = market_data.get("macro", {})
            state["fred_data"] = market_data.get("fred", {})
            state["alpha_vantage_data"] = market_data.get("alpha_vantage", {})
            
            if competitors:
                competitor_data = await asyncio.wait_for(collect_competitor_data(competitors), timeout=30.0)
                state["competitor_scraped_data"] = competitor_data
        except Exception as e:
            state["error"] = f"Data collection error: {str(e)}"
        
        return state
    
    async def _run_plan_generator(self, state: PlanState) -> PlanState:
        try:
            return await asyncio.wait_for(self.plan_generator.execute(state), timeout=120.0)
        except Exception as e:
            state["error"] = f"Plan generator error: {str(e)}"
            return state
    
    async def _run_financial_agent(self, state: PlanState) -> PlanState:
        try:
            return await asyncio.wait_for(self.financial_agent.execute(state), timeout=120.0)
        except Exception as e:
            state["error"] = f"Financial agent error: {str(e)}"
            return state
    
    async def _run_market_research(self, state: PlanState) -> PlanState:
        try:
            return await asyncio.wait_for(self.market_agent.execute(state), timeout=120.0)
        except Exception as e:
            state["error"] = f"Market research error: {str(e)}"
            return state
    
    async def _run_competitor_agent(self, state: PlanState) -> PlanState:
        try:
            return await asyncio.wait_for(self.competitor_agent.execute(state), timeout=120.0)
        except Exception as e:
            state["error"] = f"Competitor agent error: {str(e)}"
            return state
    
    async def _run_strategy_agent(self, state: PlanState) -> PlanState:
        try:
            return await asyncio.wait_for(self.strategy_agent.execute(state), timeout=120.0)
        except Exception as e:
            state["error"] = f"Strategy agent error: {str(e)}"
            return state
    
    async def _run_execution_agent(self, state: PlanState) -> PlanState:
        try:
            return await asyncio.wait_for(self.execution_agent.execute(state), timeout=30.0)
        except Exception as e:
            state["error"] = f"Execution agent error: {str(e)}"
            return state
    
    async def _save_plan(self, state: PlanState) -> PlanState:
        return state
    
    async def generate_plan(self, plan: Dict[str, Any], user_inputs: Dict[str, Any], thread_id: str = "default") -> Dict[str, Any]:
        # Warm up the model before starting
        await self.plan_generator.warmup()
        
        initial_state: PlanState = {
            "plan": plan,
            "user_inputs": user_inputs,
            "generated_plan": "",
            "financial_projections": {},
            "market_analysis": {},
            "competitor_analysis": {},
            "strategy": {},
            "execution_tracker": [],
            "version_snapshot": {},
            "industry_benchmarks": {},
            "macro_indicators": {},
            "fred_data": {},
            "alpha_vantage_data": {},
            "competitor_scraped_data": {},
            "current_agent": "starting",
            "error": ""
        }
        
        config = {"configurable": {"thread_id": thread_id}}
        result = await self.graph.ainvoke(initial_state, config)
        return result


orchestrator = PlanOrchestrator()
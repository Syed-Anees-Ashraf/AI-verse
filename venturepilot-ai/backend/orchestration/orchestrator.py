import sys
import os
from typing import Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.startup_agent import analyze_startup
from agents.policy_agent import analyze_policy
from agents.investor_agent import match_investors
from agents.market_agent import analyze_market
from agents.news_agent import analyze_news
from agents.strategy_agent import synthesize_strategy


class Orchestrator:
    """
    Orchestrates the execution of all agents in strict order.
    
    Execution Order (DO NOT CHANGE):
    1. Startup Agent
    2. Policy Agent
    3. Investor Agent
    4. Market Agent
    5. News Agent
    6. Strategy Agent
    """
    
    def __init__(self, vector_store=None):
        """Initialize orchestrator with vector store."""
        self.vector_store = vector_store
        self.execution_log = []
    
    def _log(self, agent_name: str, status: str, duration_ms: int = 0):
        """Log agent execution."""
        self.execution_log.append({
            "agent": agent_name,
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "duration_ms": duration_ms
        })
        print(f"[Orchestrator] {agent_name}: {status} ({duration_ms}ms)")
    
    def run(self, startup_input: dict) -> dict:
        """
        Run full analysis pipeline.
        
        Input: Raw startup input
        Output: Complete analysis from all agents
        
        Final output structure:
        {
            "startup_profile": {...},
            "policy": {...},
            "investors": [...],
            "market": {...},
            "news": {...},
            "strategy": {...}
        }
        """
        self.execution_log = []
        results = {}
        
        # 1. Startup Agent
        start_time = datetime.now()
        try:
            self._log("startup_agent", "started")
            startup_profile = analyze_startup(startup_input)
            
            # Merge input data with analysis for complete profile
            startup_profile.update({
                "description": startup_input.get("description", ""),
                "domain": startup_input.get("domain", ""),
                "stage": startup_input.get("stage", ""),
                "geography": startup_input.get("geography", ""),
                "customer_type": startup_input.get("customer_type", "")
            })
            
            results["startup_profile"] = startup_profile
            duration = int((datetime.now() - start_time).total_seconds() * 1000)
            self._log("startup_agent", "completed", duration)
        except Exception as e:
            self._log("startup_agent", f"failed: {str(e)}")
            raise
        
        # 2. Policy Agent
        start_time = datetime.now()
        try:
            self._log("policy_agent", "started")
            results["policy"] = analyze_policy(
                startup_profile=results["startup_profile"],
                vector_store=self.vector_store
            )
            duration = int((datetime.now() - start_time).total_seconds() * 1000)
            self._log("policy_agent", "completed", duration)
        except Exception as e:
            self._log("policy_agent", f"failed: {str(e)}")
            results["policy"] = {"error": str(e)}
        
        # 3. Investor Agent
        start_time = datetime.now()
        try:
            self._log("investor_agent", "started")
            results["investors"] = match_investors(
                startup_profile=results["startup_profile"],
                vector_store=self.vector_store
            )
            duration = int((datetime.now() - start_time).total_seconds() * 1000)
            self._log("investor_agent", "completed", duration)
        except Exception as e:
            self._log("investor_agent", f"failed: {str(e)}")
            results["investors"] = []
        
        # 4. Market Agent
        start_time = datetime.now()
        try:
            self._log("market_agent", "started")
            results["market"] = analyze_market(
                startup_profile=results["startup_profile"],
                vector_store=self.vector_store
            )
            duration = int((datetime.now() - start_time).total_seconds() * 1000)
            self._log("market_agent", "completed", duration)
        except Exception as e:
            self._log("market_agent", f"failed: {str(e)}")
            results["market"] = {"error": str(e)}
        
        # 5. News Agent
        start_time = datetime.now()
        try:
            self._log("news_agent", "started")
            results["news"] = analyze_news(
                startup_profile=results["startup_profile"],
                vector_store=self.vector_store
            )
            duration = int((datetime.now() - start_time).total_seconds() * 1000)
            self._log("news_agent", "completed", duration)
        except Exception as e:
            self._log("news_agent", f"failed: {str(e)}")
            results["news"] = {"error": str(e)}
        
        # 6. Strategy Agent (NO retriever access)
        start_time = datetime.now()
        try:
            self._log("strategy_agent", "started")
            results["strategy"] = synthesize_strategy(
                startup_profile=results["startup_profile"],
                policy_analysis=results.get("policy", {}),
                investor_matches=results.get("investors", []),
                market_analysis=results.get("market", {}),
                news_analysis=results.get("news", {})
            )
            duration = int((datetime.now() - start_time).total_seconds() * 1000)
            self._log("strategy_agent", "completed", duration)
        except Exception as e:
            self._log("strategy_agent", f"failed: {str(e)}")
            results["strategy"] = {"error": str(e)}
        
        # Add execution metadata
        results["_metadata"] = {
            "execution_log": self.execution_log,
            "total_agents": 6,
            "completed_agents": sum(1 for log in self.execution_log if "completed" in log["status"])
        }
        
        return results


def run_full_analysis(startup_input: dict, vector_store=None) -> dict:
    """
    Convenience function to run full analysis.
    
    Args:
        startup_input: Raw startup input data
        vector_store: Optional VectorStore instance
    
    Returns:
        Complete analysis results
    """
    orchestrator = Orchestrator(vector_store=vector_store)
    return orchestrator.run(startup_input)

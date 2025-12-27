from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Any
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orchestration.orchestrator import Orchestrator

router = APIRouter()

def debug_log(title: str, data):
    """Print debug information to console."""
    print(f"\n{'='*60}")
    print(f"[BACKEND DEBUG] {title}")
    print(f"{'='*60}")
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2, default=str))
    else:
        print(data)
    print(f"{'='*60}\n")


class StartupProfile(BaseModel):
    """Startup profile input."""
    description: str
    domain: str
    stage: str
    geography: str
    customer_type: str
    problem: Optional[str] = None
    value_proposition: Optional[str] = None
    market_category: Optional[str] = None
    target_customers: Optional[str] = None
    assumed_competitors: Optional[List[str]] = None
    risk_factors: Optional[List[str]] = None


class DashboardResponse(BaseModel):
    """Full dashboard response."""
    startup_profile: dict
    policy: dict
    investors: List[dict]
    market: dict
    news: dict
    strategy: dict


@router.post("/dashboard")
async def get_dashboard(profile: StartupProfile):
    """
    Get full dashboard analysis for a startup.
    
    Input: Startup profile
    Output: Full orchestrated output from all agents
    """
    try:
        debug_log("DASHBOARD REQUEST RECEIVED", profile.dict())
        
        # Import here to avoid circular imports
        from main import get_vector_store
        
        vector_store = get_vector_store()
        orchestrator = Orchestrator(vector_store=vector_store)
        
        # Run full analysis
        debug_log("STARTING ORCHESTRATOR", "Running all 6 agents...")
        results = orchestrator.run(profile.dict())
        
        debug_log("ORCHESTRATOR COMPLETE - POLICY OUTPUT", results.get('policy', {}))
        debug_log("ORCHESTRATOR COMPLETE - INVESTORS OUTPUT", results.get('investors', []))
        debug_log("ORCHESTRATOR COMPLETE - MARKET OUTPUT", results.get('market', {}))
        debug_log("ORCHESTRATOR COMPLETE - NEWS OUTPUT", results.get('news', {}))
        debug_log("ORCHESTRATOR COMPLETE - STRATEGY OUTPUT", results.get('strategy', {}))
        
        return results
    
    except Exception as e:
        debug_log("DASHBOARD ERROR", str(e))
        raise HTTPException(status_code=500, detail=f"Dashboard analysis failed: {str(e)}")


@router.post("/dashboard/investors")
async def get_investors_only(profile: StartupProfile):
    """Get only investor matches for a startup."""
    try:
        from main import get_vector_store
        from agents.investor_agent import match_investors
        
        vector_store = get_vector_store()
        investors = match_investors(profile.dict(), vector_store=vector_store)
        
        return {"investors": investors}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Investor matching failed: {str(e)}")


@router.post("/dashboard/policy")
async def get_policy_only(profile: StartupProfile):
    """Get only policy analysis for a startup."""
    try:
        from main import get_vector_store
        from agents.policy_agent import analyze_policy
        
        vector_store = get_vector_store()
        policy = analyze_policy(profile.dict(), vector_store=vector_store)
        
        return {"policy": policy}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Policy analysis failed: {str(e)}")


@router.post("/dashboard/market")
async def get_market_only(profile: StartupProfile):
    """Get only market analysis for a startup."""
    try:
        from main import get_vector_store
        from agents.market_agent import analyze_market
        
        vector_store = get_vector_store()
        market = analyze_market(profile.dict(), vector_store=vector_store)
        
        return {"market": market}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Market analysis failed: {str(e)}")


@router.post("/dashboard/news")
async def get_news_only(profile: StartupProfile):
    """Get only news analysis for a startup."""
    try:
        from main import get_vector_store
        from agents.news_agent import analyze_news
        
        vector_store = get_vector_store()
        news = analyze_news(profile.dict(), vector_store=vector_store)
        
        return {"news": news}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"News analysis failed: {str(e)}")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.startup_agent import analyze_startup

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


class StartupInput(BaseModel):
    """Input schema for startup onboarding."""
    description: str
    domain: str
    stage: str
    geography: str
    customer_type: str


class StartupProfile(BaseModel):
    """Output schema for startup profile."""
    description: str
    domain: str
    stage: str
    geography: str
    customer_type: str
    problem: str
    value_proposition: str
    market_category: str
    target_customers: str
    assumed_competitors: list[str]
    risk_factors: list[str]


@router.post("/onboard", response_model=StartupProfile)
async def onboard_startup(input_data: StartupInput):
    """
    Onboard a new startup.
    
    Input: Raw startup input
    Output: Structured startup profile
    """
    try:
        debug_log("ONBOARDING REQUEST", input_data.dict())
        
        # Analyze the startup
        debug_log("CALLING STARTUP AGENT", "Analyzing with Mistral AI...")
        analysis = analyze_startup(input_data.dict())
        
        debug_log("STARTUP AGENT OUTPUT", analysis)
        
        # Combine input with analysis
        profile = {
            **input_data.dict(),
            **analysis
        }
        
        debug_log("FINAL PROFILE TO RETURN", profile)
        
        return profile
    
    except ValueError as e:
        debug_log("ONBOARDING VALIDATION ERROR", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        debug_log("ONBOARDING ERROR", str(e))
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/onboard/validate")
async def validate_startup_input(input_data: StartupInput):
    """
    Validate startup input without full analysis.
    """
    return {
        "valid": True,
        "message": "Input is valid",
        "input": input_data.dict()
    }

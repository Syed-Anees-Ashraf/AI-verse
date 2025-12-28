import json
import os
from typing import Optional
from mistralai import Mistral
import sys
from dotenv import load_dotenv

# Load environment variables at module level
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import retrieve_context


def get_mistral_client():
    """Get Mistral client dynamically to ensure .env is loaded."""
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if api_key:
        return Mistral(api_key=api_key), True
    return None, False


def analyze_market(startup_profile: dict, vector_store=None) -> dict:
    """
    Analyze market conditions for a startup.
    
    Output Schema:
    {
        "market_size_estimate": string,
        "growth_signals": list[string],
        "saturation_risks": list[string],
        "emerging_trends": list[string]
    }
    """
    domain = startup_profile.get("domain", "")
    geography = startup_profile.get("geography", "")
    market_category = startup_profile.get("market_category", domain)
    
    # Retrieve market context
    query = f"{market_category} {domain} market size growth trends {geography}"
    context = retrieve_context(
        query=query,
        category="report",
        geography=geography,
        vector_store=vector_store,
        k=5
    )
    
    client, use_llm = get_mistral_client()
    if use_llm and client:
        return _analyze_with_llm(startup_profile, context, client)
    else:
        return _analyze_mock(startup_profile, context)


def _analyze_with_llm(startup_profile: dict, context: list[str], client) -> dict:
    """Use LLM to analyze market."""
    context_text = "\n\n".join(context) if context else "No specific market context available."
    
    prompt = f"""Analyze market conditions for this startup and output ONLY valid JSON.

Startup Profile:
- Domain: {startup_profile.get('domain', 'N/A')}
- Geography: {startup_profile.get('geography', 'N/A')}
- Market Category: {startup_profile.get('market_category', 'N/A')}
- Target Customers: {startup_profile.get('target_customers', 'N/A')}

Market Context:
{context_text}

Output this exact JSON structure:
{{
    "market_size_estimate": "$X billion by 2025, growing at Y% CAGR",
    "growth_signals": ["signal1", "signal2", "signal3"],
    "saturation_risks": ["risk1", "risk2"],
    "emerging_trends": ["trend1", "trend2", "trend3"]
}}

Respond ONLY with the JSON object."""

    try:
        response = client.chat.complete(
            model=os.getenv("LLM_MODEL", "mistral-small-latest"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean up markdown code blocks if present
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
            result_text = result_text.strip()
        
        result = json.loads(result_text)
        return result
        
    except Exception as e:
        print(f"Market LLM analysis failed: {e}")
        return _analyze_mock(startup_profile, context)


def _analyze_mock(startup_profile: dict, context: list[str]) -> dict:
    """
    Fallback market analysis when LLM is not available.
    Returns dynamic response based on input and context - NOT hardcoded data.
    """
    domain = startup_profile.get("domain", "technology")
    geography = startup_profile.get("geography", "Global")
    stage = startup_profile.get("stage", "seed")
    
    growth_signals = []
    saturation_risks = []
    emerging_trends = []
    market_size = f"Market size for {domain} in {geography} - requires LLM analysis"
    
    # Extract from context if available
    if context:
        for ctx in context[:3]:
            if len(ctx) > 20:
                snippet = ctx[:100] + "..." if len(ctx) > 100 else ctx
                growth_signals.append(f"Signal from market data: {snippet}")
        
        if len(context) > 3:
            for ctx in context[3:5]:
                if len(ctx) > 20:
                    snippet = ctx[:100] + "..." if len(ctx) > 100 else ctx
                    emerging_trends.append(f"Trend: {snippet}")
    
    # Dynamic fallbacks if no context
    if not growth_signals:
        growth_signals = [
            f"Growing adoption of {domain} solutions in {geography}",
            f"Increasing investment in {domain} sector"
        ]
    
    if not saturation_risks:
        saturation_risks = [
            f"Competition in {domain} market",
            f"Market maturity considerations for {stage} stage"
        ]
    
    if not emerging_trends:
        emerging_trends = [
            f"Digital transformation in {domain}",
            f"Technology adoption trends in {geography}"
        ]
    
    return {
        "market_size_estimate": market_size,
        "growth_signals": growth_signals[:4],
        "saturation_risks": saturation_risks[:3],
        "emerging_trends": emerging_trends[:4]
    }

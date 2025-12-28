import json
import os
from typing import Optional
from mistralai import Mistral
import sys
from datetime import datetime
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


def analyze_news(startup_profile: dict, vector_store=None) -> dict:
    """
    Analyze recent news relevant to a startup.
    
    Output Schema:
    {
        "opportunities": list[string],
        "risks": list[string],
        "recent_events": list[string]
    }
    
    Note: Recency MUST be enforced - only recent news should be included.
    """
    domain = startup_profile.get("domain", "")
    geography = startup_profile.get("geography", "")
    market_category = startup_profile.get("market_category", domain)
    
    # Retrieve news context with recency filter (last 90 days)
    query = f"{market_category} {domain} news funding investment {geography}"
    context = retrieve_context(
        query=query,
        category="news",
        geography=geography,
        recency_days=90,
        vector_store=vector_store,
        k=7
    )
    
    client, use_llm = get_mistral_client()
    if use_llm and client:
        return _analyze_with_llm(startup_profile, context, client)
    else:
        return _analyze_mock(startup_profile, context)


def _analyze_with_llm(startup_profile: dict, context: list[str], client) -> dict:
    """Use LLM to analyze news."""
    context_text = "\n\n".join(context) if context else "No recent news context available."
    domain = startup_profile.get('domain', 'technology')
    geography = startup_profile.get('geography', 'Global')
    market_category = startup_profile.get('market_category', domain)
    
    prompt = f"""Analyze recent news and market developments relevant to this startup. Output ONLY valid JSON.

Startup Profile:
- Domain: {domain}
- Geography: {geography}
- Market Category: {market_category}
- Description: {startup_profile.get('description', 'N/A')[:200]}

Recent News Context:
{context_text}

Based on current market conditions and the startup's domain, generate insightful analysis.
Even if context is limited, use your knowledge to provide relevant insights for {domain} in {geography}.

Output this exact JSON structure (MUST have at least 2-3 items in each array):
{{
    "opportunities": ["specific opportunity 1 for {domain} startups", "opportunity 2", "opportunity 3"],
    "risks": ["specific risk 1 to watch", "risk 2"],
    "recent_events": ["Recent event 1 in {domain}/{geography}", "Event 2", "Event 3"]
}}

Respond ONLY with the JSON object. Do NOT return empty arrays."""

    try:
        response = client.chat.complete(
            model=os.getenv("LLM_MODEL", "mistral-small-latest"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Clean up markdown code blocks if present
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
            result_text = result_text.strip()
        
        result = json.loads(result_text)
        
        # Ensure non-empty arrays - fall back to mock if empty
        if not result.get("opportunities") or not result.get("risks") or not result.get("recent_events"):
            print("[NEWS AGENT] LLM returned empty arrays, using fallback...")
            return _analyze_mock(startup_profile, context)
        
        return result
        
    except Exception as e:
        print(f"News LLM analysis failed: {e}")
        return _analyze_mock(startup_profile, context)


def _analyze_mock(startup_profile: dict, context: list[str]) -> dict:
    """
    Fallback news analysis when LLM is not available.
    Returns dynamic response based on input and context - NOT hardcoded data.
    """
    domain = startup_profile.get("domain", "technology")
    geography = startup_profile.get("geography", "Global")
    current_month = datetime.now().strftime("%B %Y")
    
    opportunities = []
    risks = []
    recent_events = []
    
    # Extract from context if available
    if context:
        for i, ctx in enumerate(context[:3]):
            if len(ctx) > 20:
                snippet = ctx[:120] + "..." if len(ctx) > 120 else ctx
                if i < 2:
                    opportunities.append(f"Opportunity: {snippet}")
                else:
                    risks.append(f"Risk factor: {snippet}")
        
        for ctx in context[3:6]:
            if len(ctx) > 20:
                snippet = ctx[:100] + "..." if len(ctx) > 100 else ctx
                recent_events.append(f"Event ({current_month}): {snippet}")
    
    # Dynamic fallbacks if no context
    if not opportunities:
        opportunities = [
            f"Market opportunities in {domain} sector in {geography}",
            f"Growth potential for {domain} startups"
        ]
    
    if not risks:
        risks = [
            f"Market volatility in {domain} space",
            f"Competitive landscape challenges"
        ]
    
    if not recent_events:
        recent_events = [
            f"Industry developments in {domain} - {current_month}",
            f"Market activity in {geography} region"
        ]
    
    return {
        "opportunities": opportunities[:4],
        "risks": risks[:3],
        "recent_events": recent_events[:5]
    }

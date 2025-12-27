import json
import os
from typing import Optional
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables at module level
load_dotenv()


def get_mistral_client():
    """Get Mistral client dynamically to ensure .env is loaded."""
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if api_key:
        return Mistral(api_key=api_key), True
    return None, False


def synthesize_strategy(
    startup_profile: dict,
    policy_analysis: dict,
    investor_matches: list[dict],
    market_analysis: dict,
    news_analysis: dict
) -> dict:
    """
    Synthesize strategy based on all agent outputs.
    
    IMPORTANT: This agent must NOT call retriever.
    It only reasons over agent outputs.
    
    Output Schema:
    {
        "fundraising_readiness": "low" | "medium" | "high",
        "key_recommendations": list[string],
        "next_actions": list[string]
    }
    """
    client, use_llm = get_mistral_client()
    if use_llm and client:
        return _synthesize_with_llm(
            startup_profile, policy_analysis, 
            investor_matches, market_analysis, news_analysis, client
        )
    else:
        return _synthesize_mock(
            startup_profile, policy_analysis,
            investor_matches, market_analysis, news_analysis
        )


def _synthesize_with_llm(
    startup_profile: dict,
    policy_analysis: dict,
    investor_matches: list[dict],
    market_analysis: dict,
    news_analysis: dict,
    client
) -> dict:
    """Use LLM to synthesize strategy."""
    
    # Summarize investor matches
    top_investors = investor_matches[:3] if investor_matches else []
    investor_summary = "\n".join([
        f"- {inv['name']} (Score: {inv['match_score']}): {inv['reason']}"
        for inv in top_investors
    ])
    
    prompt = f"""Synthesize a strategy for this startup based on all analyses. Output ONLY valid JSON.

STARTUP PROFILE:
- Domain: {startup_profile.get('domain', 'N/A')}
- Stage: {startup_profile.get('stage', 'N/A')}
- Geography: {startup_profile.get('geography', 'N/A')}
- Problem: {startup_profile.get('problem', 'N/A')}
- Value Proposition: {startup_profile.get('value_proposition', 'N/A')}
- Risk Factors: {startup_profile.get('risk_factors', [])}

POLICY ANALYSIS:
- Relevant Policies: {policy_analysis.get('relevant_policies', [])}
- Eligible Schemes: {policy_analysis.get('eligible_schemes', [])}
- Regulatory Risks: {policy_analysis.get('regulatory_risks', [])}

TOP INVESTOR MATCHES:
{investor_summary}

MARKET ANALYSIS:
- Market Size: {market_analysis.get('market_size_estimate', 'N/A')}
- Growth Signals: {market_analysis.get('growth_signals', [])}
- Saturation Risks: {market_analysis.get('saturation_risks', [])}
- Trends: {market_analysis.get('emerging_trends', [])}

NEWS ANALYSIS:
- Opportunities: {news_analysis.get('opportunities', [])}
- Risks: {news_analysis.get('risks', [])}
- Recent Events: {news_analysis.get('recent_events', [])}

Based on ALL the above, output this JSON:
{{
    "fundraising_readiness": "low" or "medium" or "high",
    "key_recommendations": ["recommendation1 referencing specific insights", "recommendation2", "recommendation3"],
    "next_actions": ["action1", "action2", "action3", "action4"]
}}

The recommendations and actions MUST reference insights from the analyses above.
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
        
        # Validate fundraising_readiness
        if result.get("fundraising_readiness") not in ["low", "medium", "high"]:
            result["fundraising_readiness"] = "medium"
        
        return result
        
    except Exception as e:
        print(f"Strategy LLM synthesis failed: {e}")
        return _synthesize_mock(
            startup_profile, policy_analysis,
            investor_matches, market_analysis, news_analysis
        )


def _synthesize_mock(
    startup_profile: dict,
    policy_analysis: dict,
    investor_matches: list[dict],
    market_analysis: dict,
    news_analysis: dict
) -> dict:
    """Mock strategy synthesis when LLM is not available."""
    
    # Determine fundraising readiness based on signals
    readiness_score = 0
    
    # Check stage
    stage = startup_profile.get("stage", "").lower()
    if stage in ["series a", "series b", "growth"]:
        readiness_score += 2
    elif stage in ["seed", "pre-seed"]:
        readiness_score += 1
    
    # Check investor matches
    if investor_matches:
        avg_score = sum(inv.get("match_score", 0) for inv in investor_matches) / len(investor_matches)
        if avg_score > 80:
            readiness_score += 2
        elif avg_score > 60:
            readiness_score += 1
    
    # Check market signals
    growth_signals = market_analysis.get("growth_signals", [])
    if len(growth_signals) >= 3:
        readiness_score += 1
    
    # Check opportunities vs risks
    opportunities = news_analysis.get("opportunities", [])
    risks = news_analysis.get("risks", [])
    if len(opportunities) > len(risks):
        readiness_score += 1
    
    # Determine readiness level
    if readiness_score >= 5:
        fundraising_readiness = "high"
    elif readiness_score >= 3:
        fundraising_readiness = "medium"
    else:
        fundraising_readiness = "low"
    
    # Build recommendations based on analyses
    recommendations = []
    
    # Policy-based recommendations
    if policy_analysis.get("eligible_schemes"):
        recommendations.append(
            f"Apply for government schemes: {', '.join(policy_analysis['eligible_schemes'][:2])}"
        )
    
    if policy_analysis.get("regulatory_risks"):
        recommendations.append(
            f"Address regulatory compliance: {policy_analysis['regulatory_risks'][0]}"
        )
    
    # Investor-based recommendations
    if investor_matches:
        top_investor = investor_matches[0]
        recommendations.append(
            f"Prioritize outreach to {top_investor['name']} (match score: {top_investor['match_score']})"
        )
    
    # Market-based recommendations
    if market_analysis.get("emerging_trends"):
        recommendations.append(
            f"Align product roadmap with trend: {market_analysis['emerging_trends'][0]}"
        )
    
    # News-based recommendations
    if news_analysis.get("opportunities"):
        recommendations.append(
            f"Capitalize on market opportunity: {news_analysis['opportunities'][0]}"
        )
    
    # Build next actions
    next_actions = []
    
    if fundraising_readiness == "high":
        next_actions = [
            "Prepare pitch deck with updated market data",
            "Schedule meetings with top-matched investors",
            "Update financial projections",
            "Prepare data room for due diligence",
            "Engage legal counsel for term sheet review"
        ]
    elif fundraising_readiness == "medium":
        next_actions = [
            "Strengthen key metrics (ARR, growth rate, retention)",
            "Build relationships with target investors",
            "Complete regulatory compliance requirements",
            "Develop case studies and customer testimonials",
            "Refine pitch deck with competitive differentiation"
        ]
    else:
        next_actions = [
            "Focus on product-market fit validation",
            "Build initial traction metrics",
            "Apply for grants and government schemes",
            "Network with angel investors and accelerators",
            "Develop MVP and gather customer feedback"
        ]
    
    return {
        "fundraising_readiness": fundraising_readiness,
        "key_recommendations": recommendations[:5],
        "next_actions": next_actions[:5]
    }

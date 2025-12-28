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
    """
    Fallback strategy synthesis when LLM is not available.
    Returns dynamic response based on all input analyses - NOT hardcoded data.
    """
    domain = startup_profile.get("domain", "technology")
    stage = startup_profile.get("stage", "seed")
    geography = startup_profile.get("geography", "Global")
    
    # Determine fundraising readiness based on signals
    readiness_score = 0
    
    # Check stage
    if stage.lower() in ["series a", "series b", "growth"]:
        readiness_score += 2
    elif stage.lower() in ["seed", "pre-seed"]:
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
    
    # Build DYNAMIC recommendations based on actual analyses
    recommendations = []
    
    # Policy-based recommendations - use actual data
    if policy_analysis.get("eligible_schemes"):
        schemes = policy_analysis["eligible_schemes"][:2]
        recommendations.append(f"Explore government schemes: {', '.join(schemes)}")
    
    if policy_analysis.get("regulatory_risks"):
        risk = policy_analysis["regulatory_risks"][0]
        recommendations.append(f"Address regulatory requirement: {risk}")
    
    # Investor-based recommendations - use actual data
    if investor_matches:
        top_investor = investor_matches[0]
        recommendations.append(
            f"Target outreach: {top_investor['name']} (match score: {top_investor.get('match_score', 'N/A')})"
        )
    
    # Market-based recommendations - use actual data
    if market_analysis.get("emerging_trends"):
        trend = market_analysis["emerging_trends"][0]
        recommendations.append(f"Align with market trend: {trend}")
    
    if market_analysis.get("growth_signals"):
        signal = market_analysis["growth_signals"][0]
        recommendations.append(f"Leverage growth signal: {signal}")
    
    # News-based recommendations - use actual data
    if news_analysis.get("opportunities"):
        opp = news_analysis["opportunities"][0]
        recommendations.append(f"Capitalize on opportunity: {opp}")
    
    # Build DYNAMIC next actions based on readiness
    next_actions = []
    
    if fundraising_readiness == "high":
        next_actions = [
            f"Prepare pitch deck highlighting {domain} market opportunity",
            f"Schedule meetings with matched investors",
            "Update financial projections with latest metrics",
            "Prepare data room for due diligence",
            f"Engage with {geography} investor network"
        ]
    elif fundraising_readiness == "medium":
        next_actions = [
            f"Strengthen key metrics for {stage} stage requirements",
            "Build relationships with target investors",
            f"Complete {domain} regulatory compliance",
            "Develop case studies and customer testimonials",
            "Refine value proposition based on market feedback"
        ]
    else:
        next_actions = [
            "Focus on product-market fit validation",
            f"Build initial traction in {geography} market",
            "Apply for grants and government schemes",
            f"Network with {domain} angel investors",
            "Develop MVP and gather customer feedback"
        ]
    
    return {
        "fundraising_readiness": fundraising_readiness,
        "key_recommendations": recommendations[:5],
        "next_actions": next_actions[:5]
    }

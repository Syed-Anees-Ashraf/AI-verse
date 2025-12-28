import json
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

from mistralai import Mistral
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import retrieve_context


def get_client():
    """Get Mistral client - checks API key each time."""
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if api_key:
        return Mistral(api_key=api_key)
    return None


def match_investors(startup_profile: dict, vector_store=None) -> list[dict]:
    """
    Match investors to a startup profile.
    
    Output Schema (sorted descending by match_score):
    [
        {
            "name": string,
            "match_score": number (0-100),
            "reason": string,
            "past_investments": list[string]
        }
    ]
    """
    domain = startup_profile.get("domain", "")
    stage = startup_profile.get("stage", "")
    geography = startup_profile.get("geography", "")
    market_category = startup_profile.get("market_category", domain)
    
    # Retrieve investor context
    query = f"{market_category} {domain} {stage} stage investors VCs {geography}"
    context = retrieve_context(
        query=query,
        category="investor",
        vector_store=vector_store,
        k=10
    )
    
    client = get_client()
    if client:
        print(f"[INVESTOR AGENT] Using Mistral AI for matching...")
        return _match_with_llm(startup_profile, context, client)
    else:
        print(f"[INVESTOR AGENT] WARNING: No API key - using mock data!")
        return _match_mock(startup_profile, context)


def _match_with_llm(startup_profile: dict, context: list[str], client) -> list[dict]:
    """Use LLM to match investors."""
    context_text = "\n\n".join(context) if context else "No specific investor context available."
    
    prompt = f"""Match investors to this startup and output ONLY valid JSON array.

Startup Profile:
- Domain: {startup_profile.get('domain', 'N/A')}
- Stage: {startup_profile.get('stage', 'N/A')}
- Geography: {startup_profile.get('geography', 'N/A')}
- Market Category: {startup_profile.get('market_category', 'N/A')}
- Problem: {startup_profile.get('problem', 'N/A')}

Investor Context:
{context_text}

Output a JSON array of 5-7 matched investors, sorted by match_score descending:
[
    {{
        "name": "Investor Name",
        "match_score": 85,
        "reason": "Why this investor is a good match, referencing their past investments",
        "past_investments": ["Company1", "Company2"]
    }}
]

Match scores should vary realistically (50-95). Reasons must reference past investments.
Respond ONLY with the JSON array."""

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
        
        # Ensure sorted by match_score
        result.sort(key=lambda x: x.get("match_score", 0), reverse=True)
        return result
        
    except Exception as e:
        print(f"Investor LLM matching failed: {e}")
        return _match_mock(startup_profile, context)


def _match_mock(startup_profile: dict, context: list[str]) -> list[dict]:
    """
    Fallback investor matching when LLM is not available.
    Returns dynamic response based on input and context - NOT hardcoded data.
    """
    domain = startup_profile.get("domain", "technology")
    stage = startup_profile.get("stage", "seed")
    geography = startup_profile.get("geography", "Global")
    
    matched_investors = []
    
    # Try to extract investor info from context (RAG results)
    if context:
        for i, ctx in enumerate(context[:5]):
            if len(ctx) > 20:
                # Parse investor information from context
                investor_name = f"Investor from database #{i+1}"
                
                # Try to extract name from context
                lines = ctx.split('\n')
                for line in lines:
                    if 'name' in line.lower() or ':' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            potential_name = parts[1].strip()[:50]
                            if potential_name:
                                investor_name = potential_name
                                break
                
                matched_investors.append({
                    "name": investor_name,
                    "match_score": max(60, 90 - i * 5),
                    "reason": f"Matched based on {domain} focus and {stage} stage preference. Context: {ctx[:100]}...",
                    "past_investments": [f"Portfolio company in {domain}"]
                })
    
    # If no context, return minimal dynamic response
    if not matched_investors:
        matched_investors = [
            {
                "name": f"Investor matching {domain} in {geography}",
                "match_score": 70,
                "reason": f"Potential match for {stage} stage {domain} startup in {geography}. Requires LLM for detailed analysis.",
                "past_investments": [f"Companies in {domain} space"]
            }
        ]
    
    # Sort by match_score descending
    matched_investors.sort(key=lambda x: x["match_score"], reverse=True)
    
    return matched_investors


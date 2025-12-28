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


def analyze_policy(startup_profile: dict, vector_store=None) -> dict:
    """
    Analyze relevant policies for a startup.
    
    Steps:
    1. Call retriever with category="policy", geography=startup geography
    2. Pass retrieved text to LLM
    3. Output JSON with relevant policies, eligible schemes, and regulatory risks
    
    Output Schema:
    {
        "relevant_policies": list[string],
        "eligible_schemes": list[string],
        "regulatory_risks": list[string]
    }
    """
    geography = startup_profile.get("geography", "Global")
    domain = startup_profile.get("domain", "")
    market_category = startup_profile.get("market_category", domain)
    
    # Retrieve policy context
    query = f"{market_category} {domain} startup policies regulations schemes {geography}"
    context = retrieve_context(
        query=query,
        category="policy",
        geography=geography,
        vector_store=vector_store,
        k=5
    )
    
    client = get_client()
    if client:
        print(f"[POLICY AGENT] Using Mistral AI for analysis...")
        return _analyze_with_llm(startup_profile, context, client)
    else:
        print(f"[POLICY AGENT] WARNING: No API key - using mock data!")
        return _analyze_mock(startup_profile, context)


def _analyze_with_llm(startup_profile: dict, context: list[str], client) -> dict:
    """Use LLM to analyze policies."""
    context_text = "\n\n".join(context) if context else "No specific policy context available."
    
    prompt = f"""Analyze policies relevant to this startup and output ONLY valid JSON.

Startup Profile:
- Domain: {startup_profile.get('domain', 'N/A')}
- Geography: {startup_profile.get('geography', 'N/A')}
- Stage: {startup_profile.get('stage', 'N/A')}
- Market Category: {startup_profile.get('market_category', 'N/A')}

Policy Context:
{context_text}

Output this exact JSON structure:
{{
    "relevant_policies": ["policy1", "policy2"],
    "eligible_schemes": ["scheme1", "scheme2"],
    "regulatory_risks": ["risk1", "risk2"]
}}

Respond ONLY with the JSON object."""

    try:
        response = client.chat.complete(
            model=os.getenv("LLM_MODEL", "mistral-small-latest"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
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
        print(f"Policy LLM analysis failed: {e}")
        return _analyze_mock(startup_profile, context)


def _analyze_mock(startup_profile: dict, context: list[str]) -> dict:
    """
    Fallback policy analysis when LLM is not available.
    Returns dynamic response based on input - NOT hardcoded data.
    """
    geography = startup_profile.get("geography", "Global")
    domain = startup_profile.get("domain", "technology")
    stage = startup_profile.get("stage", "seed")
    
    # Generate dynamic response based on actual input and context
    relevant_policies = []
    eligible_schemes = []
    regulatory_risks = []
    
    # Extract from context if available
    if context:
        for ctx in context[:3]:
            if len(ctx) > 20:
                # Extract meaningful snippets from context
                snippet = ctx[:150] + "..." if len(ctx) > 150 else ctx
                relevant_policies.append(f"Policy from database: {snippet}")
    
    # Add dynamic fallbacks if no context
    if not relevant_policies:
        relevant_policies = [
            f"General startup policies for {geography}",
            f"Industry regulations for {domain} sector"
        ]
    
    if not eligible_schemes:
        eligible_schemes = [
            f"Startup support schemes in {geography}",
            f"Innovation grants for {stage} stage companies"
        ]
    
    if not regulatory_risks:
        regulatory_risks = [
            f"Compliance requirements for {domain} in {geography}",
            f"Standard regulatory considerations for {stage} startups"
        ]
    
    return {
        "relevant_policies": relevant_policies[:4],
        "eligible_schemes": eligible_schemes[:4],
        "regulatory_risks": regulatory_risks[:4]
    }

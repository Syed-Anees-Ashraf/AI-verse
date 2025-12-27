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
    """Mock policy analysis when LLM is not available."""
    geography = startup_profile.get("geography", "Global")
    domain = startup_profile.get("domain", "technology").lower()
    
    # Geography-specific policies
    geography_policies = {
        "India": {
            "policies": [
                "Startup India Policy",
                "Digital India Initiative",
                "Make in India Program",
                "MSME Development Act"
            ],
            "schemes": [
                "Startup India Seed Fund Scheme",
                "Fund of Funds for Startups",
                "Credit Guarantee Scheme for Startups",
                "Tax Exemption under Section 80-IAC"
            ],
            "risks": [
                "GST compliance requirements",
                "FDI restrictions in certain sectors",
                "Data localization requirements"
            ]
        },
        "USA": {
            "policies": [
                "Small Business Administration (SBA) Programs",
                "JOBS Act for Crowdfunding",
                "Qualified Small Business Stock (QSBS) Benefits"
            ],
            "schemes": [
                "SBA Loans",
                "SBIR/STTR Grants",
                "R&D Tax Credits"
            ],
            "risks": [
                "SEC compliance for fundraising",
                "State-specific regulations",
                "Export control regulations"
            ]
        },
        "UK": {
            "policies": [
                "Enterprise Investment Scheme (EIS)",
                "Seed Enterprise Investment Scheme (SEIS)",
                "UK Innovation Strategy"
            ],
            "schemes": [
                "Innovate UK Grants",
                "R&D Tax Relief",
                "Patent Box Scheme"
            ],
            "risks": [
                "Post-Brexit regulatory changes",
                "GDPR compliance",
                "Financial services authorization"
            ]
        }
    }
    
    # Domain-specific regulatory considerations
    domain_regulations = {
        "fintech": {
            "risks": ["RBI/Financial regulatory compliance", "KYC/AML requirements", "Payment gateway licenses"]
        },
        "healthtech": {
            "risks": ["Medical device regulations", "Patient data privacy", "Clinical trial approvals"]
        },
        "edtech": {
            "risks": ["Educational institution recognition", "Content regulations", "Child data protection"]
        }
    }
    
    # Get geography-specific info or default
    geo_info = geography_policies.get(geography, {
        "policies": ["General Business Registration", "Tax Compliance Framework"],
        "schemes": ["General SME Support Programs", "Innovation Grants"],
        "risks": ["Local regulatory compliance", "Tax obligations"]
    })
    
    # Add domain-specific risks
    domain_risks = domain_regulations.get(domain, {}).get("risks", [])
    all_risks = geo_info.get("risks", []) + domain_risks
    
    # Use context to enrich if available
    if context:
        # Extract any mentioned policies from context
        for ctx in context[:2]:
            if "scheme" in ctx.lower() or "policy" in ctx.lower():
                geo_info["policies"].append(f"From context: {ctx[:100]}...")
                break
    
    return {
        "relevant_policies": geo_info.get("policies", [])[:4],
        "eligible_schemes": geo_info.get("schemes", [])[:4],
        "regulatory_risks": list(set(all_risks))[:4]
    }

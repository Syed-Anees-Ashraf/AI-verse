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
    """Mock market analysis when LLM is not available."""
    domain = startup_profile.get("domain", "technology").lower()
    geography = startup_profile.get("geography", "Global")
    
    # Domain-specific market data
    market_data = {
        "fintech": {
            "market_size": "$310 billion globally by 2026, growing at 25% CAGR",
            "growth_signals": [
                "Increasing digital payment adoption post-pandemic",
                "Government push for financial inclusion",
                "Rise of embedded finance",
                "Growing smartphone penetration"
            ],
            "saturation_risks": [
                "Intense competition from established players",
                "Regulatory tightening on digital lending",
                "Customer acquisition costs rising"
            ],
            "trends": [
                "Buy Now Pay Later (BNPL) expansion",
                "AI-powered credit scoring",
                "Blockchain in cross-border payments",
                "Open banking APIs"
            ]
        },
        "healthtech": {
            "market_size": "$660 billion globally by 2027, growing at 18% CAGR",
            "growth_signals": [
                "Telehealth adoption acceleration",
                "AI in diagnostics gaining traction",
                "Wearable health devices boom",
                "Mental health awareness increasing"
            ],
            "saturation_risks": [
                "Hospital integration challenges",
                "Patient data privacy concerns",
                "Insurance reimbursement complexities"
            ],
            "trends": [
                "Remote patient monitoring",
                "AI-assisted diagnostics",
                "Personalized medicine",
                "Digital therapeutics"
            ]
        },
        "saas": {
            "market_size": "$720 billion globally by 2028, growing at 18% CAGR",
            "growth_signals": [
                "Enterprise digital transformation",
                "Remote work tool adoption",
                "Vertical SaaS gaining momentum",
                "AI integration in workflows"
            ],
            "saturation_risks": [
                "Feature commoditization",
                "High customer acquisition costs",
                "Churn from economic downturn"
            ],
            "trends": [
                "AI-first product design",
                "Product-led growth strategies",
                "Vertical-specific solutions",
                "Usage-based pricing models"
            ]
        },
        "ai": {
            "market_size": "$1.8 trillion globally by 2030, growing at 37% CAGR",
            "growth_signals": [
                "Generative AI breakthrough adoption",
                "Enterprise AI implementation surge",
                "AI infrastructure investments",
                "AI talent availability improving"
            ],
            "saturation_risks": [
                "Compute cost pressures",
                "Regulatory uncertainty",
                "Model differentiation challenges"
            ],
            "trends": [
                "Large Language Models (LLMs)",
                "AI agents and automation",
                "Edge AI deployment",
                "Responsible AI frameworks"
            ]
        },
        "edtech": {
            "market_size": "$400 billion globally by 2028, growing at 16% CAGR",
            "growth_signals": [
                "Online learning normalization",
                "Corporate upskilling demand",
                "K-12 digital adoption",
                "AI tutoring effectiveness"
            ],
            "saturation_risks": [
                "Completion rate challenges",
                "Content quality differentiation",
                "Free content competition"
            ],
            "trends": [
                "AI personalized learning paths",
                "Micro-credentials and badges",
                "VR/AR immersive learning",
                "Cohort-based courses"
            ]
        },
        "ecommerce": {
            "market_size": "$7.5 trillion globally by 2027, growing at 10% CAGR",
            "growth_signals": [
                "D2C brand proliferation",
                "Social commerce growth",
                "Quick commerce expansion",
                "Cross-border e-commerce"
            ],
            "saturation_risks": [
                "Delivery cost pressures",
                "Return rate management",
                "Customer loyalty challenges"
            ],
            "trends": [
                "Live commerce",
                "Voice commerce",
                "Sustainable/ethical shopping",
                "AI-powered personalization"
            ]
        }
    }
    
    # Get domain-specific data or default
    domain_info = market_data.get(domain, {
        "market_size": f"${50 + hash(domain) % 200} billion by 2028, growing at {15 + hash(domain) % 15}% CAGR",
        "growth_signals": [
            "Digital transformation adoption",
            "Increasing technology investments",
            "Favorable regulatory environment"
        ],
        "saturation_risks": [
            "Competition from incumbents",
            "Economic uncertainty impact"
        ],
        "trends": [
            "AI integration",
            "Mobile-first solutions",
            "Data-driven decision making"
        ]
    })
    
    # Adjust for geography
    if geography == "India":
        domain_info["growth_signals"].append("India's digital economy growth")
        domain_info["market_size"] = domain_info["market_size"].replace("globally", "in India")
    
    return {
        "market_size_estimate": domain_info["market_size"],
        "growth_signals": domain_info["growth_signals"][:4],
        "saturation_risks": domain_info["saturation_risks"][:3],
        "emerging_trends": domain_info["trends"][:4]
    }

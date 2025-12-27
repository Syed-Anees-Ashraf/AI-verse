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
    
    prompt = f"""Analyze recent news relevant to this startup and output ONLY valid JSON.

Startup Profile:
- Domain: {startup_profile.get('domain', 'N/A')}
- Geography: {startup_profile.get('geography', 'N/A')}
- Market Category: {startup_profile.get('market_category', 'N/A')}

Recent News Context:
{context_text}

Output this exact JSON structure with insights from RECENT news only:
{{
    "opportunities": ["opportunity1 based on recent news", "opportunity2"],
    "risks": ["risk1 from recent events", "risk2"],
    "recent_events": ["Event 1 summary", "Event 2 summary", "Event 3 summary"]
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
        print(f"News LLM analysis failed: {e}")
        return _analyze_mock(startup_profile, context)


def _analyze_mock(startup_profile: dict, context: list[str]) -> dict:
    """Mock news analysis when LLM is not available."""
    domain = startup_profile.get("domain", "technology").lower()
    geography = startup_profile.get("geography", "Global")
    current_month = datetime.now().strftime("%B %Y")
    
    # Domain-specific news
    news_data = {
        "fintech": {
            "opportunities": [
                "RBI's push for digital payments creating new opportunities",
                "UPI international expansion opening cross-border payment market",
                "Account aggregator framework enabling new credit products",
                "Growing demand for embedded finance solutions"
            ],
            "risks": [
                "Increased regulatory scrutiny on digital lending apps",
                "Rising concerns about data privacy in financial services",
                "Competition from traditional banks launching digital products"
            ],
            "events": [
                f"Major fintech company raises $200M Series D in {current_month}",
                "New RBI guidelines on digital lending announced",
                "Government launches digital rupee pilot program",
                "Leading payment company reports 10B monthly transactions"
            ]
        },
        "healthtech": {
            "opportunities": [
                "Post-pandemic acceptance of telemedicine creates lasting demand",
                "Government healthcare digitization initiatives",
                "AI in diagnostics receiving regulatory fast-tracks",
                "Corporate wellness programs expanding rapidly"
            ],
            "risks": [
                "Healthcare data breach incidents increasing scrutiny",
                "Insurance integration challenges for digital health",
                "Clinical validation requirements tightening"
            ],
            "events": [
                f"Healthtech unicorn IPO announced in {current_month}",
                "New telemedicine guidelines released",
                "AI diagnostic tool receives FDA approval",
                "Major hospital chain partners with health-tech startup"
            ]
        },
        "saas": {
            "opportunities": [
                "Enterprise AI adoption driving SaaS growth",
                "SMB digital transformation accelerating",
                "Indian SaaS companies gaining global traction",
                "Product-led growth strategies proving effective"
            ],
            "risks": [
                "Economic slowdown affecting enterprise IT budgets",
                "Increasing competition in core SaaS categories",
                "AI disruption threatening existing SaaS models"
            ],
            "events": [
                f"Indian SaaS company valued at $1B in {current_month}",
                "Major SaaS player launches AI-native features",
                "Industry consolidation with key acquisition announced",
                "SaaS funding rebounds after correction period"
            ]
        },
        "ai": {
            "opportunities": [
                "Enterprise AI adoption accelerating across industries",
                "Government AI initiatives and funding programs",
                "Growing demand for AI safety and alignment solutions",
                "AI infrastructure and tooling market expanding"
            ],
            "risks": [
                "Regulatory uncertainty around AI governance",
                "Compute cost pressures affecting margins",
                "Talent competition intensifying",
                "Model commoditization concerns"
            ],
            "events": [
                f"New AI regulation framework proposed in {current_month}",
                "Major tech company open-sources large language model",
                "AI startup raises record funding round",
                "Industry group publishes AI safety standards"
            ]
        },
        "edtech": {
            "opportunities": [
                "Corporate learning budgets shifting to digital",
                "Government skill development initiatives",
                "AI tutoring showing strong learning outcomes",
                "Micro-credentials gaining employer acceptance"
            ],
            "risks": [
                "Funding winter affecting edtech valuations",
                "Completion rate skepticism from employers",
                "Free content from AI assistants"
            ],
            "events": [
                f"Edtech company announces profitability in {current_month}",
                "Major acquisition in online learning space",
                "New education policy emphasizes digital learning",
                "Corporate partnership with leading edtech announced"
            ]
        },
        "ecommerce": {
            "opportunities": [
                "Quick commerce category expanding rapidly",
                "D2C brands gaining consumer preference",
                "Social commerce integration opportunities",
                "Rural e-commerce penetration growing"
            ],
            "risks": [
                "Profitability pressures on quick commerce",
                "Logistics cost inflation",
                "Consumer sentiment affected by economy"
            ],
            "events": [
                f"Quick commerce player raises funding in {current_month}",
                "Major D2C brand acquisition announced",
                "E-commerce festive season sales break records",
                "New foreign investment rules for e-commerce"
            ]
        }
    }
    
    # Get domain-specific news or default
    domain_news = news_data.get(domain, {
        "opportunities": [
            "Digital transformation creating new market opportunities",
            "Growing investor interest in technology sector",
            "Government support for startups and innovation"
        ],
        "risks": [
            "Economic uncertainty affecting funding environment",
            "Increasing competition in digital space"
        ],
        "events": [
            f"Tech startup funding activity in {current_month}",
            "New startup-friendly policy announced",
            "Industry conference highlights emerging trends"
        ]
    })
    
    # Adjust for geography
    if geography == "India":
        domain_news["events"].append("Startup India initiative announces new support measures")
        domain_news["opportunities"].append("India's growing digital economy presents expansion opportunities")
    
    return {
        "opportunities": domain_news["opportunities"][:4],
        "risks": domain_news["risks"][:3],
        "recent_events": domain_news["events"][:4]
    }

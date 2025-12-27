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
    """Mock investor matching when LLM is not available."""
    domain = startup_profile.get("domain", "technology").lower()
    stage = startup_profile.get("stage", "seed").lower()
    geography = startup_profile.get("geography", "Global")
    
    # Domain-specific investors
    investors_db = {
        "fintech": [
            {
                "name": "Sequoia Capital India",
                "base_score": 90,
                "past_investments": ["Razorpay", "BharatPe", "Pine Labs", "Groww"],
                "focus": "fintech"
            },
            {
                "name": "Tiger Global",
                "base_score": 85,
                "past_investments": ["Slice", "Jupiter", "Fi Money"],
                "focus": "fintech"
            },
            {
                "name": "Ribbit Capital",
                "base_score": 88,
                "past_investments": ["Robinhood", "Revolut", "Credit Karma"],
                "focus": "fintech"
            },
            {
                "name": "Accel Partners",
                "base_score": 82,
                "past_investments": ["Flipkart", "Swiggy", "Freshworks"],
                "focus": "general"
            },
            {
                "name": "Blume Ventures",
                "base_score": 75,
                "past_investments": ["Slice", "Unacademy", "Dunzo"],
                "focus": "early-stage"
            }
        ],
        "healthtech": [
            {
                "name": "Lightspeed Venture Partners",
                "base_score": 88,
                "past_investments": ["Innovaccer", "Curefit", "PharmEasy"],
                "focus": "healthtech"
            },
            {
                "name": "General Atlantic",
                "base_score": 85,
                "past_investments": ["Byju's", "NoBroker", "Unacademy"],
                "focus": "growth"
            },
            {
                "name": "Chiratae Ventures",
                "base_score": 80,
                "past_investments": ["Lenskart", "Myntra", "FirstCry"],
                "focus": "consumer"
            },
            {
                "name": "Matrix Partners India",
                "base_score": 78,
                "past_investments": ["Practo", "Ola", "Razorpay"],
                "focus": "healthtech"
            }
        ],
        "saas": [
            {
                "name": "Bessemer Venture Partners",
                "base_score": 92,
                "past_investments": ["Chargebee", "Postman", "Procore"],
                "focus": "saas"
            },
            {
                "name": "Accel Partners",
                "base_score": 88,
                "past_investments": ["Freshworks", "BrowserStack", "Zenoti"],
                "focus": "saas"
            },
            {
                "name": "Tiger Global",
                "base_score": 85,
                "past_investments": ["Postman", "HighRadius", "Icertis"],
                "focus": "saas"
            },
            {
                "name": "Insight Partners",
                "base_score": 82,
                "past_investments": ["Postman", "JFrog", "Veeam"],
                "focus": "saas"
            }
        ],
        "ai": [
            {
                "name": "Andreessen Horowitz (a16z)",
                "base_score": 95,
                "past_investments": ["OpenAI", "Databricks", "Anyscale"],
                "focus": "ai"
            },
            {
                "name": "Khosla Ventures",
                "base_score": 90,
                "past_investments": ["OpenAI", "Impossible Foods", "Affirm"],
                "focus": "deep-tech"
            },
            {
                "name": "Sequoia Capital",
                "base_score": 88,
                "past_investments": ["Scale AI", "Hugging Face", "Glean"],
                "focus": "ai"
            },
            {
                "name": "Greylock Partners",
                "base_score": 85,
                "past_investments": ["Abnormal Security", "Coda", "Neeva"],
                "focus": "enterprise-ai"
            }
        ],
        "edtech": [
            {
                "name": "GSV Ventures",
                "base_score": 92,
                "past_investments": ["Coursera", "ClassDojo", "Degreed"],
                "focus": "edtech"
            },
            {
                "name": "Owl Ventures",
                "base_score": 88,
                "past_investments": ["Byju's", "Masterclass", "Newsela"],
                "focus": "edtech"
            },
            {
                "name": "Tiger Global",
                "base_score": 85,
                "past_investments": ["Byju's", "Unacademy", "Vedantu"],
                "focus": "edtech"
            },
            {
                "name": "Sequoia Capital India",
                "base_score": 82,
                "past_investments": ["Unacademy", "Eruditus", "Scaler"],
                "focus": "edtech"
            }
        ],
        "ecommerce": [
            {
                "name": "SoftBank Vision Fund",
                "base_score": 88,
                "past_investments": ["Flipkart", "Meesho", "FirstCry"],
                "focus": "ecommerce"
            },
            {
                "name": "Prosus Ventures",
                "base_score": 85,
                "past_investments": ["Swiggy", "Meesho", "ElasticRun"],
                "focus": "consumer"
            },
            {
                "name": "Peak XV Partners",
                "base_score": 82,
                "past_investments": ["Flipkart", "Myntra", "Urban Company"],
                "focus": "consumer"
            }
        ]
    }
    
    # Get investors for domain or use general list
    domain_investors = investors_db.get(domain, [
        {
            "name": "Accel Partners",
            "base_score": 80,
            "past_investments": ["Flipkart", "Swiggy", "Freshworks"],
            "focus": "general"
        },
        {
            "name": "Sequoia Capital",
            "base_score": 85,
            "past_investments": ["Stripe", "Airbnb", "DoorDash"],
            "focus": "general"
        },
        {
            "name": "Tiger Global",
            "base_score": 78,
            "past_investments": ["Byju's", "Razorpay", "Ola"],
            "focus": "growth"
        },
        {
            "name": "Peak XV Partners",
            "base_score": 75,
            "past_investments": ["Flipkart", "Ola", "Zomato"],
            "focus": "india"
        }
    ])
    
    # Adjust scores based on stage
    stage_multiplier = {
        "pre-seed": 0.9,
        "seed": 1.0,
        "series a": 1.0,
        "series b": 0.95,
        "series c": 0.90,
        "growth": 0.85
    }
    
    multiplier = stage_multiplier.get(stage, 1.0)
    
    # Build investor list with adjusted scores
    matched_investors = []
    for inv in domain_investors:
        score = min(100, int(inv["base_score"] * multiplier + (hash(inv["name"]) % 10 - 5)))
        
        matched_investors.append({
            "name": inv["name"],
            "match_score": max(50, min(98, score)),
            "reason": f"Strong track record in {domain} with investments in {', '.join(inv['past_investments'][:2])}. Focus area aligns with {startup_profile.get('market_category', domain)}.",
            "past_investments": inv["past_investments"]
        })
    
    # Sort by match_score descending
    matched_investors.sort(key=lambda x: x["match_score"], reverse=True)
    
    return matched_investors

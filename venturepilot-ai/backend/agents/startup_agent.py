import json
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from mistralai import Mistral


def get_client():
    """Get Mistral client - checks API key each time."""
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if api_key:
        return Mistral(api_key=api_key)
    return None


def analyze_startup(input_data: dict) -> dict:
    """
    Analyze a startup based on input data.
    
    Input Schema (STRICT):
    {
        "description": string,
        "domain": string,
        "stage": string,
        "geography": string,
        "customer_type": string
    }
    
    Output Schema:
    {
        "problem": string,
        "value_proposition": string,
        "market_category": string,
        "target_customers": string,
        "assumed_competitors": list[string],
        "risk_factors": list[string]
    }
    """
    # Validate input
    required_fields = ["description", "domain", "stage", "geography", "customer_type"]
    for field in required_fields:
        if field not in input_data:
            raise ValueError(f"Missing required field: {field}")
    
    client = get_client()
    if client:
        print(f"[STARTUP AGENT] Using Mistral AI for analysis...")
        return _analyze_with_llm(input_data, client)
    else:
        print(f"[STARTUP AGENT] WARNING: No API key - using mock data!")
        return _analyze_mock(input_data)


def _analyze_with_llm(input_data: dict, client) -> dict:
    """Use LLM to analyze startup."""
    prompt = f"""Analyze this startup and output ONLY valid JSON with no additional text.

Startup Information:
- Description: {input_data['description']}
- Domain: {input_data['domain']}
- Stage: {input_data['stage']}
- Geography: {input_data['geography']}
- Customer Type: {input_data['customer_type']}

Output this exact JSON structure:
{{
    "problem": "The core problem being solved",
    "value_proposition": "The unique value offered",
    "market_category": "The market category",
    "target_customers": "Description of target customers",
    "assumed_competitors": ["competitor1", "competitor2", "competitor3"],
    "risk_factors": ["risk1", "risk2", "risk3"]
}}

Respond ONLY with the JSON object, no markdown, no explanation."""

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
        
        # Try to parse JSON
        try:
            result = json.loads(result_text)
            _validate_output(result)
            return result
        except json.JSONDecodeError:
            # Retry once
            response = client.chat.complete(
                model=os.getenv("LLM_MODEL", "mistral-small-latest"),
                messages=[
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": result_text},
                    {"role": "user", "content": "That was not valid JSON. Please respond with ONLY a valid JSON object, no markdown."}
                ],
                temperature=0.1
            )
            result_text = response.choices[0].message.content.strip()
            if result_text.startswith("```"):
                result_text = result_text.split("```")[1]
                if result_text.startswith("json"):
                    result_text = result_text[4:]
                result_text = result_text.strip()
            result = json.loads(result_text)
            _validate_output(result)
            return result
            
    except Exception as e:
        print(f"LLM analysis failed: {e}")
        return _analyze_mock(input_data)


def _analyze_mock(input_data: dict) -> dict:
    """Mock analysis when LLM is not available."""
    domain = input_data.get("domain", "technology")
    geography = input_data.get("geography", "Global")
    customer_type = input_data.get("customer_type", "B2B")
    
    # Domain-specific competitors and risks
    domain_data = {
        "fintech": {
            "competitors": ["Stripe", "Razorpay", "PayPal", "Square"],
            "risks": ["Regulatory compliance", "Security vulnerabilities", "Trust building"],
            "market_category": "Financial Technology"
        },
        "healthtech": {
            "competitors": ["Practo", "1mg", "PharmEasy", "Teladoc"],
            "risks": ["Healthcare regulations", "Data privacy (HIPAA)", "Clinical validation"],
            "market_category": "Healthcare Technology"
        },
        "edtech": {
            "competitors": ["Byju's", "Coursera", "Udemy", "Khan Academy"],
            "risks": ["Content quality", "User engagement", "Certification value"],
            "market_category": "Education Technology"
        },
        "saas": {
            "competitors": ["Salesforce", "HubSpot", "Zoho", "Freshworks"],
            "risks": ["Customer acquisition cost", "Churn rate", "Feature commoditization"],
            "market_category": "Software as a Service"
        },
        "ai": {
            "competitors": ["OpenAI", "Google AI", "Microsoft Azure AI", "Anthropic"],
            "risks": ["Model accuracy", "Compute costs", "Ethical concerns", "Regulation"],
            "market_category": "Artificial Intelligence"
        },
        "ecommerce": {
            "competitors": ["Amazon", "Flipkart", "Shopify", "Meesho"],
            "risks": ["Logistics costs", "Competition", "Margin pressure"],
            "market_category": "E-Commerce"
        }
    }
    
    domain_lower = domain.lower()
    domain_info = domain_data.get(domain_lower, {
        "competitors": ["Industry Leader A", "Industry Leader B", "Emerging Player C"],
        "risks": ["Market competition", "Funding challenges", "Team scaling"],
        "market_category": domain.title()
    })
    
    return {
        "problem": f"Addressing key challenges in the {domain} space for {customer_type} customers in {geography}",
        "value_proposition": f"Innovative {domain} solution that delivers superior value through technology-driven approach",
        "market_category": domain_info["market_category"],
        "target_customers": f"{customer_type} customers in {geography} seeking {domain} solutions",
        "assumed_competitors": domain_info["competitors"],
        "risk_factors": domain_info["risks"]
    }


def _validate_output(result: dict) -> None:
    """Validate the output structure."""
    required_fields = [
        "problem", "value_proposition", "market_category",
        "target_customers", "assumed_competitors", "risk_factors"
    ]
    
    for field in required_fields:
        if field not in result:
            raise ValueError(f"Missing output field: {field}")
    
    if not isinstance(result["assumed_competitors"], list):
        raise ValueError("assumed_competitors must be a list")
    
    if not isinstance(result["risk_factors"], list):
        raise ValueError("risk_factors must be a list")

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
    """
    Fallback analysis when LLM is not available.
    Returns minimal dynamic response based on input - NOT hardcoded data.
    """
    description = input_data.get("description", "")
    domain = input_data.get("domain", "technology")
    geography = input_data.get("geography", "Global")
    customer_type = input_data.get("customer_type", "B2B")
    stage = input_data.get("stage", "seed")
    
    # Generate dynamic response based on actual input
    return {
        "problem": f"Problem extracted from: {description[:100]}..." if len(description) > 100 else f"Problem: {description}",
        "value_proposition": f"Value proposition for {domain} startup targeting {customer_type} customers in {geography}",
        "market_category": f"{domain.title()} Technology",
        "target_customers": f"{customer_type} customers in {geography} market",
        "assumed_competitors": [f"Competitor in {domain} space"],
        "risk_factors": [f"Market entry risk in {geography}", f"Competition in {domain} sector", f"Typical {stage} stage challenges"]
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

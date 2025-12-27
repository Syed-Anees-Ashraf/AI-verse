"""Utility functions for LLM interactions"""
import json
import re


def parse_llm_json(text: str) -> dict:
    """
    Parse JSON from LLM response, handling markdown code blocks.
    
    Args:
        text: Raw LLM response text
        
    Returns:
        Parsed JSON as dict/list
    """
    text = text.strip()
    
    # Handle markdown code blocks
    if text.startswith("```"):
        # Extract content between code blocks
        parts = text.split("```")
        if len(parts) >= 2:
            text = parts[1]
            # Remove language identifier if present
            if text.startswith("json"):
                text = text[4:]
            elif text.startswith("JSON"):
                text = text[4:]
            text = text.strip()
    
    # Try to find JSON object or array in text
    if not text.startswith(("{", "[")):
        # Try to extract JSON from text
        json_match = re.search(r'[\{\[].*[\}\]]', text, re.DOTALL)
        if json_match:
            text = json_match.group()
    
    return json.loads(text)


def clean_json_response(text: str) -> str:
    """
    Clean LLM response to extract just the JSON portion.
    
    Args:
        text: Raw LLM response text
        
    Returns:
        Cleaned text ready for JSON parsing
    """
    text = text.strip()
    
    # Handle markdown code blocks
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith(("{", "[")):
                return part
    
    return text

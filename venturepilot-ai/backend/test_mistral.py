"""Test Mistral AI integration with Startup Agent"""
from dotenv import load_dotenv
load_dotenv()

from agents.startup_agent import analyze_startup

print('Testing Startup Agent with Mistral AI...')
result = analyze_startup({
    'description': 'AI-powered payment processing for small businesses in India',
    'domain': 'fintech',
    'stage': 'seed',
    'geography': 'India',
    'customer_type': 'B2B'
})

print('\nStartup Analysis Result:')
print(f'  Problem: {result["problem"][:80]}...')
print(f'  Value Prop: {result["value_proposition"][:80]}...')
print(f'  Competitors: {result["assumed_competitors"]}')
print(f'  Risks: {result["risk_factors"]}')
print('\n✅ Mistral AI integration working!')

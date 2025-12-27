"""Test Mistral AI API connection"""
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('MISTRAL_API_KEY', '')
if len(api_key) > 10:
    print(f"✅ API Key loaded: {api_key[:10]}...{api_key[-5:]}")
else:
    print("❌ No API key found")
    exit(1)

# Test Mistral AI connection
from mistralai import Mistral
client = Mistral(api_key=api_key)

print("\nTesting Mistral AI API...")
try:
    response = client.chat.complete(
        model='mistral-small-latest',
        messages=[{'role': 'user', 'content': 'Say "VenturePilot AI is ready!" in exactly those words'}],
        max_tokens=20
    )
    print(f"Mistral Response: {response.choices[0].message.content}")
    print("\n✅ Mistral AI API is working correctly!")
except Exception as e:
    print(f"❌ Mistral AI API Error: {e}")

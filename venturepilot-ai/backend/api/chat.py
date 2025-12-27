from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os
import json
import sys
from dotenv import load_dotenv

# Load environment variables at module level
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rag.retriever import retrieve_context

# Import Mistral
from mistralai import Mistral


def get_mistral_client():
    """Get Mistral client dynamically to ensure .env is loaded."""
    api_key = os.getenv("MISTRAL_API_KEY", "")
    if api_key:
        return Mistral(api_key=api_key), True
    return None, False

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message input."""
    question: str
    startup_profile: Optional[dict] = None
    conversation_history: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    """Chat response output."""
    answer: str
    sources: List[str]
    related_topics: List[str]


@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Chat endpoint for Q&A.
    
    Input: User question + startup profile
    Output: LLM response using retriever + agents
    """
    try:
        from main import get_vector_store
        
        vector_store = get_vector_store()
        
        # Build context from startup profile
        profile_context = ""
        if message.startup_profile:
            profile_context = f"""
Startup Context:
- Domain: {message.startup_profile.get('domain', 'N/A')}
- Stage: {message.startup_profile.get('stage', 'N/A')}
- Geography: {message.startup_profile.get('geography', 'N/A')}
- Description: {message.startup_profile.get('description', 'N/A')}
"""
        
        # Determine category from question
        category = _detect_category(message.question)
        geography = message.startup_profile.get('geography') if message.startup_profile else None
        
        # Retrieve relevant context
        context_docs = retrieve_context(
            query=message.question,
            category=category,
            geography=geography,
            vector_store=vector_store,
            k=5
        )
        
        # Generate response
        client, use_llm = get_mistral_client()
        if use_llm and client:
            answer, sources = _generate_llm_response(
                question=message.question,
                profile_context=profile_context,
                retrieved_context=context_docs,
                conversation_history=message.conversation_history,
                client=client
            )
        else:
            answer, sources = _generate_mock_response(
                question=message.question,
                profile_context=profile_context,
                retrieved_context=context_docs
            )
        
        # Generate related topics
        related_topics = _generate_related_topics(message.question, category)
        
        return ChatResponse(
            answer=answer,
            sources=sources[:3],
            related_topics=related_topics[:4]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


def _detect_category(question: str) -> Optional[str]:
    """Detect the category relevant to the question."""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["policy", "regulation", "compliance", "government", "scheme", "tax"]):
        return "policy"
    elif any(word in question_lower for word in ["investor", "funding", "vc", "venture", "raise", "investment"]):
        return "investor"
    elif any(word in question_lower for word in ["news", "recent", "latest", "update", "announcement"]):
        return "news"
    elif any(word in question_lower for word in ["market", "size", "growth", "trend", "competition"]):
        return "report"
    
    return None


def _generate_llm_response(
    question: str,
    profile_context: str,
    retrieved_context: List[str],
    conversation_history: Optional[List[dict]] = None,
    client=None
) -> tuple[str, List[str]]:
    """Generate response using LLM."""
    
    context_text = "\n\n".join(retrieved_context) if retrieved_context else "No specific context available."
    
    system_prompt = f"""You are VenturePilot AI, an expert assistant for startup founders seeking investment and strategic guidance.

{profile_context}

Relevant Context:
{context_text}

Answer the user's question based on the context provided. Be specific, actionable, and reference the context when relevant.
If you don't have enough information to answer, say so and suggest what information would be helpful."""

    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    if conversation_history:
        for msg in conversation_history[-5:]:  # Last 5 messages
            messages.append(msg)
    
    messages.append({"role": "user", "content": question})
    
    try:
        response = client.chat.complete(
            model=os.getenv("LLM_MODEL", "mistral-small-latest"),
            messages=messages,
            temperature=0.5
        )
        
        answer = response.choices[0].message.content
        
        # Extract sources from context
        sources = []
        for ctx in retrieved_context[:3]:
            if "[Source:" in ctx:
                source = ctx.split("[Source:")[1].split("]")[0].strip()
                sources.append(source)
        
        return answer, sources
        
    except Exception as e:
        print(f"LLM chat failed: {e}")
        return _generate_mock_response(question, profile_context, retrieved_context)


def _generate_mock_response(
    question: str,
    profile_context: str,
    retrieved_context: List[str]
) -> tuple[str, List[str]]:
    """Generate mock response when LLM is not available."""
    
    question_lower = question.lower()
    
    # Generate contextual response based on question type
    if "investor" in question_lower or "funding" in question_lower:
        answer = """Based on your startup profile, here are some recommendations for finding investors:

1. **Research Target Investors**: Look for VCs and angels who have invested in similar domains and stages. Check their portfolio companies for alignment.

2. **Prepare Your Materials**: Ensure your pitch deck, financial projections, and data room are ready for due diligence.

3. **Leverage Your Network**: Warm introductions are more effective than cold outreach. Use LinkedIn, founder networks, and accelerator connections.

4. **Apply to Programs**: Consider accelerators like Y Combinator, Techstars, or domain-specific programs that provide funding and mentorship.

5. **Government Schemes**: If in India, explore Startup India Seed Fund Scheme and Fund of Funds for Startups.

Would you like me to provide more specific investor recommendations based on your domain?"""
    
    elif "policy" in question_lower or "regulation" in question_lower:
        answer = """Here's guidance on policy and regulatory considerations:

1. **Business Registration**: Ensure proper incorporation (Private Limited is recommended for raising funds).

2. **Startup Recognition**: Apply for DPIIT recognition under Startup India for tax benefits and easier compliance.

3. **Sector-Specific Compliance**: Depending on your domain (fintech, healthtech, etc.), there may be specific licenses required.

4. **Tax Benefits**: Explore Section 80-IAC for tax exemption and angel tax exemption provisions.

5. **Data Protection**: If handling user data, ensure compliance with upcoming Digital Personal Data Protection Act.

Would you like specific guidance based on your sector and geography?"""
    
    elif "market" in question_lower or "competition" in question_lower:
        answer = """Here's an analysis of market considerations:

1. **Market Sizing**: Use TAM (Total Addressable Market), SAM (Serviceable Available Market), and SOM (Serviceable Obtainable Market) framework.

2. **Competition Analysis**: Map direct competitors, indirect alternatives, and potential market entrants.

3. **Growth Drivers**: Identify macro trends supporting your market (digitization, changing consumer behavior, etc.).

4. **Barriers to Entry**: Assess what defensibility you have (technology, network effects, regulatory moats).

5. **Unit Economics**: Ensure your business model can achieve sustainable margins as you scale.

Would you like me to analyze specific market trends for your domain?"""
    
    else:
        answer = f"""Thank you for your question about "{question}".

Based on the available information:

{profile_context}

Here are some general recommendations:

1. **Focus on Core Metrics**: Track the KPIs most relevant to your stage and domain.

2. **Build Strategically**: Prioritize features that demonstrate product-market fit.

3. **Network Actively**: Engage with founder communities, mentors, and potential partners.

4. **Stay Informed**: Keep up with industry news and regulatory changes.

5. **Plan for Growth**: Think about your scaling strategy even at early stages.

Feel free to ask more specific questions about investors, policy, market analysis, or strategy!"""
    
    # Extract sources from context
    sources = []
    for ctx in retrieved_context[:3]:
        if "[Source:" in ctx:
            source = ctx.split("[Source:")[1].split("]")[0].strip()
            sources.append(source)
    
    if not sources:
        sources = ["VenturePilot Knowledge Base"]
    
    return answer, sources


def _generate_related_topics(question: str, category: Optional[str]) -> List[str]:
    """Generate related topics for exploration."""
    
    related = {
        "policy": [
            "Startup India tax benefits",
            "DPIIT recognition process",
            "Sector-specific compliance",
            "International expansion regulations"
        ],
        "investor": [
            "Pitch deck best practices",
            "Term sheet negotiation",
            "Due diligence preparation",
            "Valuation methodologies"
        ],
        "news": [
            "Recent funding rounds in your sector",
            "Policy updates",
            "Market trend analysis",
            "Competitor news"
        ],
        "report": [
            "Market size projections",
            "Industry growth trends",
            "Competitive landscape",
            "Customer segmentation"
        ]
    }
    
    if category and category in related:
        return related[category]
    
    # Default related topics
    return [
        "Fundraising strategy",
        "Investor targeting",
        "Market analysis",
        "Regulatory compliance"
    ]

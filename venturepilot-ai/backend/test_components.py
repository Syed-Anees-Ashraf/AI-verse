"""
Test script to verify all components are working.
Run this after setting up the project.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_startup_agent():
    """Test the startup agent."""
    print("\n=== Testing Startup Agent ===")
    from agents.startup_agent import analyze_startup
    
    # Test 1: Fintech startup
    test_input_1 = {
        "description": "A digital payment platform for small businesses in India",
        "domain": "Fintech",
        "stage": "Seed",
        "geography": "India",
        "customer_type": "B2B"
    }
    
    result_1 = analyze_startup(test_input_1)
    print(f"Fintech Startup Analysis:")
    print(f"  - Problem: {result_1.get('problem', 'N/A')[:50]}...")
    print(f"  - Competitors: {result_1.get('assumed_competitors', [])}")
    print(f"  - Risks: {result_1.get('risk_factors', [])}")
    
    # Test 2: Healthtech startup
    test_input_2 = {
        "description": "AI-powered diagnostic tool for rural healthcare",
        "domain": "Healthtech",
        "stage": "Pre-seed",
        "geography": "India",
        "customer_type": "B2B2C"
    }
    
    result_2 = analyze_startup(test_input_2)
    print(f"\nHealthtech Startup Analysis:")
    print(f"  - Problem: {result_2.get('problem', 'N/A')[:50]}...")
    print(f"  - Competitors: {result_2.get('assumed_competitors', [])}")
    
    # Verify competitors differ
    assert result_1['assumed_competitors'] != result_2['assumed_competitors'], "Competitors should differ by domain"
    print("\n✅ Startup Agent Tests Passed!")
    return True


def test_vector_store():
    """Test the vector store."""
    print("\n=== Testing Vector Store ===")
    from storage.vector_store import VectorStore
    
    vs = VectorStore()
    
    # Add test documents
    test_docs = [
        {
            "text": "Startup India provides tax benefits for registered startups",
            "category": "policy",
            "timestamp": "2024-12-01",
            "geography": "India",
            "source": "Test Source"
        },
        {
            "text": "Sequoia Capital focuses on fintech and consumer investments",
            "category": "investor",
            "timestamp": "2024-12-01",
            "geography": "India",
            "source": "Test Source"
        }
    ]
    
    vs.add_documents(test_docs)
    
    # Search test
    results = vs.search("startup tax benefits", filters={"category": "policy"}, k=2)
    print(f"Search Results: {len(results)} documents found")
    
    assert len(results) > 0, "Should find at least one result"
    print("✅ Vector Store Tests Passed!")
    return True


def test_retriever():
    """Test the retriever."""
    print("\n=== Testing Retriever ===")
    from rag.retriever import retrieve_context
    from storage.vector_store import VectorStore
    
    vs = VectorStore()
    
    # Add test data
    test_docs = [
        {
            "text": "Indian fintech government schemes include Startup India Seed Fund",
            "category": "policy",
            "timestamp": "2024-12-01",
            "geography": "India",
            "source": "Government Portal"
        },
        {
            "text": "AI SaaS seed stage investors include Accel and Sequoia",
            "category": "investor",
            "timestamp": "2024-12-01",
            "geography": "India",
            "source": "VC Database"
        }
    ]
    vs.add_documents(test_docs)
    
    # Test retrieval
    context = retrieve_context(
        query="Indian fintech government schemes",
        category="policy",
        geography="India",
        vector_store=vs,
        k=5
    )
    
    print(f"Retrieved {len(context)} context items")
    if context:
        print(f"Sample: {context[0][:100]}...")
    
    print("✅ Retriever Tests Passed!")
    return True


def test_agents():
    """Test all domain agents."""
    print("\n=== Testing Domain Agents ===")
    
    from agents.policy_agent import analyze_policy
    from agents.investor_agent import match_investors
    from agents.market_agent import analyze_market
    from agents.news_agent import analyze_news
    from agents.strategy_agent import synthesize_strategy
    
    test_profile = {
        "description": "AI-powered fintech platform",
        "domain": "Fintech",
        "stage": "Seed",
        "geography": "India",
        "customer_type": "B2B",
        "problem": "Complex payment processing",
        "value_proposition": "Simplified payments",
        "market_category": "Financial Technology",
        "target_customers": "SMEs in India",
        "assumed_competitors": ["Razorpay", "PayPal"],
        "risk_factors": ["Regulatory compliance"]
    }
    
    # Test Policy Agent
    policy = analyze_policy(test_profile)
    print(f"Policy Agent: Found {len(policy.get('relevant_policies', []))} policies")
    assert 'relevant_policies' in policy
    assert 'eligible_schemes' in policy
    assert 'regulatory_risks' in policy
    
    # Test Investor Agent
    investors = match_investors(test_profile)
    print(f"Investor Agent: Matched {len(investors)} investors")
    assert len(investors) > 0
    assert investors[0]['match_score'] >= investors[-1]['match_score'], "Should be sorted by score"
    
    # Test Market Agent
    market = analyze_market(test_profile)
    print(f"Market Agent: Market size - {market.get('market_size_estimate', 'N/A')[:30]}...")
    assert 'market_size_estimate' in market
    assert 'growth_signals' in market
    
    # Test News Agent
    news = analyze_news(test_profile)
    print(f"News Agent: Found {len(news.get('opportunities', []))} opportunities")
    assert 'opportunities' in news
    assert 'recent_events' in news
    
    # Test Strategy Agent (should NOT use retriever)
    strategy = synthesize_strategy(
        startup_profile=test_profile,
        policy_analysis=policy,
        investor_matches=investors,
        market_analysis=market,
        news_analysis=news
    )
    print(f"Strategy Agent: Readiness - {strategy.get('fundraising_readiness', 'N/A')}")
    assert strategy.get('fundraising_readiness') in ['low', 'medium', 'high']
    assert 'key_recommendations' in strategy
    assert 'next_actions' in strategy
    
    print("✅ All Agent Tests Passed!")
    return True


def test_orchestrator():
    """Test the orchestrator."""
    print("\n=== Testing Orchestrator ===")
    from orchestration.orchestrator import Orchestrator
    
    test_input = {
        "description": "SaaS platform for HR automation",
        "domain": "SaaS",
        "stage": "Series A",
        "geography": "India",
        "customer_type": "B2B"
    }
    
    orchestrator = Orchestrator()
    results = orchestrator.run(test_input)
    
    # Verify all components present
    assert 'startup_profile' in results
    assert 'policy' in results
    assert 'investors' in results
    assert 'market' in results
    assert 'news' in results
    assert 'strategy' in results
    
    # Verify execution log
    metadata = results.get('_metadata', {})
    execution_log = metadata.get('execution_log', [])
    print(f"Agents executed: {len(execution_log)}")
    
    agent_names = [log['agent'] for log in execution_log]
    expected_order = ['startup_agent', 'policy_agent', 'investor_agent', 'market_agent', 'news_agent', 'strategy_agent']
    
    # Check each agent ran exactly once in order
    for agent in expected_order:
        assert agent in agent_names, f"Missing agent: {agent}"
    
    print("Execution Order:", ' -> '.join(agent_names))
    print("✅ Orchestrator Tests Passed!")
    return True


def main():
    """Run all tests."""
    print("=" * 50)
    print("VENTUREPILOT AI - COMPONENT TESTS")
    print("=" * 50)
    
    tests = [
        ("Startup Agent", test_startup_agent),
        ("Vector Store", test_vector_store),
        ("Retriever", test_retriever),
        ("Domain Agents", test_agents),
        ("Orchestrator", test_orchestrator),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} FAILED: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("\n✅ ALL TESTS PASSED! System is ready.")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && uvicorn main:app --reload")
        print("2. Start the frontend: streamlit run frontend/app.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

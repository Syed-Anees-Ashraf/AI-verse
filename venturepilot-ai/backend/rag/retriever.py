from typing import Optional
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def retrieve_context(
    query: str,
    category: Optional[str] = None,
    geography: Optional[str] = None,
    recency_days: Optional[int] = None,
    vector_store = None,
    k: int = 5
) -> list[str]:
    """
    Retrieve relevant context from the vector store.
    
    Args:
        query: Search query string
        category: Filter by category ("policy", "investor", "news", "report")
        geography: Filter by geography
        recency_days: Only return documents from the last N days
        vector_store: VectorStore instance
        k: Number of results to return
    
    Returns:
        List of relevant text strings
    """
    if vector_store is None:
        print("Warning: No vector store provided")
        return []
    
    # Build filters
    filters = {}
    if category:
        filters["category"] = category
    if geography:
        filters["geography"] = geography
    
    # Search vector store
    results = vector_store.search(query, filters=filters, k=k * 2)  # Get more to filter by recency
    
    # Filter by recency if specified
    if recency_days:
        cutoff_date = datetime.now() - timedelta(days=recency_days)
        cutoff_str = cutoff_date.isoformat()[:10]
        
        results = [
            r for r in results
            if r.get("metadata", {}).get("timestamp", "") >= cutoff_str
        ]
    
    # Sort by relevance score (already sorted) and take top k
    results = results[:k]
    
    # Extract text from results
    context_texts = []
    for result in results:
        text = result.get("text", "")
        metadata = result.get("metadata", {})
        
        # Include metadata context
        source = metadata.get("source", "Unknown")
        timestamp = metadata.get("timestamp", "")
        title = metadata.get("title", "")
        
        context_entry = f"[Source: {source}]"
        if title:
            context_entry += f" [{title}]"
        if timestamp:
            context_entry += f" [{timestamp}]"
        context_entry += f"\n{text}"
        
        context_texts.append(context_entry)
    
    return context_texts


def retrieve_by_category(
    category: str,
    query: str,
    geography: Optional[str] = None,
    vector_store = None,
    k: int = 5
) -> list[dict]:
    """
    Retrieve documents filtered by category.
    
    Returns full document objects with metadata.
    """
    if vector_store is None:
        return []
    
    filters = {"category": category}
    if geography:
        filters["geography"] = geography
    
    results = vector_store.search(query, filters=filters, k=k)
    return results

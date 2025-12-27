from typing import Optional
from datetime import datetime, timedelta
import uuid
import re


class VectorStore:
    """Simple in-memory vector storage for document storage and retrieval.
    Uses keyword matching for search (can be upgraded to embeddings later).
    """
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the vector store."""
        self.documents = []  # List of document dicts
        self.doc_index = {}  # id -> document mapping
    
    def add_documents(self, documents: list[dict]) -> None:
        """
        Add documents to the vector store.
        
        Each document MUST have:
        - text: str
        - category: "policy" | "investor" | "news" | "report"
        - timestamp: ISO_DATE
        - geography: str
        - source: str
        """
        required_fields = ["text", "category", "timestamp", "geography", "source"]
        
        valid_documents = []
        for doc in documents:
            # Validate required fields
            missing_fields = [f for f in required_fields if f not in doc or not doc[f]]
            if missing_fields:
                print(f"Rejecting document - missing fields: {missing_fields}")
                continue
            
            # Validate category
            valid_categories = ["policy", "investor", "news", "report"]
            if doc["category"] not in valid_categories:
                print(f"Rejecting document - invalid category: {doc['category']}")
                continue
            
            valid_documents.append(doc)
        
        if not valid_documents:
            print("No valid documents to add")
            return
        
        # Add documents to in-memory store
        for doc in valid_documents:
            doc_id = str(uuid.uuid4())
            doc_entry = {
                "id": doc_id,
                "text": doc["text"],
                "category": doc["category"],
                "timestamp": doc["timestamp"],
                "geography": doc["geography"],
                "source": doc["source"],
                "title": doc.get("title", ""),
                "keywords": self._extract_keywords(doc["text"])
            }
            self.documents.append(doc_entry)
            self.doc_index[doc_id] = doc_entry
        
        print(f"Added {len(valid_documents)} documents to vector store")
    
    def _extract_keywords(self, text: str) -> set:
        """Extract keywords from text for simple search."""
        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        return set(words)
    
    def search(
        self, 
        query: str, 
        filters: Optional[dict] = None, 
        k: int = 5
    ) -> list[dict]:
        """
        Search the vector store for relevant documents.
        
        Args:
            query: Search query string
            filters: Optional filters (category, geography, etc.)
            k: Number of results to return
        
        Returns:
            List of matching documents with metadata
        """
        # Extract query keywords
        query_keywords = self._extract_keywords(query)
        
        # Filter and score documents
        scored_docs = []
        for doc in self.documents:
            # Apply filters
            if filters:
                if "category" in filters and filters["category"]:
                    if doc["category"] != filters["category"]:
                        continue
                if "geography" in filters and filters["geography"]:
                    if doc["geography"] != filters["geography"]:
                        continue
            
            # Calculate relevance score (keyword overlap)
            doc_keywords = doc["keywords"]
            overlap = len(query_keywords & doc_keywords)
            
            if overlap > 0:
                # Score based on overlap ratio
                score = overlap / max(len(query_keywords), 1)
                scored_docs.append((doc, score))
        
        # Sort by score descending
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Format results
        documents = []
        for doc, score in scored_docs[:k]:
            documents.append({
                "text": doc["text"],
                "metadata": {
                    "category": doc["category"],
                    "timestamp": doc["timestamp"],
                    "geography": doc["geography"],
                    "source": doc["source"],
                    "title": doc.get("title", "")
                },
                "relevance_score": score
            })
        
        return documents
    
    def filter_by_recency(
        self, 
        documents: list[dict], 
        recency_days: int
    ) -> list[dict]:
        """Filter documents by recency."""
        if not recency_days:
            return documents
        
        cutoff_date = datetime.now() - timedelta(days=recency_days)
        cutoff_str = cutoff_date.isoformat()[:10]
        
        return [
            doc for doc in documents
            if doc["metadata"].get("timestamp", "") >= cutoff_str
        ]

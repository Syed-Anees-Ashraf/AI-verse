from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.onboarding import router as onboarding_router
from api.dashboard import router as dashboard_router
from api.chat import router as chat_router
from storage.vector_store import VectorStore
from config import POLICIES_DIR, INVESTORS_DIR, NEWS_DIR, API_HOST, API_PORT
import os
import json

app = FastAPI(
    title="VenturePilot AI",
    description="AI-powered startup analysis and investment recommendation system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vector store instance
vector_store = None

def load_data_files(directory: str, category: str) -> list[dict]:
    """Load all JSON files from a directory and return as documents."""
    documents = []
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return documents
    
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            item['category'] = category
                            documents.append(item)
                    else:
                        data['category'] = category
                        documents.append(data)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
    
    return documents

@app.on_event("startup")
async def startup_event():
    """Load all data into vector store on startup."""
    global vector_store
    vector_store = VectorStore()
    
    # Load policies
    policy_docs = load_data_files(POLICIES_DIR, "policy")
    if policy_docs:
        vector_store.add_documents(policy_docs)
        print(f"Loaded {len(policy_docs)} policy documents")
    
    # Load investors
    investor_docs = load_data_files(INVESTORS_DIR, "investor")
    if investor_docs:
        vector_store.add_documents(investor_docs)
        print(f"Loaded {len(investor_docs)} investor documents")
    
    # Load news
    news_docs = load_data_files(NEWS_DIR, "news")
    if news_docs:
        vector_store.add_documents(news_docs)
        print(f"Loaded {len(news_docs)} news documents")
    
    print("VenturePilot AI started successfully!")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to VenturePilot AI", "status": "running"}

@app.get("/api/news")
async def get_news():
    """Get all news items for the news ticker."""
    try:
        news_docs = load_data_files(NEWS_DIR, "news")
        return news_docs
    except Exception as e:
        return []

# Include routers
app.include_router(onboarding_router, prefix="/api", tags=["Onboarding"])
app.include_router(dashboard_router, prefix="/api", tags=["Dashboard"])
app.include_router(chat_router, prefix="/api", tags=["Chat"])

def get_vector_store() -> VectorStore:
    """Get the global vector store instance."""
    global vector_store
    return vector_store

if __name__ == "__main__":
    uvicorn.run(app, host=API_HOST, port=API_PORT)

# VenturePilot AI

An AI-powered startup analysis and investment recommendation system.

## Features
- Startup profile analysis
- Policy and regulatory guidance
- Investor matching
- Market analysis
- News monitoring
- Strategic recommendations

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the backend:
```bash
cd backend
uvicorn main:app --reload
```

3. Run the Streamlit frontend:
```bash
streamlit run frontend/app.py
```

## Project Structure
- `backend/` - FastAPI backend with agents and orchestration
- `frontend/` - Streamlit frontend
- `data/` - Sample data for policies, investors, and news

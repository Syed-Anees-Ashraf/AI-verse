# VenturePilot AI

🚀 An AI-powered startup analysis and investment recommendation system that helps startups find their ideal investors.

![VenturePilot AI](https://img.shields.io/badge/VenturePilot-AI-blue?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?style=for-the-badge)

## ✨ Features

- 🤖 **AI-Powered Analysis** - Advanced startup profile analysis using Mistral AI
- 💰 **Smart Investor Matching** - Find the perfect investors based on your domain and stage
- 📊 **Market Intelligence** - Real-time market analysis, trends, and growth signals
- 📜 **Policy Guidance** - Government schemes, regulatory compliance, and policy insights
- 📰 **News Monitoring** - Live news ticker with industry updates
- 💬 **AI Chat Assistant** - Interactive Q&A for personalized guidance
- 📈 **Visual Analytics** - Beautiful charts and dashboards

## 🛠️ Tech Stack

### Backend
- FastAPI - High-performance Python API
- Mistral AI - LLM for analysis and recommendations
- Python 3.13+

### Frontend
- Next.js 14 - React framework
- TypeScript - Type-safe development
- Tailwind CSS - Modern styling
- Framer Motion - Smooth animations
- Recharts - Interactive charts

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### 1. Clone and Setup

```bash
git clone <repository-url>
cd venturepilot-ai
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment (optional - uses mock data without API key)
cd backend
# Edit .env file with your Mistral API key if available

# Start the backend server
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

### 4. Open the Application

Visit [http://localhost:3000](http://localhost:3000) in your browser!

## 📁 Project Structure

```
venturepilot-ai/
├── backend/
│   ├── agents/           # AI agents for analysis
│   │   ├── investor_agent.py
│   │   ├── market_agent.py
│   │   ├── news_agent.py
│   │   ├── policy_agent.py
│   │   ├── startup_agent.py
│   │   └── strategy_agent.py
│   ├── api/              # API endpoints
│   │   ├── chat.py
│   │   ├── dashboard.py
│   │   └── onboarding.py
│   ├── orchestration/    # Agent orchestration
│   ├── rag/              # Retrieval system
│   ├── storage/          # Data storage
│   ├── main.py           # FastAPI app
│   └── config.py         # Configuration
├── frontend/
│   ├── app/              # Next.js app
│   ├── components/       # React components
│   ├── package.json
│   └── tailwind.config.js
├── data/
│   ├── investors/        # Investor data
│   ├── news/             # News articles
│   └── policies/         # Government policies
└── requirements.txt
```

## 🎯 How It Works

1. **Onboarding** - Enter your startup details (domain, stage, geography, etc.)
2. **AI Analysis** - Our AI analyzes your profile and generates insights
3. **Dashboard** - View matched investors, market analysis, policy guidance
4. **Chat** - Ask questions and get personalized recommendations

## 🔧 Configuration

Create a `.env` file in the `backend` directory:

```env
# Mistral AI API Key (optional - mock data used without it)
MISTRAL_API_KEY=your_api_key_here
LLM_MODEL=mistral-small-latest

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Vector Store
CHROMA_PERSIST_DIRECTORY=./chroma_db
```

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/onboard` | POST | Submit startup profile |
| `/api/dashboard` | POST | Get full analysis |
| `/api/chat` | POST | AI chat endpoint |
| `/api/news` | GET | Get news ticker data |
| `/health` | GET | Health check |

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for your own purposes.

# VenturePilot AI - Frontend

A stunning, modern React frontend for VenturePilot AI - the AI-powered startup analysis and investor matching platform.

## Features

- 🚀 **Elegant Landing Page** - Beautiful hero section with animated backgrounds
- 📝 **Multi-step Onboarding** - Intuitive startup profile creation wizard
- 📊 **Interactive Dashboard** - Comprehensive analytics and insights
- 📰 **Live News Ticker** - Real-time scrolling news feed
- 💬 **AI Chat Assistant** - Interactive chatbot for Q&A
- 📈 **Charts & Analytics** - Visual market analysis with Recharts
- 🎨 **Modern UI** - Glass morphism, gradients, and smooth animations

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Recharts** - Interactive charts
- **Lucide React** - Beautiful icons

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Backend server running on port 8000

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Running with Backend

Make sure the backend server is running first:

```bash
# In the backend directory
cd backend
uvicorn main:app --reload --port 8000
```

Then start the frontend:

```bash
# In the frontend directory
npm run dev
```

## Project Structure

```
frontend/
├── app/
│   ├── globals.css      # Global styles and Tailwind imports
│   ├── layout.tsx       # Root layout with metadata
│   └── page.tsx         # Main page component
├── components/
│   ├── Hero.tsx         # Landing page hero section
│   ├── Navbar.tsx       # Navigation bar
│   ├── Features.tsx     # Features section
│   ├── OnboardingForm.tsx # Multi-step form wizard
│   ├── Dashboard.tsx    # Main dashboard view
│   ├── InvestorCard.tsx # Investor match card
│   ├── MarketChart.tsx  # Market analysis charts
│   ├── StrategyCard.tsx # Strategy recommendations
│   ├── NewsTicker.tsx   # Scrolling news ticker
│   ├── ChatBot.tsx      # AI chat assistant
│   ├── LoadingScreen.tsx # Loading animation
│   └── Footer.tsx       # Footer component
├── package.json
├── tailwind.config.js
├── tsconfig.json
└── next.config.js
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## API Integration

The frontend connects to the backend API at `http://localhost:8000`. The `next.config.js` is configured to proxy API requests:

- `/api/onboard` - Submit startup profile
- `/api/dashboard` - Get full analysis
- `/api/chat` - AI chat endpoint
- `/api/news` - Get news for ticker

## Customization

### Colors

Edit `tailwind.config.js` to customize the color palette:

```javascript
colors: {
  primary: { ... },  // Blue gradient
  accent: { ... },   // Purple/pink gradient
  dark: { ... },     // Dark theme colors
}
```

### Animations

Animations are defined in `tailwind.config.js` under `animation` and `keyframes`.

## License

MIT

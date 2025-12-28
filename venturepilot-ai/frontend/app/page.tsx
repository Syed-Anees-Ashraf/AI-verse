'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Hero from '@/components/Hero';
import Navbar from '@/components/Navbar';
import OnboardingForm from '@/components/OnboardingForm';
import Dashboard from '@/components/Dashboard';
import NewsTicker from '@/components/NewsTicker';
import Features from '@/components/Features';
import Footer from '@/components/Footer';
import ChatBot from '@/components/ChatBot';
import LoadingScreen from '@/components/LoadingScreen';

export interface StartupProfile {
  description: string;
  domain: string;
  stage: string;
  geography: string;
  customer_type: string;
  problem?: string;
  value_proposition?: string;
  market_category?: string;
  target_customers?: string;
  assumed_competitors?: string[];
  risk_factors?: string[];
}

export interface DashboardData {
  startup_profile: StartupProfile;
  policy: {
    relevant_policies: string[];
    eligible_schemes: string[];
    regulatory_risks: string[];
  };
  investors: {
    name: string;
    match_score: number;
    reason: string;
    past_investments: string[];
  }[];
  market: {
    market_size_estimate: string;
    growth_signals: string[];
    saturation_risks: string[];
    emerging_trends: string[];
  };
  news: {
    opportunities: string[];
    risks: string[];
    recent_events: string[];
  };
  strategy: {
    fundraising_readiness: 'low' | 'medium' | 'high';
    key_recommendations: string[];
    next_actions: string[];
  };
}

export default function Home() {
  const [currentView, setCurrentView] = useState<'landing' | 'onboarding' | 'dashboard'>('landing');
  const [startupProfile, setStartupProfile] = useState<StartupProfile | null>(null);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isChatOpen, setIsChatOpen] = useState(false);

  const handleStartOnboarding = () => {
    setCurrentView('onboarding');
  };

  const handleOnboardingComplete = async (profile: StartupProfile) => {
    setStartupProfile(profile);
    setIsLoading(true);
    
    try {
      // Call the dashboard API
      const response = await fetch('/api/dashboard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(profile),
      });

      if (!response.ok) {
        throw new Error('Failed to fetch dashboard data');
      }

      const data = await response.json();
      console.log('=== FRONTEND RECEIVED DASHBOARD DATA ===');
      console.log('Investors:', data.investors?.length, data.investors?.[0]?.name);
      console.log('Market:', data.market?.market_size_estimate);
      console.log('News opportunities:', data.news?.opportunities?.length);
      console.log('Strategy:', data.strategy?.fundraising_readiness);
      console.log('Full data:', JSON.stringify(data, null, 2));
      setDashboardData(data);
      setCurrentView('dashboard');
    } catch (error) {
      console.error('Error fetching dashboard:', error);
      // Use mock data for demo purposes
      setDashboardData(getMockDashboardData(profile));
      setCurrentView('dashboard');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToLanding = () => {
    setCurrentView('landing');
    setStartupProfile(null);
    setDashboardData(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-950 to-[#1e1b4b]">
      <Navbar 
        onLogoClick={handleBackToLanding} 
        showDashboardNav={currentView === 'dashboard'}
        onChatClick={() => setIsChatOpen(true)}
      />
      
      {/* News Ticker - Always visible */}
      <NewsTicker />
      
      <AnimatePresence mode="wait">
        {isLoading && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <LoadingScreen />
          </motion.div>
        )}

        {!isLoading && currentView === 'landing' && (
          <motion.div
            key="landing"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.5 }}
          >
            <Hero onGetStarted={handleStartOnboarding} />
            <Features />
            <Footer />
          </motion.div>
        )}

        {!isLoading && currentView === 'onboarding' && (
          <motion.div
            key="onboarding"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
          >
            <OnboardingForm 
              onComplete={handleOnboardingComplete}
              onBack={handleBackToLanding}
            />
          </motion.div>
        )}

        {!isLoading && currentView === 'dashboard' && dashboardData && (
          <motion.div
            key="dashboard"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.5 }}
          >
            <Dashboard data={dashboardData} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Chat Bot */}
      <ChatBot 
        isOpen={isChatOpen} 
        onClose={() => setIsChatOpen(false)}
        startupProfile={startupProfile}
      />
    </main>
  );
}

// Mock data for demo purposes
function getMockDashboardData(profile: StartupProfile): DashboardData {
  return {
    startup_profile: profile,
    policy: {
      relevant_policies: [
        'Startup India Initiative - Tax benefits and fast-track patent examination',
        'Fund of Funds for Startups (FFS) - Access to VC funding through AIFs',
        'Credit Guarantee Scheme - Collateral-free loans up to ₹10 crores'
      ],
      eligible_schemes: [
        'Startup India Seed Fund Scheme - Up to ₹50 lakhs for POC',
        'SIDBI Make in India Loan - Low-interest working capital',
        'State-specific incubation programs'
      ],
      regulatory_risks: [
        'Data privacy compliance under proposed Digital India Bill',
        'RBI guidelines for fintech/digital payments',
        'GST compliance requirements'
      ]
    },
    investors: [
      { name: 'Sequoia Capital India', match_score: 92, reason: 'Strong track record in your domain with investments in similar stage companies', past_investments: ['Razorpay', 'BharatPe', 'Groww'] },
      { name: 'Accel Partners', match_score: 88, reason: 'Active in early-stage investments with founder-friendly approach', past_investments: ['Flipkart', 'Swiggy', 'Freshworks'] },
      { name: 'Tiger Global', match_score: 85, reason: 'Fast decision-making and large check sizes for growth', past_investments: ['Slice', 'Jupiter', 'Fi Money'] },
      { name: 'Blume Ventures', match_score: 82, reason: 'Specializes in seed-stage with hands-on support', past_investments: ['Slice', 'Unacademy', 'Dunzo'] },
      { name: 'Matrix Partners India', match_score: 78, reason: 'Deep expertise in your sector with strong portfolio', past_investments: ['Razorpay', 'Ola', 'Practo'] },
    ],
    market: {
      market_size_estimate: '$45 billion by 2026, growing at 22% CAGR',
      growth_signals: [
        'Increasing digital adoption post-pandemic',
        'Government push for digitalization',
        'Rising smartphone penetration',
        'Growing middle class with disposable income'
      ],
      saturation_risks: [
        'Intense competition from established players',
        'High customer acquisition costs',
        'Regulatory uncertainty'
      ],
      emerging_trends: [
        'AI/ML integration in products',
        'Embedded finance solutions',
        'Sustainability focus',
        'Cross-border expansion opportunities'
      ]
    },
    news: {
      opportunities: [
        'Recent funding surge in your sector indicates strong investor interest',
        'Government incentives announced for startups in your domain',
        'Partnership opportunities with established corporates'
      ],
      risks: [
        'Economic slowdown affecting funding rounds',
        'Regulatory changes may impact business model',
        'Increasing competition from well-funded competitors'
      ],
      recent_events: [
        'Indian startup ecosystem sees record $18B funding in 2024',
        'Digital India 2.0 launched with ₹10,000 crore AI mission',
        'RBI introduces new digital lending guidelines',
        'Quick commerce achieves profitability milestone'
      ]
    },
    strategy: {
      fundraising_readiness: 'medium',
      key_recommendations: [
        'Strengthen unit economics before approaching Series A investors',
        'Build strategic partnerships to expand market reach',
        'Focus on customer retention alongside acquisition',
        'Consider applying for government schemes for non-dilutive funding'
      ],
      next_actions: [
        'Prepare detailed financial projections for next 3 years',
        'Build relationships with top 3 matched investors',
        'Apply for Startup India Seed Fund Scheme',
        'Strengthen IP portfolio with patent applications'
      ]
    }
  };
}

'use client';

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertCircle, Zap, Globe } from 'lucide-react';

interface NewsItem {
  title: string;
  category: string;
  timestamp: string;
  geography: string;
}

const defaultNews: NewsItem[] = [
  { title: "Razorpay raises $375M Series F at $7.5B valuation", category: "funding", timestamp: "2024-12-20", geography: "India" },
  { title: "Indian startup ecosystem sees record $18B funding in 2024", category: "news", timestamp: "2024-12-25", geography: "India" },
  { title: "Digital India 2.0 launches with ₹10,000 crore AI mission", category: "policy", timestamp: "2024-12-10", geography: "India" },
  { title: "AI startup funding surges globally with $25B in Q4 2024", category: "news", timestamp: "2024-12-23", geography: "Global" },
  { title: "RBI releases new guidelines for digital lending", category: "policy", timestamp: "2024-12-15", geography: "India" },
  { title: "PhonePe crosses 500 million registered users", category: "news", timestamp: "2024-12-22", geography: "India" },
  { title: "Quick commerce achieves profitability milestone", category: "news", timestamp: "2024-12-19", geography: "India" },
  { title: "Zerodha becomes India's most profitable brokerage", category: "funding", timestamp: "2024-12-18", geography: "India" },
];

const getCategoryIcon = (category: string) => {
  switch (category) {
    case 'funding': return TrendingUp;
    case 'policy': return AlertCircle;
    default: return Zap;
  }
};

const getCategoryColor = (category: string) => {
  switch (category) {
    case 'funding': return 'text-green-400';
    case 'policy': return 'text-amber-400';
    default: return 'text-primary-400';
  }
};

export default function NewsTicker() {
  const [news, setNews] = useState<NewsItem[]>(defaultNews);
  const [isPaused, setIsPaused] = useState(false);

  useEffect(() => {
    // Fetch news from API if available
    const fetchNews = async () => {
      try {
        const response = await fetch('/api/news');
        if (response.ok) {
          const data = await response.json();
          if (data && Array.isArray(data)) {
            setNews(data.map((item: any) => ({
              title: item.title || item.text?.substring(0, 100),
              category: item.category || 'news',
              timestamp: item.timestamp,
              geography: item.geography
            })));
          }
        }
      } catch (error) {
        // Use default news if API fails
        console.log('Using default news');
      }
    };
    fetchNews();
  }, []);

  // Duplicate news for seamless scrolling
  const duplicatedNews = [...news, ...news];

  return (
    <div 
      className="fixed top-16 left-0 right-0 z-40 bg-dark-950/90 backdrop-blur-sm border-b border-white/5"
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
    >
      <div className="relative overflow-hidden py-2">
        <div className="flex items-center">
          {/* Label */}
          <div className="flex-shrink-0 px-4 py-1 bg-gradient-to-r from-primary-500/20 to-accent-500/20 border-r border-white/10 flex items-center gap-2">
            <Globe className="w-4 h-4 text-primary-400" />
            <span className="text-xs font-semibold text-white uppercase tracking-wider">Live News</span>
          </div>

          {/* Scrolling Container */}
          <div className="flex-1 overflow-hidden">
            <motion.div
              className="flex gap-8 whitespace-nowrap"
              animate={{
                x: isPaused ? 0 : [0, -50 * news.length],
              }}
              transition={{
                x: {
                  duration: news.length * 5,
                  repeat: Infinity,
                  ease: "linear",
                },
              }}
            >
              {duplicatedNews.map((item, index) => {
                const Icon = getCategoryIcon(item.category);
                const colorClass = getCategoryColor(item.category);
                
                return (
                  <div
                    key={index}
                    className="flex items-center gap-3 px-4 py-1 cursor-pointer hover:bg-white/5 rounded-lg transition-colors"
                  >
                    <Icon className={`w-4 h-4 ${colorClass}`} />
                    <span className="text-sm text-gray-300">{item.title}</span>
                    <span className="text-xs text-gray-500 px-2 py-0.5 rounded-full bg-white/5">
                      {item.geography}
                    </span>
                  </div>
                );
              })}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}

'use client';

import { motion } from 'framer-motion';
import { Rocket, Sparkles, TrendingUp, Target, ArrowRight } from 'lucide-react';
import { useState, useEffect } from 'react';

interface HeroProps {
  onGetStarted: () => void;
}

// Pre-defined particle positions to avoid hydration mismatch
const PARTICLE_POSITIONS = [
  { left: 10, top: 15 }, { left: 25, top: 80 }, { left: 45, top: 20 },
  { left: 70, top: 60 }, { left: 85, top: 30 }, { left: 15, top: 45 },
  { left: 55, top: 75 }, { left: 90, top: 85 }, { left: 35, top: 55 },
  { left: 60, top: 10 }, { left: 5, top: 70 }, { left: 75, top: 45 },
  { left: 40, top: 90 }, { left: 20, top: 35 }, { left: 95, top: 50 },
  { left: 30, top: 5 }, { left: 80, top: 70 }, { left: 50, top: 40 },
  { left: 65, top: 95 }, { left: 12, top: 60 }
];

export default function Hero({ onGetStarted }: HeroProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-500/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-accent-500/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gradient-radial from-primary-500/10 to-transparent rounded-full" />
        
        {/* Floating Elements - Only render after mount to avoid hydration mismatch */}
        {mounted && PARTICLE_POSITIONS.map((pos, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 bg-primary-400/30 rounded-full"
            style={{
              left: `${pos.left}%`,
              top: `${pos.top}%`,
            }}
            animate={{
              y: [0, -30, 0],
              opacity: [0.3, 0.8, 0.3],
            }}
            transition={{
              duration: 3 + (i % 3),
              repeat: Infinity,
              delay: (i % 5) * 0.4,
            }}
          />
        ))}
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        {/* Badge */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass mb-8"
        >
          <Sparkles className="w-4 h-4 text-accent-400" />
          <span className="text-sm text-gray-300">AI-Powered Investor Matching</span>
        </motion.div>

        {/* Main Heading */}
        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-5xl md:text-7xl font-bold mb-6"
        >
          <span className="text-white">Find Your </span>
          <span className="gradient-text">Ideal Investors</span>
          <br />
          <span className="text-white">with </span>
          <span className="gradient-text">AI Intelligence</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="text-xl text-gray-400 max-w-3xl mx-auto mb-10"
        >
          VenturePilot AI analyzes your startup, matches you with the perfect investors, 
          provides market insights, and delivers strategic recommendations — all powered by advanced AI.
        </motion.p>

        {/* CTA Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
        >
          <button
            onClick={onGetStarted}
            className="group relative px-8 py-4 bg-gradient-to-r from-primary-500 to-accent-500 rounded-xl font-semibold text-white text-lg glow-button overflow-hidden transition-all duration-300 hover:shadow-glow-lg"
          >
            <span className="relative z-10 flex items-center gap-2">
              Get Started Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </span>
          </button>
          
          <button className="px-8 py-4 rounded-xl font-semibold text-white text-lg glass hover:bg-white/10 transition-all duration-300 flex items-center gap-2">
            <span>Watch Demo</span>
            <Sparkles className="w-5 h-5 text-accent-400" />
          </button>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8"
        >
          {[
            { icon: Target, value: '500+', label: 'Investors Matched' },
            { icon: Rocket, value: '150+', label: 'Startups Analyzed' },
            { icon: TrendingUp, value: '₹250Cr+', label: 'Funding Facilitated' },
            { icon: Sparkles, value: '98%', label: 'Match Accuracy' },
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: 0.6 + index * 0.1 }}
              className="text-center"
            >
              <div className="flex justify-center mb-3">
                <div className="p-3 rounded-xl glass">
                  <stat.icon className="w-6 h-6 text-primary-400" />
                </div>
              </div>
              <div className="text-3xl font-bold gradient-text">{stat.value}</div>
              <div className="text-sm text-gray-400 mt-1">{stat.label}</div>
            </motion.div>
          ))}
        </motion.div>

        {/* Trusted By */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.8 }}
          className="mt-20"
        >
          <p className="text-sm text-gray-500 mb-6">Trusted by startups backed by</p>
          <div className="flex flex-wrap justify-center items-center gap-8 opacity-50">
            {['Sequoia', 'Accel', 'Tiger Global', 'Blume', 'Matrix'].map((name) => (
              <div key={name} className="text-lg font-semibold text-gray-400">
                {name}
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1, duration: 0.5 }}
        className="absolute bottom-8 left-1/2 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="w-6 h-10 rounded-full border-2 border-gray-500 flex justify-center pt-2"
        >
          <motion.div className="w-1.5 h-1.5 bg-primary-400 rounded-full" />
        </motion.div>
      </motion.div>
    </section>
  );
}

'use client';

import { motion } from 'framer-motion';
import { Target, Lightbulb, ArrowRight, CheckCircle, Zap, TrendingUp, Shield, Rocket } from 'lucide-react';

interface Strategy {
  fundraising_readiness: 'low' | 'medium' | 'high';
  key_recommendations: string[];
  next_actions: string[];
}

interface StrategyCardProps {
  strategy: Strategy;
}

export default function StrategyCard({ strategy }: StrategyCardProps) {
  const getReadinessData = (readiness: string) => {
    switch (readiness) {
      case 'high':
        return {
          color: 'text-green-400',
          bg: 'from-green-500/20 to-emerald-500/20',
          border: 'border-green-500/30',
          percentage: 85,
          ringColor: 'stroke-green-500',
          message: 'Strong potential for fundraising',
          icon: Rocket,
          gradient: 'from-green-500 to-emerald-500'
        };
      case 'medium':
        return {
          color: 'text-amber-400',
          bg: 'from-amber-500/20 to-orange-500/20',
          border: 'border-amber-500/30',
          percentage: 60,
          ringColor: 'stroke-amber-500',
          message: 'Improvements recommended',
          icon: TrendingUp,
          gradient: 'from-amber-500 to-orange-500'
        };
      case 'low':
        return {
          color: 'text-red-400',
          bg: 'from-red-500/20 to-rose-500/20',
          border: 'border-red-500/30',
          percentage: 35,
          ringColor: 'stroke-red-500',
          message: 'Focus on fundamentals first',
          icon: Shield,
          gradient: 'from-red-500 to-rose-500'
        };
      default:
        return {
          color: 'text-gray-400',
          bg: 'from-gray-500/20 to-slate-500/20',
          border: 'border-gray-500/30',
          percentage: 50,
          ringColor: 'stroke-gray-500',
          message: 'Analysis pending',
          icon: Target,
          gradient: 'from-gray-500 to-slate-500'
        };
    }
  };

  const readinessData = getReadinessData(strategy.fundraising_readiness);
  const IconComponent = readinessData.icon;
  
  // For circular gauge
  const circumference = 2 * Math.PI * 45;
  const strokeDashoffset = circumference - (readinessData.percentage / 100) * circumference;

  return (
    <div className="glass rounded-2xl p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center gap-2">
        <Target className="w-5 h-5 text-primary-400" />
        <h2 className="text-lg font-semibold text-white">Strategy & Readiness</h2>
      </div>

      {/* Large Circular Gauge */}
      <div className={`p-6 rounded-2xl bg-gradient-to-br ${readinessData.bg} border ${readinessData.border}`}>
        <div className="flex items-center justify-center">
          <div className="relative">
            <svg className="w-32 h-32 transform -rotate-90">
              <circle
                cx="64"
                cy="64"
                r="45"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                className="text-dark-800"
              />
              <motion.circle
                cx="64"
                cy="64"
                r="45"
                strokeWidth="8"
                fill="transparent"
                strokeLinecap="round"
                className={readinessData.ringColor}
                initial={{ strokeDashoffset: circumference }}
                animate={{ strokeDashoffset }}
                transition={{ duration: 1.5, ease: 'easeOut' }}
                style={{ strokeDasharray: circumference }}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <IconComponent className={`w-6 h-6 ${readinessData.color} mb-1`} />
              <span className={`text-2xl font-bold ${readinessData.color}`}>
                {readinessData.percentage}%
              </span>
            </div>
          </div>
        </div>
        
        <div className="text-center mt-4">
          <p className={`text-lg font-semibold capitalize ${readinessData.color}`}>
            {strategy.fundraising_readiness} Readiness
          </p>
          <p className="text-sm text-gray-400 mt-1">{readinessData.message}</p>
        </div>

        {/* Mini Stats Row */}
        <div className="grid grid-cols-3 gap-2 mt-4">
          <div className="text-center p-2 rounded-lg bg-dark-800/50">
            <p className="text-lg font-bold text-primary-400">{strategy.key_recommendations.length}</p>
            <p className="text-[10px] text-gray-500 uppercase">Tips</p>
          </div>
          <div className="text-center p-2 rounded-lg bg-dark-800/50">
            <p className="text-lg font-bold text-accent-400">{strategy.next_actions.length}</p>
            <p className="text-[10px] text-gray-500 uppercase">Actions</p>
          </div>
          <div className="text-center p-2 rounded-lg bg-dark-800/50">
            <p className="text-lg font-bold text-green-400">A+</p>
            <p className="text-[10px] text-gray-500 uppercase">Grade</p>
          </div>
        </div>
      </div>

      {/* Key Recommendations - Visual Cards */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Lightbulb className="w-4 h-4 text-amber-400" />
          <h3 className="text-sm font-medium text-gray-400">Key Recommendations</h3>
        </div>
        
        <div className="space-y-2">
          {strategy.key_recommendations.slice(0, 3).map((rec, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="p-3 rounded-xl bg-gradient-to-r from-amber-500/10 to-transparent border-l-2 border-amber-500"
            >
              <div className="flex items-start gap-2">
                <div className="w-5 h-5 rounded-full bg-amber-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                  <Zap className="w-3 h-3 text-amber-400" />
                </div>
                <span className="text-sm text-gray-300">{rec}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Next Actions - Timeline Style */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <ArrowRight className="w-4 h-4 text-primary-400" />
          <h3 className="text-sm font-medium text-gray-400">Action Plan</h3>
        </div>
        
        <div className="relative pl-4">
          {/* Timeline Line */}
          <div className="absolute left-1.5 top-2 bottom-2 w-0.5 bg-gradient-to-b from-primary-500 via-accent-500 to-transparent" />
          
          <div className="space-y-3">
            {strategy.next_actions.slice(0, 4).map((action, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
                className="relative flex items-start gap-3"
              >
                {/* Timeline Dot */}
                <div className={`absolute -left-4 w-3 h-3 rounded-full bg-gradient-to-r ${
                  index === 0 ? 'from-primary-500 to-accent-500' : 'from-dark-600 to-dark-700'
                } border-2 border-dark-900`} />
                
                <div className={`flex-1 p-2 rounded-lg ${
                  index === 0 ? 'bg-primary-500/10 border border-primary-500/20' : 'bg-dark-800/50'
                }`}>
                  <div className="flex items-center gap-2">
                    <span className={`text-xs font-medium ${
                      index === 0 ? 'text-primary-400' : 'text-gray-500'
                    }`}>
                      Step {index + 1}
                    </span>
                    {index === 0 && (
                      <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-primary-500/20 text-primary-400">
                        Priority
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-300 mt-1">{action}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Button */}
      <motion.button 
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="w-full py-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-medium hover:shadow-glow transition-all flex items-center justify-center gap-2"
      >
        <CheckCircle className="w-4 h-4" />
        Generate Full Report
      </motion.button>
    </div>
  );
}

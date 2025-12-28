'use client';

import { motion } from 'framer-motion';
import { Star, TrendingUp, Building2, ExternalLink, Award, Zap } from 'lucide-react';

interface Investor {
  name: string;
  match_score: number;
  reason: string;
  past_investments: string[];
}

interface InvestorCardProps {
  investor: Investor;
  rank: number;
}

export default function InvestorCard({ investor, rank }: InvestorCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 85) return 'text-green-400';
    if (score >= 70) return 'text-amber-400';
    return 'text-gray-400';
  };

  const getScoreBg = (score: number) => {
    if (score >= 85) return 'from-green-500 to-emerald-500';
    if (score >= 70) return 'from-amber-500 to-orange-500';
    return 'from-gray-500 to-slate-500';
  };

  const getScoreRing = (score: number) => {
    if (score >= 85) return 'stroke-green-500';
    if (score >= 70) return 'stroke-amber-500';
    return 'stroke-gray-500';
  };

  const getRankBadge = (rank: number) => {
    if (rank === 1) return { bg: 'bg-gradient-to-r from-yellow-500 to-amber-500', icon: '🥇' };
    if (rank === 2) return { bg: 'bg-gradient-to-r from-gray-300 to-gray-400', icon: '🥈' };
    if (rank === 3) return { bg: 'bg-gradient-to-r from-orange-600 to-orange-700', icon: '🥉' };
    return { bg: 'bg-dark-700', icon: rank.toString() };
  };

  const rankInfo = getRankBadge(rank);
  const circumference = 2 * Math.PI * 28;
  const strokeDashoffset = circumference - (investor.match_score / 100) * circumference;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: rank * 0.1 }}
      className="group p-5 rounded-2xl bg-gradient-to-br from-dark-800/80 to-dark-900/80 hover:from-dark-800 hover:to-dark-800 border border-white/5 hover:border-primary-500/30 transition-all shadow-lg hover:shadow-xl"
    >
      <div className="flex items-start gap-4">
        {/* Circular Score Gauge */}
        <div className="relative flex-shrink-0">
          <svg className="w-20 h-20 transform -rotate-90">
            <circle
              cx="40"
              cy="40"
              r="28"
              stroke="currentColor"
              strokeWidth="6"
              fill="transparent"
              className="text-dark-700"
            />
            <motion.circle
              cx="40"
              cy="40"
              r="28"
              strokeWidth="6"
              fill="transparent"
              strokeLinecap="round"
              className={getScoreRing(investor.match_score)}
              initial={{ strokeDashoffset: circumference }}
              animate={{ strokeDashoffset }}
              transition={{ duration: 1, delay: rank * 0.1 }}
              style={{ strokeDasharray: circumference }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <span className={`text-lg font-bold ${getScoreColor(investor.match_score)}`}>
              {investor.match_score}
            </span>
            <span className="text-[8px] text-gray-500 uppercase">Match</span>
          </div>
          {/* Rank Badge */}
          <div className={`absolute -top-1 -right-1 w-6 h-6 rounded-full ${rankInfo.bg} flex items-center justify-center text-xs font-bold text-white shadow-lg`}>
            {rank <= 3 ? rankInfo.icon : rank}
          </div>
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h3 className="text-lg font-semibold text-white group-hover:text-primary-400 transition-colors truncate">
              {investor.name}
            </h3>
            {rank === 1 && <Award className="w-4 h-4 text-yellow-500" />}
            <ExternalLink className="w-4 h-4 text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0" />
          </div>
          
          <p className="text-sm text-gray-400 line-clamp-2 mb-3">{investor.reason}</p>
          
          {/* Past Investments as Tags */}
          <div className="flex flex-wrap gap-1.5">
            {investor.past_investments.slice(0, 4).map((inv, i) => (
              <motion.span 
                key={i}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: rank * 0.1 + i * 0.05 }}
                className="text-xs px-2.5 py-1 rounded-full bg-gradient-to-r from-primary-500/20 to-accent-500/20 text-primary-300 border border-primary-500/20"
              >
                {inv}
              </motion.span>
            ))}
            {investor.past_investments.length > 4 && (
              <span className="text-xs px-2.5 py-1 rounded-full bg-dark-700 text-gray-500">
                +{investor.past_investments.length - 4}
              </span>
            )}
          </div>
        </div>

        {/* Quick Stats */}
        <div className="hidden md:flex flex-col gap-2 items-end">
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Zap className="w-3 h-3 text-primary-400" />
            <span>Active</span>
          </div>
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Building2 className="w-3 h-3 text-accent-400" />
            <span>{investor.past_investments.length}+ deals</span>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

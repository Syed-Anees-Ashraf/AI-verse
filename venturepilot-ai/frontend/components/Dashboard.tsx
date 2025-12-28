'use client';

import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Users, 
  Shield, 
  Newspaper, 
  Target,
  AlertTriangle,
  CheckCircle,
  ArrowUpRight,
  Building2,
  MapPin,
  Layers,
  Sparkles,
  Zap,
  Award,
  Activity,
  PieChart
} from 'lucide-react';
import { DashboardData } from '@/app/page';
import InvestorCard from './InvestorCard';
import MarketChart from './MarketChart';
import StrategyCard from './StrategyCard';

interface DashboardProps {
  data: DashboardData;
}

// Mini Circular Gauge Component
const MiniGauge = ({ value, max, color, icon: Icon, label, size = 80 }: { 
  value: number; 
  max: number; 
  color: string; 
  icon: any;
  label: string;
  size?: number;
}) => {
  const percentage = Math.min((value / max) * 100, 100);
  const radius = (size - 10) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;
  
  return (
    <div className="flex flex-col items-center">
      <div className="relative" style={{ width: size, height: size }}>
        {/* Background ring */}
        <svg className="absolute inset-0" style={{ width: size, height: size }}>
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="rgba(255,255,255,0.1)"
            strokeWidth="6"
          />
        </svg>
        {/* Progress ring */}
        <svg className="absolute inset-0 -rotate-90" style={{ width: size, height: size }}>
          <motion.circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.2, ease: "easeOut" }}
          />
        </svg>
        {/* Icon and value */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <Icon className="w-4 h-4 mb-1" style={{ color }} />
          <span className="text-lg font-bold text-white">{value}</span>
        </div>
      </div>
      <span className="text-xs text-gray-400 mt-2 text-center">{label}</span>
    </div>
  );
};

export default function Dashboard({ data }: DashboardProps) {
  const { startup_profile, policy, investors, market, news, strategy } = data;

  // Safe defaults for potentially empty/undefined data
  const safePolicy = {
    relevant_policies: policy?.relevant_policies || [],
    eligible_schemes: policy?.eligible_schemes || [],
    regulatory_risks: policy?.regulatory_risks || []
  };

  const safeNews = {
    opportunities: news?.opportunities || [],
    risks: news?.risks || [],
    recent_events: news?.recent_events || []
  };

  const safeMarket = {
    market_size_estimate: market?.market_size_estimate || 'Data not available',
    growth_signals: market?.growth_signals || [],
    saturation_risks: market?.saturation_risks || [],
    emerging_trends: market?.emerging_trends || []
  };

  const safeStrategy = {
    fundraising_readiness: strategy?.fundraising_readiness || 'medium',
    key_recommendations: strategy?.key_recommendations || [],
    next_actions: strategy?.next_actions || []
  };

  const safeInvestors = investors || [];

  const getFundraisingColor = (readiness: string) => {
    switch (readiness) {
      case 'high': return 'text-green-400';
      case 'medium': return 'text-amber-400';
      case 'low': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getFundraisingBg = (readiness: string) => {
    switch (readiness) {
      case 'high': return 'from-green-500/20 to-emerald-500/20';
      case 'medium': return 'from-amber-500/20 to-orange-500/20';
      case 'low': return 'from-red-500/20 to-rose-500/20';
      default: return 'from-gray-500/20 to-slate-500/20';
    }
  };

  return (
    <div className="min-h-screen pt-28 pb-12 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                Your Startup Dashboard
              </h1>
              <p className="text-gray-400">
                AI-powered analysis and recommendations for your startup
              </p>
            </div>
            
            {/* Fundraising Readiness Badge */}
            <div className={`inline-flex items-center gap-3 px-6 py-3 rounded-xl bg-gradient-to-r ${getFundraisingBg(safeStrategy.fundraising_readiness)}`}>
              <Target className={`w-5 h-5 ${getFundraisingColor(safeStrategy.fundraising_readiness)}`} />
              <div>
                <p className="text-xs text-gray-400">Fundraising Readiness</p>
                <p className={`text-lg font-bold capitalize ${getFundraisingColor(safeStrategy.fundraising_readiness)}`}>
                  {safeStrategy.fundraising_readiness}
                </p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Visual Stats Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05 }}
          className="glass rounded-2xl p-6 mb-8"
        >
          <div className="flex items-center gap-2 mb-6">
            <Activity className="w-5 h-5 text-primary-400" />
            <h2 className="text-lg font-semibold text-white">Analysis Overview</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-5 gap-6 justify-items-center">
            <MiniGauge 
              value={safeInvestors.length} 
              max={10} 
              color="#0ea5e9" 
              icon={Users} 
              label="Investor Matches" 
            />
            <MiniGauge 
              value={safeMarket.growth_signals.length} 
              max={5} 
              color="#10b981" 
              icon={TrendingUp} 
              label="Growth Signals" 
            />
            <MiniGauge 
              value={safePolicy.eligible_schemes.length} 
              max={5} 
              color="#8b5cf6" 
              icon={Award} 
              label="Eligible Schemes" 
            />
            <MiniGauge 
              value={safeNews.opportunities.length} 
              max={5} 
              color="#f59e0b" 
              icon={Zap} 
              label="Opportunities" 
            />
            <MiniGauge 
              value={safeStrategy.key_recommendations.length} 
              max={5} 
              color="#ec4899" 
              icon={Target} 
              label="Key Actions" 
            />
          </div>
          
          {/* Overall Score Bar */}
          <div className="mt-6 pt-6 border-t border-white/10">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-gray-400">Overall Analysis Strength</span>
              <span className="text-sm font-medium text-primary-400">
                {Math.round((safeInvestors.length * 10 + safeMarket.growth_signals.length * 15 + safePolicy.eligible_schemes.length * 10 + safeNews.opportunities.length * 10 + safeStrategy.key_recommendations.length * 10) / 5)}%
              </span>
            </div>
            <div className="h-3 bg-dark-700 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${Math.min((safeInvestors.length * 10 + safeMarket.growth_signals.length * 15 + safePolicy.eligible_schemes.length * 10 + safeNews.opportunities.length * 10 + safeStrategy.key_recommendations.length * 10) / 5, 100)}%` }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                className="h-full bg-gradient-to-r from-primary-500 via-accent-500 to-pink-500 rounded-full"
              />
            </div>
          </div>
        </motion.div>

        {/* Startup Profile Summary */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="glass rounded-2xl p-6 mb-8"
        >
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-primary-400" />
            <h2 className="text-lg font-semibold text-white">Startup Profile</h2>
          </div>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-dark-800/50">
              <div className="flex items-center gap-2 mb-2">
                <Building2 className="w-4 h-4 text-primary-400" />
                <span className="text-xs text-gray-400">Domain</span>
              </div>
              <p className="text-white font-medium">{startup_profile.domain}</p>
            </div>
            <div className="p-4 rounded-xl bg-dark-800/50">
              <div className="flex items-center gap-2 mb-2">
                <Layers className="w-4 h-4 text-accent-400" />
                <span className="text-xs text-gray-400">Stage</span>
              </div>
              <p className="text-white font-medium">{startup_profile.stage}</p>
            </div>
            <div className="p-4 rounded-xl bg-dark-800/50">
              <div className="flex items-center gap-2 mb-2">
                <MapPin className="w-4 h-4 text-green-400" />
                <span className="text-xs text-gray-400">Geography</span>
              </div>
              <p className="text-white font-medium">{startup_profile.geography}</p>
            </div>
            <div className="p-4 rounded-xl bg-dark-800/50">
              <div className="flex items-center gap-2 mb-2">
                <Users className="w-4 h-4 text-amber-400" />
                <span className="text-xs text-gray-400">Customer Type</span>
              </div>
              <p className="text-white font-medium">{startup_profile.customer_type}</p>
            </div>
          </div>

          {startup_profile.value_proposition && (
            <div className="mt-4 p-4 rounded-xl bg-gradient-to-r from-primary-500/10 to-accent-500/10">
              <p className="text-sm text-gray-400 mb-1">Value Proposition</p>
              <p className="text-white">{startup_profile.value_proposition}</p>
            </div>
          )}
        </motion.div>

        {/* Main Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="space-y-6"
          >
            {/* Investors Section */}
            <div className="glass rounded-2xl p-6" id="investors">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-primary-400" />
                  <h2 className="text-xl font-semibold text-white">Top Investor Matches</h2>
                </div>
                <span className="text-sm text-gray-400">{safeInvestors.length} matches found</span>
              </div>
              
              <div className="space-y-4">
                {safeInvestors.slice(0, 5).map((investor, index) => (
                  <InvestorCard key={investor.name} investor={investor} rank={index + 1} />
                ))}
                {safeInvestors.length === 0 && (
                  <p className="text-gray-400 text-sm">No investor matches found. Try refining your startup profile.</p>
                )}
              </div>
            </div>

            {/* Strategy Card */}
            <StrategyCard strategy={safeStrategy} />
          </motion.div>

          {/* Right Column */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-6"
          >
            {/* Market Analysis */}
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-6">
                <TrendingUp className="w-5 h-5 text-green-400" />
                <h2 className="text-xl font-semibold text-white">Market Analysis</h2>
              </div>
              
              <MarketChart data={safeMarket} />
              
              {/* Market Stats */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                <div className="p-4 rounded-xl bg-dark-800/50">
                  <p className="text-sm text-gray-400 mb-2">Market Size Estimate</p>
                  <p className="text-lg font-semibold text-white">{safeMarket.market_size_estimate}</p>
                </div>
                <div className="p-4 rounded-xl bg-dark-800/50">
                  <p className="text-sm text-gray-400 mb-2">Emerging Trends</p>
                  <div className="flex flex-wrap gap-2">
                    {safeMarket.emerging_trends.slice(0, 3).map((trend, i) => (
                      <span key={i} className="text-xs px-2 py-1 rounded-full bg-primary-500/20 text-primary-300">
                        {trend.length > 30 ? trend.substring(0, 30) + '...' : trend}
                      </span>
                    ))}
                    {safeMarket.emerging_trends.length === 0 && (
                      <span className="text-xs text-gray-500">No trends data available</span>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Policy & Compliance */}
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-4">
                <Shield className="w-5 h-5 text-amber-400" />
                <h2 className="text-lg font-semibold text-white">Policy & Compliance</h2>
              </div>
              
              {/* Visual Stats */}
              <div className="grid grid-cols-3 gap-2 mb-4">
                <div className="p-3 rounded-xl bg-green-500/10 border border-green-500/20 text-center">
                  <p className="text-xl font-bold text-green-400">{safePolicy.relevant_policies.length}</p>
                  <p className="text-xs text-gray-500">Policies</p>
                </div>
                <div className="p-3 rounded-xl bg-primary-500/10 border border-primary-500/20 text-center">
                  <p className="text-xl font-bold text-primary-400">{safePolicy.eligible_schemes.length}</p>
                  <p className="text-xs text-gray-500">Schemes</p>
                </div>
                <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-center">
                  <p className="text-xl font-bold text-amber-400">{safePolicy.regulatory_risks.length}</p>
                  <p className="text-xs text-gray-500">Risks</p>
                </div>
              </div>
              
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-400 mb-2 flex items-center gap-1">
                    <CheckCircle className="w-3 h-3 text-green-400" />
                    Relevant Policies
                  </p>
                  <div className="space-y-2">
                    {safePolicy.relevant_policies.slice(0, 2).map((p, i) => (
                      <motion.div 
                        key={i} 
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="text-sm text-gray-300 p-2 rounded-lg bg-dark-800/50 flex items-start gap-2 border-l-2 border-green-500/50"
                      >
                        <ArrowUpRight className="w-3 h-3 mt-1 text-green-400 flex-shrink-0" />
                        <span>{p}</span>
                      </motion.div>
                    ))}
                    {safePolicy.relevant_policies.length === 0 && (
                      <p className="text-sm text-gray-500">No policy data available</p>
                    )}
                  </div>
                </div>
                
                <div>
                  <p className="text-sm text-gray-400 mb-2 flex items-center gap-1">
                    <AlertTriangle className="w-3 h-3 text-amber-400" />
                    Regulatory Risks
                  </p>
                  <div className="space-y-2">
                    {safePolicy.regulatory_risks.slice(0, 2).map((risk, i) => (
                      <motion.div 
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="text-sm text-gray-300 p-2 rounded-lg bg-amber-500/5 flex items-start gap-2 border-l-2 border-amber-500/50"
                      >
                        <AlertTriangle className="w-3 h-3 mt-1 text-amber-400 flex-shrink-0" />
                        <span>{risk}</span>
                      </motion.div>
                    ))}
                    {safePolicy.regulatory_risks.length === 0 && (
                      <p className="text-sm text-gray-500">No risk data available</p>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* News & Events */}
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-4">
                <Newspaper className="w-5 h-5 text-blue-400" />
                <h2 className="text-lg font-semibold text-white">News & Events</h2>
              </div>
              
              {/* Visual Stats */}
              <div className="grid grid-cols-2 gap-2 mb-4">
                <div className="p-3 rounded-xl bg-green-500/10 border border-green-500/20">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center">
                      <Zap className="w-4 h-4 text-green-400" />
                    </div>
                    <div>
                      <p className="text-lg font-bold text-green-400">{safeNews.opportunities.length}</p>
                      <p className="text-xs text-gray-500">Opportunities</p>
                    </div>
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center">
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                    </div>
                    <div>
                      <p className="text-lg font-bold text-amber-400">{safeNews.risks.length}</p>
                      <p className="text-xs text-gray-500">Risks</p>
                    </div>
                  </div>
                </div>
              </div>
              
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-400 mb-2">Opportunities</p>
                  <div className="space-y-2">
                    {safeNews.opportunities.slice(0, 2).map((opp, i) => (
                      <motion.div 
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="text-sm text-green-300 p-2 rounded-lg bg-green-500/5 flex items-start gap-2 border-l-2 border-green-500/50"
                      >
                        <CheckCircle className="w-3 h-3 mt-1 flex-shrink-0" />
                        <span>{opp}</span>
                      </motion.div>
                    ))}
                    {safeNews.opportunities.length === 0 && (
                      <p className="text-sm text-gray-500">No opportunities data available</p>
                    )}
                  </div>
                </div>
                
                <div>
                  <p className="text-sm text-gray-400 mb-2">Risks to Watch</p>
                  <div className="space-y-2">
                    {safeNews.risks.slice(0, 2).map((risk, i) => (
                      <motion.div 
                        key={i}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: i * 0.1 }}
                        className="text-sm text-amber-300 p-2 rounded-lg bg-amber-500/5 flex items-start gap-2 border-l-2 border-amber-500/50"
                      >
                        <AlertTriangle className="w-3 h-3 mt-1 flex-shrink-0" />
                        <span>{risk}</span>
                      </motion.div>
                    ))}
                    {safeNews.risks.length === 0 && (
                      <p className="text-sm text-gray-500">No risk alerts at this time</p>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

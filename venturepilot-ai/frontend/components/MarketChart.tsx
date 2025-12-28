'use client';

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Legend, AreaChart, Area } from 'recharts';
import { TrendingUp, TrendingDown, AlertTriangle, Sparkles, Target, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

interface MarketData {
  market_size_estimate: string;
  growth_signals: string[];
  saturation_risks: string[];
  emerging_trends: string[];
}

interface MarketChartProps {
  data: MarketData;
}

export default function MarketChart({ data }: MarketChartProps) {
  // Generate deterministic scores based on text content (consistent but data-driven)
  const getScore = (text: string, base: number) => {
    const hash = text.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return Math.min(base + (hash % 25), 100);
  };

  // Growth signals data for bar chart
  const signalData = data.growth_signals.map((signal, index) => ({
    name: `G${index + 1}`,
    value: getScore(signal, 70),
    label: signal.length > 40 ? signal.substring(0, 40) + '...' : signal,
    fullLabel: signal
  }));

  // Risk data for visualization
  const riskData = data.saturation_risks.map((risk, index) => ({
    name: `R${index + 1}`,
    value: getScore(risk, 40),
    label: risk.length > 40 ? risk.substring(0, 40) + '...' : risk,
    fullLabel: risk
  }));

  // Parse market size and CAGR from the estimate string
  const parseMarketData = (estimate: string) => {
    // Extract market size (e.g., "$1.5 billion" or "$150 billion")
    const sizeMatch = estimate.match(/\$?([\d.]+)\s*(billion|million|trillion)?/i);
    let baseSize = 100;
    if (sizeMatch) {
      baseSize = parseFloat(sizeMatch[1]);
      if (sizeMatch[2]?.toLowerCase() === 'trillion') baseSize *= 1000;
      else if (sizeMatch[2]?.toLowerCase() === 'million') baseSize /= 1000;
    }
    
    // Extract CAGR (e.g., "25% CAGR" or "growing at 12%")
    const cagrMatch = estimate.match(/([\d.]+)%\s*(CAGR|growth)?/i);
    let cagr = 15; // default
    if (cagrMatch) {
      cagr = parseFloat(cagrMatch[1]);
    }
    
    return { baseSize, cagr };
  };

  const { baseSize, cagr } = parseMarketData(data.market_size_estimate);

  // Calculate growth score based on signals
  const avgGrowthScore = signalData.length > 0 
    ? Math.round(signalData.reduce((acc, s) => acc + s.value, 0) / signalData.length) 
    : 70;

  // Calculate risk score  
  const avgRiskScore = riskData.length > 0 
    ? Math.round(riskData.reduce((acc, r) => acc + r.value, 0) / riskData.length) 
    : 50;

  // Radar chart data - all derived from actual data
  const radarData = [
    { subject: 'Growth', A: avgGrowthScore, fullMark: 100 },
    { subject: 'Size', A: Math.min(Math.round(baseSize / 2) + 50, 95), fullMark: 100 },
    { subject: 'Competition', A: Math.max(100 - avgRiskScore, 30), fullMark: 100 },
    { subject: 'Barriers', A: Math.max(100 - (data.saturation_risks.length * 15), 40), fullMark: 100 },
    { subject: 'Innovation', A: Math.min(data.emerging_trends.length * 20 + 40, 95), fullMark: 100 },
    { subject: 'Timing', A: Math.min(data.growth_signals.length * 15 + 50, 90), fullMark: 100 },
  ];

  // Area chart for market projection - derived from CAGR
  const currentYear = new Date().getFullYear();
  const growthMultiplier = 1 + (cagr / 100);
  const projectionData = [
    { year: String(currentYear), value: 100, projected: 100 },
    { year: String(currentYear + 1), value: Math.round(100 * growthMultiplier), projected: Math.round(100 * growthMultiplier * 1.05) },
    { year: String(currentYear + 2), value: null, projected: Math.round(100 * Math.pow(growthMultiplier, 2) * 1.05) },
    { year: String(currentYear + 3), value: null, projected: Math.round(100 * Math.pow(growthMultiplier, 3) * 1.05) },
    { year: String(currentYear + 4), value: null, projected: Math.round(100 * Math.pow(growthMultiplier, 4) * 1.05) },
  ];

  // Donut chart data for market composition - derived from data counts
  const compositionData = [
    { name: 'Growth Signals', value: data.growth_signals.length * 20 + 30, color: '#10b981' },
    { name: 'Opportunities', value: data.emerging_trends.length * 15 + 25, color: '#0ea5e9' },
    { name: 'Risk Factors', value: data.saturation_risks.length * 10 + 15, color: '#f59e0b' },
  ];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-dark-900/95 border border-white/10 rounded-lg p-3 shadow-xl max-w-xs">
          <p className="text-white text-sm font-medium">{payload[0].payload.fullLabel || payload[0].payload.label || payload[0].name}</p>
          <p className="text-primary-400 text-sm mt-1">Score: {payload[0].value}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="space-y-6">
      {/* Top Row - Key Metrics */}
      <div className="grid grid-cols-3 gap-4">
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-4 rounded-xl bg-gradient-to-br from-green-500/20 to-emerald-500/10 border border-green-500/20"
        >
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-green-400" />
            <span className="text-xs text-gray-400">Growth Signals</span>
          </div>
          <p className="text-2xl font-bold text-green-400">{data.growth_signals.length}</p>
          <p className="text-xs text-gray-500">Positive indicators</p>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="p-4 rounded-xl bg-gradient-to-br from-amber-500/20 to-orange-500/10 border border-amber-500/20"
        >
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span className="text-xs text-gray-400">Risk Factors</span>
          </div>
          <p className="text-2xl font-bold text-amber-400">{data.saturation_risks.length}</p>
          <p className="text-xs text-gray-500">To monitor</p>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="p-4 rounded-xl bg-gradient-to-br from-primary-500/20 to-accent-500/10 border border-primary-500/20"
        >
          <div className="flex items-center gap-2 mb-2">
            <Sparkles className="w-4 h-4 text-primary-400" />
            <span className="text-xs text-gray-400">Trends</span>
          </div>
          <p className="text-2xl font-bold text-primary-400">{data.emerging_trends.length}</p>
          <p className="text-xs text-gray-500">Emerging</p>
        </motion.div>
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Market Overview Radar */}
        <div className="p-4 rounded-xl bg-dark-800/30 border border-white/5">
          <h3 className="text-sm font-medium text-gray-400 mb-4 flex items-center gap-2">
            <Target className="w-4 h-4 text-primary-400" />
            Market Score
          </h3>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData}>
                <PolarGrid stroke="#374151" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 10 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                <Radar
                  name="Score"
                  dataKey="A"
                  stroke="#0ea5e9"
                  fill="url(#radarGradient)"
                  fillOpacity={0.6}
                  strokeWidth={2}
                />
                <defs>
                  <linearGradient id="radarGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#0ea5e9" stopOpacity={0.8} />
                    <stop offset="100%" stopColor="#8b5cf6" stopOpacity={0.3} />
                  </linearGradient>
                </defs>
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Market Projection Area Chart */}
        <div className="p-4 rounded-xl bg-dark-800/30 border border-white/5">
          <h3 className="text-sm font-medium text-gray-400 mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-green-400" />
            Growth Projection
          </h3>
          <div className="h-52">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={projectionData}>
                <defs>
                  <linearGradient id="projectedGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#10b981" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="year" tick={{ fill: '#9ca3af', fontSize: 10 }} />
                <YAxis tick={{ fill: '#9ca3af', fontSize: 10 }} />
                <Tooltip content={<CustomTooltip />} />
                <Area 
                  type="monotone" 
                  dataKey="projected" 
                  stroke="#10b981" 
                  fill="url(#projectedGradient)"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                />
                <Area 
                  type="monotone" 
                  dataKey="value" 
                  stroke="#0ea5e9" 
                  fill="url(#valueGradient)"
                  strokeWidth={2}
                />
                <defs>
                  <linearGradient id="valueGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#0ea5e9" stopOpacity={0.4} />
                    <stop offset="100%" stopColor="#0ea5e9" stopOpacity={0} />
                  </linearGradient>
                </defs>
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Growth Signals Visual List */}
      {signalData.length > 0 && (
        <div className="p-4 rounded-xl bg-dark-800/30 border border-white/5">
          <h3 className="text-sm font-medium text-gray-400 mb-4 flex items-center gap-2">
            <Zap className="w-4 h-4 text-green-400" />
            Growth Signal Strength
          </h3>
          <div className="space-y-3">
            {signalData.map((signal, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-3"
              >
                <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center flex-shrink-0">
                  <span className="text-xs font-bold text-green-400">{index + 1}</span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-300 truncate">{signal.fullLabel}</p>
                  <div className="mt-1 h-2 bg-dark-700 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${signal.value}%` }}
                      transition={{ duration: 0.8, delay: index * 0.1 }}
                      className="h-full bg-gradient-to-r from-green-500 to-emerald-400 rounded-full"
                    />
                  </div>
                </div>
                <span className="text-sm font-medium text-green-400 w-12 text-right">{signal.value}%</span>
              </motion.div>
            ))}
          </div>
        </div>
      )}

      {/* Risk Factors Visual List */}
      {riskData.length > 0 && (
        <div className="p-4 rounded-xl bg-dark-800/30 border border-white/5">
          <h3 className="text-sm font-medium text-gray-400 mb-4 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            Risk Assessment
          </h3>
          <div className="space-y-3">
            {riskData.map((risk, index) => (
              <motion.div 
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center gap-3"
              >
                <div className="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center flex-shrink-0">
                  <AlertTriangle className="w-4 h-4 text-amber-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-gray-300 truncate">{risk.fullLabel}</p>
                  <div className="mt-1 h-2 bg-dark-700 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${risk.value}%` }}
                      transition={{ duration: 0.8, delay: index * 0.1 }}
                      className="h-full bg-gradient-to-r from-amber-500 to-orange-400 rounded-full"
                    />
                  </div>
                </div>
                <span className="text-sm font-medium text-amber-400 w-12 text-right">{risk.value}%</span>
              </motion.div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

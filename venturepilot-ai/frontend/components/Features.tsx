'use client';

import { motion } from 'framer-motion';
import { 
  Zap, 
  Shield, 
  TrendingUp, 
  Users, 
  Brain, 
  Globe,
  BarChart3,
  FileText,
  MessageSquare
} from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Analysis',
    description: 'Our advanced AI analyzes your startup profile and generates comprehensive insights within seconds.',
    color: 'from-blue-500 to-cyan-500',
  },
  {
    icon: Users,
    title: 'Smart Investor Matching',
    description: 'Get matched with the most relevant investors based on your domain, stage, and growth potential.',
    color: 'from-purple-500 to-pink-500',
  },
  {
    icon: TrendingUp,
    title: 'Market Intelligence',
    description: 'Access real-time market analysis, growth signals, and emerging trends in your industry.',
    color: 'from-green-500 to-emerald-500',
  },
  {
    icon: Shield,
    title: 'Policy & Compliance',
    description: 'Stay informed about relevant policies, government schemes, and regulatory requirements.',
    color: 'from-orange-500 to-amber-500',
  },
  {
    icon: Zap,
    title: 'Strategic Recommendations',
    description: 'Receive actionable strategies for fundraising, growth, and market positioning.',
    color: 'from-red-500 to-rose-500',
  },
  {
    icon: Globe,
    title: 'News & Trends',
    description: 'Stay updated with the latest news, funding rounds, and industry developments.',
    color: 'from-indigo-500 to-violet-500',
  },
];

const howItWorks = [
  {
    step: 1,
    icon: FileText,
    title: 'Enter Your Startup Details',
    description: 'Provide basic information about your startup - domain, stage, geography, and description.',
  },
  {
    step: 2,
    icon: Brain,
    title: 'AI Analyzes Your Profile',
    description: 'Our AI processes your input and generates a comprehensive startup profile with insights.',
  },
  {
    step: 3,
    icon: BarChart3,
    title: 'Get Your Dashboard',
    description: 'View matched investors, market analysis, policy insights, and strategic recommendations.',
  },
  {
    step: 4,
    icon: MessageSquare,
    title: 'Chat with AI Assistant',
    description: 'Ask questions and get personalized advice from our AI-powered chat assistant.',
  },
];

export default function Features() {
  return (
    <section id="features" className="py-20 relative">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 right-0 w-96 h-96 bg-primary-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 left-0 w-96 h-96 bg-accent-500/5 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-white">Powerful </span>
            <span className="gradient-text">Features</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Everything you need to find the right investors and accelerate your startup's growth.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-24">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="group p-6 rounded-2xl glass card-hover"
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-gray-400">{feature.description}</p>
            </motion.div>
          ))}
        </div>

        {/* How It Works */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
          id="how-it-works"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-white">How It </span>
            <span className="gradient-text">Works</span>
          </h2>
          <p className="text-xl text-gray-400 max-w-2xl mx-auto">
            Get started in minutes and find your ideal investors today.
          </p>
        </motion.div>

        <div className="relative">
          {/* Connection Line */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-primary-500/50 via-accent-500/50 to-primary-500/50 -translate-y-1/2" />

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {howItWorks.map((item, index) => (
              <motion.div
                key={item.step}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                className="relative text-center"
              >
                {/* Step Number */}
                <div className="relative z-10 w-16 h-16 mx-auto mb-6 rounded-full bg-gradient-to-r from-primary-500 to-accent-500 flex items-center justify-center shadow-glow">
                  <span className="text-2xl font-bold text-white">{item.step}</span>
                </div>

                <div className="p-6 rounded-2xl glass">
                  <div className="w-10 h-10 mx-auto mb-4 rounded-lg bg-dark-800 flex items-center justify-center">
                    <item.icon className="w-5 h-5 text-primary-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-white mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-400">{item.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

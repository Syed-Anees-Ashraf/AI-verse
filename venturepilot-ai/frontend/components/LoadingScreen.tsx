'use client';

import { motion } from 'framer-motion';
import { Rocket, Loader2 } from 'lucide-react';

export default function LoadingScreen() {
  const loadingSteps = [
    'Analyzing startup profile...',
    'Matching with investors...',
    'Gathering market intelligence...',
    'Checking policy compliance...',
    'Generating strategic recommendations...',
  ];

  return (
    <div className="min-h-screen flex items-center justify-center pt-20">
      <div className="text-center max-w-md">
        {/* Animated Logo */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', duration: 0.5 }}
          className="relative inline-block mb-8"
        >
          <div className="w-24 h-24 rounded-2xl bg-gradient-to-r from-primary-500 to-accent-500 flex items-center justify-center shadow-glow-lg">
            <Rocket className="w-12 h-12 text-white" />
          </div>
          
          {/* Orbiting Circle */}
          <motion.div
            className="absolute inset-0 rounded-2xl border-2 border-primary-400/30"
            animate={{ rotate: 360 }}
            transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          />
        </motion.div>

        {/* Loading Text */}
        <motion.h2
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="text-2xl font-bold text-white mb-4"
        >
          Analyzing Your Startup
        </motion.h2>

        {/* Loading Steps */}
        <div className="space-y-3 mb-8">
          {loadingSteps.map((step, index) => (
            <motion.div
              key={step}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 + index * 0.5 }}
              className="flex items-center gap-3 justify-center"
            >
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: [0, 1, 1] }}
                transition={{ delay: 0.5 + index * 0.5, duration: 0.3 }}
              >
                <Loader2 className="w-4 h-4 text-primary-400 animate-spin" />
              </motion.div>
              <span className="text-sm text-gray-400">{step}</span>
            </motion.div>
          ))}
        </div>

        {/* Progress Bar */}
        <div className="w-full h-1 bg-dark-700 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-primary-500 to-accent-500"
            initial={{ width: 0 }}
            animate={{ width: '100%' }}
            transition={{ duration: 3, ease: 'easeInOut' }}
          />
        </div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-xs text-gray-500 mt-4"
        >
          This may take a moment as our AI analyzes your data...
        </motion.p>
      </div>
    </div>
  );
}

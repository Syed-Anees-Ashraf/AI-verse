'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  ArrowLeft, 
  ArrowRight, 
  Building2, 
  MapPin, 
  Users, 
  Layers,
  FileText,
  Sparkles,
  CheckCircle
} from 'lucide-react';
import toast from 'react-hot-toast';
import { StartupProfile } from '@/app/page';

interface OnboardingFormProps {
  onComplete: (profile: StartupProfile) => void;
  onBack: () => void;
}

const stages = ['Pre-Seed', 'Seed', 'Series A', 'Series B', 'Series C+', 'Growth'];
const customerTypes = ['B2B', 'B2C', 'B2B2C', 'D2C', 'B2G', 'Marketplace'];
const domains = [
  'Fintech', 'Healthtech', 'Edtech', 'E-commerce', 'SaaS', 'AI/ML',
  'CleanTech', 'AgriTech', 'Logistics', 'Real Estate', 'Gaming', 'Other'
];
const geographies = [
  'India', 'USA', 'UK', 'Singapore', 'UAE', 'Europe', 'Southeast Asia', 'Global'
];

export default function OnboardingForm({ onComplete, onBack }: OnboardingFormProps) {
  const [step, setStep] = useState(1);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [formData, setFormData] = useState({
    description: '',
    domain: '',
    stage: '',
    geography: '',
    customer_type: '',
  });

  const totalSteps = 5;

  const handleNext = () => {
    if (validateCurrentStep()) {
      if (step < totalSteps) {
        setStep(step + 1);
      } else {
        handleSubmit();
      }
    }
  };

  const handlePrev = () => {
    if (step > 1) {
      setStep(step - 1);
    } else {
      onBack();
    }
  };

  const validateCurrentStep = () => {
    switch (step) {
      case 1:
        if (!formData.description || formData.description.length < 50) {
          toast.error('Please provide a detailed description (at least 50 characters)');
          return false;
        }
        return true;
      case 2:
        if (!formData.domain) {
          toast.error('Please select your startup domain');
          return false;
        }
        return true;
      case 3:
        if (!formData.stage) {
          toast.error('Please select your startup stage');
          return false;
        }
        return true;
      case 4:
        if (!formData.geography) {
          toast.error('Please select your target geography');
          return false;
        }
        return true;
      case 5:
        if (!formData.customer_type) {
          toast.error('Please select your customer type');
          return false;
        }
        return true;
      default:
        return true;
    }
  };

  const handleSubmit = async () => {
    setIsAnalyzing(true);
    
    try {
      // First, try to onboard through API to get enhanced profile
      const response = await fetch('/api/onboard', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const enhancedProfile = await response.json();
        toast.success('Profile analyzed successfully!');
        onComplete(enhancedProfile);
      } else {
        // If API fails, use basic profile
        toast.success('Profile created successfully!');
        onComplete(formData as StartupProfile);
      }
    } catch (error) {
      console.error('Error during onboarding:', error);
      // Use basic profile if API is unavailable
      toast.success('Profile created successfully!');
      onComplete(formData as StartupProfile);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <motion.div
            key="step1"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500">
                <FileText className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Tell us about your startup</h3>
                <p className="text-gray-400">Describe what your startup does in detail</p>
              </div>
            </div>
            
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="We are building an AI-powered platform that helps startups find the right investors by analyzing their profile, market conditions, and investor preferences..."
              className="w-full h-48 px-4 py-3 rounded-xl bg-dark-800 border border-white/10 text-white placeholder-gray-500 focus:border-primary-500 transition-colors resize-none"
            />
            <p className="text-sm text-gray-500">
              {formData.description.length}/50 characters minimum
            </p>
          </motion.div>
        );
      
      case 2:
        return (
          <motion.div
            key="step2"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500">
                <Building2 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Select your domain</h3>
                <p className="text-gray-400">What industry does your startup operate in?</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {domains.map((domain) => (
                <button
                  key={domain}
                  onClick={() => setFormData({ ...formData, domain })}
                  className={`px-4 py-3 rounded-xl text-left transition-all ${
                    formData.domain === domain
                      ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-glow'
                      : 'bg-dark-800 text-gray-300 hover:bg-dark-700 border border-white/10'
                  }`}
                >
                  {domain}
                </button>
              ))}
            </div>
          </motion.div>
        );
      
      case 3:
        return (
          <motion.div
            key="step3"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500">
                <Layers className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">What's your stage?</h3>
                <p className="text-gray-400">Select your current funding stage</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {stages.map((stage) => (
                <button
                  key={stage}
                  onClick={() => setFormData({ ...formData, stage })}
                  className={`px-4 py-3 rounded-xl text-left transition-all ${
                    formData.stage === stage
                      ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-glow'
                      : 'bg-dark-800 text-gray-300 hover:bg-dark-700 border border-white/10'
                  }`}
                >
                  {stage}
                </button>
              ))}
            </div>
          </motion.div>
        );
      
      case 4:
        return (
          <motion.div
            key="step4"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500">
                <MapPin className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Target geography</h3>
                <p className="text-gray-400">Where is your primary market?</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {geographies.map((geo) => (
                <button
                  key={geo}
                  onClick={() => setFormData({ ...formData, geography: geo })}
                  className={`px-4 py-3 rounded-xl text-left transition-all ${
                    formData.geography === geo
                      ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-glow'
                      : 'bg-dark-800 text-gray-300 hover:bg-dark-700 border border-white/10'
                  }`}
                >
                  {geo}
                </button>
              ))}
            </div>
          </motion.div>
        );
      
      case 5:
        return (
          <motion.div
            key="step5"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-6"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500">
                <Users className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-semibold text-white">Customer type</h3>
                <p className="text-gray-400">Who are your target customers?</p>
              </div>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {customerTypes.map((type) => (
                <button
                  key={type}
                  onClick={() => setFormData({ ...formData, customer_type: type })}
                  className={`px-4 py-3 rounded-xl text-left transition-all ${
                    formData.customer_type === type
                      ? 'bg-gradient-to-r from-primary-500 to-accent-500 text-white shadow-glow'
                      : 'bg-dark-800 text-gray-300 hover:bg-dark-700 border border-white/10'
                  }`}
                >
                  {type}
                </button>
              ))}
            </div>
          </motion.div>
        );
      
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center pt-28 pb-12 px-4">
      <div className="w-full max-w-2xl">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-gray-400">Step {step} of {totalSteps}</span>
            <span className="text-sm text-gray-400">{Math.round((step / totalSteps) * 100)}%</span>
          </div>
          <div className="h-2 bg-dark-800 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-primary-500 to-accent-500"
              initial={{ width: 0 }}
              animate={{ width: `${(step / totalSteps) * 100}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Step Indicators */}
        <div className="flex justify-center gap-2 mb-8">
          {Array.from({ length: totalSteps }).map((_, index) => (
            <div
              key={index}
              className={`w-3 h-3 rounded-full transition-all ${
                index + 1 === step
                  ? 'bg-gradient-to-r from-primary-500 to-accent-500 scale-125'
                  : index + 1 < step
                  ? 'bg-primary-500'
                  : 'bg-dark-700'
              }`}
            />
          ))}
        </div>

        {/* Form Card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl p-8"
        >
          <AnimatePresence mode="wait">
            {renderStep()}
          </AnimatePresence>

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between mt-8 pt-6 border-t border-white/10">
            <button
              onClick={handlePrev}
              className="flex items-center gap-2 px-6 py-3 rounded-xl text-gray-300 hover:text-white hover:bg-dark-700 transition-all"
            >
              <ArrowLeft className="w-4 h-4" />
              {step === 1 ? 'Back to Home' : 'Previous'}
            </button>
            
            <button
              onClick={handleNext}
              disabled={isAnalyzing}
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500 text-white font-medium hover:shadow-glow transition-all disabled:opacity-50"
            >
              {isAnalyzing ? (
                <>
                  <Sparkles className="w-4 h-4 animate-spin" />
                  Analyzing...
                </>
              ) : step === totalSteps ? (
                <>
                  <CheckCircle className="w-4 h-4" />
                  Analyze Startup
                </>
              ) : (
                <>
                  Next
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

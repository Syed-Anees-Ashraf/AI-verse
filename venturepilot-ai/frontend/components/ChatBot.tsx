'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Send, MessageSquare, Bot, User, Sparkles, Loader2 } from 'lucide-react';
import { StartupProfile } from '@/app/page';

interface ChatBotProps {
  isOpen: boolean;
  onClose: () => void;
  startupProfile: StartupProfile | null;
}

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatBot({ isOpen, onClose, startupProfile }: ChatBotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hi! I'm your VenturePilot AI assistant. I can help you understand your investor matches, market analysis, policies, and strategic recommendations. What would you like to know?",
      timestamp: new Date(),
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Try to call the API
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: userMessage.content,
          startup_profile: startupProfile,
          conversation_history: messages.map(m => ({
            role: m.role,
            content: m.content,
          })),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: data.answer,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        // Generate mock response if API fails
        const mockResponse = generateMockResponse(userMessage.content, startupProfile);
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content: mockResponse,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, assistantMessage]);
      }
    } catch (error) {
      // Generate mock response if API is unavailable
      const mockResponse = generateMockResponse(userMessage.content, startupProfile);
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: mockResponse,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const suggestedQuestions = [
    "Why is Sequoia a good match for my startup?",
    "What government schemes can I apply for?",
    "What are the market risks in my sector?",
    "How can I improve my fundraising readiness?"
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
          />

          {/* Chat Window */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="fixed bottom-4 right-4 w-full max-w-md h-[600px] max-h-[80vh] glass rounded-2xl overflow-hidden z-50 flex flex-col"
          >
            {/* Header */}
            <div className="p-4 border-b border-white/10 flex items-center justify-between bg-gradient-to-r from-primary-500/10 to-accent-500/10">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">VenturePilot AI</h3>
                  <p className="text-xs text-gray-400">Your startup advisor</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : ''}`}
                >
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                    message.role === 'user' 
                      ? 'bg-primary-500' 
                      : 'bg-gradient-to-r from-primary-500 to-accent-500'
                  }`}>
                    {message.role === 'user' ? (
                      <User className="w-4 h-4 text-white" />
                    ) : (
                      <Sparkles className="w-4 h-4 text-white" />
                    )}
                  </div>
                  <div className={`max-w-[80%] p-3 rounded-xl ${
                    message.role === 'user'
                      ? 'bg-primary-500 text-white'
                      : 'bg-dark-800 text-gray-200'
                  }`}>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p className={`text-xs mt-1 ${
                      message.role === 'user' ? 'text-primary-200' : 'text-gray-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </motion.div>
              ))}
              
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex gap-3"
                >
                  <div className="w-8 h-8 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 flex items-center justify-center">
                    <Sparkles className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-dark-800 p-3 rounded-xl">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 text-primary-400 animate-spin" />
                      <span className="text-sm text-gray-400">Thinking...</span>
                    </div>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Suggested Questions */}
            {messages.length <= 2 && (
              <div className="px-4 py-2 border-t border-white/5">
                <p className="text-xs text-gray-500 mb-2">Suggested questions:</p>
                <div className="flex flex-wrap gap-2">
                  {suggestedQuestions.map((question, i) => (
                    <button
                      key={i}
                      onClick={() => setInput(question)}
                      className="text-xs px-3 py-1.5 rounded-full bg-dark-800 text-gray-300 hover:bg-dark-700 hover:text-white transition-colors"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="p-4 border-t border-white/10">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask anything about your startup..."
                  className="flex-1 px-4 py-3 rounded-xl bg-dark-800 border border-white/10 text-white placeholder-gray-500 focus:border-primary-500 transition-colors"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!input.trim() || isLoading}
                  className="p-3 rounded-xl bg-gradient-to-r from-primary-500 to-accent-500 text-white disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-glow transition-all"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

function generateMockResponse(question: string, profile: StartupProfile | null): string {
  const lowerQ = question.toLowerCase();
  
  if (lowerQ.includes('sequoia') || lowerQ.includes('investor')) {
    return `Based on your ${profile?.domain || 'technology'} startup at the ${profile?.stage || 'early'} stage, Sequoia Capital India is an excellent match because:

1. **Track Record**: They have invested in similar companies like Razorpay, BharatPe, and Groww
2. **Stage Fit**: They actively invest from Seed to Growth stages
3. **Domain Expertise**: Strong fintech and technology portfolio in India
4. **Value Add**: Beyond capital, they provide extensive operational support and access to their global network

Would you like me to explain why other investors might also be a good fit?`;
  }
  
  if (lowerQ.includes('scheme') || lowerQ.includes('government') || lowerQ.includes('policy')) {
    return `For your startup in ${profile?.geography || 'India'}, here are relevant schemes you can apply for:

1. **Startup India Seed Fund Scheme**: Up to ₹50 lakhs for proof of concept and prototype development
2. **Credit Guarantee Scheme (CGSS)**: Collateral-free loans up to ₹10 crores
3. **Fund of Funds (FFS)**: Access to SEBI-registered AIFs with SIDBI backing

**Next Steps**:
- Register on Startup India portal
- Get DPIIT recognition
- Prepare necessary documentation

Would you like detailed guidance on any specific scheme?`;
  }
  
  if (lowerQ.includes('risk') || lowerQ.includes('market')) {
    return `Here are the key market risks for your ${profile?.domain || 'technology'} startup:

**Competition Risks**:
- Intense competition from well-funded players
- Established companies entering the space

**Regulatory Risks**:
- Evolving compliance requirements
- Data privacy regulations

**Market Risks**:
- Customer acquisition costs rising
- Economic uncertainty affecting funding

**Mitigation Strategies**:
1. Focus on unique value proposition
2. Build strong unit economics
3. Diversify revenue streams

Would you like more specific risk mitigation recommendations?`;
  }
  
  if (lowerQ.includes('fundraising') || lowerQ.includes('readiness') || lowerQ.includes('improve')) {
    return `To improve your fundraising readiness, I recommend focusing on:

**Immediate Actions (Next 30 days)**:
1. Strengthen your pitch deck with clear metrics
2. Document your competitive advantages
3. Build a detailed financial model

**Short-term Goals (60-90 days)**:
1. Achieve specific growth milestones
2. Secure customer testimonials/case studies
3. Build relationships with target investors

**Key Metrics Investors Look For**:
- Monthly recurring revenue (MRR) growth
- Customer acquisition cost (CAC)
- Lifetime value (LTV)
- Churn rate

Would you like me to elaborate on any of these areas?`;
  }
  
  return `That's a great question! Based on your ${profile?.domain || 'technology'} startup profile:

I can help you with:
- **Investor Matching**: Understanding why specific investors are recommended
- **Market Analysis**: Deep dive into growth signals and risks
- **Policy Guidance**: Navigating government schemes and compliance
- **Strategy**: Actionable recommendations for growth

Could you please be more specific about what aspect you'd like to explore? For example:
- "Why is [Investor Name] a good fit?"
- "What policies apply to my startup?"
- "How can I improve my market position?"`;
}

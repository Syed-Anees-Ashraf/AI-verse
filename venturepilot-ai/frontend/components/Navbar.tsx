'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Rocket, Menu, X, MessageSquare, BarChart3, Users } from 'lucide-react';

interface NavbarProps {
  onLogoClick: () => void;
  showDashboardNav?: boolean;
  onChatClick?: () => void;
}

export default function Navbar({ onLogoClick, showDashboardNav, onChatClick }: NavbarProps) {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled ? 'glass-dark shadow-lg' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <motion.button
            onClick={onLogoClick}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center gap-2"
          >
            <div className="p-2 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500">
              <Rocket className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold gradient-text">VenturePilot</span>
          </motion.button>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-6">
            {showDashboardNav ? (
              <>
                <NavLink href="#overview" icon={<BarChart3 className="w-4 h-4" />}>
                  Overview
                </NavLink>
                <NavLink href="#investors" icon={<Users className="w-4 h-4" />}>
                  Investors
                </NavLink>
                <button
                  onClick={onChatClick}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white font-medium hover:shadow-glow transition-all"
                >
                  <MessageSquare className="w-4 h-4" />
                  AI Chat
                </button>
              </>
            ) : (
              <>
                <NavLink href="#features">Features</NavLink>
                <NavLink href="#how-it-works">How it Works</NavLink>
                <NavLink href="#pricing">Pricing</NavLink>
                <button className="px-4 py-2 rounded-lg glass hover:bg-white/10 transition-all text-white font-medium">
                  Sign In
                </button>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="md:hidden p-2 rounded-lg glass"
          >
            {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="md:hidden glass-dark"
        >
          <div className="px-4 py-4 space-y-4">
            {showDashboardNav ? (
              <>
                <MobileNavLink href="#overview">Overview</MobileNavLink>
                <MobileNavLink href="#investors">Investors</MobileNavLink>
                <button
                  onClick={() => {
                    setIsMobileMenuOpen(false);
                    onChatClick?.();
                  }}
                  className="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500 text-white font-medium"
                >
                  <MessageSquare className="w-4 h-4" />
                  AI Chat
                </button>
              </>
            ) : (
              <>
                <MobileNavLink href="#features">Features</MobileNavLink>
                <MobileNavLink href="#how-it-works">How it Works</MobileNavLink>
                <MobileNavLink href="#pricing">Pricing</MobileNavLink>
                <button className="w-full px-4 py-2 rounded-lg glass text-white font-medium">
                  Sign In
                </button>
              </>
            )}
          </div>
        </motion.div>
      )}
    </motion.nav>
  );
}

function NavLink({ href, children, icon }: { href: string; children: React.ReactNode; icon?: React.ReactNode }) {
  return (
    <a
      href={href}
      className="flex items-center gap-2 text-gray-300 hover:text-white transition-colors font-medium"
    >
      {icon}
      {children}
    </a>
  );
}

function MobileNavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <a
      href={href}
      className="block px-4 py-2 text-gray-300 hover:text-white transition-colors font-medium"
    >
      {children}
    </a>
  );
}

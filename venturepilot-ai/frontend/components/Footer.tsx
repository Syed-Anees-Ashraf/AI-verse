'use client';

import { Rocket, Twitter, Linkedin, Github, Mail } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="relative border-t border-white/5 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <div className="p-2 rounded-lg bg-gradient-to-r from-primary-500 to-accent-500">
                <Rocket className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">VenturePilot AI</span>
            </div>
            <p className="text-gray-400 max-w-md mb-6">
              AI-powered startup analysis and investor matching platform. 
              Find your ideal investors, understand market dynamics, and get strategic guidance.
            </p>
            <div className="flex items-center gap-4">
              <a href="#" className="p-2 rounded-lg glass hover:bg-white/10 transition-colors">
                <Twitter className="w-5 h-5 text-gray-400 hover:text-primary-400" />
              </a>
              <a href="#" className="p-2 rounded-lg glass hover:bg-white/10 transition-colors">
                <Linkedin className="w-5 h-5 text-gray-400 hover:text-primary-400" />
              </a>
              <a href="#" className="p-2 rounded-lg glass hover:bg-white/10 transition-colors">
                <Github className="w-5 h-5 text-gray-400 hover:text-primary-400" />
              </a>
              <a href="#" className="p-2 rounded-lg glass hover:bg-white/10 transition-colors">
                <Mail className="w-5 h-5 text-gray-400 hover:text-primary-400" />
              </a>
            </div>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-white mb-4">Product</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Features</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Pricing</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">API</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Integrations</a></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-white mb-4">Company</h3>
            <ul className="space-y-2">
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">About</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Blog</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Careers</a></li>
              <li><a href="#" className="text-gray-400 hover:text-white transition-colors">Contact</a></li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-12 pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-gray-500">
            © {new Date().getFullYear()} VenturePilot AI. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <a href="#" className="text-sm text-gray-500 hover:text-white transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-gray-500 hover:text-white transition-colors">
              Terms of Service
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

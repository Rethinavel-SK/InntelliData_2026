import React, { useState } from 'react';
import { Zap, LayoutDashboard, Search, Menu, X, ArrowUpRight, Cpu } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onOpenMLModels }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleSectionNavigate = (sectionId) => {
    if (activeTab !== 'landing') {
      setActiveTab('landing');
      setTimeout(() => {
        const el = document.getElementById(sectionId);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth' });
        } else {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      }, 150);
    } else {
      const el = document.getElementById(sectionId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    }
  };

  const handleMLClick = () => {
    if (activeTab === 'dashboard') {
      if (onOpenMLModels) onOpenMLModels();
    } else {
      handleSectionNavigate('models');
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-[#0b0f17]/90 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo */}
          <div
            onClick={() => { setActiveTab('landing'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-slate-950 font-black shadow-lg shadow-emerald-500/30 group-hover:scale-105 transition-transform">
              <Zap className="w-5 h-5 fill-slate-950" />
            </div>
            <div>
              <div className="text-xl font-black tracking-tight text-white flex items-center gap-1">
                <span>Stock</span>
                <span className="text-emerald-400">Sense</span>
              </div>
              <span className="text-[10px] font-extrabold uppercase tracking-widest text-slate-400 block -mt-1">
                NovaMart Retail Intelligence
              </span>
            </div>
          </div>

          {/* Center Links */}
          <div className="hidden lg:flex items-center bg-slate-900/90 border border-white/10 rounded-full px-6 py-2 shadow-inner">
            <nav className="flex items-center gap-6 text-xs font-bold tracking-wide">
              <button
                onClick={() => { setActiveTab('landing'); window.scrollTo({ top: 0, behavior: 'smooth' }); }}
                className={`transition-colors ${activeTab === 'landing' ? 'text-emerald-400 font-extrabold' : 'text-slate-300 hover:text-white'}`}
              >
                Home
              </button>
              
              <button
                onClick={() => handleSectionNavigate('features')}
                className="text-slate-300 hover:text-emerald-400 transition-colors"
              >
                Market Activity
              </button>

              <button
                onClick={() => handleSectionNavigate('how-it-works')}
                className="text-slate-300 hover:text-emerald-400 transition-colors"
              >
                News & Insight
              </button>

              <button
                onClick={() => setActiveTab('dashboard')}
                className={`transition-colors ${activeTab === 'dashboard' ? 'text-emerald-400 font-extrabold' : 'text-slate-300 hover:text-white'}`}
              >
                Dashboard
              </button>

              <button
                onClick={handleMLClick}
                className="text-slate-300 hover:text-emerald-400 transition-colors flex items-center gap-1"
              >
                <Cpu className="w-3.5 h-3.5 text-emerald-400" />
                <span>ML Models</span>
              </button>
            </nav>
          </div>

          {/* Right Actions */}
          <div className="hidden md:flex items-center gap-4">
            <div className="relative">
              <input
                type="text"
                placeholder="Search SKUs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="bg-slate-900/90 border border-white/10 rounded-full py-1.5 pl-4 pr-9 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 w-36 focus:w-48 transition-all"
              />
              <Search className="w-3.5 h-3.5 absolute right-3 top-2.5 text-slate-400" />
            </div>

            <button
              onClick={() => setActiveTab('dashboard')}
              className="btn-emerald-glow px-5 py-2.5 rounded-full text-xs uppercase tracking-wider flex items-center gap-1.5 shadow-lg"
            >
              <span>{activeTab === 'dashboard' ? 'Dashboard' : 'Start Reordering'}</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="md:hidden flex items-center gap-2">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 text-slate-400 hover:text-white rounded-lg bg-white/5"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-white/10 bg-[#0b0f17] px-4 pt-3 pb-6 space-y-3">
          <button
            onClick={() => { setActiveTab('landing'); window.scrollTo({ top: 0, behavior: 'smooth' }); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-slate-300"
          >
            Home
          </button>
          <button
            onClick={() => { handleSectionNavigate('features'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-slate-300"
          >
            Market Activity
          </button>
          <button
            onClick={() => { handleSectionNavigate('how-it-works'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-slate-300"
          >
            News & Insight
          </button>
          <button
            onClick={() => { setActiveTab('dashboard'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-emerald-400"
          >
            Dashboard
          </button>
          <button
            onClick={() => { handleMLClick(); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-slate-300"
          >
            ML Models
          </button>
        </div>
      )}
    </header>
  );
}

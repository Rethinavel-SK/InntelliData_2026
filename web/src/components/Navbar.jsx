import React, { useState } from 'react';
import { Zap, LogIn, LayoutDashboard, User, LogOut, Menu, X, Cpu } from 'lucide-react';

export default function Navbar({ onOpenLogin, user, onLogout, activeTab, setActiveTab, onOpenMLModels }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleMLModelsClick = () => {
    if (onOpenMLModels) {
      onOpenMLModels();
    } else {
      const el = document.getElementById('models');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-white/10 bg-[#0b0f19]/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          
          {/* Logo */}
          <div
            onClick={() => setActiveTab('landing')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform">
              <Zap className="w-5 h-5" />
            </div>
            <div>
              <span className="text-xl font-black tracking-tight text-white group-hover:text-indigo-300 transition-colors">
                STOCKSENSE
              </span>
              <span className="text-[10px] font-extrabold uppercase tracking-widest text-indigo-400 block -mt-1">
                NovaMart AI
              </span>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-8">
            <button
              onClick={() => setActiveTab('landing')}
              className={`text-sm font-semibold transition-colors ${activeTab === 'landing' ? 'text-white' : 'text-slate-400 hover:text-slate-200'}`}
            >
              Home
            </button>
            <a href="#features" onClick={() => { if (activeTab !== 'landing') setActiveTab('landing'); }} className="text-sm font-semibold text-slate-400 hover:text-slate-200 transition-colors">
              Features
            </a>
            <a href="#how-it-works" onClick={() => { if (activeTab !== 'landing') setActiveTab('landing'); }} className="text-sm font-semibold text-slate-400 hover:text-slate-200 transition-colors">
              How it Works
            </a>
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`text-sm font-semibold transition-colors ${activeTab === 'dashboard' ? 'text-indigo-400 font-bold' : 'text-slate-400 hover:text-slate-200'}`}
            >
              Dashboard
            </button>
            <button
              onClick={handleMLModelsClick}
              className="text-sm font-semibold text-slate-400 hover:text-indigo-300 transition-colors flex items-center gap-1.5"
            >
              <Cpu className="w-4 h-4 text-indigo-400" />
              <span>ML Models</span>
            </button>
          </nav>

          {/* Action Buttons / Auth */}
          <div className="hidden md:flex items-center gap-4">
            {user ? (
              <div className="flex items-center gap-3 bg-white/5 border border-white/10 px-4 py-2 rounded-full">
                <div className="w-7 h-7 rounded-full bg-indigo-500/30 border border-indigo-400/40 flex items-center justify-center text-indigo-300 text-xs font-bold">
                  {user.name[0]}
                </div>
                <span className="text-xs font-bold text-white">{user.name}</span>
                <button
                  onClick={onLogout}
                  title="Sign Out"
                  className="text-slate-400 hover:text-rose-400 transition-colors ml-1"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button
                onClick={onOpenLogin}
                className="text-sm font-bold text-slate-300 hover:text-white px-4 py-2 rounded-full border border-white/10 hover:border-white/20 transition-all flex items-center gap-2"
              >
                <LogIn className="w-4 h-4" />
                <span>Sign In</span>
              </button>
            )}

            <button
              onClick={() => setActiveTab('dashboard')}
              className="cronza-glow-button px-5 py-2.5 rounded-full text-white text-sm font-extrabold flex items-center gap-2"
            >
              <LayoutDashboard className="w-4 h-4" />
              <span>{activeTab === 'dashboard' ? 'Live Dashboard' : 'Open Dashboard'}</span>
            </button>
          </div>

          {/* Mobile Hamburger Button */}
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
        <div className="md:hidden border-b border-white/10 bg-[#0b0f19] px-4 pt-2 pb-6 space-y-3">
          <button
            onClick={() => { setActiveTab('landing'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-slate-300"
          >
            Home
          </button>
          <button
            onClick={() => { setActiveTab('dashboard'); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-indigo-400"
          >
            Dashboard
          </button>
          <button
            onClick={() => { handleMLModelsClick(); setMobileMenuOpen(false); }}
            className="block w-full text-left py-2 text-sm font-bold text-slate-300"
          >
            ML Models
          </button>
          {!user ? (
            <button
              onClick={() => { onOpenLogin(); setMobileMenuOpen(false); }}
              className="block w-full text-left py-2 text-sm font-bold text-slate-300"
            >
              Sign In
            </button>
          ) : (
            <button
              onClick={onLogout}
              className="block w-full text-left py-2 text-sm font-bold text-rose-400"
            >
              Sign Out ({user.name})
            </button>
          )}
        </div>
      )}
    </header>
  );
}

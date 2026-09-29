import React from 'react';
import { Zap, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-[#07090e] py-12 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-500 to-cyan-400 flex items-center justify-center text-white">
              <Zap className="w-4 h-4" />
            </div>
            <span className="text-lg font-black text-white">STOCKSENSE</span>
          </div>

          <div className="text-sm text-slate-400 text-center">
            IntelliData 2026 Hackathon • Sri Eshwar College of Engineering
          </div>

          <div className="text-xs text-slate-500 flex items-center gap-1">
            <span>Built with Cronza Aesthetic System &</span>
            <Heart className="w-3.5 h-3.5 text-rose-500 inline fill-rose-500" />
          </div>
        </div>
      </div>
    </footer>
  );
}

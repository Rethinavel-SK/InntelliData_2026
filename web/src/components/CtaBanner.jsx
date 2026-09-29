import React from 'react';
import { ArrowUpRight } from 'lucide-react';

export default function CtaBanner({ onOpenDashboard }) {
  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="stocksense-glass p-8 sm:p-12 rounded-3xl border border-emerald-500/30 bg-gradient-to-r from-slate-900/90 via-emerald-950/30 to-slate-900/90 relative overflow-hidden flex flex-col md:flex-row items-center justify-between gap-8 shadow-2xl">
        <div className="max-w-xl space-y-2 text-center md:text-left">
          <h2 className="text-2xl sm:text-4xl font-extrabold text-white leading-tight">
            Start Optimizing NovaMart <span className="text-emerald-400">Inventory Accounts</span> Today.
          </h2>
          <p className="text-slate-400 text-sm">
            Join store managers across Coimbatore, Chennai, Madurai, and Salem using automated AI stock recommendations.
          </p>
        </div>

        <button
          onClick={onOpenDashboard}
          className="btn-emerald-glow px-8 py-4 rounded-full text-slate-950 font-black text-xs uppercase tracking-wider flex items-center gap-2 shrink-0 shadow-xl"
        >
          <span>START REORDERING NOW</span>
          <ArrowUpRight className="w-4 h-4" />
        </button>
      </div>
    </section>
  );
}

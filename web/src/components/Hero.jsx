import React from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight, TrendingUp, ShieldCheck, CheckCircle2 } from 'lucide-react';

export default function Hero({ onOpenDashboard }) {
  return (
    <section className="relative pt-8 pb-16 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          
          {/* Left Hero Content matching Screenshot */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="lg:col-span-7 space-y-6"
          >
            <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight text-white leading-tight">
              Stock <span className="text-emerald-400">Sense</span> is the Best Way to <span className="text-emerald-400">Optimize</span> your Supply Chains
            </h1>

            <p className="text-base sm:text-lg text-slate-400 leading-relaxed max-w-2xl">
              Turn raw point-of-sale transactions, 7-day machine learning demand forecasts, and lead-time analytics into automated, prescriptive replenishment orders for NovaMart stores.
            </p>

            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={onOpenDashboard}
                className="btn-emerald-glow px-8 py-4 rounded-full text-slate-950 font-black text-sm uppercase tracking-wider flex items-center gap-2"
              >
                <span>Start Reordering Now</span>
                <ArrowUpRight className="w-5 h-5" />
              </button>

              <a
                href="#features"
                className="btn-emerald-outline px-6 py-4 rounded-full font-bold text-sm flex items-center gap-2"
              >
                <span>Learn More</span>
                <ArrowUpRight className="w-4 h-4" />
              </a>
            </div>
          </motion.div>

          {/* Right Hero Image / Overlay Chart Graphic matching Screenshot */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="lg:col-span-5 relative"
          >
            <div className="stocksense-glass rounded-3xl border border-white/10 p-6 relative overflow-hidden shadow-2xl">
              {/* Overlay simulated chart & user graphic */}
              <div className="relative rounded-2xl overflow-hidden bg-slate-900/90 h-80 flex flex-col justify-between p-6 border border-emerald-500/20">
                {/* Floating Metric Tooltip Pill matching top right screenshot */}
                <div className="self-end bg-emerald-500/20 border border-emerald-400/40 px-3 py-1 rounded-full text-xs font-bold text-emerald-300 flex items-center gap-1 shadow-lg">
                  <TrendingUp className="w-3.5 h-3.5" />
                  <span>+28.4% Demand Surge</span>
                </div>

                {/* SVG Trendline Graphic matching Green Sparkline in screenshot */}
                <svg className="w-full h-32 text-emerald-400" viewBox="0 0 300 100" fill="none">
                  <path
                    d="M 0 80 Q 50 90, 80 50 T 150 40 T 220 20 T 300 10"
                    stroke="#10b981"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    d="M 0 80 Q 50 90, 80 50 T 150 40 T 220 20 T 300 10 L 300 100 L 0 100 Z"
                    fill="url(#emerald-gradient)"
                    opacity="0.25"
                  />
                  <defs>
                    <linearGradient id="emerald-gradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#10b981" />
                      <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                </svg>

                {/* Bottom floating badge matching screenshot */}
                <div className="flex items-center justify-between bg-slate-950/80 p-3 rounded-xl border border-white/10">
                  <div className="flex items-center gap-2 text-xs font-bold text-white">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    <span>Forecast Accuracy: 99.47% R²</span>
                  </div>
                  <span className="text-[11px] font-extrabold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded">PASSED</span>
                </div>
              </div>
            </div>
          </motion.div>

        </div>

        {/* Big Stat Counters matching Screenshot Section 3 (125+ / 2000+) */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-16">
          <div className="stocksense-glass p-8 rounded-2xl border border-white/10 text-center md:text-left flex items-center justify-between">
            <div>
              <div className="text-4xl sm:text-5xl font-black text-emerald-400">125+</div>
              <div className="text-sm font-bold text-slate-300 uppercase tracking-wider mt-1">Powering Retail Stores & SKUs</div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-500/15 text-emerald-400 flex items-center justify-center font-black">
              ⚡
            </div>
          </div>

          <div className="stocksense-glass p-8 rounded-2xl border border-white/10 text-center md:text-left flex items-center justify-between">
            <div>
              <div className="text-4xl sm:text-5xl font-black text-emerald-400">2000+</div>
              <div className="text-sm font-bold text-slate-300 uppercase tracking-wider mt-1">Daily Inventory Ledgers Reconciled</div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-emerald-500/15 text-emerald-400 flex items-center justify-center font-black">
              📊
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}

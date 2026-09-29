import React from 'react';
import Hero from '../components/Hero';
import StockTicker from '../components/StockTicker';
import MarketSection from '../components/MarketSection';
import FeatureSection from '../components/FeatureSection';
import CtaBanner from '../components/CtaBanner';
import ModelPerformance from '../components/ModelPerformance';

export default function Landing({ onOpenDashboard, recommendations = [], demandComp = [], stockoutComp = [] }) {
  return (
    <div className="space-y-12">
      {/* 1. Hero Section matching top screenshot */}
      <div id="home">
        <Hero onOpenDashboard={onOpenDashboard} />
      </div>

      {/* 2. Top Performing Ticker Row */}
      <StockTicker />

      {/* 3. Market Activity Section */}
      <div id="features">
        <MarketSection recommendations={recommendations} onOpenDashboard={onOpenDashboard} />
      </div>

      {/* 4. News & Insight / Feature Section */}
      <div id="how-it-works">
        <FeatureSection />
      </div>

      {/* 5. CTA Banner */}
      <CtaBanner onOpenDashboard={onOpenDashboard} />

      {/* 6. ML Models Benchmark Section */}
      <section id="models" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 scroll-mt-24">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 mb-3 uppercase">
            🔬 MACHINE LEARNING BENCHMARKS
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
            Production Machine Learning <span className="text-emerald-400">Performance</span>
          </h2>
          <p className="text-slate-400 mt-2 text-sm">
            Time-aware benchmarking across 7 classical regression and 7 classification algorithms.
          </p>
        </div>

        <ModelPerformance demandComp={demandComp} stockoutComp={stockoutComp} />
      </section>
    </div>
  );
}

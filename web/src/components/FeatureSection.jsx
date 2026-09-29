import React from 'react';
import { Shield, Sparkles, CheckCircle2 } from 'lucide-react';

export default function FeatureSection() {
  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        {/* Left Column matching Screenshot Section 5 */}
        <div className="lg:col-span-6 space-y-6">
          <div className="text-xs font-extrabold uppercase tracking-wider text-emerald-400">
            Why Partner With StockSense
          </div>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white leading-tight">
            Managing Inventory With <span className="text-emerald-400">StockSense</span>
          </h2>
          <p className="text-slate-400 text-base leading-relaxed">
            Eliminate costly stock-outs and excess holding costs through automated machine learning demand predictions, lead-time variance buffers, and prescriptive manager purchase orders.
          </p>

          <div className="space-y-4 pt-4">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-full bg-emerald-500/20 border border-emerald-400/40 text-emerald-400 flex items-center justify-center shrink-0">
                <Shield className="w-6 h-6" />
              </div>
              <div>
                <h4 className="text-base font-bold text-white">Low and Transparent Lead Time Variance</h4>
                <p className="text-xs text-slate-400 mt-1">Calculates safety stock based on 95% service level confidence intervals and actual supplier lead days.</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-full bg-emerald-500/20 border border-emerald-400/40 text-emerald-400 flex items-center justify-center shrink-0">
                <Sparkles className="w-6 h-6" />
              </div>
              <div>
                <h4 className="text-base font-bold text-white">Intuitive, Prescriptive Recommendation Platform</h4>
                <p className="text-xs text-slate-400 mt-1">Direct manager actions with root-cause explanations eliminate complex decision delays.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Offset Image Cards matching Screenshot */}
        <div className="lg:col-span-6 grid grid-cols-2 gap-4 relative">
          <div className="stocksense-glass p-6 rounded-3xl border border-white/10 space-y-3 transform translate-y-4 shadow-2xl">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
              99.47%
            </div>
            <h4 className="text-lg font-bold text-white">Random Forest Accuracy</h4>
            <p className="text-xs text-slate-400">R² Score achieved across 7-day future regression models on validation test splits.</p>
          </div>

          <div className="stocksense-glass p-6 rounded-3xl border border-white/10 space-y-3 shadow-2xl">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
              100%
            </div>
            <h4 className="text-lg font-bold text-white">Stock-out Recall</h4>
            <p className="text-xs text-slate-400">Zero missed stockout events in production testing with Decision Tree Classifier.</p>
          </div>
        </div>

      </div>
    </section>
  );
}

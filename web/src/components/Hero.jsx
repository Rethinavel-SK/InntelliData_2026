import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, ArrowRight, ShieldCheck, TrendingUp, AlertCircle, ShoppingBag } from 'lucide-react';
import MetricCard from './MetricCard';

export default function Hero({ onOpenDashboard, onOpenLogin }) {
  return (
    <section className="relative pt-12 pb-20 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        
        {/* Pill Badge */}
        <motion.div
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-extrabold tracking-wider uppercase bg-indigo-500/10 border border-indigo-400/30 text-indigo-300 mb-6 shadow-lg shadow-indigo-500/20"
        >
          <Sparkles className="w-4 h-4 text-indigo-400 animate-pulse" />
          <span>INTELLIDATA 2026 • ROUND 3 PROTOTYPE</span>
        </motion.div>

        {/* Title */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-5xl mx-auto leading-tight mb-6"
        >
          AI-Powered Retail Inventory <br />
          <span className="cronza-gradient-text">Optimization & Stockout Prevention</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="text-lg sm:text-xl text-slate-400 max-w-3xl mx-auto mb-10 leading-relaxed"
        >
          Turn raw POS transactions, 7-day machine learning demand forecasts, and lead-time analytics into automated, prescriptive replenishment orders for NovaMart stores.
        </motion.p>

        {/* Action Buttons */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16"
        >
          <button
            onClick={onOpenDashboard}
            className="cronza-glow-button px-8 py-4 rounded-full text-white font-extrabold text-base flex items-center gap-3 w-full sm:w-auto justify-center"
          >
            <span>Open Live Dashboard</span>
            <ArrowRight className="w-5 h-5" />
          </button>

          <button
            onClick={onOpenLogin}
            className="px-8 py-4 rounded-full text-slate-200 font-bold text-base bg-white/5 border border-white/10 hover:bg-white/10 hover:border-white/20 transition-all w-full sm:w-auto justify-center"
          >
            Manager Sign In
          </button>
        </motion.div>

        {/* Floating Glass Metric Cards (Hero Showcase) */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-left max-w-6xl mx-auto"
        >
          <MetricCard
            label="Retail POS Sales"
            value="₹1,44,229.00"
            subtext="Across 4 Tamil Nadu stores"
            icon={ShoppingBag}
            color="indigo"
          />
          <MetricCard
            label="Units Demand Sold"
            value="2,203 units"
            subtext="Cleaned transaction volume"
            icon={TrendingUp}
            color="cyan"
          />
          <MetricCard
            label="Forecast Accuracy"
            value="99.47% R²"
            subtext="Random Forest Regressor"
            icon={ShieldCheck}
            color="emerald"
          />
          <MetricCard
            label="Stockout Recall"
            value="100.0%"
            subtext="Decision Tree Classifier"
            icon={AlertCircle}
            color="rose"
          />
        </motion.div>

      </div>
    </section>
  );
}

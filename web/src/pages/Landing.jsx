import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { TrendingUp, AlertTriangle, ShieldCheck, Database, Cpu, Sparkles, ArrowRight, UserCheck } from 'lucide-react';
import Hero from '../components/Hero';
import FeatureCard from '../components/FeatureCard';

export default function Landing({ onOpenDashboard, onOpenLogin }) {
  // Live Reorder Calculator state
  const [simStore, setSimStore] = useState('S01');
  const [simCat, setSimCat] = useState('Beverages');
  const [simStock, setSimStock] = useState(65);

  // Compute live simulated recommendation
  const forecastDemand = simCat === 'Beverages' ? 921 : (simCat === 'Dairy' ? 731 : (simCat === 'Snacks' ? 826 : 178));
  const safetyStock = 38;
  const recommendedOrder = Math.max(0, forecastDemand + safetyStock - simStock);
  const isHighRisk = simStock < 100;

  return (
    <div className="space-y-24">
      {/* Hero */}
      <Hero onOpenDashboard={onOpenDashboard} onOpenLogin={onOpenLogin} />

      {/* Features Grid */}
      <section id="features" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 mb-3 uppercase">
            ⚡ CORE PLATFORM CAPABILITIES
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white cronza-gradient-text">
            Engineered for Retail Operations Excellence
          </h2>
          <p className="text-slate-400 mt-2 max-w-2xl mx-auto">
            Combining rigorous statistical data cleaning with classical machine learning algorithms.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureCard
            icon={TrendingUp}
            title="7-Day Demand Forecasting"
            description="Random Forest Regressor benchmarks 20 time-series & lag features to achieve 99.47% R² accuracy and MAE of 17.36 units."
            badge="ML REGRESSION"
          />
          <FeatureCard
            icon={AlertTriangle}
            title="Stock-out Risk Prediction"
            description="Decision Tree Classifier predicts stock-out probabilities with 100.0% recall on validation sets to eliminate empty shelves."
            badge="ML CLASSIFIER"
          />
          <FeatureCard
            icon={ShieldCheck}
            title="Safety Stock Economics"
            description="Dynamically computes safety buffers based on 95% service level confidence intervals and lead-time variance."
            badge="INVENTORY OPTIM"
          />
          <FeatureCard
            icon={Sparkles}
            title="Prescriptive Action Cards"
            description="Translates model probabilities into direct manager commands with clear operational root-cause explanations."
            badge="ACTION ENGINE"
          />
          <FeatureCard
            icon={Database}
            title="Automated Data Audit"
            description="Non-mutating data quality pipeline verifies 100% accounting formula consistency (closing = opening + received - sold)."
            badge="ETL PIPELINE"
          />
          <FeatureCard
            icon={Cpu}
            title="Model Explainability"
            description="Extracts global feature importances and row-level SHAP-like explanations for high-risk store SKUs."
            badge="EXPLAINABLE AI"
          />
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="cronza-glass p-10 lg:p-14 rounded-3xl border border-white/10 relative overflow-hidden">
          <div className="text-center max-w-3xl mx-auto mb-14">
            <h2 className="text-3xl font-extrabold text-white cronza-gradient-text">
              How StockSense Works
            </h2>
            <p className="text-slate-400 mt-2">
              From raw store transaction logs to intelligent purchase orders in 3 simple steps.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative z-10">
            <div className="bg-white/5 p-6 rounded-2xl border border-white/5 relative">
              <div className="w-10 h-10 rounded-xl bg-indigo-500/20 text-indigo-400 font-black text-lg flex items-center justify-center mb-4">
                01
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Clean & Integrate</h3>
              <p className="text-sm text-slate-400">
                Raw POS logs, inventory ledgers, and weather factors are cleaned, deduplicated, and aggregated to the 1 Date × 1 Store × 1 Product grain.
              </p>
            </div>

            <div className="bg-white/5 p-6 rounded-2xl border border-white/5 relative">
              <div className="w-10 h-10 rounded-xl bg-cyan-500/20 text-cyan-400 font-black text-lg flex items-center justify-center mb-4">
                02
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Predict & Classify</h3>
              <p className="text-sm text-slate-400">
                Random Forest Regressor predicts 7-day demand, while Decision Tree Classifier assigns risk probabilities (HIGH, MEDIUM, LOW).
              </p>
            </div>

            <div className="bg-white/5 p-6 rounded-2xl border border-white/5 relative">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 font-black text-lg flex items-center justify-center mb-4">
                03
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Prescribe Order</h3>
              <p className="text-sm text-slate-400">
                Reorder engine computes optimal replenishment quantities and emits urgent manager alerts to store operations.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Live Reorder Simulator */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="cronza-glass p-8 lg:p-12 rounded-3xl border border-indigo-500/30 bg-gradient-to-br from-slate-900/90 to-indigo-950/40 shadow-2xl">
          <div className="text-center max-w-2xl mx-auto mb-8">
            <span className="px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-400/30">
              ⚡ INTERACTIVE SIMULATOR
            </span>
            <h3 className="text-2xl sm:text-3xl font-extrabold text-white mt-3">
              Test the Reorder Recommendation Engine
            </h3>
            <p className="text-slate-400 text-sm mt-1">
              Select store parameters to compute instant purchase order recommendations.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto mb-8">
            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Select Store
              </label>
              <select
                value={simStore}
                onChange={(e) => setSimStore(e.target.value)}
                className="w-full bg-slate-900 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500"
              >
                <option value="S01">S01 - Coimbatore Supermarket</option>
                <option value="S02">S02 - Chennai Hypermarket</option>
                <option value="S03">S03 - Madurai Express</option>
                <option value="S04">S04 - Salem Supermarket</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Select Product Category
              </label>
              <select
                value={simCat}
                onChange={(e) => setSimCat(e.target.value)}
                className="w-full bg-slate-900 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500"
              >
                <option value="Beverages">Beverages (Soft Drink)</option>
                <option value="Dairy">Dairy (Milk 1L)</option>
                <option value="Snacks">Snacks (Biscuits)</option>
                <option value="Personal Care">Personal Care (Shampoo)</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Current Closing Stock
              </label>
              <input
                type="number"
                value={simStock}
                onChange={(e) => setSimStock(Number(e.target.value))}
                className="w-full bg-slate-900 border border-white/10 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-indigo-500"
              />
            </div>
          </div>

          {/* Simulator Result Box */}
          <div className={`p-6 rounded-2xl border backdrop-blur-md max-w-3xl mx-auto ${isHighRisk ? 'bg-rose-950/40 border-rose-500/40' : 'bg-emerald-950/40 border-emerald-500/40'}`}>
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${isHighRisk ? 'bg-rose-500/20 text-rose-300' : 'bg-emerald-500/20 text-emerald-300'}`}>
                  RISK LEVEL: {isHighRisk ? 'HIGH' : 'LOW'}
                </span>
                <h4 className="text-xl font-extrabold text-white mt-2">
                  Recommended Purchase Order: <span className="text-indigo-400">{recommendedOrder.toLocaleString()} units</span>
                </h4>
                <p className="text-xs text-slate-300 mt-1">
                  <strong>Manager Action: </strong>
                  {isHighRisk ? 'CRITICAL: Issue emergency purchase order immediately to prevent stockout.' : 'NORMAL: Stock levels optimal; maintain regular cycle.'}
                </p>
              </div>

              <button
                onClick={onOpenDashboard}
                className="cronza-glow-button px-6 py-3 rounded-full text-xs font-bold text-white shrink-0"
              >
                View Full Dashboard
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section id="team" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-white cronza-gradient-text">
            Hackathon Development Team
          </h2>
          <p className="text-slate-400 mt-1">IntelliData 2026 • Sri Eshwar College of Engineering</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div className="cronza-glass p-6 rounded-2xl border border-white/10 text-center">
            <div className="w-14 h-14 rounded-full bg-indigo-500/20 border border-indigo-400/30 flex items-center justify-center text-indigo-300 font-extrabold text-lg mx-auto mb-4">
              M1
            </div>
            <h3 className="text-base font-bold text-white">Member 1</h3>
            <p className="text-xs text-indigo-400 font-semibold mb-2">Data & Audit Lead</p>
            <p className="text-xs text-slate-400">Data cleaning, non-mutating data audit, and master dataset ETL integration.</p>
          </div>

          <div className="cronza-glass p-6 rounded-2xl border border-white/10 text-center">
            <div className="w-14 h-14 rounded-full bg-cyan-500/20 border border-cyan-400/30 flex items-center justify-center text-cyan-300 font-extrabold text-lg mx-auto mb-4">
              M2
            </div>
            <h3 className="text-base font-bold text-white">Member 2</h3>
            <p className="text-xs text-cyan-400 font-semibold mb-2">ML & Data Science Lead</p>
            <p className="text-xs text-slate-400">Feature engineering, demand forecasting, stockout classifier, and explainability.</p>
          </div>

          <div className="cronza-glass p-6 rounded-2xl border border-white/10 text-center">
            <div className="w-14 h-14 rounded-full bg-emerald-500/20 border border-emerald-400/30 flex items-center justify-center text-emerald-300 font-extrabold text-lg mx-auto mb-4">
              M3
            </div>
            <h3 className="text-base font-bold text-white">Member 3</h3>
            <p className="text-xs text-emerald-400 font-semibold mb-2">Frontend & UI/UX Engineer</p>
            <p className="text-xs text-slate-400">Streamlit decision support tool, React Cronza design web application.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

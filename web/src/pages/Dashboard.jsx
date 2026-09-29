import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { LayoutDashboard, AlertTriangle, ShoppingCart, TrendingUp, Cpu, Sparkles, Filter, Download, ArrowLeft } from 'lucide-react';
import MetricCard from '../components/MetricCard';
import RiskBadge from '../components/RiskBadge';
import ActionCard from '../components/ActionCard';
import RiskTable from '../components/RiskTable';
import DemandChart from '../components/DemandChart';
import ModelPerformance from '../components/ModelPerformance';
import { loadAllDashboardData } from '../utils/dataLoader';

export default function Dashboard({ onBackToLanding }) {
  const [data, setData] = useState({
    recommendations: [],
    decisionOutput: [],
    demandComparison: [],
    stockoutComparison: []
  });
  const [loading, setLoading] = useState(true);

  // Active Tab: 'summary' | 'risk' | 'action' | 'intelligence' | 'performance'
  const [activeTab, setActiveTab] = useState('summary');

  // Filters
  const [selectedStore, setSelectedStore] = useState('ALL');
  const [selectedCategory, setSelectedCategory] = useState('ALL');
  const [selectedRisk, setSelectedRisk] = useState('ALL');

  useEffect(() => {
    async function initData() {
      setLoading(true);
      const res = await loadAllDashboardData();
      setData(res);
      setLoading(false);
    }
    initData();
  }, []);

  const recData = data.recommendations || [];
  const decData = data.decisionOutput || [];

  // Filter recommendations
  const filteredRec = recData.filter(r => {
    if (selectedStore !== 'ALL' && r.Store !== selectedStore) return false;
    if (selectedCategory !== 'ALL' && r.Category !== selectedCategory) return false;
    if (selectedRisk !== 'ALL' && r.Risk_Level !== selectedRisk) return false;
    return true;
  });

  // Calculate KPIs
  const totalRev = decData.reduce((acc, curr) => acc + (Number(curr.tx_total_revenue) || 0), 0);
  const totalUnits = decData.reduce((acc, curr) => acc + (Number(curr.daily_demand) || 0), 0);
  const highRiskCount = filteredRec.filter(r => r.Risk_Level === 'HIGH').length;
  const reorderCount = filteredRec.filter(r => Number(r.Recommended_Order_Qty) > 0).length;

  if (loading) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center text-center p-8">
        <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mb-4" />
        <h3 className="text-xl font-bold text-white">Loading StockSense Decision Engine...</h3>
        <p className="text-sm text-slate-400 mt-1">Parsing store transactions, forecasts, and risk models...</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Top Controls & Navigation Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/10 pb-6">
        <div>
          <button
            onClick={onBackToLanding}
            className="inline-flex items-center gap-2 text-xs font-bold text-slate-400 hover:text-white transition-colors mb-2"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Landing Page</span>
          </button>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl sm:text-3xl font-black text-white tracking-tight">
              NovaMart Operations Dashboard
            </h1>
            <span className="px-3 py-1 rounded-full text-[11px] font-extrabold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30">
              ● LIVE DATA
            </span>
          </div>
        </div>

        {/* Dashboard Tabs */}
        <div className="flex flex-wrap items-center gap-2 bg-slate-900/80 p-1.5 rounded-2xl border border-white/10">
          <button
            onClick={() => setActiveTab('summary')}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${activeTab === 'summary' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:text-white'}`}
          >
            Executive Summary
          </button>
          <button
            onClick={() => setActiveTab('risk')}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${activeTab === 'risk' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:text-white'}`}
          >
            Risk Centre
          </button>
          <button
            onClick={() => setActiveTab('action')}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${activeTab === 'action' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:text-white'}`}
          >
            Action Centre ({highRiskCount})
          </button>
          <button
            onClick={() => setActiveTab('intelligence')}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${activeTab === 'intelligence' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:text-white'}`}
          >
            Demand Intel
          </button>
          <button
            onClick={() => setActiveTab('performance')}
            className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${activeTab === 'performance' ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30' : 'text-slate-400 hover:text-white'}`}
          >
            Model Benchmark
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="cronza-glass p-4 rounded-2xl border border-white/10 flex flex-wrap items-center gap-4 text-xs font-semibold">
        <div className="flex items-center gap-2 text-slate-400 font-bold uppercase mr-2">
          <Filter className="w-4 h-4 text-indigo-400" />
          <span>Filters:</span>
        </div>

        {/* Store Filter */}
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Store:</span>
          <select
            value={selectedStore}
            onChange={(e) => setSelectedStore(e.target.value)}
            className="bg-slate-900 border border-white/10 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="ALL">All Stores</option>
            <option value="S01">S01 - Coimbatore</option>
            <option value="S02">S02 - Chennai</option>
            <option value="S03">S03 - Madurai</option>
            <option value="S04">S04 - Salem</option>
          </select>
        </div>

        {/* Category Filter */}
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Category:</span>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-slate-900 border border-white/10 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="ALL">All Categories</option>
            <option value="Beverages">Beverages</option>
            <option value="Dairy">Dairy</option>
            <option value="Snacks">Snacks</option>
            <option value="Personal Care">Personal Care</option>
          </select>
        </div>

        {/* Risk Level Filter */}
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Risk Level:</span>
          <select
            value={selectedRisk}
            onChange={(e) => setSelectedRisk(e.target.value)}
            className="bg-slate-900 border border-white/10 rounded-lg px-3 py-1.5 text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="ALL">All Risk Levels</option>
            <option value="HIGH">HIGH Risk</option>
            <option value="MEDIUM">MEDIUM Risk</option>
            <option value="LOW">LOW Risk</option>
          </select>
        </div>

        <div className="ml-auto text-slate-400 font-mono text-[11px]">
          Showing <span className="text-indigo-400 font-bold">{filteredRec.length}</span> SKUs
        </div>
      </div>

      {/* TAB 1: EXECUTIVE SUMMARY */}
      {activeTab === 'summary' && (
        <div className="space-y-8">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              label="Total Store Revenue"
              value={`₹${totalRev.toLocaleString('en-IN', { maximumFractionDigits: 2 })}`}
              subtext="4 Tamil Nadu retail outlets"
              color="indigo"
            />
            <MetricCard
              label="Total POS Demand"
              value={`${totalUnits.toLocaleString()} units`}
              subtext="Cleaned transaction volume"
              color="cyan"
            />
            <MetricCard
              label="High Risk SKUs"
              value={highRiskCount}
              subtext="Action required immediately"
              color="rose"
            />
            <MetricCard
              label="Reorders Needed"
              value={reorderCount}
              subtext="Stock below safety threshold"
              color="amber"
            />
          </div>

          <DemandChart decisionData={decData} />
        </div>
      )}

      {/* TAB 2: INVENTORY RISK CENTRE */}
      {activeTab === 'risk' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-white">Inventory Risk Table</h3>
            <span className="text-xs text-slate-400">Real-time stockout probability scores</span>
          </div>
          <RiskTable data={filteredRec} />
        </div>
      )}

      {/* TAB 3: MANAGER ACTION CENTRE */}
      {activeTab === 'action' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <ShoppingCart className="w-5 h-5 text-indigo-400" />
              <span>Prescriptive Reorder Recommendations</span>
            </h3>
            <span className="text-xs text-slate-400">Prioritized by urgency</span>
          </div>

          {filteredRec.map((item, idx) => (
            <ActionCard key={idx} item={item} defaultOpen={idx < 3} />
          ))}
        </div>
      )}

      {/* TAB 4: DEMAND INTELLIGENCE */}
      {activeTab === 'intelligence' && (
        <div className="space-y-6">
          <DemandChart decisionData={decData} />
        </div>
      )}

      {/* TAB 5: MODEL PERFORMANCE */}
      {activeTab === 'performance' && (
        <ModelPerformance
          demandComp={data.demandComparison}
          stockoutComp={data.stockoutComparison}
        />
      )}
    </div>
  );
}

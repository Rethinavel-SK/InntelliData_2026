import React, { useState } from 'react';
import { ArrowUpRight, TrendingUp, TrendingDown, Store, Package, AlertTriangle, Layers } from 'lucide-react';
import RiskBadge from './RiskBadge';

export default function MarketSection({ recommendations = [], onOpenDashboard }) {
  const [activeCategory, setActiveCategory] = useState('ALL');

  const categories = [
    { id: 'ALL', label: 'MOST POPULAR', icon: Layers },
    { id: 'Beverages', label: 'BEVERAGES', icon: Package },
    { id: 'Dairy', label: 'DAIRY', icon: Package },
    { id: 'Snacks', label: 'SNACKS', icon: Package },
    { id: 'HIGH', label: 'HIGH RISK REORDERS', icon: AlertTriangle },
  ];

  const filteredData = recommendations.filter(r => {
    if (activeCategory === 'HIGH') return r.Risk_Level === 'HIGH';
    if (activeCategory !== 'ALL') return r.Category === activeCategory;
    return true;
  });

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white">
          Monitor Over <span className="text-emerald-400">736 Daily</span> Retail SKUs
        </h2>
        <p className="text-slate-400 text-sm mt-2 max-w-xl mx-auto">
          Real-time point-of-sale customer demand forecasts and automated stockout risk classification.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Category Sidebar matching Screenshot */}
        <div className="lg:col-span-3 stocksense-glass p-4 rounded-2xl border border-white/10 space-y-1">
          {categories.map(cat => {
            const Icon = cat.icon;
            const isActive = activeCategory === cat.id;
            return (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-xs font-extrabold tracking-wider transition-all text-left ${
                  isActive
                    ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/30'
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-slate-950' : 'text-slate-400'}`} />
                <span>{cat.label}</span>
              </button>
            );
          })}
        </div>

        {/* Center Market Data Table matching Screenshot */}
        <div className="lg:col-span-9 stocksense-glass rounded-2xl border border-white/10 overflow-hidden shadow-2xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900/90 text-[11px] font-bold uppercase tracking-wider text-slate-400 border-b border-white/10">
                <tr>
                  <th className="px-5 py-4">#</th>
                  <th className="px-5 py-4">Store</th>
                  <th className="px-5 py-4">Product SKU</th>
                  <th className="px-5 py-4">Category</th>
                  <th className="px-5 py-4 text-right">Closing Stock</th>
                  <th className="px-5 py-4 text-right">7-Day Forecast</th>
                  <th className="px-5 py-4 text-right">Risk Level</th>
                  <th className="px-5 py-4 text-right">Reorder Qty</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {(filteredData.length > 0 ? filteredData.slice(0, 8) : [
                  { Store: 'S01', Product: 'P330', Category: 'Beverages', Current_Stock: 136, '7_Day_Forecast': 921, Risk_Level: 'HIGH', Recommended_Order_Qty: 823 },
                  { Store: 'S04', Product: 'P330', Category: 'Beverages', Current_Stock: 59, '7_Day_Forecast': 835, Risk_Level: 'HIGH', Recommended_Order_Qty: 810 },
                  { Store: 'S01', Product: 'P101', Category: 'Dairy', Current_Stock: 66, '7_Day_Forecast': 731, Risk_Level: 'HIGH', Recommended_Order_Qty: 691 },
                  { Store: 'S04', Product: 'P101', Category: 'Dairy', Current_Stock: 60, '7_Day_Forecast': 679, Risk_Level: 'HIGH', Recommended_Order_Qty: 666 },
                  { Store: 'S02', Product: 'P442', Category: 'Snacks', Current_Stock: 165, '7_Day_Forecast': 826, Risk_Level: 'HIGH', Recommended_Order_Qty: 601 }
                ]).map((row, idx) => (
                  <tr key={idx} className="market-table-row">
                    <td className="px-5 py-4 font-bold text-slate-500">{idx + 1}</td>
                    <td className="px-5 py-4 font-bold text-white">Store {row.Store}</td>
                    <td className="px-5 py-4 font-medium text-slate-200">SKU {row.Product}</td>
                    <td className="px-5 py-4 text-slate-400">{row.Category}</td>
                    <td className="px-5 py-4 text-right font-semibold text-slate-200">{row.Current_Stock}</td>
                    <td className="px-5 py-4 text-right font-extrabold text-emerald-400 flex items-center justify-end gap-1">
                      <TrendingUp className="w-3.5 h-3.5" />
                      <span>{Number(row['7_Day_Forecast'] || 0).toLocaleString()}</span>
                    </td>
                    <td className="px-5 py-4 text-right">
                      <RiskBadge level={row.Risk_Level} />
                    </td>
                    <td className="px-5 py-4 text-right font-black text-white">
                      {Number(row.Recommended_Order_Qty || 0).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="p-6 bg-slate-900/60 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4">
            <button
              onClick={onOpenDashboard}
              className="btn-emerald-outline px-6 py-2.5 rounded-full text-xs font-bold"
            >
              VIEW ALL MARKET DATA
            </button>

            <button
              onClick={onOpenDashboard}
              className="btn-emerald-glow px-6 py-2.5 rounded-full text-xs font-black uppercase tracking-wider flex items-center gap-1.5"
            >
              <span>START REORDERING NOW</span>
              <ArrowUpRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

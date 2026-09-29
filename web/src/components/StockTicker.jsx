import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

export default function StockTicker() {
  const tickers = [
    { title: "S01 COIMBATORE", value: "₹48,920", change: "+28.4%", isPositive: true },
    { title: "S02 CHENNAI", value: "₹62,150", change: "+34.1%", isPositive: true },
    { title: "S03 MADURAI", value: "₹18,450", change: "-2.4%", isPositive: false },
    { title: "S04 SALEM", value: "₹24,800", change: "+18.9%", isPositive: true },
    { title: "BEVERAGES (P330)", value: "921 units", change: "+42.5%", isPositive: true },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-wider">
          <span>🔥</span>
          <span>Top Performing Stores & SKUs</span>
          <span className="text-slate-600">(Tamil Nadu Region)</span>
        </div>
        <a href="#features" className="text-xs font-bold text-emerald-400 hover:underline flex items-center gap-1">
          <span>View Market Activity</span>
          <span>↗</span>
        </a>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {tickers.map((t, idx) => (
          <div key={idx} className="stocksense-glass p-4 rounded-xl border border-white/10 hover:border-emerald-500/40 transition-all">
            <div className="text-[11px] font-extrabold text-slate-400 tracking-wider uppercase mb-1">
              {t.title}
            </div>
            <div className="text-lg font-black text-white">
              {t.value}
            </div>
            <div className={`text-xs font-bold flex items-center gap-1 mt-1 ${t.isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
              {t.isPositive ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
              <span>{t.change}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

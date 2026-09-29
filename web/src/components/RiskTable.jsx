import React from 'react';
import RiskBadge from './RiskBadge';

export default function RiskTable({ data }) {
  if (!data || data.length === 0) {
    return (
      <div className="p-8 text-center text-slate-400 cronza-glass rounded-2xl">
        No records match active filters.
      </div>
    );
  }

  return (
    <div className="cronza-glass rounded-2xl overflow-x-auto border border-white/10 shadow-2xl">
      <table className="w-full text-left text-sm text-slate-300">
        <thead className="bg-slate-900/80 text-xs uppercase tracking-wider text-slate-400 border-b border-white/10">
          <tr>
            <th className="px-5 py-4">Date</th>
            <th className="px-5 py-4">Store</th>
            <th className="px-5 py-4">Product</th>
            <th className="px-5 py-4">Category</th>
            <th className="px-5 py-4 text-right">Current Stock</th>
            <th className="px-5 py-4 text-right">7-Day Forecast</th>
            <th className="px-5 py-4 text-right">Stockout Prob</th>
            <th className="px-5 py-4">Risk Level</th>
            <th className="px-5 py-4 text-right">Reorder Qty</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5">
          {data.slice(0, 50).map((row, idx) => (
            <tr key={idx} className="hover:bg-white/5 transition-colors">
              <td className="px-5 py-4 font-mono text-xs text-slate-400">{row.date}</td>
              <td className="px-5 py-4 font-bold text-white">Store {row.Store}</td>
              <td className="px-5 py-4 font-medium text-slate-200">SKU {row.Product}</td>
              <td className="px-5 py-4 text-slate-400">{row.Category}</td>
              <td className="px-5 py-4 text-right font-semibold text-slate-200">{row.Current_Stock}</td>
              <td className="px-5 py-4 text-right font-semibold text-indigo-300">{Number(row['7_Day_Forecast'] || 0).toLocaleString()}</td>
              <td className="px-5 py-4 text-right font-mono font-bold text-rose-400">
                {(Number(row.Stockout_Probability || 0) * 100).toFixed(1)}%
              </td>
              <td className="px-5 py-4">
                <RiskBadge level={row.Risk_Level} />
              </td>
              <td className="px-5 py-4 text-right font-black text-emerald-400 text-base">
                {Number(row.Recommended_Order_Qty || 0).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

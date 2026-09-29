import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, ChevronDown, PackageCheck, ShoppingCart, Info } from 'lucide-react';
import RiskBadge from './RiskBadge';

export default function ActionCard({ item, defaultOpen = false }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  const isHigh = item.Risk_Level === 'HIGH';
  const borderColor = isHigh ? 'border-l-rose-500' : (item.Risk_Level === 'MEDIUM' ? 'border-l-amber-500' : 'border-l-emerald-500');

  return (
    <div className={`cronza-glass rounded-2xl border-t border-r border-b border-white/10 border-l-4 ${borderColor} overflow-hidden mb-4 shadow-xl`}>
      {/* Clickable Header */}
      <div
        onClick={() => setIsOpen(!isOpen)}
        className="p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 cursor-pointer hover:bg-white/5 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className={`p-2.5 rounded-xl ${isHigh ? 'bg-rose-500/10 text-rose-400' : 'bg-indigo-500/10 text-indigo-400'}`}>
            <ShoppingCart className="w-5 h-5" />
          </div>

          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-extrabold text-white text-base">Store {item.Store}</span>
              <span className="text-slate-400">•</span>
              <span className="text-slate-300 font-medium text-sm">SKU {item.Product} ({item.Category})</span>
              <RiskBadge level={item.Risk_Level} />
            </div>
            <div className="text-xs text-slate-400 mt-1">
              Brand: <span className="text-slate-200">{item.Brand || 'Master Catalog'}</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="text-right">
            <div className="text-xs text-slate-400 font-semibold uppercase">Reorder Qty</div>
            <div className="text-lg font-black text-indigo-300">{Number(item.Recommended_Order_Qty || 0).toLocaleString()} <span className="text-xs text-slate-400">units</span></div>
          </div>

          <div className="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center text-slate-400">
            <ChevronDown className={`w-4 h-4 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`} />
          </div>
        </div>
      </div>

      {/* Expandable Details Body */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-white/5 bg-slate-900/60 p-5 space-y-4"
          >
            {/* Quick Metrics Row */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="bg-white/5 p-3 rounded-xl border border-white/5">
                <div className="text-[11px] font-bold text-slate-400 uppercase">7-Day Forecast</div>
                <div className="text-base font-extrabold text-white">{Number(item['7_Day_Forecast'] || 0).toLocaleString()} units</div>
              </div>
              <div className="bg-white/5 p-3 rounded-xl border border-white/5">
                <div className="text-[11px] font-bold text-slate-400 uppercase">Current Stock</div>
                <div className="text-base font-extrabold text-white">{item.Current_Stock || 0} units</div>
              </div>
              <div className="bg-white/5 p-3 rounded-xl border border-white/5">
                <div className="text-[11px] font-bold text-slate-400 uppercase">Incoming Stock</div>
                <div className="text-base font-extrabold text-white">{item.Incoming_Stock || 0} units</div>
              </div>
              <div className="bg-white/5 p-3 rounded-xl border border-white/5">
                <div className="text-[11px] font-bold text-slate-400 uppercase">Stockout Prob</div>
                <div className="text-base font-extrabold text-rose-400">{(Number(item.Stockout_Probability || 0) * 100).toFixed(1)}%</div>
              </div>
            </div>

            {/* Prescriptive Action Box */}
            <div className={`p-4 rounded-xl border ${isHigh ? 'bg-rose-950/30 border-rose-500/40' : 'bg-indigo-950/30 border-indigo-500/40'}`}>
              <div className="flex items-center gap-2 mb-1">
                <AlertTriangle className={`w-4 h-4 ${isHigh ? 'text-rose-400' : 'text-indigo-400'}`} />
                <span className={`text-xs font-black uppercase tracking-wider ${isHigh ? 'text-rose-300' : 'text-indigo-300'}`}>
                  Prescriptive Manager Action
                </span>
              </div>
              <p className="text-sm font-semibold text-slate-100 mb-3">
                {item.Manager_Action}
              </p>

              <div className="flex items-start gap-2 pt-2 border-t border-white/10 text-xs text-slate-300">
                <Info className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold text-slate-200">Root Cause Driver: </span>
                  {item.Key_Reasons}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

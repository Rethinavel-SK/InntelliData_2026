import React from 'react';
import { motion } from 'framer-motion';

export default function MetricCard({ label, value, subtext, icon: Icon, color = "indigo" }) {
  const colorMap = {
    indigo: "from-indigo-500/20 to-indigo-600/5 text-indigo-400 border-indigo-500/30",
    rose: "from-rose-500/20 to-rose-600/5 text-rose-400 border-rose-500/30",
    amber: "from-amber-500/20 to-amber-600/5 text-amber-400 border-amber-500/30",
    emerald: "from-emerald-500/20 to-emerald-600/5 text-emerald-400 border-emerald-500/30",
    cyan: "from-cyan-500/20 to-cyan-600/5 text-cyan-400 border-cyan-500/30",
  };

  return (
    <motion.div
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
      className={`cronza-glass p-5 rounded-2xl border bg-gradient-to-br ${colorMap[color] || colorMap.indigo} shadow-xl relative overflow-hidden`}
    >
      <div className="flex justify-between items-start mb-3">
        <span className="text-xs font-bold tracking-wider text-slate-400 uppercase">{label}</span>
        {Icon && (
          <div className={`p-2.5 rounded-xl bg-white/5 border border-white/10 ${colorMap[color]?.split(' ')[2]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>

      <div className="text-2xl lg:text-3xl font-extrabold text-white tracking-tight">
        {value}
      </div>

      {subtext && (
        <div className="mt-2 text-xs font-medium text-slate-400 flex items-center gap-1">
          {subtext}
        </div>
      )}
    </motion.div>
  );
}

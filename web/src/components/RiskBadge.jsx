import React from 'react';

export default function RiskBadge({ level }) {
  if (level === 'HIGH') {
    return (
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-extrabold bg-rose-500/15 border border-rose-500/40 text-rose-300 shadow-sm shadow-rose-900/30">
        <span className="w-1.5 h-1.5 rounded-full bg-rose-400 mr-1.5 animate-pulse"></span>
        HIGH RISK
      </span>
    );
  } else if (level === 'MEDIUM') {
    return (
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-extrabold bg-amber-500/15 border border-amber-500/40 text-amber-300 shadow-sm shadow-amber-900/30">
        <span className="w-1.5 h-1.5 rounded-full bg-amber-400 mr-1.5"></span>
        MEDIUM RISK
      </span>
    );
  } else {
    return (
      <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-extrabold bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 shadow-sm shadow-emerald-900/30">
        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5"></span>
        LOW RISK
      </span>
    );
  }
}

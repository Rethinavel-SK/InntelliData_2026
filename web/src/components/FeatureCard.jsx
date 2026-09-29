import React from 'react';
import { motion } from 'framer-motion';

export default function FeatureCard({ icon: Icon, title, description, badge }) {
  return (
    <motion.div
      whileHover={{ y: -6, transition: { duration: 0.2 } }}
      className="cronza-glass cronza-glass-hover p-8 rounded-2xl relative overflow-hidden group border border-white/10"
    >
      <div className="w-12 h-12 rounded-xl bg-indigo-500/15 border border-indigo-400/30 flex items-center justify-center text-indigo-400 mb-6 group-hover:scale-110 transition-transform">
        {Icon && <Icon className="w-6 h-6" />}
      </div>

      {badge && (
        <span className="absolute top-6 right-6 px-3 py-1 rounded-full text-[11px] font-extrabold tracking-wider uppercase bg-indigo-500/10 border border-indigo-400/20 text-indigo-300">
          {badge}
        </span>
      )}

      <h3 className="text-xl font-bold text-white mb-3 group-hover:text-indigo-300 transition-colors">
        {title}
      </h3>

      <p className="text-slate-400 text-sm leading-relaxed">
        {description}
      </p>
    </motion.div>
  );
}

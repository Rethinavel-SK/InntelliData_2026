import React, { useState } from 'react';
import { Zap, Send } from 'lucide-react';

export default function NewsletterFooter() {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (email) {
      setSubscribed(true);
      setTimeout(() => setSubscribed(false), 3000);
      setEmail('');
    }
  };

  return (
    <footer className="border-t border-white/10 bg-[#07090e] pt-16 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Newsletter Section matching Screenshot Section 7 */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center border-b border-white/10 pb-16">
          <div className="lg:col-span-6 space-y-3">
            <h3 className="text-2xl sm:text-4xl font-extrabold text-white">
              Make Sure You Don't Miss Any <span className="text-emerald-400">Inventory Info</span>.
            </h3>
            <p className="text-slate-400 text-sm">
              Subscribe to our operational newsletter to get the latest retail stock insights and market activities.
            </p>
          </div>

          <div className="lg:col-span-6">
            <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row items-center gap-3">
              <input
                type="email"
                placeholder="Enter Your Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-900 border border-white/10 rounded-full px-6 py-3.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
                required
              />
              <button
                type="submit"
                className="btn-emerald-glow px-8 py-3.5 rounded-full text-slate-950 font-black text-xs uppercase tracking-wider shrink-0 w-full sm:w-auto"
              >
                {subscribed ? 'SUBSCRIBED!' : 'SUBSCRIBE'}
              </button>
            </form>
          </div>
        </div>

        {/* Footer Multi-Column Links matching Screenshot Bottom Footer */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 py-12 text-xs">
          <div className="col-span-2 space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-emerald-500 text-slate-950 flex items-center justify-center font-black">
                <Zap className="w-4 h-4 fill-slate-950" />
              </div>
              <span className="text-lg font-black text-white">Stock<span className="text-emerald-400">Sense</span></span>
            </div>
            <p className="text-slate-400 text-xs max-w-xs">
              NovaMart AI Retail Inventory Optimization Platform built for IntelliData 2026.
            </p>
          </div>

          <div className="space-y-2">
            <div className="font-extrabold text-white uppercase tracking-wider mb-2">Navigation</div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">Home</a></div>
            <div><a href="#features" className="text-slate-400 hover:text-emerald-400">Market Activity</a></div>
            <div><a href="#how-it-works" className="text-slate-400 hover:text-emerald-400">News & Insight</a></div>
            <div><a href="#models" className="text-slate-400 hover:text-emerald-400">Solution</a></div>
          </div>

          <div className="space-y-2">
            <div className="font-extrabold text-white uppercase tracking-wider mb-2">Categories</div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">Beverages</a></div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">Dairy</a></div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">Snacks</a></div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">Personal Care</a></div>
          </div>

          <div className="space-y-2">
            <div className="font-extrabold text-white uppercase tracking-wider mb-2">Stores</div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">S01 Coimbatore</a></div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">S02 Chennai</a></div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">S03 Madurai</a></div>
            <div><a href="#" className="text-slate-400 hover:text-emerald-400">S04 Salem</a></div>
          </div>
        </div>

        <div className="pt-6 border-t border-white/5 text-center text-slate-500 text-xs flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Copyright © 2026 StockSense. All rights reserved.</span>
          <span>IntelliData 2026 • Sri Eshwar College of Engineering</span>
        </div>

      </div>
    </footer>
  );
}

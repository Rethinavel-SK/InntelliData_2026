import React from 'react';
import { ResponsiveContainer, LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

export default function DemandChart({ decisionData, selectedStore = 'ALL', selectedCategory = 'ALL' }) {
  if (!decisionData || decisionData.length === 0) {
    return (
      <div className="cronza-glass p-8 rounded-2xl border border-white/10 text-center text-slate-400">
        No demand data matches the selected filters.
      </div>
    );
  }

  // Aggregate daily demand & 7-day forecast by date for filtered dataset
  const dateMap = {};
  const storeMap = {};
  const categoryMap = {};

  decisionData.forEach(row => {
    const d = row.date;
    const store = row.store_id || row.Store || 'Unknown';
    const cat = row.category || row.Category || 'Unknown';

    const actual = Number(row.daily_demand || row.Current_Stock || 0);
    const forecast = Number(row.forecasted_7day_demand || row['7_Day_Forecast'] || 0);
    const revenue = Number(row.tx_total_revenue || 0);

    // Group by Date
    if (!dateMap[d]) {
      dateMap[d] = { date: d, actualDemand: 0, forecast7Day: 0, revenue: 0 };
    }
    dateMap[d].actualDemand += actual;
    dateMap[d].forecast7Day += Math.round(forecast / 7); // Daily average forecast
    dateMap[d].revenue += revenue;

    // Group by Store
    if (!storeMap[store]) {
      storeMap[store] = { store, totalDemand: 0, totalForecast: 0 };
    }
    storeMap[store].totalDemand += actual;
    storeMap[store].totalForecast += forecast;

    // Group by Category
    if (!categoryMap[cat]) {
      categoryMap[cat] = { category: cat, totalDemand: 0, totalForecast: 0 };
    }
    categoryMap[cat].totalDemand += actual;
    categoryMap[cat].totalForecast += forecast;
  });

  const timeData = Object.values(dateMap).sort((a, b) => new Date(a.date) - new Date(b.date));
  const storeChartData = Object.values(storeMap);
  const catChartData = Object.values(categoryMap);

  return (
    <div className="space-y-6">
      {/* Dynamic Line Chart */}
      <div className="cronza-glass p-6 rounded-2xl border border-white/10 shadow-2xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-4 gap-2">
          <div>
            <h4 className="text-lg font-extrabold text-white flex items-center gap-2">
              <span className="text-emerald-400">📈</span> Daily POS Demand History & Forecast Horizon
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              Filtered View: <span className="text-emerald-400 font-bold">{selectedStore === 'ALL' ? 'All Stores' : `Store ${selectedStore}`}</span> • <span className="text-emerald-400 font-bold">{selectedCategory === 'ALL' ? 'All Categories' : selectedCategory}</span>
            </p>
          </div>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }}
              />
              <Legend />
              <Line type="monotone" dataKey="actualDemand" name="Actual Daily POS Demand" stroke="#10b981" strokeWidth={3} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="forecast7Day" name="7-Day Model Forecast (Avg/Day)" stroke="#6366f1" strokeWidth={2} strokeDasharray="5 5" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Dynamic Category & Store Breakdown Charts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="cronza-glass p-6 rounded-2xl border border-white/10">
          <h5 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <span className="text-emerald-400">🏷️</span> Category Demand vs 7-Day Forecast
          </h5>
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={catChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="category" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }} />
                <Legend />
                <Bar dataKey="totalDemand" name="Actual Demand" fill="#10b981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="totalForecast" name="7-Day Forecast" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="cronza-glass p-6 rounded-2xl border border-white/10">
          <h5 className="text-sm font-bold text-white mb-4 flex items-center gap-2">
            <span className="text-emerald-400">🏬</span> Store Demand vs 7-Day Forecast
          </h5>
          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={storeChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="store" stroke="#64748b" tick={{ fontSize: 11 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }} />
                <Legend />
                <Bar dataKey="totalDemand" name="Actual Demand" fill="#06b6d4" radius={[4, 4, 0, 0]} />
                <Bar dataKey="totalForecast" name="7-Day Forecast" fill="#818cf8" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

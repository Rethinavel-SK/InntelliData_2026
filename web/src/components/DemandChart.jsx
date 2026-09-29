import React from 'react';
import { ResponsiveContainer, LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';

export default function DemandChart({ decisionData }) {
  if (!decisionData || decisionData.length === 0) {
    return <div className="p-6 text-center text-slate-400">No chart data available</div>;
  }

  // Aggregate daily demand trend by date
  const dateMap = {};
  decisionData.forEach(row => {
    const d = row.date;
    if (!dateMap[d]) {
      dateMap[d] = { date: d, actualDemand: 0, forecastDemand: 0 };
    }
    dateMap[d].actualDemand += Number(row.daily_demand || 0);
    dateMap[d].forecastDemand += Number(row.forecasted_7day_demand || row['7_Day_Forecast'] || 0) / 7;
  });

  const chartData = Object.values(dateMap).sort((a, b) => new Date(a.date) - new Date(b.date));

  return (
    <div className="space-y-6">
      <div className="cronza-glass p-6 rounded-2xl border border-white/10">
        <h4 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <span>📈</span> Daily POS Demand History & Forecast Horizon
        </h4>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="date" stroke="#64748b" tick={{ fontSize: 11 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 11 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }}
              />
              <Legend />
              <Line type="monotone" dataKey="actualDemand" name="Actual Daily POS Demand" stroke="#6366f1" strokeWidth={3} dot={{ r: 3 }} />
              <Line type="monotone" dataKey="forecastDemand" name="7-Day Model Forecast (Avg/Day)" stroke="#10b981" strokeWidth={2} strokeDasharray="5 5" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

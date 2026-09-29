import React from 'react';

export default function ModelPerformance({ demandComp, stockoutComp }) {
  return (
    <div className="space-y-6">
      {/* Champion Banner */}
      <div className="p-6 rounded-2xl bg-gradient-to-r from-indigo-950/60 to-purple-950/60 border border-indigo-500/30 backdrop-blur-xl">
        <div className="text-xs font-black uppercase text-indigo-400 tracking-wider mb-1">🏆 Production Machine Learning Champions</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
          <div className="bg-white/5 p-4 rounded-xl border border-white/10">
            <div className="text-xs text-slate-400 font-bold uppercase">7-Day Demand Forecasting</div>
            <div className="text-lg font-bold text-emerald-400 mt-1">Random Forest Regressor</div>
            <div className="text-xs text-slate-300 mt-1">MAE: 17.36 units | MAPE: 3.08% | R² Score: 0.9947</div>
          </div>
          <div className="bg-white/5 p-4 rounded-xl border border-white/10">
            <div className="text-xs text-slate-400 font-bold uppercase">Stock-out Classification</div>
            <div className="text-lg font-bold text-emerald-400 mt-1">Decision Tree Classifier</div>
            <div className="text-xs text-slate-300 mt-1">Accuracy: 96.25% | Recall: 100.0% | F1-Score: 0.9771</div>
          </div>
        </div>
      </div>

      {/* Benchmarking Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Demand Forecasting Table */}
        <div className="cronza-glass p-6 rounded-2xl border border-white/10">
          <h4 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <span>📈</span> 7-Day Demand Regression Benchmark
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900/80 uppercase text-slate-400 border-b border-white/10">
                <tr>
                  <th className="p-3">Model</th>
                  <th className="p-3 text-right">MAE</th>
                  <th className="p-3 text-right">RMSE</th>
                  <th className="p-3 text-right">R² Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {(demandComp.length > 0 ? demandComp : [
                  { model: "Random Forest", mae: 17.36, rmse: 23.09, r2_score: 0.9947 },
                  { model: "Decision Tree", mae: 19.64, rmse: 28.88, r2_score: 0.9918 },
                  { model: "KNN Regressor", mae: 25.79, rmse: 36.17, r2_score: 0.9871 },
                  { model: "Linear Regression", mae: 25.99, rmse: 31.82, r2_score: 0.9900 },
                  { model: "Baseline 7-Day Sum", mae: 27.36, rmse: 35.39, r2_score: 0.9876 },
                  { model: "XGBoost", mae: 28.92, rmse: 51.76, r2_score: 0.9735 },
                ]).map((r, idx) => (
                  <tr key={idx} className={idx === 0 ? "bg-emerald-500/10 font-bold" : ""}>
                    <td className="p-3 font-semibold text-white">{r.model}</td>
                    <td className="p-3 text-right">{r.mae}</td>
                    <td className="p-3 text-right">{r.rmse}</td>
                    <td className="p-3 text-right text-emerald-400 font-mono">{r.r2_score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Stockout Classification Table */}
        <div className="cronza-glass p-6 rounded-2xl border border-white/10">
          <h4 className="text-base font-bold text-white mb-4 flex items-center gap-2">
            <span>⚠️</span> Stock-out Classification Benchmark
          </h4>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="bg-slate-900/80 uppercase text-slate-400 border-b border-white/10">
                <tr>
                  <th className="p-3">Model</th>
                  <th className="p-3 text-right">Accuracy</th>
                  <th className="p-3 text-right">Recall</th>
                  <th className="p-3 text-right">F1-Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {(stockoutComp.length > 0 ? stockoutComp : [
                  { model: "Decision Tree", accuracy: 0.9625, recall: 1.0000, f1_score: 0.9771 },
                  { model: "Random Forest", accuracy: 0.9625, recall: 0.9844, f1_score: 0.9767 },
                  { model: "XGBoost", accuracy: 0.9500, recall: 0.9844, f1_score: 0.9692 },
                  { model: "Logistic Regression", accuracy: 0.9500, recall: 0.9688, f1_score: 0.9688 },
                  { model: "SVM Classifier", accuracy: 0.9125, recall: 0.9531, f1_score: 0.9457 },
                ]).map((r, idx) => (
                  <tr key={idx} className={idx === 0 ? "bg-emerald-500/10 font-bold" : ""}>
                    <td className="p-3 font-semibold text-white">{r.model}</td>
                    <td className="p-3 text-right">{(Number(r.accuracy) * 100).toFixed(2)}%</td>
                    <td className="p-3 text-right font-mono text-emerald-400">{(Number(r.recall) * 100).toFixed(1)}%</td>
                    <td className="p-3 text-right font-mono">{r.f1_score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

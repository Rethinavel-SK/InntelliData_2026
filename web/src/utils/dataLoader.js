import Papa from 'papaparse';

/**
 * Helper to fetch and parse CSV files asynchronously
 */
export async function fetchCSV(path) {
  try {
    const response = await fetch(path);
    if (!response.ok) {
      throw new Error(`Failed to fetch ${path}: ${response.statusText}`);
    }
    const text = await response.text();
    return new Promise((resolve, reject) => {
      Papa.parse(text, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: (results) => resolve(results.data),
        error: (error) => reject(error),
      });
    });
  } catch (err) {
    console.warn(`CSV fetch fallback for ${path}:`, err.message);
    return [];
  }
}

export async function loadAllDashboardData() {
  const [recommendations, decisionOutput, demandComparison, stockoutComparison] = await Promise.all([
    fetchCSV('/data/recommendations.csv'),
    fetchCSV('/data/stocksense_decision_output.csv'),
    fetchCSV('/data/demand_model_comparison.csv'),
    fetchCSV('/data/stockout_model_comparison.csv')
  ]);

  return {
    recommendations,
    decisionOutput,
    demandComparison,
    stockoutComparison
  };
}

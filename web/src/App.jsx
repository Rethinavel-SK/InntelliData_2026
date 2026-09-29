import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import NewsletterFooter from './components/NewsletterFooter';
import { loadAllDashboardData } from './utils/dataLoader';

export default function App() {
  const [activeTab, setActiveTab] = useState('landing');
  const [dashboardSubTab, setDashboardSubTab] = useState('summary');
  const [appData, setAppData] = useState({
    recommendations: [],
    demandComparison: [],
    stockoutComparison: []
  });

  useEffect(() => {
    async function init() {
      const res = await loadAllDashboardData();
      setAppData(res);
    }
    init();
  }, []);

  const handleOpenMLModels = () => {
    if (activeTab === 'dashboard') {
      setDashboardSubTab('performance');
    } else {
      setActiveTab('landing');
      setTimeout(() => {
        const el = document.getElementById('models');
        if (el) {
          el.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    }
  };

  return (
    <div className="min-h-screen flex flex-col justify-between">
      <div>
        <Navbar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          onOpenMLModels={handleOpenMLModels}
        />

        <main className="pt-2">
          {activeTab === 'landing' ? (
            <Landing
              onOpenDashboard={() => { setActiveTab('dashboard'); setDashboardSubTab('summary'); }}
              recommendations={appData.recommendations}
              demandComp={appData.demandComparison}
              stockoutComp={appData.stockoutComparison}
            />
          ) : (
            <Dashboard
              onBackToLanding={() => setActiveTab('landing')}
              initialTab={dashboardSubTab}
            />
          )}
        </main>
      </div>

      <NewsletterFooter />
    </div>
  );
}

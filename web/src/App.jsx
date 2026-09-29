import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import LoginModal from './components/LoginModal';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import NewsletterFooter from './components/NewsletterFooter';
import { loadAllDashboardData } from './utils/dataLoader';

export default function App() {
  const [user, setUser] = useState(null);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
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

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setActiveTab('dashboard');
    setDashboardSubTab('summary');
  };

  const handleLogout = () => {
    setUser(null);
    setActiveTab('landing');
  };

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
          user={user}
          onOpenLogin={() => setIsLoginOpen(true)}
          onLogout={handleLogout}
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          onOpenMLModels={handleOpenMLModels}
        />

        <main className="pt-2">
          {activeTab === 'landing' ? (
            <Landing
              onOpenDashboard={() => { setActiveTab('dashboard'); setDashboardSubTab('summary'); }}
              onOpenLogin={() => setIsLoginOpen(true)}
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

      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
}

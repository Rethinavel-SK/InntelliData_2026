import React, { useState } from 'react';
import Navbar from './components/Navbar';
import LoginModal from './components/LoginModal';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Footer from './components/Footer';

export default function App() {
  const [user, setUser] = useState(null);
  const [isLoginOpen, setIsLoginOpen] = useState(false);
  const [activeTab, setActiveTab] = useState('landing');

  const handleLoginSuccess = (userData) => {
    setUser(userData);
    setActiveTab('dashboard');
  };

  const handleLogout = () => {
    setUser(null);
    setActiveTab('landing');
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
        />

        <main className="pt-6">
          {activeTab === 'landing' ? (
            <Landing
              onOpenDashboard={() => setActiveTab('dashboard')}
              onOpenLogin={() => setIsLoginOpen(true)}
            />
          ) : (
            <Dashboard
              onBackToLanding={() => setActiveTab('landing')}
            />
          )}
        </main>
      </div>

      <Footer />

      <LoginModal
        isOpen={isLoginOpen}
        onClose={() => setIsLoginOpen(false)}
        onLoginSuccess={handleLoginSuccess}
      />
    </div>
  );
}

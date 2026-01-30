import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/DashBoard';
import Equipment from './pages/Equipment';
import UploadPage from './pages/UploadPages';
import LoginPage from './pages/LoginPage';
import './styles/App.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isDarkMode, setIsDarkMode] = useState(false);

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: (
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M3 3H8V10H3V3Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M3 13H8V17H3V13Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M12 3H17V7H12V3Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M12 10H17V17H12V10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    },
    {
      id: 'equipment',
      label: 'Equipment',
      icon: (
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M3 7H17V17H3V7Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M6 7V4C6 3.44772 6.44772 3 7 3H13C13.5523 3 14 3.44772 14 4V7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    },
    {
      id: 'upload',
      label: 'Upload Data',
      icon: (
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M17.5 12.5V15.8333C17.5 16.2754 17.3244 16.6993 17.0118 17.0118C16.6993 17.3244 16.2754 17.5 15.8333 17.5H4.16667C3.72464 17.5 3.30072 17.3244 2.98816 17.0118C2.67559 16.6993 2.5 16.2754 2.5 15.8333V12.5M14.1667 6.66667L10 2.5M10 2.5L5.83333 6.66667M10 2.5V12.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    },
    {
      id: 'history',
      label: 'History',
      icon: (
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M10 5V10L13 13" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    }
  ];

  const supportItems = [
    {
      id: 'help',
      label: 'Help Center',
      icon: (
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M7.5 7.5C7.5 6.11929 8.61929 5 10 5C11.3807 5 12.5 6.11929 12.5 7.5C12.5 8.88071 11.3807 10 10 10V11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <circle cx="10" cy="14" r="0.5" fill="currentColor"/>
        </svg>
      )
    },
    {
      id: 'settings',
      label: 'Settings',
      icon: (
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 12.5C11.3807 12.5 12.5 11.3807 12.5 10C12.5 8.61929 11.3807 7.5 10 7.5C8.61929 7.5 7.5 8.61929 7.5 10C7.5 11.3807 8.61929 12.5 10 12.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          <path d="M16.5 10C16.5 9.5 16.25 9 16 8.75L14.5 7.5L15 5.5C15 5 14.75 4.5 14.25 4.25L12.5 3.5L11.5 2C11 1.5 10.5 1.5 10 1.5C9.5 1.5 9 1.5 8.5 2L7.5 3.5L5.75 4.25C5.25 4.5 5 5 5 5.5L5.5 7.5L4 8.75C3.75 9 3.5 9.5 3.5 10C3.5 10.5 3.75 11 4 11.25L5.5 12.5L5 14.5C5 15 5.25 15.5 5.75 15.75L7.5 16.5L8.5 18C9 18.5 9.5 18.5 10 18.5C10.5 18.5 11 18.5 11.5 18L12.5 16.5L14.25 15.75C14.75 15.5 15 15 15 14.5L14.5 12.5L16 11.25C16.25 11 16.5 10.5 16.5 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      )
    }
  ];

  const renderContent = () => {
    switch(activeTab) {
      case 'dashboard':
        return <Dashboard isDarkMode={isDarkMode} />;
      case 'equipment':
        return <Equipment isDarkMode={isDarkMode} />;
      case 'upload':
        return <UploadPage isDarkMode={isDarkMode} />;
      case 'history':
        return (
          <div className="placeholder-content">
            <h1>History</h1>
            <p>History content coming soon...</p>
          </div>
        );
      case 'help':
        return (
          <div className="placeholder-content">
            <h1>Help Center</h1>
            <p>Help center content coming soon...</p>
          </div>
        );
      case 'settings':
        return (
          <div className="placeholder-content">
            <h1>Settings</h1>
            <p>Settings content coming soon...</p>
          </div>
        );
      default:
        return <Dashboard isDarkMode={isDarkMode} />;
    }
  };

  // Show login page if not logged in
  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className={`app-wrapper ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isDarkMode={isDarkMode}
        setIsDarkMode={setIsDarkMode}
        menuItems={menuItems}
        supportItems={supportItems}
      />
      <div className="main-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default App;
import React from 'react';
import '../styles/Sidebar.css';

const Sidebar = ({ activeTab, setActiveTab, isDarkMode, setIsDarkMode, menuItems, supportItems }) => {
  return (
    <div className={`sidebar ${isDarkMode ? 'dark' : 'light'}`}>
      <div className="sidebar-content">
        {/* Logo */}
        <div className="sidebar-logo">
          <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
            <rect width="36" height="36" rx="7" fill="#DC2626"/>
            <path d="M18 10L14 18H22L18 26" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className="logo-text">CHEMDATA</span>
        </div>

        {/* Navigation Menu */}
        <nav className="sidebar-nav">
          <div className="nav-section">
            {menuItems.map((item) => (
              <button
                key={item.id}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </button>
            ))}
          </div>

          {/* Support Section */}
          <div className="nav-section">
            <div className="section-label">SUPPORT</div>
            {supportItems.map((item) => (
              <button
                key={item.id}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={() => setActiveTab(item.id)}
              >
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-label">{item.label}</span>
              </button>
            ))}
          </div>
        </nav>

        {/* User Profile */}
        <div className="sidebar-footer">
          <div className="user-profile">
            <div className="user-avatar">
              <span>DS</span>
            </div>
            <div className="user-info">
              <div className="user-name">Dr. Sam Wheeler</div>
              <div className="user-role">Chief Engineer</div>
            </div>
          </div>
          
          {/* Theme Toggle */}
          <button 
            className="theme-toggle-sidebar"
            onClick={() => setIsDarkMode(!isDarkMode)}
            aria-label="Toggle theme"
          >
            {isDarkMode ? (
              <svg width="22" height="22" viewBox="0 0 20 20" fill="none">
                <path d="M10 3V5M10 15V17M17 10H15M5 10H3M15.5 4.5L14 6M6 14L4.5 15.5M15.5 15.5L14 14M6 6L4.5 4.5M13 10C13 11.6569 11.6569 13 10 13C8.34315 13 7 11.6569 7 10C7 8.34315 8.34315 7 10 7C11.6569 7 13 8.34315 13 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            ) : (
              <svg width="22" height="22" viewBox="0 0 20 20" fill="none">
                <path d="M17 10.5C16.8 14.6 13.4 18 9.3 18C5.2 18 2 14.8 2 10.7C2 6.6 5.4 3.2 9.5 3C9.2 3.6 9 4.3 9 5C9 7.8 11.2 10 14 10C15.1 10 16.1 9.6 16.9 9C17 9.5 17 10 17 10.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
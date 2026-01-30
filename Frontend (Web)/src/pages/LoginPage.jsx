import React, { useState } from 'react';
import apiService from '../services/api';
import '../styles/LoginPage.css';

const LoginPage = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Call API login
      await apiService.login(email, password);
      
      // If remember me is checked, store a flag
      if (rememberMe) {
        localStorage.setItem('rememberMe', 'true');
      }
      
      // Call parent onLogin to update app state
      onLogin();
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSubmit();
    }
  };

  return (
    <div className={`login-container ${isDarkMode ? 'dark' : 'light'}`}>
      <button 
        className="theme-toggle"
        onClick={() => setIsDarkMode(!isDarkMode)}
        aria-label="Toggle theme"
      >
        {isDarkMode ? '☀️' : '🌙'}
      </button>

      <div className="login-header">
        <div className="logo">
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="6" fill="#2563EB"/>
            <path d="M16 8L12 16H20L16 24" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span className="logo-text">ChemData.io</span>
        </div>
      </div>

      <div className="login-card">
        <div className="card-header">
          <h1>Welcome Back</h1>
          <p>Enter your credentials to access the equipment dashboard.</p>
        </div>

        {error && (
          <div className="error-message">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M10 6V10M10 14H10.01" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            {error}
          </div>
        )}

        <div className="login-form">
          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <div className="input-wrapper">
              <span className="input-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M2.5 5.83333L10 10.8333L17.5 5.83333M3.33333 15H16.6667C17.5871 15 18.3333 14.2538 18.3333 13.3333V6.66667C18.3333 5.74619 17.5871 5 16.6667 5H3.33333C2.41286 5 1.66667 5.74619 1.66667 6.66667V13.3333C1.66667 14.2538 2.41286 15 3.33333 15Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </span>
              <input
                type="email"
                id="email"
                placeholder="name@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <div className="input-wrapper">
              <span className="input-icon">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M5.83333 9.16667V6.66667C5.83333 4.36548 7.69881 2.5 10 2.5C12.3012 2.5 14.1667 4.36548 14.1667 6.66667V9.16667M10 12.0833V13.75M6.66667 17.5H13.3333C14.2538 17.5 15 16.7538 15 15.8333V10.8333C15 9.91286 14.2538 9.16667 13.3333 9.16667H6.66667C5.74619 9.16667 5 9.91286 5 10.8333V15.8333C5 16.7538 5.74619 17.5 6.66667 17.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </span>
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <button
                type="button"
                className="toggle-password"
                onClick={() => setShowPassword(!showPassword)}
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                disabled={loading}
              >
                {showPassword ? (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M2.5 2.5L17.5 17.5M8.818 8.818C8.309 9.327 8 10.027 8 10.8C8 12.346 9.254 13.6 10.8 13.6C11.574 13.6 12.273 13.291 12.782 12.782M14.364 14.364C13.174 15.255 11.674 15.8 10 15.8C5.6 15.8 2 12.2 2 10C2 9.083 2.364 8.083 2.964 7.164M5.636 4.964C6.826 4.073 8.326 3.528 10 3.528C14.4 3.528 18 7.128 18 9.328C18 10.245 17.636 11.245 17.036 12.164" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 12.5C11.381 12.5 12.5 11.381 12.5 10C12.5 8.619 11.381 7.5 10 7.5C8.619 7.5 7.5 8.619 7.5 10C7.5 11.381 8.619 12.5 10 12.5Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    <path d="M1.667 10C1.667 10 4.167 4.167 10 4.167C15.833 4.167 18.333 10 18.333 10C18.333 10 15.833 15.833 10 15.833C4.167 15.833 1.667 10 1.667 10Z" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                )}
              </button>
            </div>
          </div>

          <div className="form-options">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                disabled={loading}
              />
              <span>Remember me</span>
            </label>
            <button 
              className="forgot-password" 
              onClick={() => console.log('Forgot password')}
              disabled={loading}
            >
              Forgot Password?
            </button>
          </div>

          <button 
            onClick={handleSubmit} 
            className="sign-in-btn"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Signing In...
              </>
            ) : (
              'Sign In'
            )}
          </button>
        </div>

        <div className="card-footer">
          <span>Don't have an account?</span>
          <button 
            className="contact-admin" 
            onClick={() => console.log('Contact admin')}
            disabled={loading}
          >
            Contact Admin
          </button>
        </div>
      </div>

      <footer className="login-footer">
        © 2023 Chemical Data Solutions. All rights reserved.
      </footer>
    </div>
  );
};

export default LoginPage;

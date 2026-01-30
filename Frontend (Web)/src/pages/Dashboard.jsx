import React, { useEffect, useState } from 'react';
import { useDashboardStats, useAlerts, useCharts} from '../hooks/useApi';
import '../styles/DashBoard.css';

const Dashboard = ({ isDarkMode }) => {
  const [timeframe, setTimeframe] = useState('24h');
  const [location, setLocation] = useState('all');
  const [equipmentType, setEquipmentType] = useState('all');

  // Fetch dashboard stats from API
  const { data: stats, loading: statsLoading, error: statsError, refetch: refetchStats } = useDashboardStats({
    timeframe,
    location: location !== 'all' ? location : undefined,
    equipment_type: equipmentType !== 'all' ? equipmentType : undefined
  });

  const { data: chartData, loading: chartLoading } = useCharts({
    type: 'temperature_pressure_trends', 
    dark_mode: isDarkMode
  });

  // Fetch alerts
  const { data: alerts, loading: alertsLoading } = useAlerts({
    severity: 'critical',
    limit: 5
  });

  // Default stats if API data not available
  const dashboardStats = stats ? {
    ...stats,
    // Create the nested object the UI expects
    equipment_status: {
      normal: stats.normal_count || 0,
      warning: stats.warning_count || 0,
      critical: stats.critical_count || 0,
      offline: stats.offline_count || 0
    },
    // Default trends to 0 since backend doesn't calculate them yet
    pressure_trend: stats.pressure_trend || 0,
    temperature_trend: stats.temperature_trend || 0,
    equipment_capacity: 150 // Hardcoded capacity
  } : {
    total_equipment: 0,
    avg_pressure: 0,
    avg_temperature: 0,
    max_flowrate: 0,
    equipment_capacity: 150,
    equipment_status: { normal: 0, warning: 0, critical: 0 }
  };

  const criticalAlerts = alerts?.results || alerts || [];

  return (
    <main className="dashboard-main">
      <div className="dashboard-header">
        <div className="header-left">
          <h1 className="page-title">Equipment Overview</h1>
          <p className="page-subtitle">Monitor and manage your chemical processing equipment</p>
        </div>
        <div className="header-actions">
          <button className="btn-secondary">
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M10 3V17M3 10H17" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
            </svg>
            Import CSV
          </button>
          <button className="btn-primary">
            <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M10 3V13M10 13L6 9M10 13L14 9M3 17H17" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
            Download Report
          </button>
        </div>
      </div>

      <div className="dashboard-filters">
        <div className="filter-group">
          <label>Timeframe</label>
          <select 
            className="filter-select"
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
          >
            <option value="24h">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
        </div>
        <div className="filter-group">
          <label>Plant Location</label>
          <select 
            className="filter-select"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          >
            <option value="all">All Locations</option>
            <option value="north">North Plant</option>
            <option value="south">South Plant</option>
            <option value="east">East Plant</option>
          </select>
        </div>
        <div className="filter-group">
          <label>Equipment Type</label>
          <select 
            className="filter-select"
            value={equipmentType}
            onChange={(e) => setEquipmentType(e.target.value)}
          >
            <option value="all">All Types</option>
            <option value="reactors">Reactors</option>
            <option value="pumps">Pumps</option>
            <option value="mixers">Mixers</option>
          </select>
        </div>
      </div>

      {statsLoading ? (
        <div className="loading-container">
          <div className="spinner-large"></div>
          <p>Loading dashboard data...</p>
        </div>
      ) : statsError ? (
        <div className="error-container">
          <svg width="48" height="48" viewBox="0 0 20 20" fill="none">
            <path d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18Z" stroke="currentColor" strokeWidth="1.5"/>
            <path d="M10 6V10M10 14H10.01" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          <h3>Failed to load dashboard data</h3>
          <p>{statsError}</p>
          <button onClick={refetchStats} className="retry-button">Try Again</button>
        </div>
      ) : (
        <>
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-label">Total Equipment</span>
                <div className="stat-icon blue">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <rect x="3" y="7" width="14" height="10" stroke="currentColor" strokeWidth="1.5" rx="1"/>
                    <path d="M6 7V4C6 3.44772 6.44772 3 7 3H13C13.5523 3 14 3.44772 14 4V7" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                </div>
              </div>
              <div className="stat-value">{dashboardStats.total_equipment}</div>
              <div className="stat-footer">
                <span className="stat-meta">/ {dashboardStats.equipment_capacity} capacity</span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-label">Avg Pressure</span>
                <div className="stat-icon purple">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 3V17M3 10H17" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                </div>
              </div>
              <div className="stat-value">
                {dashboardStats.avg_pressure.toFixed(0)} <span className="stat-unit">PSI</span>
              </div>
              <div className="stat-footer">
                <span className={`stat-trend ${dashboardStats.pressure_trend >= 0 ? 'up' : 'down'}`}>
                  {dashboardStats.pressure_trend >= 0 ? '↗' : '↘'} {Math.abs(dashboardStats.pressure_trend || 0).toFixed(1)}%
                </span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-label">Avg Temperature</span>
                <div className="stat-icon orange">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M10 14V6M8 6H12M8 9H12M10 14C11.1046 14 12 13.1046 12 12C12 10.8954 11.1046 10 10 10C8.89543 10 8 10.8954 8 12C8 13.1046 8.89543 14 10 14Z" stroke="currentColor" strokeWidth="1.5"/>
                  </svg>
                </div>
              </div>
              <div className="stat-value">{dashboardStats.avg_temperature.toFixed(0)}°C</div>
              <div className="stat-footer">
                <span className={`stat-trend ${dashboardStats.temperature_trend >= 0 ? 'up' : 'down'}`}>
                  {dashboardStats.temperature_trend >= 0 ? '↗' : '↘'} {Math.abs(dashboardStats.temperature_trend || 0).toFixed(1)}%
                </span>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-header">
                <span className="stat-label">Max Flowrate</span>
                <div className="stat-icon teal">
                  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <path d="M3 10H17M17 10L13 6M17 10L13 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </div>
              </div>
              <div className="stat-value">
                {dashboardStats.max_flowrate.toFixed(0)} <span className="stat-unit">L/min</span>
              </div>
              <div className="stat-footer">
                <span className="stat-meta">Optimal range</span>
              </div>
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="dashboard-card">
              <div className="card-header">
                <h3>Equipment Status</h3>
                <button className="card-menu">⋯</button>
              </div>
              <div className="card-content">
                {dashboardStats.equipment_status ? (
                  <div className="status-breakdown">
                    <div className="status-item">
                      <div className="status-indicator normal"></div>
                      <span className="status-label">Normal</span>
                      <span className="status-count">{dashboardStats.equipment_status.normal || 0}</span>
                    </div>
                    <div className="status-item">
                      <div className="status-indicator warning"></div>
                      <span className="status-label">Warning</span>
                      <span className="status-count">{dashboardStats.equipment_status.warning || 0}</span>
                    </div>
                    <div className="status-item">
                      <div className="status-indicator critical"></div>
                      <span className="status-label">Critical</span>
                      <span className="status-count">{dashboardStats.equipment_status.critical || 0}</span>
                    </div>
                  </div>
                ) : (
                  <p className="card-placeholder">Chart and equipment status visualization will appear here</p>
                )}
              </div>
            </div>

            <div className="dashboard-card">
              <div className="card-header">
                <h3>Pressure Trends</h3>
                <span className="card-badge">PSI</span>
              </div>
              <div className="card-content">
                {chartLoading ? (
                  <div className="loading-small">Loading Chart...</div>
                ) : chartData?.chart ? (
                  <img 
                    src={chartData.chart} 
                    alt="Pressure Trends" 
                    style={{ width: '100%', height: 'auto', borderRadius: '8px' }} 
                  />
                ) : (
                  <p className="card-placeholder">No chart data available</p>
                )}
              </div>
            </div>

            <div className="dashboard-card full-width">
              <div className="card-header">
                <h3>High-Pressure Alerts</h3>
                <span className={`alert-badge critical`}>
                  {criticalAlerts.length} Critical
                </span>
              </div>
              <div className="card-content">
                {alertsLoading ? (
                  <div className="loading-small">Loading alerts...</div>
                ) : criticalAlerts.length > 0 ? (
                  <div className="alerts-list">
                    {criticalAlerts.map((alert, index) => (
                      <div key={alert.id || index} className="alert-item">
                        <div className="alert-icon critical">!</div>
                        <div className="alert-details">
                          <div className="alert-title">{alert.message || alert.title}</div>
                          <div className="alert-meta">
                            {alert.equipment_name} • {new Date(alert.created_at).toLocaleString()}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="card-placeholder">No critical alerts at this time</p>
                )}
              </div>
            </div>
          </div>
        </>
      )}
    </main>
  );
};

export default Dashboard;

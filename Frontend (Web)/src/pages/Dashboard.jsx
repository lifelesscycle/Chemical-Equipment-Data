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
                  <div className={`status-grid ${isDarkMode ? 'dark-mode' : 'light-mode'}`}>
                    <div className="status-card status-normal">
                      <div className="status-card-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                          <path d="M20 6L9 17L4 12" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      </div>
                      <div className="status-card-label">Normal</div>
                      <div className="status-card-count">{dashboardStats.equipment_status.normal || 0}</div>
                      <div className="status-card-footer">Equipment</div>
                    </div>
                    
                    <div className="status-card status-warning">
                      <div className="status-card-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                          <path d="M12 9V13M12 17H12.01M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                        </svg>
                      </div>
                      <div className="status-card-label">Warning</div>
                      <div className="status-card-count">{dashboardStats.equipment_status.warning || 0}</div>
                      <div className="status-card-footer">Equipment</div>
                    </div>
                    
                    <div className="status-card status-critical">
                      <div className="status-card-icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                          <path d="M12 9V13M12 17H12.01M10.29 3.86L1.82 18C1.64537 18.3024 1.55296 18.6453 1.55199 18.9945C1.55101 19.3437 1.64151 19.6871 1.81445 19.9905C1.98738 20.2939 2.23675 20.5467 2.53773 20.7239C2.83871 20.9011 3.18082 20.9962 3.53 21H20.47C20.8192 20.9962 21.1613 20.9011 21.4623 20.7239C21.7633 20.5467 22.0126 20.2939 22.1856 19.9905C22.3585 19.6871 22.449 19.3437 22.448 18.9945C22.447 18.6453 22.3546 18.3024 22.18 18L13.71 3.86C13.5317 3.56611 13.2807 3.32312 12.9812 3.15448C12.6817 2.98585 12.3437 2.89725 12 2.89725C11.6563 2.89725 11.3183 2.98585 11.0188 3.15448C10.7193 3.32312 10.4683 3.56611 10.29 3.86Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                      </div>
                      <div className="status-card-label">Critical</div>
                      <div className="status-card-count">{dashboardStats.equipment_status.critical || 0}</div>
                      <div className="status-card-footer">Equipment</div>
                    </div>

                    {dashboardStats.equipment_status.offline !== undefined && (
                      <div className="status-card status-offline">
                        <div className="status-card-icon">
                          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2"/>
                            <path d="M15 9L9 15M9 9L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                          </svg>
                        </div>
                        <div className="status-card-label">Offline</div>
                        <div className="status-card-count">{dashboardStats.equipment_status.offline || 0}</div>
                        <div className="status-card-footer">Equipment</div>
                      </div>
                    )}
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

import React, { useState, useEffect } from 'react';
import { Droplet, Gauge, Thermometer, AlertTriangle, CheckCircle, BarChart3, Grid3X3, Search } from 'lucide-react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter } from 'recharts';
import { useEquipment, useEquipmentTypes } from '../hooks/useApi';
import '../styles/Equipment.css';

// Safe Operating Ranges (fallback if not provided by API)
const defaultSafeRanges = {
  Pump: { flowrate: [100, 150], pressure: [4, 7], temperature: [100, 120] },
  Compressor: { flowrate: [80, 120], pressure: [7, 10], temperature: [90, 100] },
  Valve: { flowrate: [50, 70], pressure: [3, 5], temperature: [100, 110] },
  HeatExchanger: { flowrate: [140, 170], pressure: [5, 8], temperature: [120, 140] },
  Reactor: { flowrate: [130, 160], pressure: [6, 9], temperature: [130, 145] },
  Condenser: { flowrate: [150, 180], pressure: [6, 8], temperature: [120, 135] }
};



// Utility Functions
const checkStatus = (equipment, safeRanges) => {
  const ranges = safeRanges[equipment.type] || defaultSafeRanges[equipment.type];
  if (!ranges) return 'unknown';
  
  const flowrateOk = equipment.flowrate >= ranges.flowrate[0] && equipment.flowrate <= ranges.flowrate[1];
  const pressureOk = equipment.pressure >= ranges.pressure[0] && equipment.pressure <= ranges.pressure[1];
  const tempOk = equipment.temperature >= ranges.temperature[0] && equipment.temperature <= ranges.temperature[1];
  return flowrateOk && pressureOk && tempOk ? 'normal' : 'warning';
};

const getEquipmentIcon = (type) => {
  switch(type) {
    case 'Pump':
    case 'Compressor':
      return <Droplet className="equipment-icon" size={24} />;
    case 'Valve':
      return <Gauge className="equipment-icon" size={24} />;
    case 'Reactor':
    case 'HeatExchanger':
    case 'Condenser':
      return <Thermometer className="equipment-icon" size={24} />;
    default:
      return <Gauge className="equipment-icon" size={24} />;
  }
};

// Search and Controls Component
const SearchAndControls = ({ searchTerm, setSearchTerm }) => {
  return (
    <div className="search-controls">
      <div className="search-bar-container">
        <Search className="search-icon" size={20} />
        <input
          type="text"
          placeholder="Search equipment by name or type..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>
    </div>
  );
};

// Stats Summary Component
const StatsSummary = ({ equipmentData, safeRanges }) => {
  const normalCount = equipmentData.filter(eq => checkStatus(eq, safeRanges) === 'normal').length;
  const warningCount = equipmentData.filter(eq => checkStatus(eq, safeRanges) === 'warning').length;

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <div className="stat-content">
          <div>
            <p className="stat-label">Total Equipment</p>
            <p className="stat-value">{equipmentData.length}</p>
          </div>
          <Gauge className="stat-icon" size={40} />
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-content">
          <div>
            <p className="stat-label">Normal Status</p>
            <p className="stat-value stat-value-success">{normalCount}</p>
          </div>
          <CheckCircle className="icon-success" size={40} />
        </div>
      </div>
      <div className="stat-card">
        <div className="stat-content">
          <div>
            <p className="stat-label">Warnings</p>
            <p className="stat-value stat-value-warning">{warningCount}</p>
          </div>
          <AlertTriangle className="icon-warning" size={40} />
        </div>
      </div>
    </div>
  );
};

// Equipment Card Component
const EquipmentCard = ({ equipment, safeRanges }) => {
  const status = checkStatus(equipment, safeRanges);

  return (
    <div className="equipment-card">
      <div className="equipment-card-header">
        <div className="equipment-info">
          {getEquipmentIcon(equipment.type)}
          <div>
            <h3 className="equipment-name">{equipment.name}</h3>
            <p className="equipment-type">{equipment.type}</p>
          </div>
        </div>
        <div className={`status-badge ${status === 'normal' ? 'status-normal' : 'status-warning'}`}>
          <span className="status-text">
            {status === 'normal' ? 'NORMAL' : 'WARNING'}
          </span>
        </div>
      </div>

      <div className="equipment-metrics">
        <div className="metric-item">
          <span className="metric-label">Flowrate</span>
          <span className="metric-value">{equipment.flowrate} L/min</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Pressure</span>
          <span className="metric-value">{equipment.pressure} bar</span>
        </div>
        <div className="metric-item">
          <span className="metric-label">Temperature</span>
          <span className="metric-value">{equipment.temperature}°C</span>
        </div>
      </div>
    </div>
  );
};

// Equipment Grid Component
const EquipmentGrid = ({ filteredData, safeRanges, loading }) => {
  if (loading) {
    return (
      <div className="loading-container">
        <div className="spinner-large"></div>
        <p>Loading equipment data...</p>
      </div>
    );
  }

  return (
    <div className="equipment-grid">
      {filteredData.length > 0 ? (
        filteredData.map((equipment) => (
          <EquipmentCard key={equipment.id} equipment={equipment} safeRanges={safeRanges} />
        ))
      ) : (
        <div className="no-results">
          <p>No equipment found matching your search.</p>
        </div>
      )}
    </div>
  );
};

// Charts Components
const FlowrateComparisonChart = ({ darkMode, data }) => {
  return (
    <div className="chart-card">
      <h3 className="chart-title">Flowrate Comparison</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#374151' : '#e5e7eb'} />
          <XAxis dataKey="name" stroke={darkMode ? '#9ca3af' : '#6b7280'} angle={-45} textAnchor="end" height={100} />
          <YAxis stroke={darkMode ? '#9ca3af' : '#6b7280'} label={{ value: 'L/min', angle: -90, position: 'insideLeft' }} />
          <Tooltip contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}` }} />
          <Bar dataKey="flowrate" fill="#3b82f6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const TemperaturePressureChart = ({ darkMode, data }) => {
  return (
    <div className="chart-card">
      <h3 className="chart-title">Temperature & Pressure Trends</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#374151' : '#e5e7eb'} />
          <XAxis dataKey="name" stroke={darkMode ? '#9ca3af' : '#6b7280'} angle={-45} textAnchor="end" height={100} />
          <YAxis stroke={darkMode ? '#9ca3af' : '#6b7280'} />
          <Tooltip contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}` }} />
          <Legend />
          <Line type="monotone" dataKey="temperature" stroke="#ef4444" strokeWidth={2} name="Temperature (°C)" />
          <Line type="monotone" dataKey="pressure" stroke="#10b981" strokeWidth={2} name="Pressure (bar)" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

const EquipmentTypeDistribution = ({ darkMode, data }) => {
  const typeCounts = data.reduce((acc, eq) => {
    acc[eq.type] = (acc[eq.type] || 0) + 1;
    return acc;
  }, {});

  const pieData = Object.entries(typeCounts).map(([type, count]) => ({
    name: type,
    value: count
  }));

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  return (
    <div className="chart-card">
      <h3 className="chart-title">Equipment Type Distribution</h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={pieData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {pieData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}` }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

const PressureTemperatureScatter = ({ darkMode, data }) => {
  return (
    <div className="chart-card">
      <h3 className="chart-title">Pressure vs Temperature Correlation</h3>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" stroke={darkMode ? '#374151' : '#e5e7eb'} />
          <XAxis type="number" dataKey="pressure" name="Pressure" unit=" bar" stroke={darkMode ? '#9ca3af' : '#6b7280'} />
          <YAxis type="number" dataKey="temperature" name="Temperature" unit="°C" stroke={darkMode ? '#9ca3af' : '#6b7280'} />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: darkMode ? '#1f2937' : '#ffffff', border: `1px solid ${darkMode ? '#374151' : '#e5e7eb'}` }} />
          <Scatter name="Equipment" data={data} fill="#8b5cf6" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

// Main Equipment Component
const Equipment = ({ isDarkMode }) => {
  const [view, setView] = useState('grid');
  const [searchTerm, setSearchTerm] = useState('');
  const [safeRanges, setSafeRanges] = useState(defaultSafeRanges);

  // Fetch equipment data from API
  const { data: equipmentData, loading, error, refetch } = useEquipment();
  const { data: equipmentTypes } = useEquipmentTypes();

  const rawData = Array.isArray(equipmentData)
    ? equipmentData
    : Array.isArray(equipmentData?.results)
      ? equipmentData.results
      : [];

  // Process equipment data
  const processedData = rawData.map(item => ({
    ...item,
    // Fix undefined types by checking alternate field names
    type: item.type || item.equipment_type_name || 'Unknown', 
    location: item.location || item.plant_location_name || 'Unknown'
  }));


  // Update safe ranges if equipment types provide them
  useEffect(() => {
    if (equipmentTypes) {
      const newRanges = {};

      const typesList = Array.isArray(equipmentTypes) 
        ? equipmentTypes 
        : (equipmentTypes.results || []);

      typesList.forEach(type => {
        if (type.safe_ranges) {
          newRanges[type.name] = type.safe_ranges;
        }
      });

      if (Object.keys(newRanges).length > 0) {
        setSafeRanges({ ...defaultSafeRanges, ...newRanges });
      }
    }
  }, [equipmentTypes]);

  const filteredData = processedData.filter(equipment => 
    equipment.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    equipment.type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Handle error state
  if (error) {
    return (
      <div className={isDarkMode ? 'app-dark' : 'app-light'}>
        <div className="main-container">
          <div className="error-container">
            <AlertTriangle size={48} className="error-icon" />
            <h2>Failed to load equipment data</h2>
            <p>{error}</p>
            <button onClick={refetch} className="retry-button">
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={isDarkMode ? 'app-dark' : 'app-light'}>
      <div className="main-container">
        <SearchAndControls 
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
        />

        <StatsSummary equipmentData={processedData} safeRanges={safeRanges} />

        <div className="view-toggle">
          <button
            onClick={() => setView('grid')}
            className={`toggle-button ${view === 'grid' ? 'toggle-active' : 'toggle-inactive'}`}
          >
            <Grid3X3 size={20} />
            <span>Equipment Grid</span>
          </button>
          <button
            onClick={() => setView('charts')}
            className={`toggle-button ${view === 'charts' ? 'toggle-active' : 'toggle-inactive'}`}
          >
            <BarChart3 size={20} />
            <span>Analytics Charts</span>
          </button>
        </div>

        {view === 'grid' ? (
          <EquipmentGrid 
            filteredData={filteredData} 
            safeRanges={safeRanges} 
            loading={loading}
          />
        ) : (
          <div className="charts-container">
            <FlowrateComparisonChart darkMode={isDarkMode} data={filteredData} />
            <TemperaturePressureChart darkMode={isDarkMode} data={filteredData} />
            <div className="charts-grid">
              <EquipmentTypeDistribution darkMode={isDarkMode} data={filteredData} />
              <PressureTemperatureScatter darkMode={isDarkMode} data={filteredData} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Equipment;

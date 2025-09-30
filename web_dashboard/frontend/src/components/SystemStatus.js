import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Thermometer, 
  Droplets, 
  Sun, 
  Zap,
  RefreshCw,
  AlertTriangle,
  CheckCircle
} from 'lucide-react';
import './SystemStatus.css';

const SystemStatus = ({ systemStatus, onRefresh }) => {
  const [sensorData, setSensorData] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (systemStatus) {
      setSensorData(systemStatus.sensor_data || {});
    }
  }, [systemStatus]);

  const handleRefresh = async () => {
    setLoading(true);
    try {
      await onRefresh();
    } finally {
      setLoading(false);
    }
  };

  const getSensorIcon = (sensorType) => {
    switch (sensorType) {
      case 'temperature':
        return <Thermometer size={20} />;
      case 'humidity':
        return <Droplets size={20} />;
      case 'light':
        return <Sun size={20} />;
      case 'soil_moisture':
        return <Droplets size={20} />;
      default:
        return <Activity size={20} />;
    }
  };

  const getSensorStatus = (sensor) => {
    if (sensor.status === 'error') {
      return { status: 'error', color: '#dc3545', text: 'Error' };
    }
    if (sensor.value === null || sensor.value === undefined) {
      return { status: 'warning', color: '#ffc107', text: 'No Data' };
    }
    return { status: 'ok', color: '#28a745', text: 'OK' };
  };

  const getRelayStatus = (isActive) => {
    return isActive ? 
      { status: 'active', color: '#28a745', text: 'ON' } :
      { status: 'inactive', color: '#6c757d', text: 'OFF' };
  };

  return (
    <div className="system-status-page">
      <div className="page-header">
        <h1 className="page-title">System Status</h1>
        <p className="page-subtitle">Monitor system health and sensor data</p>
        <button 
          className="btn btn-primary refresh-btn"
          onClick={handleRefresh}
          disabled={loading}
        >
          <RefreshCw size={16} className={loading ? 'spinning' : ''} />
          {loading ? 'Refreshing...' : 'Refresh'}
        </button>
      </div>

      {/* System Overview */}
      <div className="system-overview">
        <div className="overview-card">
          <div className="overview-header">
            <Activity size={24} />
            <h3>System Status</h3>
          </div>
          <div className="overview-content">
            <div className="status-item">
              <span className="status-label">Overall Status:</span>
              <span className={`status-badge ${systemStatus?.is_running ? 'success' : 'danger'}`}>
                {systemStatus?.is_running ? 'ONLINE' : 'OFFLINE'}
              </span>
            </div>
            <div className="status-item">
              <span className="status-label">Last Updated:</span>
              <span className="status-value">
                {systemStatus?.timestamp ? 
                  new Date(systemStatus.timestamp).toLocaleString() : 
                  'Never'
                }
              </span>
            </div>
            <div className="status-item">
              <span className="status-label">Active Sensors:</span>
              <span className="status-value">
                {Object.keys(sensorData).length}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Sensor Data */}
      <div className="sensors-section">
        <h3 className="section-title">Sensor Data</h3>
        <div className="sensor-grid">
          {Object.entries(sensorData).map(([sensorName, sensor]) => {
            const sensorStatus = getSensorStatus(sensor);
            return (
              <div key={sensorName} className="sensor-card">
                <div className="sensor-header">
                  <div className="sensor-icon">
                    {getSensorIcon(sensor.type || sensorName)}
                  </div>
                  <div className="sensor-name">
                    {sensorName.replace('_', ' ').toUpperCase()}
                  </div>
                  <div 
                    className="sensor-status"
                    style={{ color: sensorStatus.color }}
                  >
                    {sensorStatus.text}
                  </div>
                </div>
                <div className="sensor-value">
                  {sensor.value !== null && sensor.value !== undefined ? 
                    `${sensor.value} ${sensor.unit || ''}` : 
                    'N/A'
                  }
                </div>
                <div className="sensor-timestamp">
                  {sensor.timestamp ? 
                    new Date(sensor.timestamp).toLocaleTimeString() : 
                    'No data'
                  }
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Relay Status */}
      {systemStatus?.relay_states && (
        <div className="relays-section">
          <h3 className="section-title">Relay Status</h3>
          <div className="relay-grid">
            {Object.entries(systemStatus.relay_states).map(([pin, isActive]) => {
              const relayStatus = getRelayStatus(isActive);
              return (
                <div key={pin} className="relay-card">
                  <div className="relay-header">
                    <Zap size={20} />
                    <span className="relay-name">Relay {pin}</span>
                    <span 
                      className="relay-status"
                      style={{ color: relayStatus.color }}
                    >
                      {relayStatus.text}
                    </span>
                  </div>
                  <div className="relay-indicator">
                    <div 
                      className={`indicator ${relayStatus.status}`}
                      style={{ backgroundColor: relayStatus.color }}
                    ></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Motor Status */}
      {systemStatus?.motor_position !== undefined && (
        <div className="motor-section">
          <h3 className="section-title">Motor Status</h3>
          <div className="motor-card">
            <div className="motor-info">
              <div className="motor-item">
                <span className="motor-label">Current Position:</span>
                <span className="motor-value">
                  {systemStatus.motor_position}°
                </span>
              </div>
              <div className="motor-item">
                <span className="motor-label">Status:</span>
                <span className="motor-status">
                  <CheckCircle size={16} />
                  Operational
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* System Logs */}
      <div className="logs-section">
        <h3 className="section-title">System Logs</h3>
        <div className="log-container">
          <div className="log-entry info">
            <span className="timestamp">{new Date().toLocaleTimeString()}</span>
            System status refreshed
          </div>
          {systemStatus?.is_running && (
            <div className="log-entry success">
              <span className="timestamp">{new Date().toLocaleTimeString()}</span>
              All systems operational
            </div>
          )}
          {Object.entries(sensorData).map(([sensorName, sensor]) => {
            if (sensor.status === 'error') {
              return (
                <div key={sensorName} className="log-entry error">
                  <span className="timestamp">{new Date().toLocaleTimeString()}</span>
                  Sensor {sensorName} error: {sensor.error || 'Unknown error'}
                </div>
              );
            }
            return null;
          })}
        </div>
      </div>
    </div>
  );
};

export default SystemStatus;

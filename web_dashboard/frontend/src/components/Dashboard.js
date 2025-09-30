import React, { useState, useEffect } from 'react';
import { 
  Camera, 
  Activity, 
  AlertTriangle, 
  CheckCircle,
  TrendingUp,
  Users
} from 'lucide-react';
import './Dashboard.css';

const Dashboard = ({ systemStatus, realtimeData }) => {
  const [statistics, setStatistics] = useState(null);
  const [recentDetections, setRecentDetections] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch statistics
      const statsResponse = await fetch('/statistics');
      const statsData = await statsResponse.json();
      setStatistics(statsData);
      
      // Fetch recent detections
      const detectionsResponse = await fetch('/detections?limit=5');
      const detectionsData = await detectionsResponse.json();
      setRecentDetections(detectionsData.detections || []);
      
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSystemHealthStatus = () => {
    if (!systemStatus) return { status: 'unknown', color: 'gray' };
    
    const isOnline = systemStatus.is_running;
    const sensorCount = Object.keys(systemStatus.sensor_data || {}).length;
    
    if (isOnline && sensorCount > 0) {
      return { status: 'healthy', color: 'green' };
    } else if (isOnline) {
      return { status: 'warning', color: 'yellow' };
    } else {
      return { status: 'error', color: 'red' };
    }
  };

  const healthStatus = getSystemHealthStatus();

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="page-header">
        <h1 className="page-title">Farm Dashboard</h1>
        <p className="page-subtitle">Monitor your pest detection system in real-time</p>
      </div>

      {/* System Status Overview */}
      <div className="stats-grid">
        <div className="stat-card success">
          <div className="stat-icon">
            <CheckCircle size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{statistics?.total_detections || 0}</div>
            <div className="stat-label">Total Detections</div>
            <div className="stat-change positive">
              +{statistics?.recent_activity || 0} today
            </div>
          </div>
        </div>

        <div className="stat-card info">
          <div className="stat-icon">
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">
              <span className={`status-indicator ${healthStatus.status}`}></span>
              {healthStatus.status.toUpperCase()}
            </div>
            <div className="stat-label">System Status</div>
            <div className="stat-change">
              {systemStatus ? 'All systems operational' : 'System offline'}
            </div>
          </div>
        </div>

        <div className="stat-card warning">
          <div className="stat-icon">
            <AlertTriangle size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">
              {Object.keys(statistics?.pest_types || {}).length}
            </div>
            <div className="stat-label">Pest Types Detected</div>
            <div className="stat-change">
              {statistics?.pest_types ? 
                Object.entries(statistics.pest_types).map(([type, count]) => 
                  `${type}: ${count}`
                ).join(', ') : 
                'No pests detected'
              }
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">
              {statistics?.confidence_stats?.avg ? 
                (statistics.confidence_stats.avg * 100).toFixed(1) + '%' : 
                'N/A'
              }
            </div>
            <div className="stat-label">Avg Confidence</div>
            <div className="stat-change">
              Min: {statistics?.confidence_stats?.min ? 
                (statistics.confidence_stats.min * 100).toFixed(1) + '%' : 
                'N/A'
              }
            </div>
          </div>
        </div>
      </div>

      {/* Real-time Data */}
      {realtimeData && (
        <div className="alert alert-info">
          <strong>Real-time Update:</strong> {realtimeData.type} - 
          {realtimeData.data ? JSON.stringify(realtimeData.data) : 'No data'}
        </div>
      )}

      {/* Recent Detections */}
      <div className="chart-container">
        <h3 className="chart-title">Recent Pest Detections</h3>
        {recentDetections.length > 0 ? (
          <div className="detection-list">
            {recentDetections.map((detection, index) => (
              <div key={index} className="detection-item">
                <div className="detection-info">
                  <div className="detection-time">
                    {new Date(detection.timestamp).toLocaleString()}
                  </div>
                  <div className="detection-filename">
                    {detection.filename}
                  </div>
                </div>
                <div className="detection-stats">
                  <span className="detection-count">
                    {detection.results?.total_detections || 0} pests detected
                  </span>
                  <div className="detection-confidence">
                    Avg: {detection.results?.detections?.length > 0 ? 
                      (detection.results.detections.reduce((sum, d) => sum + d.confidence, 0) / 
                       detection.results.detections.length * 100).toFixed(1) + '%' : 
                      'N/A'
                    }
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="no-data">
            <Camera size={48} />
            <p>No recent detections</p>
            <p>Upload an image to start detecting pests</p>
          </div>
        )}
      </div>

      {/* Quick Actions */}
      <div className="chart-container">
        <h3 className="chart-title">Quick Actions</h3>
        <div className="action-buttons">
          <button className="btn btn-primary">
            <Camera size={16} />
            New Detection
          </button>
          <button className="btn btn-success">
            <Activity size={16} />
            System Status
          </button>
          <button className="btn btn-warning">
            <AlertTriangle size={16} />
            Emergency Stop
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

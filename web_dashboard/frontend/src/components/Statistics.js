import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { TrendingUp, BarChart3, PieChart as PieChartIcon, Activity } from 'lucide-react';
import './Statistics.css';

const Statistics = () => {
  const [statistics, setStatistics] = useState(null);
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('7d');

  useEffect(() => {
    fetchStatistics();
  }, [timeRange]);

  const fetchStatistics = async () => {
    try {
      setLoading(true);
      
      // Fetch statistics
      const statsResponse = await fetch('/statistics');
      const statsData = await statsResponse.json();
      setStatistics(statsData);
      
      // Fetch detections for charts
      const detectionsResponse = await fetch('/detections?limit=100');
      const detectionsData = await detectionsResponse.json();
      setDetections(detectionsData.detections || []);
      
    } catch (error) {
      console.error('Error fetching statistics:', error);
    } finally {
      setLoading(false);
    }
  };

  const processPestTypeData = () => {
    if (!statistics?.pest_types) return [];
    
    return Object.entries(statistics.pest_types).map(([name, count]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      count: count,
      percentage: ((count / statistics.total_detections) * 100).toFixed(1)
    }));
  };

  const processTimeSeriesData = () => {
    // Group detections by date
    const groupedData = {};
    
    detections.forEach(detection => {
      const date = new Date(detection.timestamp).toDateString();
      if (!groupedData[date]) {
        groupedData[date] = {
          date: date,
          detections: 0,
          pests: 0
        };
      }
      groupedData[date].detections += 1;
      groupedData[date].pests += detection.results?.total_detections || 0;
    });
    
    return Object.values(groupedData).slice(-7); // Last 7 days
  };

  const processConfidenceData = () => {
    const confidenceRanges = [
      { range: '0-20%', min: 0, max: 0.2, count: 0 },
      { range: '20-40%', min: 0.2, max: 0.4, count: 0 },
      { range: '40-60%', min: 0.4, max: 0.6, count: 0 },
      { range: '60-80%', min: 0.6, max: 0.8, count: 0 },
      { range: '80-100%', min: 0.8, max: 1.0, count: 0 }
    ];
    
    detections.forEach(detection => {
      const detections = detection.results?.detections || [];
      detections.forEach(det => {
        const confidence = det.confidence;
        const range = confidenceRanges.find(r => confidence >= r.min && confidence < r.max);
        if (range) range.count++;
      });
    });
    
    return confidenceRanges;
  };

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7C7C'];

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading statistics...</p>
      </div>
    );
  }

  const pestTypeData = processPestTypeData();
  const timeSeriesData = processTimeSeriesData();
  const confidenceData = processConfidenceData();

  return (
    <div className="statistics-page">
      <div className="page-header">
        <h1 className="page-title">Statistics & Analytics</h1>
        <p className="page-subtitle">Analyze pest detection patterns and trends</p>
        <div className="time-range-selector">
          <select 
            value={timeRange} 
            onChange={(e) => setTimeRange(e.target.value)}
            className="time-select"
          >
            <option value="1d">Last 24 Hours</option>
            <option value="7d">Last 7 Days</option>
            <option value="30d">Last 30 Days</option>
            <option value="90d">Last 90 Days</option>
          </select>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Activity size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{statistics?.total_detections || 0}</div>
            <div className="stat-label">Total Detections</div>
            <div className="stat-change positive">
              +{statistics?.recent_activity || 0} recent
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <BarChart3 size={24} />
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
              Range: {statistics?.confidence_stats?.min ? 
                (statistics.confidence_stats.min * 100).toFixed(1) + '%' : 
                'N/A'
              } - {statistics?.confidence_stats?.max ? 
                (statistics.confidence_stats.max * 100).toFixed(1) + '%' : 
                'N/A'
              }
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <PieChartIcon size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">
              {Object.keys(statistics?.pest_types || {}).length}
            </div>
            <div className="stat-label">Pest Types</div>
            <div className="stat-change">
              Most common: {pestTypeData.length > 0 ? pestTypeData[0].name : 'None'}
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">
              {timeSeriesData.length > 0 ? 
                Math.round(timeSeriesData.reduce((sum, day) => sum + day.detections, 0) / timeSeriesData.length) : 
                0
              }
            </div>
            <div className="stat-label">Daily Average</div>
            <div className="stat-change">
              Last {timeSeriesData.length} days
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="charts-grid">
        {/* Pest Types Bar Chart */}
        <div className="chart-container">
          <h3 className="chart-title">Pest Types Detected</h3>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={pestTypeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Detection Timeline */}
        <div className="chart-container">
          <h3 className="chart-title">Detection Timeline</h3>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={timeSeriesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="detections" stroke="#8884d8" strokeWidth={2} />
                <Line type="monotone" dataKey="pests" stroke="#82ca9d" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Confidence Distribution */}
        <div className="chart-container">
          <h3 className="chart-title">Confidence Distribution</h3>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={confidenceData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ range, count }) => `${range}: ${count}`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {confidenceData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pest Types Pie Chart */}
        <div className="chart-container">
          <h3 className="chart-title">Pest Distribution</h3>
          <div className="chart-content">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pestTypeData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentage }) => `${name}: ${percentage}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {pestTypeData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Data Table */}
      <div className="chart-container">
        <h3 className="chart-title">Recent Detections</h3>
        <div className="data-table">
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Image</th>
                <th>Pests Detected</th>
                <th>Avg Confidence</th>
                <th>Pest Types</th>
              </tr>
            </thead>
            <tbody>
              {detections.slice(0, 10).map((detection, index) => (
                <tr key={index}>
                  <td>{new Date(detection.timestamp).toLocaleString()}</td>
                  <td>{detection.filename}</td>
                  <td>{detection.results?.total_detections || 0}</td>
                  <td>
                    {detection.results?.detections?.length > 0 ? 
                      (detection.results.detections.reduce((sum, d) => sum + d.confidence, 0) / 
                       detection.results.detections.length * 100).toFixed(1) + '%' : 
                      'N/A'
                    }
                  </td>
                  <td>
                    {detection.results?.detections?.map(d => d.class_name).join(', ') || 'None'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Statistics;

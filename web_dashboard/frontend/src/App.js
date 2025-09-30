import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Header from './components/Header';
import Dashboard from './components/Dashboard';
import Detection from './components/Detection';
import SystemStatus from './components/SystemStatus';
import Statistics from './components/Statistics';
import Sidebar from './components/Sidebar';

import './App.css';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [systemStatus, setSystemStatus] = useState(null);
  const [realtimeData, setRealtimeData] = useState(null);

  useEffect(() => {
    // Initialize WebSocket connection for real-time updates
    const ws = new WebSocket('ws://localhost:8000/ws');
    
    ws.onopen = () => {
      console.log('WebSocket connected');
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setRealtimeData(data);
      
      if (data.type === 'new_detection') {
        // Handle new detection notification
        console.log('New pest detection:', data.data);
      }
    };
    
    ws.onclose = () => {
      console.log('WebSocket disconnected');
    };
    
    // Fetch initial system status
    fetchSystemStatus();
    
    return () => {
      ws.close();
    };
  }, []);

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('/system/status');
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error('Error fetching system status:', error);
    }
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <Router>
      <div className="app">
        <Header onToggleSidebar={toggleSidebar} />
        <div className="app-body">
          <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
          <main className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <Routes>
              <Route path="/" element={<Dashboard systemStatus={systemStatus} realtimeData={realtimeData} />} />
              <Route path="/detection" element={<Detection />} />
              <Route path="/system" element={<SystemStatus systemStatus={systemStatus} onRefresh={fetchSystemStatus} />} />
              <Route path="/statistics" element={<Statistics />} />
            </Routes>
          </main>
        </div>
        <ToastContainer
          position="top-right"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
        />
      </div>
    </Router>
  );
}

export default App;

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Camera, 
  Activity, 
  BarChart3, 
  Settings,
  X
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ isOpen, onClose }) => {
  const location = useLocation();

  const menuItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/detection', icon: Camera, label: 'Pest Detection' },
    { path: '/system', icon: Activity, label: 'System Status' },
    { path: '/statistics', icon: BarChart3, label: 'Statistics' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ];

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>Menu</h2>
          <button className="close-button" onClick={onClose}>
            <X size={20} />
          </button>
        </div>
        <nav className="sidebar-nav">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`nav-item ${isActive ? 'active' : ''}`}
                onClick={onClose}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
        <div className="sidebar-footer">
          <div className="system-status">
            <div className="status-indicator online"></div>
            <span>System Online</span>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;

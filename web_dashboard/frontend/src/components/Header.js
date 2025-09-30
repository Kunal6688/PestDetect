import React from 'react';
import { Menu, Bell, Settings } from 'lucide-react';
import './Header.css';

const Header = ({ onToggleSidebar }) => {
  return (
    <header className="header">
      <div className="header-left">
        <button className="menu-button" onClick={onToggleSidebar}>
          <Menu size={24} />
        </button>
        <h1 className="header-title">Pest Detection System</h1>
      </div>
      <div className="header-right">
        <button className="notification-button">
          <Bell size={20} />
          <span className="notification-badge">3</span>
        </button>
        <button className="settings-button">
          <Settings size={20} />
        </button>
        <div className="user-info">
          <span className="user-name">Farmer</span>
        </div>
      </div>
    </header>
  );
};

export default Header;

import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

const navLinks = [
  { path: '/', name: 'Real-time' },
  { path: '/monitoring', name: 'Monitoring' },
  { path: '/execution', name: 'Test Execution' },
  { path: '/dashboard', name: 'Dashboard' },
  { path: '/configuration', name: 'Configuration' },
];

const Layout = () => {
  return (
    <div className="drawer lg:drawer-open" data-theme="cyberpunk">
      <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content flex flex-col items-center p-4">
        <label htmlFor="my-drawer-2" className="btn btn-primary drawer-button lg:hidden mb-4">
          Open Menu
        </label>
        <Outlet />
      </div>
      <div className="drawer-side">
        <label htmlFor="my-drawer-2" aria-label="close sidebar" className="drawer-overlay"></label>
        <ul className="menu p-4 w-60 min-h-full bg-base-200 text-base-content">
          <li className="text-xl font-bold mb-4 p-4">Emulflow 2.0</li>
          {navLinks.map((link) => (
            <li key={link.path}>
              <NavLink
                to={link.path}
                className={({ isActive }) => (isActive ? 'active' : '')}
              >
                {link.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Layout; 
import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  const navbarStyle = {
    // backgroundColor: 'white',
  };

  const navLinkStyle = {
    color: 'black', 
    marginRight: '15px', 
    textDecoration: 'none', 
    fontWeight: 'bold', 
    fontSize: '16px', 
    transition: 'background-color 0.3s, color 0.3s', 
    padding: '10px 20px', 
    backgroundColor: 'transparent', 
  };

  // Hover effect styles
  const hoverStyle = {
    backgroundColor: '#007bff', // Change background color on hover
    color: 'white', // Change text color on hover
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light" style={navbarStyle}>
      <div className="container">
        <ul className="navbar-nav align-items-center" style={{ marginLeft: 'auto' }}>
          <li className="nav-item">
            <Link className="nav-link" to="/ExplorePackages" style={navLinkStyle} activeStyle={hoverStyle}>
              Explore Graphs
            </Link>
          </li>
          <li className="nav-item">
            <Link className="nav-link" to="/" style={navLinkStyle} activeStyle={hoverStyle}>
              Search Package
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

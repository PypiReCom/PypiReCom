import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import logo from '../Assets/logo.png'; // Import your logo

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

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
        {location.pathname === '/comparison_Matrix' && ( // Conditional rendering of the logo
          <Link to="/comparison_Matrix">
            <img src={logo} alt="Logo" style={{ height: '40px', marginRight: 'auto' }} />
          </Link>
        )}
        <button 
          className="navbar-toggler" 
          type="button" 
          onClick={() => setIsOpen(!isOpen)}
          aria-controls="navbarSupportedContent" 
          aria-expanded={isOpen ? 'true' : 'false'}
          aria-label="Toggle navigation"
          style={{position: 'absolute', top: 10, right: 10, backgroundColor: 'transparent', border: 'none'}}
        >
          {isOpen ? (
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="24" 
              height="24" 
              fill="currentColor" 
              className="bi bi-x" 
              viewBox="0 0 16 16"
              style={{color: 'black'}}
            >
              <path fillRule="evenodd" d="M12.354 3.354a.5.5 0 0 0-.708-.708L8 7.293 4.354 3.646a.5.5 0 1 0-.708.708L7.293 8l-3.647 3.646a.5.5 0 0 0 .708.708L8 8.707l3.646 3.647a.5.5 0 0 0 .708-.708L8.707 8l3.647-3.646z"/>
            </svg>
          ) : (
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              width="24" 
              height="24" 
              fill="currentColor" 
              className="bi bi-list" 
              viewBox="0 0 16 16"
              style={{color: 'black'}}
            >
              <path fillRule="evenodd" d="M2 3.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5zm0 5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5zm0 5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5z"/>
            </svg>
          )}
        </button>
        <div className={`collapse navbar-collapse ${isOpen ? 'show' : ''}`} id="navbarSupportedContent">
          <ul className="navbar-nav align-items-center" style={{ marginLeft: 'auto' }}>
            <li className="nav-item">
              <Link className="nav-link" to="/ExplorePackages" style={navLinkStyle} activestyle={hoverStyle}>
                Explore Graphs
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/" style={navLinkStyle} activestyle={hoverStyle}>
                Search Package
              </Link>
            </li>
            <li className="nav-item">
              <Link className="nav-link" to="/comparison_Matrix" style={navLinkStyle} activestyle={hoverStyle}>
                Comparison Matrix
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

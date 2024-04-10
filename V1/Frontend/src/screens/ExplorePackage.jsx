import React, { useState, useEffect } from 'react';
import Footer from "../components/Footer.jsx";
import Navbar from "../components/Navbar.jsx";
import logo from '../Assets/logo.png';
import { useNavigate } from 'react-router-dom';
import { BASE_URL } from '../api-endpoint.js';

export default function ExplorePackage() {
  const [searchContextList, setSearchContextList] = useState([]);
  const [dateUpdated, setDateUpdated] = useState([]);
  const [totalPackages, setTotalPackages] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`${BASE_URL}/get_seach_context_list`);
        const data = await response.json();
        setSearchContextList(data['Search Context']);
        setDateUpdated(data['Date Updated']);
        setTotalPackages(data['Total Packages']);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleSearch = (context) => {
    navigate(`/?searchText=${context}`);
  };

  return (
    <div>
      <Navbar />

      <div className="text-center mt-5 mb-4">
        <img src={logo} alt="Logo" style={{ width: '300px' }} />
      </div>

      <h3 className="text-center mb-4">Package Data Ready for you!</h3>

      <div className="row justify-content-center">
        <div className="col-md-10">
          {isLoading ? (
            <p>Loading...</p>
          ) : (
            <table className="table table-bordered table-hover">
              <thead className="thead-dark">
                <tr>
                  <th style={{ width: '40%' }}>Search Context</th>
                  <th style={{ width: '20%' }}>Date Updated</th>
                  <th style={{ width: '20%' }}>Total Packages</th>
                  <th style={{ width: '20%' }}>Search</th>
                </tr>
              </thead>
              <tbody>
                {searchContextList.map((context, index) => (
                  <tr key={index}>
                    <td>{context}</td>
                    <td>{dateUpdated[index]}</td>
                    <td>{totalPackages[index]}</td>
                    <td>
                      <button 
                        className="btn btn-primary btn-sm"
                        onClick={() => handleSearch(context)}
                      >
                        Search
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <Footer />
    </div>
  );
}


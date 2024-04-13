import React, { useState, useEffect } from 'react';
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import logo from '../Assets/logo.png';
import { useNavigate } from 'react-router-dom';
import { BASE_URL } from "../api-endpoint";

export default function About() {
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

  const handleComparison = (context) => {
    navigate(`/comparison_Matrix?searchText=${context}`); // Redirect to comparison matrix page
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
                  <th style={{ width: '40%' }}>Search Context</th> {/* Updated column header */}
                  <th style={{ width: '20%' }}>Date Updated</th>
                  <th style={{ width: '20%' }}>Total Packages</th>
                  <th style={{ width: '20%' }}>Actions</th> {/* New column header */}
                </tr>
              </thead>
              <tbody>
                {searchContextList.map((context, index) => (
                  <tr key={index}>
                    <td>{context}</td>
                    <td>{dateUpdated[index]}</td>
                    <td>{totalPackages[index]}</td>
                    <td> {/* Actions column */}
                      <div className="d-flex justify-content-between">
                        <button 
                          className="btn btn-primary btn-sm mr-2"
                          onClick={() => handleSearch(context)}
                        >
                          Search
                        </button>
                        <button 
                          className="btn btn-success btn-sm"
                          onClick={() => handleComparison(context)}
                        >
                          Compare
                        </button>
                      </div>
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

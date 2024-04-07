import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import logo from '../Assets/logo.png';
import InfiniteLogo from "../components/InfiniteLogo";
import { useLocation } from 'react-router-dom';
import GraphComponent from "../components/Graph";

export default function Home() {
  const [searchText, setSearchText] = useState('');
  const [results, setResults] = useState([]);
  const [GraphData, setGraph] = useState([]);
  const [filteredResults, setFilteredResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [tableRendered, setTableRendered] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [searched, setSearched] = useState(false);
  const location = useLocation(); 
  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const searchTextParam = searchParams.get('searchText');
    if (searchTextParam) {
      setSearchText(searchTextParam);
      // fetchData();
    }
  }, [location.search]); 

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`https://pypirecom-api.azurewebsites.net/search?Search_Text=${searchText}`);
      const data = await response.json();
      
      if (data === "Please check back again" || data === "Check back after few minutes result is being prepared.") {
        setErrorMessage(data);
        setResults([]);
      } else {
        setResults(data.result);
        setGraph(data);
        setFilteredResults(data.result); // Initialize filteredResults with all results
        setErrorMessage('');
      }
      
    } catch (error) {
      console.error("Error fetching data:", error);
      setErrorMessage("Error fetching data. Please try again.");
      setResults([]);
    } finally {
      setIsLoading(false);
      setTableRendered(true);
      setSearched(true); // Set searched to true when fetching data completes
    }
  };

  const handleSearch = () => {
    if (searchText) {
      fetchData();
    }
  };

  const handleStatusFilter = (status) => {
    setSelectedStatus(status);
    filterResultsByStatus(status); // Trigger filtering process
  };

  const filterResultsByStatus = (status) => {
    if (status === '') {
      setFilteredResults(results); // If no filter selected, show all results
    } else {
      const filtered = results.filter(item => item.attributes.dev_status === status);
      setFilteredResults(filtered);
    }
  };

  // Function to handle downloading graph file
  const downloadGraphFile = async () => {
    try {
      const response = await fetch(`https://pypirecom-api.azurewebsites.net/get_graph_file?Search_Text=${searchText}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'graph_file.json');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error("Error downloading graph file:", error);
    }
  };

  // Function to handle downloading GML file
  const downloadGmlFile = async () => {
    try {
      const response = await fetch(`https://pypirecom-api.azurewebsites.net/get_gml_file?Search_Text=${searchText}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(new Blob([blob]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'graph_file.gml');
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
    } catch (error) {
      console.error("Error downloading GML file:", error);
    }
  };

  const clearSearch = () => {
    setSearchText('');
    setResults([]);
    setFilteredResults([]);
    setTableRendered(false);
    setSearched(false);
    setSelectedStatus('');
    window.location.href = '/'; // Redirect to the home page
  };

  return (
    <div>
      <Navbar />
      
      <div className="container mt-5">
        <div className="row justify-content-center">
          <div className="col-md-8 text-center">
            <img src={logo} alt="Logo" style={{ width: '300px' }} />
            <h3 className="mt-4">Get the perfect Python package for you!</h3>
          </div>
        </div>
        
        <div className="row justify-content-center mt-4">
          <div className="col-md-6">
            <div className="input-group">
              <input 
                type="text" 
                className="form-control" 
                placeholder="Search for a Python package..." 
                aria-label="Search for a Python package" 
                aria-describedby="basic-addon2"
                value={searchText}
                onChange={(e) => setSearchText(e.target.value)}
              />
              <button className="btn btn-outline-secondary" type="button" onClick={handleSearch}>Search</button>
              <button className="btn btn-outline-secondary" type="button" onClick={clearSearch}>Clear</button>           
            </div>
          </div>
          <div className="col-md-3">
            <div className="input-group">
              <label className="input-group-text" htmlFor="statusFilter">Filter by Status:</label>
              <select id="statusFilter" className="form-select" value={selectedStatus} onChange={(e) => handleStatusFilter(e.target.value)}>
                <option value="">All</option>
                <option value="4 - Beta">Beta</option>
                <option value="5 - Production/Stable">Production/Stable</option>
                <option value="3 - Alpha">Alpha</option>
                <option value="2 - Pre-Alpha">Pre-Alpha</option>
              </select>
            </div>
          </div>
        </div>

        {searched &&  errorMessage !== "Please check back again" && errorMessage !== "Check back after few minutes result is being prepared." && ( // Render buttons only if user has searched something
          <div className="row justify-content-center mt-4">
            <div className="col-md-3">
              <button className="btn btn-primary w-100 mb-2 mb-md-0" onClick={downloadGraphFile}>Download Graph File</button>
            </div>
            <div className="col-md-3">
              <button className="btn btn-primary w-100" onClick={downloadGmlFile}>Download GML File</button>
            </div>
          </div>
        )}
       {searched && errorMessage !== "Please check back again" && errorMessage !== "Check back after few minutes result is being prepared." && (
  <GraphComponent data={GraphData} />
)}
        {tableRendered && (
          <div className="row justify-content-center mt-4">
            <div className="col-md-10">
              {isLoading ? (
                <p className="text-center">Loading...</p>
              ) : (
                errorMessage ? (
                  <p className="text-center">{errorMessage}</p>
                ) : (
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Package Name</th>
                        <th>Author</th>
                        <th>Email</th>
                        <th>Development Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredResults && filteredResults.length > 0 ? (
                        filteredResults.map((item, index) => (
                          <tr key={index}>
                            <td>{item.v_id}</td>
                            <td>{item.attributes.author}</td>
                            <td>{item.attributes.author_email}</td>
                            <td>{item.attributes.dev_status}</td>
                          </tr>
                        ))
                      ) : (
                        <tr>
                          <td colSpan="4" className="text-center">No results found</td>
                        </tr>
                      )}
                    </tbody>
                  </table>
                )
              )}
            </div>
          </div>
        )}
      </div>
      
      
      <h4 className="text-center mt-5 mb-4">Contributing Libraries</h4>
      <InfiniteLogo/>
      
      {/* {data.result && Object.keys(data.result).length >0 && < GraphComponent data={data.result} />} */}

      <Footer />
    </div>
  );
}

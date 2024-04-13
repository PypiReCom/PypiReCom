import React, { useState, useEffect } from "react";
import Footer from "../components/Footer";
import SearchBar from "../components/Searchbar";
import { BASE_URL } from "../api-endpoint";
import Navbar from "../components/Navbar";
import InfiniteLogo from "../components/InfiniteLogo";
import { useLocation } from 'react-router-dom';

export default function ComparisonPage() {
  const [searchText, setSearchText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [comparisonData, setComparisonData] = useState([]);
  const [errorMessage, setErrorMessage] = useState('');
  const [selectedOptions, setSelectedOptions] = useState({});
  const [truePositive, setTruePositive] = useState('');
  const [trueNegative, setTrueNegative] = useState('');
  const location = useLocation();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const searchTextParam = searchParams.get('searchText');
    if (searchTextParam && searchTextParam !== searchText) {
      setSearchText(searchTextParam);
    }
  }, [location.search, searchText]);

  useEffect(() => {
    if (searchText) {
      fetchComparisonData(searchText);
    }
  }, [searchText]);

  const fetchComparisonData = async (searchText) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${BASE_URL}/search?Search_Text=${searchText}`);
      const data = await response.json();
      if (data === "Please check back again" || data === "Check back after few minutes result is being prepared.") {
        setErrorMessage(data);
        setComparisonData([]);
        setTruePositive('');
        setTrueNegative(''); 
      } else {
        setComparisonData(data);
        setErrorMessage('');
        updateConfusionMatrix(data); // Update confusion matrix based on fetched data
        fetchPipResult(searchText); 
        
      }
    } catch (error) {
      console.error("Error fetching comparison data:", error);
      setErrorMessage("Error fetching comparison data. Please try again.");
      setComparisonData(null);
      setTruePositive('');
      setTrueNegative('');
    } finally {
      setIsLoading(false);
    }
  };
  

  const updateConfusionMatrix = (data) => {
    // Calculate true positive and true negative values based on selected options
    if (Object.keys(selectedOptions).length > 0) {
      let relevantPackagesCount = 0;
      data.result.forEach(pkg => {
        if (Object.keys(selectedOptions).some(option => pkg.attributes.dev_status.includes(option))) {
          relevantPackagesCount++;
        }
      });
      setTruePositive(relevantPackagesCount);
      setTrueNegative(data.result.length - relevantPackagesCount);
    } else {
      const relevantPackages = data.result.filter(pkg => pkg.attributes.dev_status.includes('4 - Beta') || pkg.attributes.dev_status.includes('5 - Production/Stable'));
      setTruePositive(relevantPackages.length);
      setTrueNegative(data.result.length - relevantPackages.length);
    }
  };

  const handleSearch = (searchText) => {
    if (searchText) {
      fetchComparisonData(searchText);
    }
  };

  const handleOptionSelect = (option) => {
    setSelectedOptions(prevOptions => {
      if (prevOptions[option]) {
        const updatedOptions = { ...prevOptions };
        delete updatedOptions[option];
        return updatedOptions;
      } else {
        return { ...prevOptions, [option]: true };
      }
    });
  };

  const fetchPipResult = async (searchText) => {
    try {
      const response = await fetch(`${BASE_URL}/get_json_file?Search_Text=${searchText}`);
      const data = await response.json();
      if (data && data.result) {
        const packageNames = data.result.map(pkg => pkg.v_id);
        setComparisonData(prevData => ({
          ...prevData,
          Pip: { result: packageNames }
        }));
      }
    } catch (error) {
      console.error("Error fetching pip result:", error);
    }
  };

  const clearSearch = () => {
    
    setIsLoading(false);
    setComparisonData([]);
    setErrorMessage('');
    setSelectedOptions({});
    setTruePositive('');
    setTrueNegative('');
    // setSearched(false);
  };


  return (
    <div>
      <Navbar />
      <div className="container mt-5">
      <h2 className="text-center mb-4">Package Comparison Tool</h2>
        {/* Search input */}
        <div className="row justify-content-center">
          <div className="col-md-6">
            <SearchBar handleSearch={handleSearch} clearSearch={clearSearch}/>
          </div>
        </div>
        {/* Confusion Matrix and Filter Options */}
        
        <div className="row justify-content-center mt-4">
          {/* Confusion Matrix */}
          {!isLoading && comparisonData && truePositive !== '' && trueNegative !== '' &&(
          <div className="col-md-6">
            <div className="border p-3" style={{ minHeight: '210px' }}>
              <h4>Confusion Matrix</h4>
              <div className="row">
                {/* Display True Positive and False Positive */}
                <div className="col-md-6">
                  <p>True Positive: {truePositive}</p>
                  <p>False Positive: {comparisonData && comparisonData.false_positive}</p>
                </div>
                {/* Display True Negative and False Negative */}
                <div className="col-md-6">
                  <p>True Negative: {trueNegative}</p>
                  <p>False Negative: {comparisonData && comparisonData.false_negative}</p>
                </div>
              </div>
            </div>
            <hr />
          </div>
          )}

          {/* Filter Options */}
          <div className="col-md-6 order-md-last">
            <div className="border p-3" style={{ minHeight: '210px' }}>
              <h4>Filter Options</h4>
              {/* Display filter options checkboxes */}
              {["Production/Stable", "Alpha", "Pre-Alpha", "Beta"].map(option => (
                <div key={option} className="form-check">
                  <input
                    className="form-check-input"
                    type="checkbox"
                    value={option}
                    checked={selectedOptions[option]}
                    onChange={() => handleOptionSelect(option)}
                  />
                  <label className="form-check-label">{option}</label>
                </div>
              ))}
            </div>
          </div>
        </div>
        {/* Display Pip Result and PypiReCom Result */}
        <div className="row justify-content-center mt-4">
          <div className="col-md-10">
            {isLoading ? (
              <p className="text-center">Loading...</p>
            ) : (
              errorMessage ? (
                <p className="text-center">{errorMessage}</p>
              ) : (
                <>
                {!errorMessage && comparisonData && comparisonData.result && comparisonData.result.length > 0 && ( // Check if PypiReCom result exists and not empty
                  <div className="row">
                    {/* Display Pip Result */}
                    <div className="col-md-6">
                      <h4>Pip Result</h4>
                      {comparisonData && comparisonData.Pip && comparisonData.Pip.result && comparisonData.Pip.result.map((packageName, index) => (
                        <p key={index}>{packageName}</p>
                      ))}
                      <hr />
                    </div>
                    {/* Display PypiReCom Result */}
                    <div className="col-md-6">
                      <h4>PypiReCom Result</h4>
                      <div className="table-responsive">
                        <table className="table">
                          <thead>
                            <tr>
                              <th>Package Name</th>
                              <th>Total Dependencies</th>
                              <th>Development Status</th>
                            </tr>
                          </thead>
                          <tbody>
                            {comparisonData && comparisonData.result && comparisonData.result.map((pkg, index) => (
                              <tr key={index}>
                                <td>{pkg.v_id}</td>
                                <td>{comparisonData.Package_Dependency.filter(dep => dep.package === pkg.v_id).length}</td>
                                <td>{pkg.attributes.dev_status}</td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </div>
                   )}
                </>
              ))}
          </div>
        </div>
      </div>
      <h4 className="text-center mt-5 mb-4">Contributing Libraries</h4>
      <InfiniteLogo/>
      <Footer />
    </div>
  );
  
}

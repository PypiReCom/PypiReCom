import React, { useState, useEffect } from "react";
import { useLocation } from 'react-router-dom';
import { BASE_URL } from "../api-endpoint";

const SearchBar = ({ handleSearch, clearSearch }) => {
  const [searchText, setSearchText] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const searchTextParam = searchParams.get('searchText');
    if (searchTextParam) {
      setSearchText(searchTextParam);
    }
  }, [location.search]); 

  useEffect(() => {
    const fetchSuggestions = async () => {
      try {
        const response = await fetch(`${BASE_URL}/get_seach_context_list`);
        const data = await response.json();
        setSuggestions(data['Search Context']); // Fetching suggestions from 'Search Context'
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }
    };

    fetchSuggestions();
  }, []);

  const handleInputChange = (event) => {
    const { value } = event.target;
    setSearchText(value);
    setShowDropdown(true); // Always show dropdown when there's input
    updateUrlParams(value);
  };

  const handleSuggestionClick = (suggestion) => {
    setSearchText(suggestion);
    setShowDropdown(false);
    updateUrlParams(suggestion);
  };

  const updateUrlParams = (value) => {
    const searchParams = new URLSearchParams(location.search);
    searchParams.set('searchText', value);
    const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
    window.history.pushState({ path: newUrl }, '', newUrl);
  };

  const handleSearchButtonClick = () => {
    setShowDropdown(false); // Close the dropdown when search button is clicked
    handleSearch(searchText);
  };


  return (
    <div className="input-group position-relative">
      <input
        type="text"
        className="form-control"
        placeholder="Search for a Python package..."
        aria-label="Search for a Python package"
        aria-describedby="basic-addon2"
        value={searchText}
        onChange={handleInputChange}
        style={{ borderRadius: "5px" }}
      />
      {showDropdown && searchText && suggestions.length > 0 && suggestions.some(pkg => pkg.toLowerCase().includes(searchText.toLowerCase())) && (
        <div
          className="autocomplete dropdown-menu show position-absolute w-100 border border-top-0 rounded-bottom bg-white"
          style={{
            top: "calc(100% + 5px)",
            maxHeight: "200px",
            overflowY: "auto",
            zIndex: 1050,
          }}
        >
          {suggestions
            .filter((pkg) => pkg.toLowerCase().includes(searchText.toLowerCase()))
            .map((pkg, index) => (
              <div
                key={index}
                className="suggestion dropdown-item"
                style={{ padding: "10px", cursor: "pointer" }}
                onClick={() => handleSuggestionClick(pkg)} // Handle suggestion click
              >
                {pkg}
              </div>
            ))}
        </div>
      )}
      <div className="input-group-append">
        <button
          className="btn btn-outline-secondary"
          type="button"
           //onClick={() => handleSearch(searchText)} // Pass the current searchText to handleSearch
          onClick={handleSearchButtonClick}
          style={{ borderRadius: "0" }}
        >
          Search
        </button>
        <button
          className="btn btn-outline-secondary"
          type="button"
          onClick={() => {
            clearSearch();
            setSearchText('');
            updateUrlParams('');
          }}
          style={{ borderRadius: "0 5px 5px 0" }}
        >
          Clear
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
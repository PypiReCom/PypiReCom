import React from 'react';
import './App.css';
import Home from './screens/Home';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import ExplorePackage from './screens/ExplorePackage.jsx';
import ComparisonPage from './screens/ComparisonMatrix.jsx';
import ChatGraph from './screens/ChatGraph.jsx';
// import '../node_modules/bootstrap-dark-5/dist/css/bootstrap-dark.min.css'
import '../node_modules/bootstrap-dark-5/dist/css/bootstrap.min.css'
import '../node_modules/bootstrap/dist/js/bootstrap.bundle';
import '../node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'


function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/ExplorePackages" element={<ExplorePackage />} />
          <Route exact path="/comparison_Matrix" element={<ComparisonPage />} />
          <Route path="/chat/:searchText" element={<ChatGraph />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

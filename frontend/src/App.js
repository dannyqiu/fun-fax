import React, { Component } from 'react';
import { Link } from "react-router-dom";
import QuerySearch from './components/QuerySearch';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="nav">
          <Link to="/about"><i className="fas fa-info-circle"/> About</Link>
        </div>
        <header className="App-header">
          <h1 className="title">Fun Fax? Fun Fax.</h1>
        </header>
        <div className="torso">
          <QuerySearch />
        </div>
      </div>
    );
  }
}

export default App;

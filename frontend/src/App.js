import React, { Component } from 'react';
import { Link } from "react-router-dom";
import QuerySearch from './components/QuerySearch';
import './App.css';

class App extends Component {
  render() {
    return (
      <React.Fragment>
        <div className="nav">
          <Link to="/about"><i className="fas fa-info-circle"/> About</Link>
        </div>
        <div className="App">
          <header className="App-header">
            <h1 className="title">Fun Fax? Fun Fax.</h1>
          </header>
          <div className="torso">
            <QuerySearch />
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default App;

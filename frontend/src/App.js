import React, { Component } from 'react';
import './App.css';
import QuerySearch from './components/QuerySearch';
// import FactCard from '.components/FactCard';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <div>
            <span className="title">Fun Fax? Fun Fax.</span>
          </div>
          <div className="torso">
            <QuerySearch />
          </div>
        </header>
        
      </div>
    );
  }
}

export default App;

import React, { Component } from 'react';
import './App.css';
import QuerySearch from './components/QuerySearch';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <div>
            <span className="title">Fun Fax? Fun Fax.</span>
          </div>
        </header>
        <div className="torso">
          <QuerySearch />
        </div>
      </div>
    );
  }
}

export default App;

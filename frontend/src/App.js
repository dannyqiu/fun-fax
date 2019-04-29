import React, { Component } from 'react';
import QuerySearch from './components/QuerySearch';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
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

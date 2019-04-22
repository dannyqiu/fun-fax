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
            {/* <span class="odd">F</span><span class="even">u</span><span class="odd">n</span><span> </span>
            <span class="even">F</span><span class="odd">a</span><span class="even">x</span><span class="odd">.</span> */}
            <span class="odd">Fun Fax? Fun Fax.</span>
          </div>
          <div>
          <QuerySearch />
          </div>
        </header>
        
      </div>
    );
  }
}

export default App;

import React, { Component } from 'react';
import { Link } from "react-router-dom";
import './App.css';

class About extends Component {
  render() {
    return (
      <React.Fragment>
        <div className="nav">
          <Link to="/"><i className="fas fa-igloo"/> Home</Link>
        </div>
        <div className="App">
          <header className="App-header">
            <h1 className="title">What is Fun Fax?</h1>
          </header>
          <div className="about container">
            <div className="row">
              <div className="col-10 offset-1">
                <p>Fun Fax is a project by Arshi Bhatnager, Ryan Davila, Rebecca Jiang, Danny Qiu, and Nehal Rawat of Cornell University.</p>
                <p>We created this recommendation system for the final project of CS/INFO 4300, taught by Professor <a href="http://www.cs.cornell.edu/~cristian/">DNM</a>.</p>
                <p>Our code can be viewed on GitHub&nbsp;<a href="https://github.com/dannyqiu/fun-fax">here</a>.</p>
              </div>
            </div>
          </div>
        </div>
      </React.Fragment>
    );
  }
}

export default About;

import React from 'react';
import FactCard from './FactCard';
const URL = "localhost:3000/"
const API = "/api/irsystem/search?q="

class QuerySearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: '',
      results: [],
      failedQuery: null,
      };
  
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
      this.setState({query: event.target.value});
    }
  
  handleSubmit(event) {
    this.getInfo()
    event.preventDefault();
  }

  randomSearch(event) {
    event.preventDefault();
  }

  componentDidMount() {
    window.onpopstate = (event) => {
      console.log(JSON.stringify(event.state));
      fetch(API+event.state, {
        method: 'GET' 
      })
    .then(response => response.json())
    .then(data => {
      let results = data.data.results
      if (results.length === 0) {
        this.setState( {
          query: event.state,
          results: [],
          failedQuery: event.state,
        });
      }
      else {
        this.setState( {
          query: event.state,
          results: results,
          failedQuery: null,
        })
      }
    });
  };
}
    
  getInfo = () => fetch(API+this.state.query, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(data => {
      let results = data.data.results
      if (results.length === 0) {
        this.setState( {
          results: [],
          failedQuery: this.state.query,
        });
      }
      else {
        this.setState( {
          results: results,
          failedQuery: null,
        })
      }
      window.history.pushState(""+this.state.query, ""+this.state.query, "?q="+this.state.query);
    });

  queryRender() {
    if (this.state.query && this.state.results) {
      return (
        <p>Query: {this.state.query}</p>
      )
    }
  }
  resultsRender() {
    if (this.state.failedQuery) {
      return (
      <p>{"'"+this.state.failedQuery+"' returned 0 results. Please specify a different query."}</p>
      )
    }
    else {
      return (
    <div id="results">{this.state.results.map(result => (
      <div className="fact"><FactCard title={result.title} source={result.subreddit} permalink={result.permalink} score={result.score}/></div>
    ))}</div>
      )
  }
}

  render() {
    return (
      <form class="active-cyan-3 active-cyan-4" onSubmit={this.handleSubmit}>
      <i class="fas fa-search" aria-hidden="true"></i>
          <div class="active-cyan-3 active-cyan-4 mb-4">
            <input type="text" placeholder="Search for..." value={this.state.value} onChange={this.handleChange} aria-label="Search" class="search-bar" id="query"/>
          </div>
        <div>
        <input type="submit" value="Search!" class="btn btn-primary" id="button"/> <input type="submit" disabled={true} onClick={this.randomSearch} value="Random?" class="btn btn-primary" id="button"/>
        </div>
        {this.queryRender()}
        {this.resultsRender()}
        </form>
    );
 }
}

export default QuerySearch;

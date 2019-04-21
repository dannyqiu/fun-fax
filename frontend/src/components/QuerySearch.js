import React from 'react';
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
      window.location.href = URL+"?q="+this.state.query;
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
    <p>{this.state.results.map(result => (
      <div className="fact"> <a href={"https://reddit.com/"+result.permalink}>{result.title} </a> <br></br>{"Score: "+result.score+" upvotes | "} Subreddit: r/{result.subreddit}</div>
    ))}</p>
      )
  }
}

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          <br></br> 
          <input type="text" placeholder="Search for..." value={this.state.value} onChange={this.handleChange} />
        </label><br></br>
        <input type="submit" value="Search!" /> <input type="submit" disabled={true} onClick={this.randomSearch} value="Random?" />
        {this.queryRender()}
        {this.resultsRender()}

        </form>
    );
 }
}

export default QuerySearch;
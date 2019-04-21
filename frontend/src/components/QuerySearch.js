import React, { Component } from 'react';

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

  componentDidMount() {

  }

  handleChange(event) {
      this.setState({query: event.target.value});
    }
  
  handleSubmit(event) {
    this.getInfo()
    event.preventDefault();
  }

  randomSearch(event) {
    alert('Random search specified')
    event.preventDefault();
  }
    
  getInfo = () => fetch("/api/irsystem/search?q="+this.state.query, {
    method: 'GET'
  })
    .then(response => response.json())
    .then(data => {
      let results = data.data.results
      if (results.length === 0) {
        this.setState( {
          "results": [],
          failedQuery: this.state.query,
        });
      }
      else {
        this.setState( {
          "results": results,
          "failedQuery": null,
        })
      }
      console.log(results);
    });

  queryRender() {
    if (this.state.query && this.state.results) {
      return (
        <p>Query: {this.state.query}</p>
      )
    }
  }
    // else if (this.state.query && this.state.results === ['failed']) {
    //   return (
    //     <p>Query: {this.state.query} returned 0 results.</p> 
    //   )
    // }
    // else {
    //   return (
    //     <p>Query: {this.state.query}</p>
    //   )
    // }
  // }

  resultsRender() {
    console.log(this.state.success)
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
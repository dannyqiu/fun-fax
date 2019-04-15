import React, { Component } from 'react';

class QuerySearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: '',
      results: []
      };
  
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
      this.setState({query: event.target.value});
    }
  
  handleSubmit(event) {
    alert('A query was submitted: ' + this.state.query);
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
      this.setState( {
        "results": data.data.results
      });
    });

  queryRender() {
    if (this.state.query) {
      return (
        <p>Query: {this.state.query}</p>
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
        {this.state.results.map(result => (
      <div className="fact"> <a href={result.permalink}>{result.title} </a> <br></br>{result.score} Subreddit: r/{result.subreddit}</div>
    ))}
        </form>
    );
  }
}

export default QuerySearch;
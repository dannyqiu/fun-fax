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

  componentDidMount() {
    document.title = "Fun Fax: Fact Generator";
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
      this.setState( {
        "results": data.data.results
      });
      console.log(data);
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
      <div className="fact"> <a href={"https://reddit.com/"+result.permalink}>{result.title} </a> <br></br>{"Score: "+result.score+" upvotes | "} Subreddit: r/{result.subreddit}</div>
    ))}
        </form>
    );
  }
}

export default QuerySearch;
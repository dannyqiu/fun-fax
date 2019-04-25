import React from 'react';
import FactCard from './FactCard';
const API = "/api/irsystem/search?q="

class QuerySearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      query: '',
      results: [],
      failedQuery: null,
      advancedSearch: false,
      category: null,
      recency: null,
      controversial: null
      };
  
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    if (event.target.name === "query") {
      this.setState( {
        query: event.target.value,
        value: event.target.value, // accounts for when the value was predetermined on a reload
       });
    }
    else {
      this.setState( {
        [event.target.name]: event.target.value
      });
    }
  }
  
  handleSubmit(event) {
    this.getInfo()
    event.preventDefault();
  }

  randomSearch(event) {
    event.preventDefault();
  }

  buildURLQuery(path, params) {
    let url = new URL(`${window.location.origin}${path}`);
    url.search = new URLSearchParams(params);
    return url
  }

  /* Uses built-in React method to allow for URL based query. 
  window.onpopstate and below allows for browser history modifications within React app
  to allow for query to be tracked */
  componentDidMount() {
    let params = new URLSearchParams(window.location.search);
    let queryTerm = params.get('q');
    let category = params.get("category");
    let recency = params.get("recency");
    let controversial = params.get("controversial");

    if (queryTerm !== null) {
      this.setState({
        value: queryTerm
      })
      fetch(this.buildURLQuery(API, params) ,{
        method: 'GET' 
      })
    .then(response => response.json())
    .then(data => {
      let results = data.data.results
      if (results.length === 0) {
        this.setState( {
          query: queryTerm,
          results: [],
          failedQuery: queryTerm,
          category: category,
          recency: recency,
          controversial: controversial
        });
      }
      else {
        this.setState( {
          query: queryTerm,
          results: results,
          failedQuery: null,
          category: category,
          recency: recency,
          controversial: controversial
        })
      }
    });
    }
    
    window.onpopstate = (event) => {
      if (event.state) {
        fetch(this.buildURLQuery(API, params), {
          method: 'GET' 
        })
        .then(response => response.json())
        .then(data => {
          let results = data.data.results
          if (results.length === 0) {
            this.setState( {
              query: event.state.query,
              results: [],
              failedQuery: event.state.query,
              category: event.state.category,
              recency: event.state.recency,
              controversial: event.state.controversial
            });
          }
          else {
            this.setState( {
              query: event.state.query,
              results: results,
              failedQuery: null,
              category: event.state.category,
              recency: event.state.recency,
              controversial: event.state.controversial
            })
          }
        });
        }
        else {
          this.setState( {
            query: '',
            results: [],
            failedQuery: null
          })
        }
      };
    }
  
  /* Baseline fetch function to return query results from backend. */
  getInfo = () => {
    let params = {
      'q': this.state.query,
      'category': this.state.category,
      'recency': this.state.recency,
      'controversial': this.state.controversial
     }
    fetch(this.buildURLQuery(API, params), {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      let results = data.data.results
      if (results.length === 0) {
        this.setState( {
          results: [],
          failedQuery: this.state.query,
          category: this.state.category,
          recency: this.state.recency,
          controversial: this.state.controversial
        });
      }
      else {
        this.setState( {
          results: results,
          failedQuery: null,
        })
      }
      window.history.pushState(this.state, "", this.buildURLQuery(API, params));
    });
  }

  /*Renders failed query HTML */
  failedRender() {
    if (this.state.failedQuery) {
      return (
      <div class="failed">
        <p>{"'"+this.state.failedQuery+"' returned 0 results. Please specify a different query."}</p>
      </div>
      )
    }
  }

  /*Result rendering function, feeds props to FactCard component */
  resultsRender() {
    if (!this.state.failedQuery) {
      return (
        <div>{this.state.results.map(result => (
          <div className="fact">
            <FactCard
              title={result.title}
              similar={result.similar}
              permalink={"https://reddit.com"+result.permalink}
              score={result.score}
              />
          </div>
        ))}</div>
          )
      } 
    }
  
  /*Enables advanced searching slider */
  enableAdvancedSearch = () => {
    if (this.state.advancedSearch) {
      this.setState( {
        advancedSearch: !this.state.advancedSearch,
        recency: null,
        controversial: null
      });
    }
    else {
      this.setState( {
        advancedSearch: !this.state.advancedSearch 
    });
  }
}

  /*Renders advanced search section */
  renderAdvancedSearch() {
    if (this.state.advancedSearch) {
      return (
        <div>
          <span>Recency Sort:</span>
          <select name="recency" onChange={this.handleChange}>
              <option value="null"></option>
              <option value="newtoold">Newest to Oldest</option>
              <option value="oldtonew">Oldest to Newest</option>
          </select>

          <span>Controversial Sort:</span>
          <select name="controversial" onChange={this.handleChange}>
              <option value="null"></option>
              <option value="mosttoleast">Most to Least</option>
              <option value="leasttomost">Least to Most</option>
          </select>
        </div>
      )
    }
  }

  render() {
    return (
      <div class="search">
      <form class="active-cyan-3 active-cyan-4" onSubmit={this.handleSubmit}>
      <i class="fas fa-search" aria-hidden="true"></i>
          <div class="active-cyan-3 active-cyan-4 mb-4">
            <input name="query" type="text" placeholder="Search for..." value={this.state.value} onChange={this.handleChange} aria-label="Search" class="search-bar" id="query"/>
            <select class="selectpicker" name="category" onChange={this.handleChange}>
              <option value="general">General</option>
              <option value="discussion">Discussion</option>
              <option value="sports">Educational</option>
              <option value="entertainment">Entertainment</option>
              <option value="lifestyle">Lifestyle</option>
              <option value="technology">Technology</option>
              <option value="humor">Humor</option>
              <option value="other">Other</option>
            </select>
          </div>
        <div>
        <input type="submit" value="Search!" class="btn btn-primary" id="button"/> <input type="submit" disabled={true} onClick={this.randomSearch} value="Random?" class="btn btn-primary" id="button"/>
        <div class="advanced search">
        <label class="switch">
          <input type="checkbox" value={this.state.advancedSearch} onClick={this.enableAdvancedSearch}></input>
          <span class="slider round"></span>
        </label>
        </div>
        </div>
        </form>
        {this.failedRender()}
        {this.renderAdvancedSearch()}
        <div className="results">
        {this.resultsRender()} 
        </div>
       </div> 
    );
 }
}

export default QuerySearch;
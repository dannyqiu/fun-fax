import React from 'react';
import FailedResults from './FailedResults';
import Results from './Results';
import AdvancedSearch from './AdvancedSearch';
import SearchBar from './SearchBar';
import { buildURLQuery } from '../utils';
const API = "/api/irsystem/search"

class QuerySearch extends React.Component {
  constructor(props) {
    super(props);
    let params = new URLSearchParams(window.location.search);
    this.state = {
      query: params.get('q') || '',
      results: [],
      failedQuery: null,
      advancedSearch: params.get("recency") !== null || params.get("controversial") !== null,
      category: params.get("category"),
      recency: params.get("recency"),
      controversial: params.get("controversial")
      };
  
    this.getInfo = this.getInfo.bind(this);
  }
  
  handleSubmit(event) {
    this.getInfo()
    event.preventDefault();
  }

  /* Uses built-in React method to allow for URL based query. 
   * window.onpopstate deals with history behvaviors.
   */
  componentDidMount() {
    if (this.state.query !== '') {
      this.getInfo();
    }

    window.onpopstate = (event) => {
      if (event.state) {
        this.setState(event.state, this.getInfo);
      }
    }
  }
  
  /* Baseline fetch function to return query results from backend. Pushes app history 
   * for browser history management */
  getInfo() {
    let params = {
      'q': this.state.query,
    };
    if (this.state.category !== null) {
      params['category'] = this.state.category;
    }
    if (this.state.recency !== null) {
      params['recency'] = this.state.recency;
    }
    if (this.state.controversial !== null) {
      params['controversial'] = this.state.controversial;
    }
    let url = buildURLQuery(API, params);
    let displayUrl = buildURLQuery('/', params);
    window.history.pushState(this.state, "", displayUrl);
    fetch(url, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      let results = data.data.results;
      this.setState( {
        results: results,
        failedQuery: results.length === 0 ? params.q : null
      });
    });
  }
  
  /* Enables advanced searching slider */
  enableAdvancedSearch() {
    this.setState((prevState) => ({
      advancedSearch: !prevState.advancedSearch,
      recency: null,
      controversial: null
    }));
  }

  render() {
    return (
      <div>
        <form className="active-cyan-3 active-cyan-4" onSubmit={this.handleSubmit}>
          <SearchBar 
            queryChanged={v => this.setState({ query: v})}
            categoryChanged={v => this.setState({ category: v})}
            query={this.state.query}
            category={this.state.category}
            />
            <AdvancedSearch
              recencyChanged={v => this.setState({ recency: v })}
              controversialChanged={v => this.setState({ controversial: v })}
              recency={this.state.recency}
              controversial={this.state.controversial}
              advancedChanged={() => this.enableAdvancedSearch()}
              isAdvancedSearch={this.state.advancedSearch}
              />
          <div className="button-area">
            <input type="submit" value="Search!" className="btn btn-primary" id="button" onClick={(e) => this.handleSubmit(e)} /> 
            <input type="submit" disabled={true}  value="Random?" className="btn btn-primary" id="button" onClick={this.randomSearch} />
          </div>
        </form>
        {this.state.failedQuery !== null
          ? <FailedResults query={this.state.failedQuery} />
          : <Results results={this.state.results} />
        }
      </div> 
    );
  }

}

export default QuerySearch;
import React from 'react';
import FailedResults from './FailedResults';
import Results from './Results';
import AdvancedSearch from './AdvancedSearch';
import SearchBar from './SearchBar';
import { buildURLQuery } from '../utils';

const SEARCH_API = "/api/irsystem/search";
const RANDOM_API = "/api/irsystem/random";
// const SEARCH_API = "/api/irsystem/dummy";

class QuerySearch extends React.Component {
  constructor(props) {
    super(props);
    let params = new URLSearchParams(window.location.search);
    this.state = {
      query: params.get('q') || '',
      results: [],
      failedQuery: null,
      advancedSearch: params.get("recency") !== null || params.get("sort") !== null,
      category: params.get("category"),
      recency: params.get("recency"),
      sort: params.get("sort")
    };
  }

  /* Uses built-in React method to allow for URL based query.
   * window.onpopstate deals with history behvaviors.
   */
  componentDidMount() {
    if (this.state.query !== '') {
      this.doSearch();
    }

    window.onpopstate = (event) => {
      if (event.state) {
        this.setState(event.state, () => this.doSearch());
      }
    }
  }

  /* Baseline fetch function to return query results from backend. Pushes app history
   * for browser history management */
  async doSearch() {
    let params = {
      'q': this.state.query,
    };
    if (this.state.category !== null) {
      params['category'] = this.state.category;
    }
    if (this.state.recency !== null) {
      params['recency'] = this.state.recency;
    }
    if (this.state.sort !== null) {
      params['sort'] = this.state.sort;
    }
    let url = buildURLQuery(SEARCH_API, params);
    let displayUrl = buildURLQuery('/', params);
    window.history.pushState(this.state, "", displayUrl);
    return fetch(url, {
      method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
      let results = data.data.results;
      this.setState({
        results: results,
        failedQuery: results.length === 0 ? params.q : null
      });
    });
  }

  async randomSearch() {
    return this.setState({
      query: "",
    }, (newState) => {
      window.history.pushState(newState, "", '/random');
      return fetch(RANDOM_API, {
        method: 'GET'
      })
      .then(response => response.json())
      .then(data => {
        let results = data.data.results;
        this.setState({
          results: results,
          failedQuery: null
        });
      });
    });
  }

  /* Enables advanced searching slider */
  enableAdvancedSearch() {
    this.setState((prevState) => ({
      advancedSearch: !prevState.advancedSearch,
      recency: null,
      sort: null
    }));
  }

  render() {
    return (
      <div className="query-search">
        <form className="active-cyan-3 active-cyan-4 justify-content-center"
              onSubmit={e => { this.doSearch(); e.preventDefault(e) }}
              autoComplete="off">
          <SearchBar
            queryChanged={v => this.setState({ query: v})}
            categoryChanged={v => this.setState({ category: v})}
            query={this.state.query}
            category={this.state.category}
            />
          <div className="mb-3" />
          <AdvancedSearch
            recencyChanged={v => this.setState({ recency: v })}
            sortChanged={v => this.setState({ sort: v })}
            recency={this.state.recency}
            sort={this.state.sort}
            advancedChanged={() => this.enableAdvancedSearch()}
            isAdvancedSearch={this.state.advancedSearch}
            />
          <div className="mb-2" />
          <div className="button-area">
            <button type="submit" className="btn btn-primary mr-3">Search!</button>
            <button type="button" className="btn btn-primary" onClick={() => this.randomSearch()}>Random?</button>
          </div>
        </form>
        <div className="mt-4">
          {this.state.failedQuery !== null
            ? <FailedResults query={this.state.failedQuery} />
            : <Results results={this.state.results}
                      seeMoreEngabled={(docID) => console.log(docID)} />
          }
        </div>
    </div>
    );
  }

}

export default QuerySearch;

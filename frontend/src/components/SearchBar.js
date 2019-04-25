import React, { Component } from 'react';

class SearchBar extends Component {

  render() {
    return (
      <div className="search">
        <div className="active-cyan-3 active-cyan-4 mb-4">
          <i className="fas fa-search" aria-hidden="true" />
          <input name="query"
                type="text"
                placeholder="Search for..."
                value={this.props.query}
                onChange={e => {this.props.queryChanged(e.target.value)}}
                aria-label="Search"
                className="search-bar"
                id="query"
                />
          <select className="selectpicker"
                  name="category"
                  value={this.props.category || ''}
                  onChange={e => {this.props.categoryChanged(e.target.value)}}
                  >
            <option value="">General</option>
            <option value="discussion">Discussion</option>
            <option value="sports">Educational</option>
            <option value="entertainment">Entertainment</option>
            <option value="lifestyle">Lifestyle</option>
            <option value="technology">Technology</option>
            <option value="humor">Humor</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>
    )
  }
}

export default SearchBar;
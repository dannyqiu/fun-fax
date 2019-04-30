import React, { Component } from 'react';

class SearchBar extends Component {

  render() {
    return (
      <div className="form-inline justify-content-center mb-2">
        <div className="input-group mr-2">
          <div className="input-group-prepend">
            <span className="input-group-text" id="queryInput">
              <i className="fas fa-search" aria-hidden="true" />
            </span>
          </div>
          <input name="query"
                 type="text"
                 className="form-control"
                 placeholder="Search for..."
                 aria-label="Search"
                 aria-describedby="queryInput"
                 value={this.props.query}
                 onChange={e => {this.props.queryChanged(e.target.value)}}
              />
        </div>
        <select className="selectpicker form-control"
                name="category"
                value={this.props.category || ''}
                onChange={e => {this.props.categoryChanged(e.target.value)}}
                >
          <option value="">General</option>
          <option value="sports">Educational</option>
          <option value="entertainment">Entertainment</option>
          <option value="lifestyle">Lifestyle</option>
          <option value="technology">Technology</option>
          <option value="humor">Humor</option>
        </select>
      </div>
    )
  }
}

export default SearchBar;

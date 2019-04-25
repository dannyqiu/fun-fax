import React, { Component } from 'react';

class AdvancedSearch extends Component {

  render() {
    return (
      <div className="advanced-search">
        <div className="custom-control custom-switch">
          <input type="checkbox"
                 className="custom-control-input"
                 id="advancedSearchToggle"
                 checked={this.props.isAdvancedSearch}
                 onChange={() => this.props.advancedChanged()}>
          </input>
          <label className="custom-control-label" htmlFor="advancedSearchToggle">Toggle Advanced Search</label>
        </div>
        {this.props.isAdvancedSearch && (
          <div className="sorting-area">
            <span>Recency Sort:</span>
            <select name="recency" value={this.props.recency || ''} onChange={e => {this.props.recencyChanged(e.target.value)}}>
              <option value=""></option>
              <option value="newtoold">Newest to Oldest</option>
              <option value="oldtonew">Oldest to Newest</option>
            </select>

            <span>Controversial Sort:</span>
            <select name="controversial" value={this.props.controversial || ''} onChange={e => {this.props.controversialChanged(e.target.value)}}>
              <option value=""></option>
              <option value="mosttoleast">Most to Least</option>
              <option value="leasttomost">Least to Most</option>
            </select>
          </div>
        )}
      </div>
    )
  }
}

export default AdvancedSearch;
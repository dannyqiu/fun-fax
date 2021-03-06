import React, { Component } from 'react';

class AdvancedSearch extends Component {

  render() {
    return (
      <div className="advanced-search">
        <div className="custom-control custom-switch mb-2">
          <input type="checkbox"
                 className="custom-control-input"
                 id="advancedSearchToggle"
                 checked={this.props.isAdvancedSearch}
                 onChange={() => this.props.advancedChanged()}>
          </input>
          <label className="custom-control-label noselect" htmlFor="advancedSearchToggle">Toggle Advanced Search</label>
        </div>
        {this.props.isAdvancedSearch && (
          <div className="sorting-area form-inline justify-content-center">
            <span className="mr-1">Recency preference:</span>
            <select name="recency"
                    className="form-control form-control-sm mr-2 ml-2 ml-md-0"
                    value={this.props.recency || ''}
                    onChange={e => {this.props.recencyChanged(e.target.value === "" ? null : e.target.value)}}>
              <option value=""></option>
              <option value="new">Newer</option>
              <option value="old">Older</option>
            </select>

            <span className="mr-1">Sort Preference:</span>
            <select name="sort"
                    className="form-control form-control-sm ml-2 ml-md-0 mr-2 mr-md-0"
                    value={this.props.sort || ''}
                    onChange={e => {this.props.sortChanged(e.target.value)}}>
              <option value="relevancy">Relevancy</option>
              <option value="popularity">Popularity</option>
            </select>
          </div>
        )}
      </div>
    )
  }
}

export default AdvancedSearch;

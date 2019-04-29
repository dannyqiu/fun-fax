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
          <label className="custom-control-label" htmlFor="advancedSearchToggle">Toggle Advanced Search</label>
        </div>
        {this.props.isAdvancedSearch && (
          <div className="sorting-area form-inline justify-content-center">
            <span className="mr-1">Recency:</span>
            <select name="recency"
                    className="form-control form-control-sm mr-2"
                    value={this.props.recency || ''}
                    onChange={e => {this.props.recencyChanged(e.target.value)}}>
              <option value={null}></option>
              <option value="new">Newest to Oldest</option>
              <option value="old">Oldest to Newest</option>
            </select>

            <span className="mr-1">Sort Preference:</span>
            <select name="controversial"
                    className="form-control form-control-sm"
                    value={this.props.controversial || ''}
                    onChange={e => {this.props.controversialChanged(e.target.value)}}>
              <option value={null}></option>
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

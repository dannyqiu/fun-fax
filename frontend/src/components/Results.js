import React, { Component } from 'react';
import FactCard from './FactCard'

class Results extends Component {

  /* Result rendering function, feeds props to FactCard component */
  render() {
    return (
      <div>
      {this.props.results.map(result => (
          <FactCard
            key={result.permalink}
            title={result.title}
            similar={result.similar}
            permalink={`https://reddit.com${result.permalink}`}
            score={result.score}
            />
      ))}
      </div>
    );
  } 
}

export default Results;
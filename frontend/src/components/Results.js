import React, { Component } from 'react';
import FactCard from './FactCard'
import moment from 'moment';

class Results extends Component {

  /* Result rendering function, feeds props to FactCard component */
  render() {
    return (
      <div className="results">
      {this.props.results.map(result => (
          <FactCard
            key={result.permalink}
            title={result.title}
            similar={result.similar}
            permalink={`https://reddit.com${result.permalink}`}
            subreddit={result.subreddit}
            score={result.score}
            comments={result.num_comments}
            imgURL={result.imgURL}
            time={moment.unix(result.created_utc).fromNow()}
            seeMoreEnabled={(docID) => this.props.seeMoreEnabled(docID)}
            />
      ))}
      </div>
    );
  } 
}

export default Results;
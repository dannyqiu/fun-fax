import React, { Component } from 'react';
import FactCard from './FactCard'
import Words from './Words'
import moment from 'moment';

class Results extends Component {

  /* Result rendering function, feeds props to FactCard component */
  render() {
    return (
      <div className="results container">
          <Words
            words={this.props.words}
          />
        {this.props.results && this.props.results.map(result => (
          <FactCard
            key={result.permalink}
            title={result.title}
            similar={result.similar}
            permalink={`https://reddit.com${result.permalink}`}
            subreddit={result.subreddit}
            score={result.score}
            comments={result.num_comments}
            thumbnail={result.thumbnail}
            time={moment.unix(result.created_utc).fromNow()}
            seeMoreClicked={() => this.props.seeMoreClicked(result.see_more_query_vector)}
            />
        ))}
      </div>
    );
  }
}

export default Results;

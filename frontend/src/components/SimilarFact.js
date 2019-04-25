import React from 'react'

function renderSimilar(sources) {
  if (sources) {
    return sources.map((subfact) =>
    <div>
      <li className="list-group-item subfact">
        <a className="sub-card-text" target="_blank" rel="noopener noreferrer" id="fact" href={subfact.permalink}>{subfact.title}</a>
      </li>
      <li className="list-group-item subsource">{subfact.subreddit} | {subfact.score} ⭐'s</li>
    </div>
    );
  }
} 

const SimilarFact = (props) => {
  return (
      <div className="subfact">
      <ul className="list-group list-group-flush">
          {renderSimilar(props.similar)}
      </ul>
    </div>
    )
  }

export default SimilarFact;
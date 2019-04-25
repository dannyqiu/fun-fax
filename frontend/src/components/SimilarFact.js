import React from 'react'

function renderSimilar(sources) {
    if (sources) {
      return sources.map((subfact) =>
      <div>
        <li class="list-group-item subfact"><a class="sub-card-text" target="_blank" id="fact" href={subfact.permalink}>{subfact.title}</a></li>
        <li class="list-group-item subsource">{subfact.subreddit} | {subfact.score} ⭐'s</li>
      </div>
      );
    }
  } 

const SimilarFact = (props) => {
    return (
        <div class="subfact">
        <ul class="list-group list-group-flush">
            {renderSimilar(props.similar)}
        </ul>
      </div>
      )
    }

export default SimilarFact;
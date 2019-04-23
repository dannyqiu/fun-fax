import React from 'react';

const FactCard = (props) => {
  return (
    <div class="card">
    <div class="card-body">
      <a class="card-text" id="fact" href={props.permalink}>{props.title}</a>
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item" id="score">Score: {props.score} upvotes</li>
      <li class="list-group-item" id="subreddit">Subreddit: r/{props.source}</li>
    </ul>
  </div>
  )
}

export default FactCard;
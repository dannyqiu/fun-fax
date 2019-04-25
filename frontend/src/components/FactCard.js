import React from 'react';
import SimilarFact from "./SimilarFact";
 
const FactCard = (props) => {
  return (
    <div class="card">
    <div class="card-body">
      <a class="card-text" target="_blank" id="fact" href={props.permalink}>{props.title}</a>
    </div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item" id="score">{props.score} ⭐️'s</li>
      <SimilarFact similar={props.similar}/>
    </ul>
  </div>
  )
}

export default FactCard;
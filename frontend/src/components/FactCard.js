import React from 'react';
import SimilarFact from "./SimilarFact";
 
const FactCard = (props) => {
  return (
    <div className="card">
    <div className="card-body">
      <a className="card-text" target="_blank" rel="noopener noreferrer" id="fact" href={props.permalink}>{props.title}</a>
    </div>
    <ul className="list-group list-group-flush">
      <li className="list-group-item" id="score">{props.score} ⭐️'s</li>
      <SimilarFact similar={props.similar}/>
    </ul>
  </div>
  )
}

export default FactCard;
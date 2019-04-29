import React from 'react';
 
const FactCard = (props) => {
  return (
    <div className="card container mx-auto mb-5">
      <div className="card-body">
        <div className="row">
          <div className="col-10">
          <p className="text-left"><a className="card-text mb-2" target="_blank" rel="noopener noreferrer" id="fact" href={props.permalink}>{props.title}</a></p>
          <div className="row">
            <div className="col-3">
              <p className="text-left">r/{props.subreddit}</p>
            </div>
            <div className="col-2"></div>
            <div className="col-3">
              <p className="text-left">{props.score} ⭐️'s</p>
            </div>
            <div className="col-2">
              <p className="text-left">{props.comments} ✉️'s</p>
            </div>
          </div>
        </div>
        <div className="col-2">
          {/* <img className="fact-picture mt-2 justify-content-center" src={"https://media.wired.com/photos/5b8999943667562d3024c321/master/w_1164,c_limit/trash2-01.jpg"} alt="Piction in question"></img> */}
          {props.imgURL && (
            <img className="fact-picture mt-2 justify-content-center" src={props.imgURL} alt="Piction in question"></img>
            )}
        </div>
            
        <button id="see-more"
                type="button"
                className="btn btn-outline-primary btn-small mt-2 mb-2"
                onClick={(docID) => props.seeMoreEnabled(docID)}
                >
              See Similar Queries
        </button>
        </div>
      </div>
    </div>
  )
}

export default FactCard;
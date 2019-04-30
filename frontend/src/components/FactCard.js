import React from 'react';

const FactCard = (props) => {
  return (
    <div className="card container mx-auto mb-3">
      <div className="card-body">
        <div className="row">
          <div className="col-10">
          <p className="text-left"><a className="card-text" target="_blank" rel="noopener noreferrer" id="fact" href={props.permalink}>{props.title}</a></p>
          <div className="row">
            <div className="col-3">
              <p className="text-left gray-text">r/{props.subreddit}</p>
            </div>
            <div className="col-4">
              <p className="text-left score">{props.score} <i className="fas fa-heart"></i>&nbsp;&nbsp;|&nbsp;&nbsp;{props.comments} <i className="fas fa-comments"></i> </p>
            </div>
            <div className="col-4">
              <button type="button"
                      className="btn btn-outline-primary btn-small"
                      onClick={() => props.seeMoreClicked()}
                      >
                    See Similar Queries
              </button>
            </div>
          </div>
        </div>
        <div className="col-2">
          <p className="gray-text">{props.time}</p>
          {props.thumbnail.startsWith("http") && (
            <img className="fact-picture" src={props.thumbnail}></img>
            )}
        </div>
        </div>
      </div>
    </div>
  )
}

export default FactCard;

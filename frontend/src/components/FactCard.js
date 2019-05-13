import React from 'react';

const FactCard = (props) => {
  return (
    <div className="card">
      <div className="card-body">
        <div className="row">
          <div className="col-10">
            <div className="card-title">
              <a className="card-text" target="_blank" rel="noopener noreferrer" href={props.permalink}>
                <h5 className="fact-title">{props.title}</h5>
              </a>
            </div>
            <div className="row">
              <div className="col-3">
                <span className="fact-subreddit">r/{props.subreddit}</span>
              </div>
              <div className="col-3">
                <span className="fact-score">
                  {props.score} <i className="fas fa-heart" />&nbsp;&nbsp;|&nbsp;&nbsp;{props.comments} <i className="fas fa-comments" />
                </span>
              </div>
              <div className="col-3 offset-3">
                <button type="button"
                        className="btn btn-outline-primary btn-sm"
                        onClick={() => props.seeMoreClicked()}
                        >
                  See Similar Queries
                </button>
              </div>
            </div>
          </div>
          <div className="col-2">
            <span className="fact-time">{props.time}</span>
            {props.thumbnail.startsWith("http") && (
              <img className="fact-picture" src={props.thumbnail.replace("http://", "https://")} alt={props.title} />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FactCard;

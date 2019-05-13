import React from 'react';

const FactCard = (props) => {
  return (
    <div className="card">
      <div className="card-body">
        <div className="row">
          <div className="col-12 col-md-10 order-12 order-md-1">
            <div className="card-title mb-1 mb-md-2">
              <a className="card-text" target="_blank" rel="noopener noreferrer" href={props.permalink}>
                <h5 className="fact-title mb-0">{props.title}</h5>
              </a>
            </div>
            <div className="row">
              <div className="col-6 col-md-3">
                <span className="fact-subreddit">r/{props.subreddit}</span>
              </div>
              <div className="col-6 col-md-3">
                <span className="fact-score">
                  {props.score} <i className="fas fa-heart" />&nbsp;&nbsp;|&nbsp;&nbsp;{props.comments} <i className="fas fa-comments" />
                </span>
              </div>
              <div className="col-12 col-md-3 offset-md-3 mt-1 mt-md-0">
                <button type="button"
                        className="btn btn-outline-primary btn-sm"
                        onClick={() => props.seeMoreClicked()}
                        >
                  See Similar Queries
                </button>
              </div>
            </div>
          </div>
          <div className="col-12 col-md-2 order-1 order-md-12 text-right text-md-left">
            <span className="fact-time">{props.time}</span>
            {props.thumbnail.startsWith("http") && (
              <img className="fact-picture d-none d-md-block" src={props.thumbnail.replace("http://", "https://")} alt={props.title} />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FactCard;

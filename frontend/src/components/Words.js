import React from 'react';

const Words = (props) => (
  (props.words.length !== 0) && (
    <div className="row">
      <div className="words col-12">
        Considered Terms: &nbsp;
          {props.words.map(word => (
          <span key={word}
                className="badge badge-info mr-2 mb-1"
                onClick={() => props.simTermSearched(word)}>
            {word}
          </span>
        ))}
      </div>
    </div>
  )
)

export default Words;
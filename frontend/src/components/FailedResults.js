import React from 'react';

/* Renders failed query HTML */
const FailedResults = (props) => (
  <div className="failed">
    <p>{`${props.query} returned 0 results. Please specify a different query.`}</p>
  </div>
);

export default FailedResults;

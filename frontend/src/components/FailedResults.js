import React from 'react';

const FailedResults = (props) => (
  /* Renders failed query HTML */
  <div class="failed">
    <p>{`${props.query} returned 0 results. Please specify a different query.`}</p>
  </div>
);

export default FailedResults;
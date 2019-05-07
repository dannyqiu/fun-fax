import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import App from './App';
import About from './About';
import * as serviceWorker from './serviceWorker';
import './index.css';

ReactDOM.render(
  <BrowserRouter>
    <Switch>
      <Route path="/about" component={ About }/>
      <Route path="/" component={ App }/>
    </Switch>
  </BrowserRouter>, document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();

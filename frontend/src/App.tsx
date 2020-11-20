import React from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom';
import ShowList from "./components/ShowList";
import Show from "./components/Show";
import './App.css';

function App() {
  return (
    <Router>
      <Switch>
        <Route path="/show/:showSlug">
          <Show/>
        </Route>
        <Route path="/">
          <ShowList/>
        </Route>
      </Switch>
    </Router>
  );
}

export default App;

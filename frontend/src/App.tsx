import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import ShowList from "./components/ShowList";
import Show from "./components/Show";
import Episode from "./components/Episode";
import './App.css';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <Navbar />
      <Switch>
        <Route path="/show/:show/season/:season/episode/:episode">
          <Episode />
        </Route>
        <Route path="/show/:showSlug">
          <Show />
        </Route>
        <Route path="/">
          <ShowList />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;

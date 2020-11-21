import React from 'react';
import { Link } from 'react-router-dom';
import HomeIcon from 'mdi-react/HomeIcon';
import ArrowBackIcon from 'mdi-react/ArrowBackIcon';
import ArrowForwardIcon from 'mdi-react/ArrowForwardIcon';
import ArrowUpIcon from 'mdi-react/ArrowUpIcon';
import { useSelector } from 'react-redux';
import { INavState } from '../redux/actions/navbar';

const selectNavState = (state: {navbar: INavState}) => state.navbar;

const Navbar = () => {
  const { back, forward, up } = useSelector(selectNavState);

  return (
    <nav className="appnav">
      <Link to="/">
        <HomeIcon />
      </Link>
      <Link to={back || '#'} className={back ? '' : 'hidden'}>
        <ArrowBackIcon />
      </Link>
      <Link to={up || '#'} className={up ? '' : 'hidden'}>
        <ArrowUpIcon />
      </Link>
      <Link to={forward || '#'} className={forward ? '' : 'hidden'}>
        <ArrowForwardIcon />
      </Link>
    </nav>
  );
};

export default Navbar;

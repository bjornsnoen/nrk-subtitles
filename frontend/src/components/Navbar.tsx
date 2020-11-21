import React from 'react';
import { Link } from 'react-router-dom';
import HomeIcon from 'mdi-react/HomeIcon'

const Navbar = () => {
    return (
        <Link to="/">
            <HomeIcon/>
        </Link>
    )
}

export default Navbar;
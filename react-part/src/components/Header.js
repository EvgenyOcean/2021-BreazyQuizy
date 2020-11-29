import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import {Link} from 'react-router-dom';

import { LogoutAPI } from '../api/axios';
import { parseJwt } from '../utils';
import { useLocation, Redirect, useHistory } from 'react-router-dom';
import { useEffect } from 'react';

export const Header = () => {
  let location = useLocation();
  let history = useHistory();
  useEffect(()=>{
    isUserLoggedIn();
  }, [location])

  const isUserLoggedIn = () => {
    let refreshToken = localStorage.getItem('refresh');
    if (!refreshToken){
      return false;
    }

    let parsedData = parseJwt(refreshToken);
    if (Math.trunc(Date.now() / 1000) < +parsedData.exp){
      return true;
    } else {
      return false;
    }
  }

  const handleLogout = async () => {
    try{
      await LogoutAPI();
    } catch(err){
      console.log(err);
    } finally{
      return history.push('/');
    }
  }

  return (
    <Navbar bg="dark" variant="dark">
      <Link to="/" className="navbar-brand">BreathyQuizzy</Link>
      <Nav className="ml-auto">
        {isUserLoggedIn() ? 
          <Nav.Link to="/logout" onClick={handleLogout}>Logout</Nav.Link> :
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="nav-link">Sign up</Link>
          </>
        }
      </Nav>
    </Navbar>
  )
}

export default Header;
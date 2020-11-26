import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import {Link} from 'react-router-dom';

export const Header = () => {
  return (
    <Navbar bg="dark" variant="dark">
      <Link to="/" className="navbar-brand">BreathyQuizzy</Link>
      <Nav className="ml-auto">
        <Nav.Link href="#home">Quizzes</Nav.Link>
      </Nav>
    </Navbar>
  )
}

export default Header;
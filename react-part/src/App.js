import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Header from './components/Header';
import QuizDetail from './pages/QuizDetail';
import QuizzesList from './pages/QuizzesList';
import Login from './pages/Login';
import Register from './pages/Register';
import QuizQuestion from './pages/QuizQuestion';


function App() {
  return (
    <>
    <Router>
      <Header />
      <Switch>
        <Route exact path='/' component={QuizzesList}/>
        <Route exact path='/quizzes/:slug/' component={QuizDetail}/>
        <Route exact path='/quizzes/:slug/:order/' component={QuizQuestion}/>
        <Route exact path='/login/' component={Login}/>
        <Route exact path='/register/' component={Register}/>
      </Switch>
    </Router>
    </>
  );
}

export default App;

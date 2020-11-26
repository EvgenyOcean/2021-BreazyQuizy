import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Header from './components/Header';
import QuizDetail from './pages/QuizDetail';
import QuizzesList from './pages/QuizzesList';

function App() {
  return (
    <>
    <Router>
      <Header />
      <Switch>
        <Route exact path='/' component={QuizzesList}/>
        <Route exact path='/quizzes/:slug/' component={QuizDetail}/>
      </Switch>
    </Router>
    </>
  );
}

export default App;

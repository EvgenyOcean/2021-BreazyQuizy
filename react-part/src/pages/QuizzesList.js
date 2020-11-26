import { useEffect, useState } from 'react';
import quizzesListAPI from '../api/axios';
import { useHistory } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Table from 'react-bootstrap/Table'

export const QuizzesList = () => {
  const [quizzes, setQuizzes] = useState({loading: true, data: []});
  const history = useHistory();
  useEffect(()=>{
    if ((quizzes.data.length === 0) && quizzes.loading){
      (async () => {
        let r = await quizzesListAPI();
        if (r.error){
          console.log(r.error);
        } else {
          let data = r.data; 
          setQuizzes({data: data, loading: false});
        }
      })();
    }
  }, [quizzes])

  if (quizzes.loading){
    return (
      <h1>Quizzes are loading!</h1>
    )
  } else {
    const quizzesTable = quizzes.data.map(quiz => {
      return (
        <tr key={quiz.slug} id={quiz.slug} className="quiz-row" onClick={(e) => {
          history.push('/quizzes/' + e.target.closest('tr').id + '/');
        }}>
          <td>{quiz.id}</td>
          <td>{quiz.title}</td>
          <td>{quiz.number_of_questions}</td>
          <td>{quiz.date_created}</td>
        </tr>
      )
    });
    return (
      <Container>
        <Row className="justify-content-center">
          <Col xs={10}>
            <Table striped bordered hover variant="dark" className='mt-4'>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Name</th>
                  <th>Questions Number</th>
                  <th>Date Created</th>
                </tr>
              </thead>
              <tbody>
                {quizzesTable}
              </tbody>
            </Table>
          </Col>
        </Row>
      </Container>
    )
  }

}

export default QuizzesList;
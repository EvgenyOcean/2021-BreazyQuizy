import {useEffect, useState} from 'react';
import {quizDetailAPI} from '../api/axios';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';


export const QuizDetail = (props) => {
  const [quiz, setQuiz] = useState({data: {}, loading: true, notFound: false});

  let quizSlug = props.match.params.slug;
  useEffect(()=>{
    if (quiz.loading && Object.getOwnPropertyNames(quiz.data).length === 0){
      (async ()=>{        
        const r = await quizDetailAPI(quizSlug);
        if (r.status === 404){
          setQuiz({...quiz, loading: false, notFound: true});
        } else {
          let data = r.data;
          setQuiz({data, loading: false});
        }
      })()
    }
  }, [quiz, quizSlug])

  if (quiz.loading){
    return (
      <div>Quiz is loading!</div>
    )
  } else if (quiz.notFound) {
    return (
      <div>This quiz does not exist or has been removed!</div>
    )
  } else {
    let q = quiz.data;
    return (
      <Container className="mt-4">
        <Row className="justify-content-center">
          <Col xs={10} className="border border-secondary bg-dark text-white p-3">
            <h2>{q.title}</h2>
            <p>{q.desc}</p>
            <Button variant="primary">Start Quiz!</Button>
          </Col>
        </Row>
      </Container>
    )
  }
}

export default QuizDetail;
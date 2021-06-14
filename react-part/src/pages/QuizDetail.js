import React, { useEffect, useState } from "react";
import { useHistory } from 'react-router-dom';

import { quizDetailAPI } from "../api/axios";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
import Alert from "react-bootstrap/Alert";

export const QuizDetail = (props) => {
  const [quiz, setQuiz] = useState({
    data: {},
    loading: true,
    notFound: false,
  });

  const history = useHistory();
  let quizSlug = props.match.params.slug;
  useEffect(() => {
    if (quiz.loading && Object.getOwnPropertyNames(quiz.data).length === 0) {
      (async () => {
        const r = await quizDetailAPI(quizSlug);
        if (r.status === 404) {
          setQuiz({ ...quiz, loading: false, notFound: true });
        } else if (r.status === 401) {
          console.log(r.error);
          setQuiz({ ...quiz, loading: false, notFound: true });
        } else {
          let data = r.data;
          setQuiz({ data, loading: false });
        }
      })();
    }
  }, [quiz, quizSlug]);

  const handleQuizActionClick = (action) => {
    if (action === 'start'){
      history.push('/quizzes/' + quizSlug + '/0/');
    } else if (action === 'continue'){
      history.push(`/quizzes/${quizSlug}/${(quiz.data['questions_info']['last_answered_question'] + 1) || 0}/`);
    }
  }

  if (quiz.loading) {
    return <div>Quiz is loading!</div>;
  } else if (quiz.notFound) {
    return <div>This quiz does not exist or has been removed!</div>;
  } else {
    let q = quiz.data;
    const status = q["user_quiz_status"];
    console.log(q);
    return (
      <Container className="mt-4">
        <Row className="justify-content-center">
          <Col
            xs={10}
            className="border border-secondary bg-dark text-white p-3"
          >
            <h2>{q.title}</h2>
            <p>{q.desc}</p>
            {status === "STARTED" ? (
              <React.Fragment>
                <Alert variant="info">
                  You have started the quiz and yet have some time to complete
                  it.
                </Alert>
                <Button variant="info" onClick={() => handleQuizActionClick('continue')}>Continue</Button>
              </React.Fragment>
            ) : status === "COMPLETED" ? (
              <React.Fragment>
                <Alert variant="success">
                  You have completed this quiz.
                </Alert>
                <Button variant="success" onClick={() => handleQuizActionClick('results')}>See results</Button>
              </React.Fragment>
            ) : (
              <Button variant="primary" onClick={() => handleQuizActionClick('start')}>Start Quiz</Button>
            )}
          </Col>
        </Row>
      </Container>
    );
  }
};

export default QuizDetail;

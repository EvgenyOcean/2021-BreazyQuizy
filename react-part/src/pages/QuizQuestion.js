import React, { useEffect, useState } from "react";
import { useHistory } from "react-router-dom";

import { QuizQuestionAPI } from "../api/axios";

import Button from "react-bootstrap/Button";

import QuestionMS from "../components/QuestionMS";
import QuestionText from "../components/QuestionText";

import Swal from 'sweetalert2'
import withReactContent from 'sweetalert2-react-content'

import axios from "axios";

export default function QuizQuestion(props) {
  const [questionData, setQuestionData] = useState({ loading: true });
  const [choice, setChoice] = useState(null);
  const [choices, setChoices] = useState([]);
  const [answer, setAnswer] = useState("");

  const quizSlug = props.match.params.slug;
  const questionOrder = props.match.params.order;

  const history = useHistory();
  const MySwal = withReactContent(Swal);

  useEffect(() => {
    QuizQuestionAPI(quizSlug, questionOrder).then((r) => {
      if (r.status === 200) {
        const data = r.data;
        const answer = data['questions_info'].answer;
        if (answer.length > 0){         
          if (data.variant === 'SS'){
            setChoice(data.choices.find(choice => choice['title'] === answer[0]).id);
          } else if (data.variant === 'MS'){
            setChoices(data.choices.filter(choice => answer.includes(choice['title'])).map(choice => choice.id));
          } else if (data.variant === 'T'){
            setAnswer(answer[0])
          }
        }
        setQuestionData((prevState) => {
          return { loading: false, ...data };
        });
      }
    });
  }, [quizSlug, questionOrder]);

  if (questionData.loading) {
    return <h1>Question is loading!</h1>;
  }

  const handleChoiceClick = (el) => {
    const choiceEl = el.closest(".choice");
    setChoice(+choiceEl.dataset["choiceId"]);
  };

  const handleChoicesClick = (el) => {
    const choiceId = +el.closest(".choice").dataset["choiceId"];
    if (choices.includes(choiceId)) {
      setChoices((prevState) => {
        return prevState.filter((el) => el !== choiceId);
      });
    } else {
      setChoices([...choices, choiceId]);
    }
  };

  const handleAnswerChange = (value) => {
    setAnswer(value);
  };

  const handleNextClick = () => {
    sendAnswer();
    history.push(`/quizzes/${quizSlug}/${+questionOrder + 1}/`);
  };

  const handleCircleClick = (q) => {
    sendAnswer();
    history.push(`/quizzes/${quizSlug}/${q}/`);
  };

  const handleFinishQuiz = () => {
    sendAnswer(true);
  };

  const sendAnswer = (lastOne = false) => {
    if (questionData.variant === "SS") {
      if (!choice) return;
      axios
        .post(`/api/quizzes/${quizSlug}/${questionOrder}/`, {
          choice_id: choice,
        })
        .then(console.log)
        .catch(console.log);
      console.log("sending an answer to SS!");
    } else if (questionData.variant === "MS") {
      axios
        .post(`/api/quizzes/${quizSlug}/${questionOrder}/`, {
          choices_ids: choices,
        })
        .then(console.log)
        .catch(console.log);
      console.log("sending an answer to MS!");
    } else if (questionData.variant === "T") {
      axios
        .post(`/api/quizzes/${quizSlug}/${questionOrder}/`, {
          answer: answer,
        })
        .then(console.log)
        .catch(console.log);
      console.log("sending an answer to T!");
    }

    if (lastOne) {
      MySwal.fire({
        title: 'Finish the quiz?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes'
      }).then((result) => {
        if (result.isConfirmed) {
          axios
            .post(`/api/quizzes/${quizSlug}/${questionOrder}/`, {
              submitted: true,
            })
            .then(() => {
              MySwal.fire(
                'Your results are ready!',
                'It\'s time to check em out!',
                'success'
              )
            })
            .catch(console.log);
        }
      })
      
      console.log("finish the quiz and redirect!");
    }
  };

  const qsInfo = questionData["questions_info"];
  return (
    <div className="quiz-question">
      <div className="chat"></div>
      <main>
        <div className="questions-info">
          {qsInfo["questions_order"].map((q) => (
            // circle; answered; current
            <div
              key={q}
              className={
                "circle " +
                (qsInfo["answered_questions"].includes(q) ? "answered " : "") +
                (+questionOrder === q ? "current" : "")
              }
              onClick={(e) => handleCircleClick(q)}
            >
              {q}
            </div>
          ))}
        </div>
        <div className="question">
          <h3 className="question-title">{questionData.title}</h3>
          {questionData.variant === "SS" ? (
            <div className="choices">
              {questionData.choices.map((c, inx) => (
                <div
                  key={c.id}
                  className="choice"
                  data-choice-id={c.id}
                  onClick={(e) => handleChoiceClick(e.target)}
                >
                  <div className="circle">
                    {c.id === choice && <div className="inner-circle"></div>}
                  </div>
                  <div className="choice-ss">{c.title}</div>
                </div>
              ))}
            </div>
          ) : questionData.variant === "MS" ? (
            <QuestionMS
              question={questionData}
              handleChoicesClick={handleChoicesClick}
              choices={choices}
            />
          ) : (
            <QuestionText
              handleAnswerChange={handleAnswerChange}
              answer={answer}
            />
          )}
          <Button variant="info" className="mt-4">
            Hint
          </Button>
        </div>
        {Math.max(...qsInfo["questions_order"]) === +questionOrder ? (
          <Button variant="danger" onClick={handleFinishQuiz}>
            Finish
          </Button>
        ) : (
          <Button variant="primary" onClick={handleNextClick}>
            Next
          </Button>
        )}
      </main>
    </div>
  );
}

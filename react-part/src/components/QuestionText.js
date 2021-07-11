import React from 'react'
import Form from "react-bootstrap/Form";
import classnames from 'classnames';


export default function QuestionText(props) {
  const question = props.question;
  const isResult = props.isResult;

  return (
    <div className="question">
      <h3 className="question-title">{question.title}</h3>
      <div className="choices">
        <Form.Control
          as="textarea"
          placeholder="Type your answer here!"
          {...({'onChange': !isResult ? (e) => props.handleAnswerChange(e.target.value) : () => {}})}
          value={props.answer}
          style={{ height: '50' }}
          className={classnames('textarea', {'correct': props.answer === question['choices']}, {'wrong': props.answer !== question['choices']})}
        />
        {isResult && (
          <div>
            Correct answer: {question['choices']}
          </div>
        )}
      </div>
    </div>
  )
}

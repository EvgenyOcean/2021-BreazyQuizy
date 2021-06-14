import React, {useState} from 'react'
import Form from "react-bootstrap/Form";


export default function QuestionText(props) {
  const question = props.question;
  const [answer, setAnswer] = useState('');

  return (
    <div className="choices">
      <Form.Control
        as="textarea"
        placeholder="Type your answer here!"
        onChange={(e) => props.handleAnswerChange(e.target.value)}
        value={props.answer}
        style={{ height: '100px' }}
      />
    </div>
  )
}

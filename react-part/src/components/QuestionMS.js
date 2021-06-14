import React from 'react';

export default function QuestionMS(props) {
  const question = props.question;

  return (
    <div className="choices">
      {question.choices.map((c, inx) => (
        <div
          key={c.id}
          className="choice"
          data-choice-id={c.id}
          onClick={(e) => props.handleChoicesClick(e.target)}
        >
          <div className="square">
            {props.choices.includes(c.id) && <div className="inner-circle"></div>}
          </div>
          <div className="choice-ms">{c.title}</div>
        </div>
      ))}
    </div>
  )
}

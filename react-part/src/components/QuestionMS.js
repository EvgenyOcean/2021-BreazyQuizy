import React from 'react';
import classnames from 'classnames';

export default function QuestionMS(props) {
  const question = props.question;
  const isResult = props.isResult;

  return (
    <div className='question'>
      <h3 className="question-title">{question.title}</h3>
      <div className="choices">
        {question.choices.map((c) => (
          <div
            key={c.id}
            className={classnames('choice', {'correct': c['is_correct'] && isResult}, {'wrong': props.choices.includes(c.id) && !c['is_correct'] && isResult})}
            data-choice-id={c.id}
            {...(!isResult ? {'onClick': (e) => props.handleChoicesClick(e.target)} : () => {})}
          >
            <div className="square">
              {props.choices.includes(c.id) && <div className="inner-circle"></div>}
            </div>
            <div className="choice-ms">{c.title}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
